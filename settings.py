
baseUrl = ""
debug = True

defaultActions = [
	# The defaults of MVC2/3
	"",
	"Home",
	"Account",
	"Account/LogOn",
	"Account/LogOff",
	"Account/Register",
	"Account/ChangePassword",
	"Account/ChangePasswordSuccess",
	"Home/Index",
	"Home/About",

	# Some extras for WebEng to fuzz
	"Home/UpdateStatus",
	"Photos",
	"Calendar",
	"Stock",
	"Stock/List",
	"Stock/Add"
]

defaultParameters = [
	"OldPassword",
	"NewPassword",
	"ConfirmPassword",
	"UserName",
	"Password",
	"RememberMe",
	"Email",
	"access_token"
]

defaultArgs = [
	"admin",

	# Basic XSS
	"<script>document.write(\"XSS PROBLEM\");</script>",

	# Basic SQL Injection
	"admin') --",
	""
]

if __name__ == '__main__':
	print("Actions:")
	print(defaultActions)
	print("Params:")
	print(defaultParameters)
