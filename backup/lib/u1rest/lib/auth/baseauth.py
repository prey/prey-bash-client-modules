#Copyright (C) 2011 by John O'Brien
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
"""Authentication Library for authorizing clients."""

from oauth import oauth
import json, urllib2, urllib
from time import sleep
# pylint: disable=C0301
# URLS used for SSO and Ubuntu One OAuth token creation and authorization
REQUEST_URL = "https://login.ubuntu.com/api/1.0/authentications?ws.op=authenticate&token_name=Ubuntu%%20One%%20@%%20%(token_name)s"
AUTHORIZE_URL = 'https://one.ubuntu.com/oauth/sso-finished-so-get-tokens/%(email)s'
TEST_URL = "https://one.ubuntu.com/api/account/"
# pylint: enable=C0301

class BaseAuthenticator(object):
    """A base OAuthAuthenticator."""

    _credentials = None

    def get_consumer_and_token(self):
        """Get consumer and token from credentials."""
        if self._credentials is None:
            self.load_credentials()
        consumer = oauth.OAuthConsumer(self._credentials['consumer_key'],
                                       self._credentials['consumer_secret'])
        token = oauth.OAuthToken(self._credentials['token'],
                                 self._credentials['token_secret'])
        return consumer, token

    def get_auth_headers(self, url, params, http_method):
        """Get authentication headers to be sent with the request.

        @param url: The URL being requested.
        @param params: A {dict} of quesry string parameters
        @param http_method: The HTTP Method being used.
        """
        consumer, token = self.get_consumer_and_token()
        oauth_req = oauth.OAuthRequest.from_consumer_and_token(
            http_url=url,
            http_method=http_method,
            token=token,
            oauth_consumer=consumer,
            parameters=params)
        # using PLAINTEXT, because HMAC doesn't work for all urls
        signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
        oauth_req.sign_request(signature_method, consumer, token)
        return oauth_req.to_header()

    def load_credentials(self):
        """Load the credentials.

        To be overridden by subclasses.
        """
        raise NotImplementedError("load_credentials has not been implemented.")

    def simple_signed_get_request(self, url):
        """Handle a simple signed request.

        @param url: The URL to sign and get.
        """
        consumer, token = self.get_consumer_and_token()
        req = oauth.OAuthRequest.from_consumer_and_token(
            consumer,
            token=token,
            http_url=url)
        req.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(),
                         consumer, token)
        return urllib.urlopen(req.to_url())

    def _authorize_credentials(self, email):
        """Authorize the OAuth SSO Request Token."""
        url = AUTHORIZE_URL % dict(email=email)
        response = self.simple_signed_get_request(url)
        if response.code == 200:
            print "Token Succesfully Authorized"
        else:
            raise Exception(
                "There was a problem Authorizing the Token\n%s" % response.read)

    def _test_credentials(self):
        """Test the OAuth token against Ubuntu One."""
        response = self.simple_signed_get_request(TEST_URL)
        if response.code == 200:
            print "Auth token tested OK"
        else:
            raise Exception(
                "There was a problem Testing the Token.\n%s" % response.read)

    def get_request_token(self, token_name, email, password):
        """Get an OAuth request token from SSO.

        @param token_name: A Name to give the OAuth Token.
        @param email: Your SSO Email.
        @param password: Your SSO Password.
        """
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        top_level_url = "https://login.ubuntu.com/api/1.0"
        password_mgr.add_password(None, top_level_url, email, password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        response = opener.open(REQUEST_URL % dict(token_name=token_name))
        req_token = response.read()
        self._credentials = json.loads(req_token)
        # authorize the request token
        self._authorize_credentials(email)
        # give a moment for some SSO -> U1 chatter
        sleep(1)
        self._test_credentials()
