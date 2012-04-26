
baseUrl = ""
debug = True

defaultActions = [
	"",
	"Home",
	"Account",
	"Account/LogOn",
	"Account/LogOff",
	"Account/Register",
	"Account/ChangePassword",
	"Account/ChangePasswordSuccess",
	"Home/Index",
	"Home/About"
]

defaultParameters = [
	"OldPassword",
	"NewPassword",
	"ConfirmPassword",
	"UserName",
	"Password",
	"RememberMe",
	"Email"
]

if __name__ == '__main__':
	print("Actions:")
	print(defaultActions)
	print("Params:")
	print(defaultParameters)
