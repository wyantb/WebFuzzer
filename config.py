""" Configuration File """
debug = True

fp_size = 10
fp_maxlen = 15
fp_maxfailure = 3
fp_reltolerance = 5
fp_abstolerance = 6

""" Site specific configuration """
seoURLs = [
	['clan','{param}'],
	['clans', 'default', 'ASC', '{param}'],
	['clan','{param}','members','{param}'],
	['clan','{param}','members','{param}','{param}'],
	['clan','{param}','members','{param}','{param}','{param}']
]

class tests:
	# Indices of enabled tests
	enabled = [0,1,2,3,4]

	"""
	 testDict

	 This is the dictionary used to run tests on a given page.
	 The general format test specifications should follow is:

		{
			'ind' : <index>,
			'pre' : <pre-condition dictionary>,
			'edit': <how the HTTP request should change>,
			'post': <post-condition dictionary>,
			'mesg': <message or test name>
		}

	 If the precondition is matched, the <edit> case will be
	 executed, and if the postcondition is matched by the
	 corresponding request, the attached message will be inserted
	 into the page issues.

	 Available keywords:
	 <pre>:
		random		: [True, False] Allow precondition to select pages that
					  have random content (source varies by request).
		strictRandom: Includes random, but has additional checks to discern
					  whether or not the page has dynamic content.
		g_params	: ALlow precondition to select pages that have GET params.
		///Not Implemented!///
		g_params_incl
		g_paramlen

	 <pre/post>:
		mimetype	: Restrict pre/post condition based on mimetype.
		response	: Restrict pre/post condition based on response code.
		content		: Restrict pre/post condition based on page content.
	
	<post>:
		compare		: Restrict post condition based on the result of a
					  comparison. It is an array of arrays, where each inner
					  array is in the form [m,n,True/False], meaning
					  if m AND n being equal in  comparison is True/False,
					  post-condition matched. Each integer within the inner
					  array ('n' and 'm' in the example) cooresponds to the
					  index of an entity within the <edit> array.
					  NOTE - Each test result must pass all other <post>
					  conditions prior to being compared with each other.

	 <edit>:
		g_paramseq	: An array of vectors to inject in GET upon satisfaction of
					  preconditions. {orig} injects the original parameter.
		g_params	: A more specialized version of g_paramseq, where type of
					  parameter is discerned. Available types; 'int','str'.
					  Each of these types act like g_paramseq, but only act on
					  parameters that match the type indicated.
	 
	 <mesg>:
	 	level		: 0- Info, 1- Warn,  2- Lo, 3- Med, 4- Hi
	 	text		: The text that will display in the report upon satisfaction
	 				  of the postconditions

	 Note: missing conditions will be treated as wildcards (*)
	"""
	# XSS Injection Test
	#
	# This test injects a specially crafted vector into and GET parameter,
	# and checks for various unescaped portions of the vector. If any of
	# the groups match within the content, XSS is possible.
	testDict = [
	{
		'ind': 0,
		'pre':
			{
			'mimetype'	: ['text/html'],
			'response'	: [200],
			'g_params'	: True,
			'random'  	: False,
			},
		'edit':
			[{
			'g_paramseq': ['{orig}\\<>%27?%22n_i_n_j_a%2527%253E%2522'],
			}],
		'post':
			{
			'mimetype'	: ['text/html'],
			'response'	: [200],
			'content' 	: ['\'?"n_i_n_j_a','\\<>\\\'?\\\"','n_i_n_j_a\'>"'],
			},
		'mesg':
			{
			'level'		: 2,
			'text'		: "XSS injection possible."
			}
	},
	# SQL Injection Test
	#
	# By making various comparisions based on parameter type, we can find out
	# if there is SQL injection possible.
	{
		'ind': 1,
		'pre':
			{
			'mimetype'			: ['text/html'],
			'response'			: [200],
			'g_params'			: True,
			'random'  			: False,
			},
		'edit':
			[
				{
				'g_params':
					{
						'str': ['9-8'],
						'int': ['{orig}-0']
					},
				},
				{
				'g_params':
					{
						'str': ['8-7'],
						'int': ['{orig}-0-0']
					}
				},
				{
				'g_params':
					{
						'str': ['9-1'],
						'int': ['{orig}-0-9']
					}
				},
				{
				'g_paramseq': ['{orig}\\%27\\%22']
				},
				{
				'g_paramseq': ['{orig}%27%22']
				},
				{
				'g_paramseq': ['{orig}\\\\%27\\\\%22']
				},
				{
				'g_params':
					{
						'str': ['9 - 1'],
						'int': ['{orig} - 0 - 0']
					}
				},
				{
				'g_params':
					{
						'str': ['9 1 -'],
						'int': ['{orig} 0 0 - -']
					}
				}
			],
		'post':
			{
			'mimetype'	: ['text/html'],
			'response'	: [200],
			'compare'	: 
						[[
							(0,1,True),
							(0,2,False)
						],
						[
							(1,6,True),
							(6,7,False)
						],
						[
							(3,4,False),
							(3,5,False)
						]]
			},
		'mesg':
			{
			'level'		: 4,
			'text'		: "SQL injection possible."
			}
	},
	# Directory Traversal
	#
	# This test sends requests with various traversals injected. If the 
	# original parameter and the same directory (./) injection are the same,
	# and the malformed directory traversal (.../) and the same directory
	# injection yield different results, directory traversal is possible.
	{
		'ind': 2,
		'pre':
			{
			'mimetype'	: ['text/html'],
			'response'	: [200],
			'g_params'	: True,
			'random'  	: False,
			},
		'edit':
			[
				{
					'g_paramseq'	: ['{orig}'],
					'noDirectories'	: True
				},
				{
					'g_paramseq'	: ['./{orig}'],
					'noDirectories'	: True
				},
				{
					'g_paramseq'	: ['.../{orig}'],
					'noDirectories'	: True
				}
			],
		'post':
			{
			'mimetype'	: ['text/html'],
			'compare'	: 
						[[
							(0,1,True),
							(1,2,False)
						]]
			},
		'mesg':
			{
			'level'		: 3,
			'text'		: "Directory traversal possible."
			}
	},
	# Shell command injection
	#
	# Attempt to inject shell calls to 'true', 'false', and 'uname'
	# If the responses are the same for 'true' and 'false', but are different
	# for 'true' and 'uname', shell injection is possible.
	{
		'ind': 3,
		'pre':
			{
			'mimetype'	: ['text/html'],
			'response'	: [200],
			'g_params'	: True,
			'random'  	: False,
			},
		'edit':
			[
				{
					'g_paramseq': ['{orig}`true`'],
				},
				{
					'g_paramseq': ['{orig}`false`'],
				},
				{
					'g_paramseq': ['{orig}`uname`'],
				},
				{
					'g_paramseq': ['{orig}%27`true`%27'],
				},
				{
					'g_paramseq': ['{orig}%27`false`%27'],
				},
				{
					'g_paramseq': ['{orig}%27`uname`%27'],
				},
				{
					'g_paramseq': ['{orig}%22`true`%22'],
				},
				{
					'g_paramseq': ['{orig}%22`false`%22'],
				},
				{
					'g_paramseq': ['{orig}%22`uname`%22'],
				}
			],
		'post':
			{
			'mimetype'	: ['text/html'],
			'compare'	:
						[[
							(0,1,True),
							(0,2,False)
						],
						[
							(3,4,True),
							(3,5,False)
						],
						[
							(6,7,True),
							(6,8,False)							
						]]
			},
		'mesg':
			{
			'level'		: 4,
			'text'		: "Shell injection possible."
			}
	},
	# Swearword checking.
	#
	# This just demonstrates what the config can produce. This will check for
	# certain swearwords in the content of all pages.
	{
		'ind': 4,
		'pre':
			{
			'response'	: [200],
			},
		'edit':
			[],
		'post':
			{
			'response'	: [200],
			'content' 	: [' fuck ',' shit ',' piss ',' ass '],
			},
		'mesg':
			{
			'level'		: 0,
			'text'		: "Explicative found on page."
			}
	}
	]

