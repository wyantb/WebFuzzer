#!/usr/bin/env python
import re
import sys
import requests

from urlparse import urlparse
from bs4 import BeautifulSoup

urldict = {}

def add_to_dict(url):
	global urldict
	if url not in urldict:
		urldict[url] = {}
		
def add_to_params(url, type, param):
	global urldict
	if url in urldict:
		tuple = urldict[url]
		if type not in tuple:
			tuple[type] = []
		tuple[type].append(param)

def analyze_inputs(url):
	# Check the target location
	if valid_target(url):
		add_to_dict(url)
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
		content = BeautifulSoup(content.text)
		for form in content.find_all("form"):
			# Check the post target location
			target = convert_to_abs(url, form['action'])
			if valid_target(target):
				add_to_dict(target)
				for input in form.find_all("input"):
					add_to_params(target, "post", input['name'])
				
def convert_to_abs(parent, child):
	child = urlparse(child)
	parent = urlparse(parent)
	if not child.netloc:
		# This is a relative URL, convert it
		return parent.scheme + "://" + parent.netloc + child.path + child.query
	else:
		# This was an absolute URL, return it
		return child
				
def valid_target(url):
	global target
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
		analyze_inputs(sys.argv[1])
		print urldict