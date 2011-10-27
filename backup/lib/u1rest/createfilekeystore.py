#!/usr/bin/python
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
"""Use this to create a file to store credentials.

This is used instead of using the credentials stored in the Gnome Keyring.
You must already have an Ubuntu One subscription before you do this.
"""

from optparse import OptionParser
from u1rest.lib.auth.simpleauth import FileStoreAuthenticator

def create_credential_file():
    """Create the credential file."""
    op_parser = OptionParser()
    op_parser.add_option("--email", dest="email",
                      help="The SSO Email Address for the user.")
    op_parser.add_option("--password", dest="password",
                      help="The SSO Password for the user.")
    op_parser.add_option("--name", dest="name",
                      help="The Token Name for the client's OAuth token.")
    (options, _) = op_parser.parse_args()
    auth_store = FileStoreAuthenticator()
    auth_store.create_and_save_credentials(
        options.name, options.email, options.password)

if __name__ == '__main__':
    create_credential_file()
