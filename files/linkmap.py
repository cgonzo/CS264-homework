#!/usr/bin/python

import common
import re
import json

def map(line):
	# find the title
	common.ununicode(line)
	title_match=re.match('<page>\s*<title>(.*?)<',line)
	if title_match:
		title=title_match.group(1)
	else:
		title=''
	#find enclosed links
	if re.search('\[\[',line):	# make sure there is a link first
		link_array=re.split('\[\[',line)
		link_array.pop(0)	# we don't care about the stuff before the first link
		for link in link_array:
#			link_match=re.match('(.*?)\||\]\]',link)
#			if link_match:
#				print link_match.groups()
  			split_link=re.split('\]\]',link)
 			link_text=split_link[0]
  			link_text_array=re.split('\|',link_text)
  			yield(title.upper(),link_text_array[0].upper())

def reduce(word, counts):
	pagerank=1.0
	data_to_output=[pagerank, counts]
	yield(word,json.dumps(data_to_output))

if __name__ == "__main__":
  common.main(map, reduce)
