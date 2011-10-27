#!/usr/bin/env python
#############################################
# Prey Ubuntu One API
# By Tomas Pollak - (c) 2011 Fork Ltd.
# http://preyproject.com
# License: GPLv3
#############################################

import os, sys

try:
	file = sys.argv[1]
except IndexError:
	print "You need to pass in the file path"
	sys.exit(1)

if not os.path.exists(file):
	print "File does not exist: " + file
	sys.exit(1)

if not os.path.exists('credentialfile.txt'):
	print "Credentials file not found. Please run u1rest/createfilekeystore.py"
	sys.exit(1)

file_name = os.path.basename(file)

from u1rest import get_files_user
user = get_files_user(use_file_keystore=True)
f = user.upload_file(file, "~/Ubuntu One/" + file_name)
