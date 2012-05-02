#!/usr/bin/env python
#
# Demonstration of how to walk the links on a webpage with
# requests and BeautifulSoup4.
#

import requests
import settings
from bs4 import BeautifulSoup
from collections import deque

def get_children(url):
	"""
	Queue all the valid links referenced on this page.

	"""

	children = []
	response = requests.get(root % url)
	soup = BeautifulSoup(response.text)
	for atag in soup.find_all('a'):
		if check_prefixes(atag):
			children.append(atag['href'])
		
	return children

def check_prefixes(atag):
	"""
	Don't leave the domain, don't mess with FTP, don't try and follow mailto: links.

	"""

	bad_prefixes = ["http", "ftp", "mailto"]
	if atag.has_key('href'):
		for prefix in bad_prefixes:
			if str(atag['href']).startswith(prefix):
				return False
		if not atag['href'] in queue and not atag['href'] in visited:
			print "Found link: " + str(atag['href'])
			return True
	return False

if __name__ == "__main__":

	queue = deque(['/'])
	visited = []
	root = 'http://www.xkcd.com%s'

	while len(queue) > 0:
		url = queue.pop()
		visited.append(url)
		children = get_children(url)
		for child in children:
			if child not in visited:
				queue.append(child)
	print visited

def find_forms(url):
	response = requests.get(root % url)
	soup = BeautifulSoup(response.text)
	return soup.find_all("form")
	
def fuzz_form(form):
	import urllib

	params = {}
	for input in form.find_all("input"):
		if 'user' in input['name']:
			val = 'admin'
		elif 'password' in input['type']:
			val = 'password'
		else:
			val = "<script>document.write(\"XSS PROBLEM\");</script>"
		params[input['name']] = val # trash value that should be determined based on input type
	
	data = urllib.urlencode(params)

	return requests.get(settings.base_url % ("?" + data))