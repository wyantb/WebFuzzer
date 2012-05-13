#!/usr/bin/env python
import re
import sys
import time
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

def add_to_params(url, type, param):
	url = urlparse(url)
	url = url.scheme + "://" + url.netloc + url.path
	if url not in paramdict:
		paramdict[url] = {}
	tuple = paramdict[url]
	if type not in tuple:
		tuple[type] = []
	if param not in tuple[type]:
		tuple[type].append(param)

def analyze_inputs(url):
	# Check the target location (deprecate?)
	if valid_target(url):
		# Obtain the GET inputs
		query = urlparse(url).query
		if query:
			query = query.split('&')
			# Get only the names, not the values
			for tuple in query:
				param = tuple.split('=')[0]
				add_to_params(url, "get", param)
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
							add_to_params(target, method, input['name'])
					
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
	else:
		print paramdict

def check_sanitization(url):
	for evilstring in settings.sanitize_checks:
		for paramtype, params in paramdict[url].items():
			content = None
			payload = {}
			for param in params:
				payload[param] = evilstring
			if(paramtype == "get"):
				content = session.get(url, params=payload)
			elif(paramtype == "post"):
				content = session.post(url, params=payload)
			if evilstring in content.text:
				print evilstring + " unsanitized in " + url, payload

def fuzz_all_urls():
	for url in paramdict:
		check_sanitization(url)
				
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
		login_data = settings.login_data
		if login_data["rtype"] == "get":
			session.get(login_data["url"], login_data["data"])
		else:
			session.post(login_data["url"], login_data["data"])
		

if __name__ == "__main__":
	if(len(sys.argv) > 1):
		# Create a session
		session = requests.session()
		# Set the target
		set_target(sys.argv[1])
		# Attempt to login
		login()
		# Add the given page to the queue
		append_to_queue(sys.argv[1])
		# Crawl
		crawl_recursively()
		# Fuzz
		fuzz_all_urls()
