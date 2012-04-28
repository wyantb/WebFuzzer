#!/usr/bin/env python
#
# Demonstration of how to walk the links on a webpage with
# requests and BeautifulSoup4.
#

import requests
from time import time
from bs4 import BeautifulSoup
from collections import deque

import settings

def get_children(url, count=0):
	"""
	Queue all the valid links referenced on this page.

	"""

	children = []
	if settings.debug:
		print "Fetching: %s" % (root % url)
	response = requests.get(root % url)
	soup = BeautifulSoup(response.text)

	# Dump response to a file
	filename = "%s/%d.html" % (settings.output_dir, count)
	count += 1
	resp_dump = open(filename, "w")
	try:
		resp_dump.write(response.text)
		print "Dumped to: %s" % filename
	except UnicodeEncodeError:
		pass
	finally:
		resp_dump.close()

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

	queue = settings.default_actions
	visited = []
	root = settings.base_url
	count = 0

	while len(queue) > 0:
		count += 1
		url = queue.pop()
		visited.append(url)
		children = get_children(url, count)
		for child in children:
			if child not in visited:
				queue.append(child)
	print visited

