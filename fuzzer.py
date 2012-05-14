#!/usr/bin/env python
import re
import sys
import time
import copy
import requests
import settings

from urlparse import urljoin, urlparse
from bs4 import BeautifulSoup

target = None
session = None
visited = []
crawlqueue = []
paramdict = {}

def append_to_visited(url):
	visited.append(url)

def append_to_queue(url):
	if url not in visited and url not in crawlqueue:
		crawlqueue.append(url)

def add_to_params(url, type, param, value):
	url = urlparse(url)
	url = url.scheme + "://" + url.netloc + url.path
	if url not in paramdict:
		paramdict[url] = {}
	tuple = paramdict[url]
	if type not in tuple:
		tuple[type] = {}
	if param not in tuple[type]:
		tuple[type][param] = value

def analyze_inputs(url):
	# Check the target location (deprecate?)
	if valid_target(url):
		# Obtain the GET inputs
		query = urlparse(url).query
		if query:
			query = query.split('&')
			# Get only the names, not the values
			for tuple in query:
				split = tuple.split('=')
				param = split[0]
				value = split[1]
				add_to_params(url, "get", param, value)
		# Obtain the forms on this page
		content = session.get(url)
		if content.headers['content-type'].startswith('text'):
			content = BeautifulSoup(content.text)
			for form in content.find_all("form"):
				method = None
				# Check the post method
				if 'method' in form.attrs:
					method = form['method'].lower()
				else:
					method = "get"
				# Check the post target location
				if 'action' in form.attrs:
					target = urljoin(url, form['action'])
				else:
					target = url
				if valid_target(target):
					for input in form.find_all("input"):
						# Weed out dummy inputs
						if 'name' in input.attrs:
							add_to_params(target, method, input['name'], "")
					
def children_of_page(url):
	result = []
	content = session.get(url)
	if content.headers['content-type'].startswith('text'):
		content = BeautifulSoup(content.text)
		for link in content.find_all("a"):
			if 'href' in link.attrs:
				absurl = urljoin(url, link['href'])
				if valid_target(absurl):
					result.append(absurl)
	return result
				
def crawl_recursively():
	if crawlqueue:
		url = crawlqueue.pop(0)
		append_to_visited(url)
		analyze_inputs(url)
		if settings.page_discovery:
			for child in children_of_page(url):
				append_to_queue(child)
			time.sleep(settings.wait_time)
			crawl_recursively()

def guess_pages():
	if settings.page_guessing:
		for page in settings.guess_pages:
			url = urljoin("http://"+target, page)
			result = session.get(url)
			if result.status_code == 200:
				append_to_queue(url)

def guess_passwords():
	if settings.pass_guessing:
		response = None
		for u,p in settings.guess_passwords.items():
			payload = {}
			data = settings.login_data
			url = urljoin(data["proto"]+"://"+target, data["url"])
			keys = data["data"].keys()
			payload[keys[0]] = u
			payload[keys[1]] = p
			if data["rtype"] == "get":
				response = requests.get(url, params=payload)
			else:
				response = requests.post(url, data=payload)
			if data["success_text"] in response.text:
				print "-"*80
				print "Guessed login successful with %s:%s" % (u,p)

def fuzz_all():
	for url in paramdict:
		fuzz_test(url)

def fuzz_test(url):
	if settings.fuzz_complete:
		# Iterate over each test
		for name, test in settings.fuzz_tests.items():
			# Iterate over types
			for type, params in paramdict[url].items():
				# Iterate over each parameter
				for param in params:
					# Iterate over each vector
					for vector in test["vector"]:
						fail = False
						result = None
						payload = copy.copy(params)
						payload[param] = vector
						if type == "get":
							result = session.get(url, params=payload)
						else:
							result = session.post(url, data=payload)
						if 'fail_results' in test:
							for string in test["fail_results"]:
								if string in result.text:
									fail = True
							if fail:
								print "-"*80
								print test["fail_message"] % (type.upper(), url, param)

def print_attack_surface():
	print "=" * 80
	print "Attack Surface:"
	print "=" * 80
	for url, types in paramdict.items():
		print ">"*80
		print url
		for type, params in types.items():
			print type.upper()
			for param, value in params.items():
				print "%s (Default: %s)" % (param,value)
				
def valid_target(url):
	location = urlparse(url).netloc
	if location == target:
		return True
	else:
		return False
		
def set_target(url):
	global target
	# Obtain the domain
	target = urlparse(url).netloc

def login():
	if settings.attempt_login:
		response = None
		login_data = settings.login_data
		url = urljoin(login_data["proto"]+"://"+target, login_data["url"])
		if login_data["rtype"] == "get":
			response = session.get(url, login_data["data"])
		else:
			response = session.post(url, login_data["data"])
		if login_data["success_text"] in response.text:
			print "Login successful."
		

if __name__ == "__main__":
	if(len(sys.argv) > 1):
		# Create a session
		session = requests.session()
		# Set the target
		set_target(sys.argv[1])
		# Add the given page to the queue
		append_to_queue(sys.argv[1])
		# Attempt to login
		login()
		# Guess passwords
		guess_passwords()
		# Guess pages
		guess_pages()
		# Crawl
		crawl_recursively()
		# Fuzz
		fuzz_all()
		# Print human readable attack surface
		print_attack_surface()
	else:
		print "Usage: %s [target]" % (sys.argv[0])
		print "Don't forget the trailing slash!"
