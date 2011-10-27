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
"""Ubuntu One Rest Client.

This is a Rest Client library for using Ubuntu One REST APIs.
For an example of its use see the doctest in example.txt.

This source is maintained at http://launchpad.net/restful-u1
or you can grabe the source with bzr branch lp:restful-u1

Have fun.
"""

from u1rest.files.resources import get_user

def get_files_user(resource_host="https://edge.one.ubuntu.com",
                   content_host="https://files.one.ubuntu.com",
                   use_file_keystore=False):
    """The main entry point for the API for files.

    The idea is to get a user which is the client for a specific user. For
    more information, refer to u1rest.files.resources.FileStorageUser.
    """
    # pylint: disable=W0404
    if use_file_keystore:
        from u1rest.lib.auth.simpleauth import FileStoreAuthenticator
        auth = FileStoreAuthenticator()
    else:
        from u1rest.lib.auth.gnomeauth import GnomeStoreAuthenticator
        auth = GnomeStoreAuthenticator()

    return get_user(resource_host, content_host, auth)
