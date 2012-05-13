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
		
def add_to_params(url, type, params):
	global urldict
	if url in urldict:
		tuple = urldict[url]
		if type in tuple:
			tuple[type].extend(params)
		else:
			tuple[type] = params

def analyze_inputs(url):
	# Check the target location
	if valid_target(url):
		add_to_dict(url)
		# Obtain the GET inputs
		query = urlparse(url).query
		query = query.split('&')
		# Get only the names, not the values
		for tuple in query:
			param = tuple.split('=')[0]
			print param
		# Obtain the forms on this page
		content = requests.get(url)
		content = BeautifulSoup(content.text)
		for form in content.find_all("form"):
			# Check the post target location
			if valid_target(form['action']):
				
				
def valid_target(url):
	global target
	location = urlparse(url).netloc
	if location == target or len(location) == 0:
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