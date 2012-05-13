# Flags
attempt_login = False			# Attempt login (Requires login_data)
page_discovery = True			# Crawl and discover pages
page_guessing = False			# Guess pages based on internal list (Requires guess_pages)
pass_guessing = False			# Guess passwords based on internal list (Requires guess_passwords)
fuzz_complete = False			# False implies random fuzzing

# Wait time between requests in seconds
wait_time = 0

# Tests for sanitization
sanitize_checks = [
	'"youwillneverfindthiselsewhere',
	"'youwillneverfindthiselsewhere",
	">youwillneverfindthiselsewhere",
	"<youwillneverfindthiselsewhere"
]

# Data for a login
login_data = {
	"url": "meep",
	"rtype": "post",
	"data": {
		"x": 1,
		"y": 2
	}
}

# Relative URLs for guessing
guess_pages = [

]

# Password dictionary for guessing
guess_passwords = {

}
