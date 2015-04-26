#!/usr/bin/env python

import sys

import probing
import vectors
import versions
import vulnerabilities
import time
import argparse



G="\033[32m"
GR="\033[2m"
B="\033[34m"
R="\033[31m"
W="\033[m"
BOG="\033[30m\033[42m"


if __name__ == "__main__":
	# parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity. Can be stacked, e.g. -vvv")
	parser.add_argument("-V", "--vulnerabilities", action="count", default=0, help="increase output verbosity. Can be stacked, e.g. -vvv")
	parser.add_argument("url", help="location of piwik")
	
	args = parser.parse_args()
	
	# process arguments
	probing.VERBOSITY = args.verbosity
	
	possible_versions = probing.fingerprint(args.url)
	if not possible_versions:
		print "Version detection failed"
		sys.exit(-1)
	print "Piwik was detected as one of the following versions:"
	print possible_versions


	# print related vulnerabilities
	if args.vulnerabilities:
		vulns = vulnerabilities.get_list(possible_versions)
		if vulns:
			print ""
			print "The following versions may be vulnerable:"
			for v in vulns:
				print "Title:   ", v[2]
				print "Link:    ", v[1]
				print "Affected:", v[0]
				print ""
