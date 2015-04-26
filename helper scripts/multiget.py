#!/usr/bin/env python

## do GET requests to all my Piwik installations and save the responses grouped by ressource

import sys
import urllib3
import os
import time
import pprint
import string


def get(url):
	http = urllib3.PoolManager()
	r = http.request("GET", url )
	return r

def main():
	
	repetitions = 5

	if len(sys.argv) != 3:
		print "usage: %s <prefixes> <postfixes>\nIt will do a GET for each prefix-postfix-combination."%sys.argv[0]
		exit(0)

	with open(sys.argv[1],"r") as f:
		urls = f.read().split("\n")
		urls = filter(lambda x: x and not x.startswith("#"),urls)
	if not urls:
		print "could not load hosts"
		exit(-1)

	with open(sys.argv[2],"r") as f:
		files = f.read().split("\n")
		files = filter(lambda x: x and not x.startswith("#"),files)
	if not files:
		print "could not load files"
		exit(-1)

	t = time.ctime()
	if not os.path.exists("multiget %s"%t):
		os.mkdir("multiget %s"%t)
	if not os.path.exists("multiget %s/byfile"%t):
		os.mkdir("multiget %s/byfile"%t)
	if not os.path.exists("multiget %s/byhost"%t):
		os.mkdir("multiget %s/byhost"%t)
		

	# get the responses and save them by host and by file
	for f in files:
		# skip empty / comment lines
		if not f or not f.strip() or f.startswith("#"):
			continue
		for u in urls:
			# skip empty / comment lines
			if not u or not u.strip() or u.startswith("#"):
				continue

			# append postfix to prefix
			l = u.strip("/") + "/" + f.strip("/")
			print l

			# get the response <repetitions> times
			responses = []
			for i in range(repetitions):
				r = get(l)
				# do not allow duplicates
				# a duplicate has:
				# - same response status (200, 400 etc)
				# - same body
				# - same header keys (values like dates, session ids change too often to be considered for equality)
				duplicate = False
				if responses:
					for x in responses:
						if r.status == x.status and str(r.data) == str(x.data) and set(r.getheaders().keys()) == set(x.getheaders().keys()):
							duplicate = True
							break
				if not duplicate:
					responses.append(r)

			# format the responses
			sep = "#"*60 + "\n"
			sep2 = "-"*60 + "\n"
			resp = sep*2 + l + "\n"
			for r in responses:
				headers = pprint.pformat(r.getheaders())
				body = "".join([ x if x in string.printable else "\\x%02x"%ord(x) for x in r.data ])
				resp += sep2 + str(r.status) + "\n" + sep2 + headers + "\n" + sep2 + body + "\n"

			# write the formatted response into the two related files
			with open("multiget %s/byfile/"%t+f.replace("/",""),"a") as outfile1:
				outfile1.write( resp )
			with open("multiget %s/byhost/"%t+u.replace("/",""),"a") as outfile2:
				outfile2.write( resp )

if __name__ == "__main__":
	main()
