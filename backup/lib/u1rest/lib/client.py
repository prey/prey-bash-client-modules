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
"""Client classes used by REST Client."""
#pylint: disable=R0903
import urllib
import urllib2
import urlparse
import json



class BaseClient(object):
    """Base client to provide common functionaility."""
    # pylint: disable=R0201
    def __init__(self, http_host, auth):
        """Ubuntu One RESTful Client."""
        self.auth = auth
        self.http_host = http_host

    def get_url_from_path(self, path, params=None):
        """Using the path, parameters and host, create a URL.

        @param path: The url path
        @param params: A dict of parameters to be used as a query string.
        """
        path = urllib.quote(path.encode('utf-8'), '~/[]()')
        if params:
            path = "%s?%s" % (path, urllib.urlencode(params))
        return urlparse.urljoin(self.http_host, path)

    def _get_authenticated_request(self, url, params=None, method='GET',
                                   data=None):
        """Helper to get a urllib2.Request object with the auth headers."""
        headers = self.auth.get_auth_headers(url, params, method)
        request = urllib2.Request(url, data, headers)
        request.get_method = lambda: method
        return request

    def _handle_request(self, request):
        """Helper to handle urllib2.Resquest object."""
        opener = urllib2.build_opener(urllib2.BaseHandler)
        try:
            return opener.open(request, timeout=30)
        except urllib2.URLError, ex:
            raise Exception(
                "Error opening %s\n%s" % (request.get_full_url(), ex.message))


class ResourceClient(BaseClient):
    """A client used to handle authenticated REST Requests."""

    def __init__(self, http_host, auth, base_api_path):
        super(ResourceClient, self).__init__(http_host, auth)
        self.base_path = base_api_path

    def process_request(self, path, method, params=None, data=None):
        """Process a REST request.

        This is specifically for JSON request/responses. The data, for PUT must
        be serializable by JSON. The http responses must be JSON serializable as
        well.
        """
        url = self.get_url_from_path(path, params)
        if method == 'PUT' and data:
            data = json.dumps(data)
        else:
            data = None
        request = self._get_authenticated_request(url, params, method, data)
        request.add_header('Content-Type', 'application/json')
        response = self._handle_request(request)
        content = response.read()
        try:
            return json.loads(content)
        except ValueError:
            raise Exception("JSON could not be decoded.\n%s\n%s" % (url,
                                                                    content))

    def _get_path(self, path):
        """Join the path with the API base path.

        This also removes trailing slashes wish are not part of the resource.
        """
        if path:
            return self.base_path + '/' + path.lstrip("/")
        return self.base_path

    def get_resource(self, path="", params=None):
        """Get a Resource."""
        return self.process_request(
            self._get_path(path), 'GET', params=params)

    def delete_resource(self, path, params=None):
        """Delete a Resource."""
        return self.process_request(
            self._get_path(path), 'DELETE', params=params)

    def put_resource(self, path, data=None, params=None):
        """PUT a Resource."""
        return self.process_request(
            self._get_path(path), 'PUT', params=params, data=data)
