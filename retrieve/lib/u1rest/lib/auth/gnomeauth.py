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
"""An authenticator based on the Gnome Keyring."""
import gobject

try:
    from ubuntuone.clientdefs import APP_NAME
except ImportError:
    APP_NAME = "Ubuntu One"
from ubuntu_sso.main import Credentials

from u1rest.lib.auth.baseauth import BaseAuthenticator

class GnomeStoreAuthenticator(BaseAuthenticator):
    """A Gnome based Authenticator."""

    def __init__(self):
        super(GnomeStoreAuthenticator, self).__init__()
        self.app = gobject.MainLoop()

    def load_credentials(self):
        """Load the OAuth credentials."""
        #pylint: disable=E1101
        if self._credentials is None:
            fc_deferred = Credentials(APP_NAME).find_credentials()
            fc_deferred.addCallback(self._set_credentials)
            fc_deferred.addBoth(self._stop)
            self.app.run()

    def _set_credentials(self, credentials):
        """Set the credentials."""
        self._credentials = credentials

    def _stop(self, _):
        """Stop the MainLoop."""
        self.app.quit()
