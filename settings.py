
import os
from time import time
from collections import deque

base_url = "http://vm549-03b.se.rit.edu%s"
debug = True

output_dir = "output/%d" % time()

default_actions = deque([
	# The defaults of MVC2/3
	"/",
	"/Home/",
	"/Account/",
	"/Account/LogOn/",
	"/Account/LogOff/",
	"/Account/Register/",
	"/Account/ChangePassword/",
	"/Account/ChangePasswordSuccess/",
	"/Home/Index/",
	"/Home/About/",

	# Some extras for WebEng to fuzz
	"/Home/UpdateStatus/",
	"/Photos/",
	"/Calendar/",
	"/Stock/",
	"/Stock/List/",
	"/Stock/Add/"
])

default_parameters = [
	"OldPassword",
	"NewPassword",
	"ConfirmPassword",
	"UserName",
	"Password",
	"RememberMe",
	"Email",
	"access_token"
]

default_args = [
	"admin",

	# Basic XSS
	"<script>document.write(\"XSS PROBLEM\");</script>",

	# Basic SQL Injection
	"admin') --",
	""
]

from settings_user import *

if not os.path.exists(output_dir):
	os.makedirs(output_dir)

if __name__ == '__main__':
	print "Base URL:"
	print base_url
	print "Actions:"
	print default_actions
	print "Params:"
	print default_parameters
