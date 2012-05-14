# Flags
attempt_login = False			# Attempt login (Requires login_data)
page_discovery = True			# Crawl and discover pages
page_guessing = False			# Guess pages based on internal list (Requires guess_pages)
pass_guessing = True			# Guess passwords based on internal list (Requires guess_passwords)
fuzz_complete = False			# False implies random fuzzing

# Wait time between requests in seconds
wait_time = 0

# Data for a login
login_data = {
	"url": "login.jsp",
	"rtype": "post",
	"data": {
		"x": 1,
		"y": 2
	},
	"success_text": "You have logged in successfully"
}

# Relative URLs for guessing
guess_pages = [

]

# Password dictionary for guessing
guess_passwords = {
	"admin": "pass",
	"administrator": "password"
}

# Tests to execute on pages
fuzz_tests = {
	"Sanitization": {
		"vector": "'derp",
		"fail_results": ["'derp"],
		"fail_message": "%s input unsanitized on %s in param %s" 
	},
	"SQL Injection": {
		"vector": "' OR '1'='1"
	}
}
