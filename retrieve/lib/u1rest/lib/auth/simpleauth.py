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
"""A set of simple authenticators."""
import pickle

from u1rest.lib.auth.baseauth import BaseAuthenticator

class FileStoreAuthenticator(BaseAuthenticator):
    """A file based Authenticator."""

    def __init__(self, filename="credentialfile.txt"):
        super(FileStoreAuthenticator, self).__init__()
        self.filename = filename

    def load_credentials(self):
        """Load the oauth credentials."""
        if self._credentials is None:
            with open(self.filename, 'rb') as credfile:
                self._credentials = pickle.load(credfile)

    def create_and_save_credentials(self, token_name, email, password):
        """Create an file for credentials.

        @param token_name: A Name to give the OAuth Token.
        @param email: Your SSO Email.
        @param password: Your SSO Password.
        """
        self.get_request_token(token_name, email, password)
        # save the credentials to a file
        with open(self.filename, 'wb') as credfile:
            pickle.dump(self._credentials, credfile)
