#!/usr/bin/env python
import re
import sys
import requests

from urlparse import urlparse
from bs4 import BeautifulSoup

target = None
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
		content = requests.get(url)
		if content.headers['content-type'].startswith('text'):
			content = BeautifulSoup(content.text)
			for form in content.find_all("form"):
				# Check the post target location
				if 'action' in form.attrs:
					target = convert_to_abs(url, form['action'])
				else:
					target = url
				if valid_target(target):
					for input in form.find_all("input"):
						# Weed out dummy inputs
						if 'name' in input.attrs:
							add_to_params(target, "post", input['name'])
					
def children_of_page(url):
	result = []
	content = requests.get(url)
	if content.headers['content-type'].startswith('text'):
		content = BeautifulSoup(content.text)
		for link in content.find_all("a"):
			if 'href' in link.attrs:
				absurl = convert_to_abs(url, link['href'])
				if valid_target(absurl):
					result.append(absurl)
	return result
				
def crawl_recursively():
	if crawlqueue:
		url = crawlqueue.pop(0)
		append_to_visited(url)
		analyze_inputs(url)
		for child in children_of_page(url):
			append_to_queue(child)
		crawl_recursively()
	else:
		print paramdict
		
def convert_to_abs(parent, child):
	parsedChild = urlparse(child)
	parsedParent = urlparse(parent)
	if not parsedChild.netloc:
		# This is a relative URL, convert it
		extra  = ""
		if not parsedChild.path.startswith('/'):
			extra = "/"
		return (parsedParent.scheme + "://" + parsedParent.netloc + extra +
				parsedChild.path + parsedChild.query)
	else:
		# This was an absolute URL, return it
		return child
				
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

if __name__ == "__main__":
	if(len(sys.argv) > 1):
		set_target(sys.argv[1])
		append_to_queue(sys.argv[1])
		crawl_recursively()
		# analyze_inputs(sys.argv[1])
