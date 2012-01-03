# -*- coding: utf-8 -*-
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
"""Special cleint for uploading and downloading files."""

import httplib, urlparse
import urllib2
import os
import errno
import json
import mimetypes

from u1rest.lib.client import BaseClient


class ContentClient(BaseClient):
    """A client used to handle file content Requests."""

    #modify this to change the destination folder for downloads
    download_directory = "content"

    def get_or_make_download_path(self, path, download_directory=None):
        """Create local directories for the downloaded files."""
        if download_directory is None:
            path = os.path.join(self.download_directory, path)
        else:
            _, filename = os.path.split(path)
            path = os.path.join(download_directory, filename)
        subdir, _ = os.path.split(path)
        try:
            os.makedirs(subdir)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else: raise
        return path

    def get_file(self, path, download_directory=None):
        """Download a file from an http get."""
        file_path = self.get_or_make_download_path(path, download_directory)
        path = 'content/' + path.lstrip("/")
        url = self.get_url_from_path(path, None)
        request = self._get_authenticated_request(url, None)
        opener = urllib2.build_opener(urllib2.BaseHandler)
        response = opener.open(request)
        block_sz = 8192
        with open(file_path, 'w') as new_file:
            while True:
                read_bytes = response.read(block_sz)
                if not read_bytes:
                    break
                new_file.write(read_bytes)

    def put_file(self, filename, path):
        """Upload a file with PUT."""
        path = 'content/' + path.lstrip("/")
        url = self.get_url_from_path(path, None)
        return self._upload_file(filename, url)

    def _upload_file(self, filename, url):
        """Stream a file as an upload."""
        auth_header = self.auth.get_auth_headers(url, None, 'PUT')
        parsed_url = urlparse.urlparse(url)
        size = os.path.getsize(filename)
        content_type = mimetypes.guess_type(filename)[0]
        connection = httplib.HTTPSConnection(parsed_url.hostname,
                                             parsed_url.port)
        connection.putrequest('PUT', parsed_url.path)
        connection.putheader('User-Agent', 'restful-u1')
        connection.putheader('Content-Length', size)
        connection.putheader('Connection', 'close')
        connection.putheader('Content-Type',
                             content_type or 'application/octet-stream')
        connection.putheader('Authorization', auth_header['Authorization'])
        connection.endheaders()
        transferred = 0
        with open(filename, 'rb') as upload_file:
            while True:
                bytes_read = upload_file.read(4096)
                if not bytes_read:
                    break
                transferred += len(bytes_read)
                connection.send(bytes_read)
        connection.send('0\r\n\r\n')
        resp = connection.getresponse()
        if transferred != size:
            raise Exception("Transferred bytes do not equal file size.")
        if resp.status < 200 or resp.status > 299:
            resp.read()
            raise Exception(resp.status, resp.reason)
        else:
            return json.loads(resp.read())
