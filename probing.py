#!/usr/bin/env python

# system libs:
import urllib3
import hashlib
import random
import re
import time
import pprint
import string

# local libs:
import versions
import vectors

QUIET = 0
INFO = 1
VERBOSE = 2
DEBUG = 3

VERBOSITY = QUIET
DEBUG_VERSION_TO_PROBE = None

G="\033[32m"
R="\033[31m"
W="\033[m"
BOG="\033[30m\033[42m"

the_time = time.ctime()

#################################################################################
## Hash related
#################################################################################

def md5(text):
	'''simply does the md5sum'''
	m = hashlib.md5()
	m.update(text)
	h = m.hexdigest()
	return h

#################################################################################
## HTTP related
#################################################################################

# save the amount of requests made
requests_made = 0
requests_made_total = 0

def get(url):
	global requests_made
	global requests_made_total
	requests_made += 1
	requests_made_total += 1
	http = urllib3.PoolManager()
	r = http.request("GET", url )
	return r


#################################################################################
## Vector execution
#################################################################################

def answer_match(answer, response):
	# rename to clarify
	probing_method = answer[1]
	if probing_method == "just add":
		return True
	# rename to clarify
	probing_parameter = answer[2]
	
	# if the return value is not of type 'Boolean', cast it in order to filter e.g. regex match objects
	if probing_method == "equals":
		return str(response.data) == str(probing_parameter)
	elif probing_method == "contains":
		return str(probing_parameter) in str(response.data)
	elif probing_method == "matches":
		return True if re.match(probing_parameter,response.data) else False
	elif probing_method == "hash":
		# field response.hash is calculated in probin.execute, not by urllib3
		return response.hash == probing_parameter	
	elif probing_method == "status":
		return response.status == int(probing_parameter)
	elif probing_method == "header field exists":
		return probing_parameter in response.getheaders()
	elif probing_method == "header field equals":
		name, val = probing_parameter
		hs = response.getheaders()
		return name in hs and hs[name] == val
	elif probing_method == "header field contains":
		name, val = probing_parameter
		hs = response.getheaders()
		return name in hs and val in hs[name]
	else:
		raise Exception("Error: '%s' is not a known matching type"%str(answer[1]))
	return False


def execute(baseurl, vector, possible_versions_already_found=None):

	if type(vector) == str:
		vector = vectors.by_id(vector)

	if VERBOSITY >= INFO:
		print '[ ] execute vector (%s) %s'%(vector['id'], vector['desc'])

	# Get the ressource from the probed website
	url = baseurl.rstrip('/') + '/' + vector['url'].lstrip('/')
	response = get(url)
	
	# set the response hash so it only needs to be done once
	response.hash = md5(response.data)

	# classify response
	matches = answer_testing = 0
	possible_versions = []
	for answer in vector['answers']:
		answer_testing += 1
		# assert proper var type of version
		answer_versions = [answer[0]] if isinstance(answer[0], str) else answer[0]
		
		if answer_match(answer, response):			
			matches += 1
			if matches == 1:
				possible_versions = answer_versions
			else:
				possible_versions = versions.intersect( possible_versions, answer_versions )
			
			# print out the matching answer
			if VERBOSITY >= DEBUG:
				print '  - match: [ "%s", "%s", "%s" ]'%(versions.pprint(answer[0]), answer[1], str(answer[2])[:10].replace("\n","")+"...")
				
		# If we are testing and the answer should have matched, write the situation to a file
		elif DEBUG_VERSION_TO_PROBE and DEBUG_VERSION_TO_PROBE in answer_versions:
			if VERBOSITY >= INFO:
				print R + "    record %s should have matched"%(answer_testing) + W
			if VERBOSITY >= DEBUG:
				with open("/tmp/fpp_v%s_vector%s_answer%s_fail.txt"%(DEBUG_VERSION_TO_PROBE, str(vector['id']),str(answer_testing)),"a") as f:
					f.write("#"*60+"\n")
					f.write("#"*60+"\n")
					f.write("url: "+str(url)+"\n")
					f.write("-"*60+"\n")
					f.write("testet against: "+str(answer)+"\n")
					f.write("-"*60+"\n")
					f.write("response status: " +str(response.status)+"\n")
					f.write("-"*60+"\n")
					f.write("response headers: "+str(response.getheaders())+"\n")
					f.write("-"*60+"\n")
					f.write("".join([ x if x in string.printable else "\\x%02x"%ord(x) for x in response.data ])+"\n")
	if VERBOSITY >= INFO and DEBUG_VERSION_TO_PROBE and possible_versions and DEBUG_VERSION_TO_PROBE not in possible_versions:
		print R + "    Vector %s concluded a wrong range for tested version %s:\n    %s"%(vector['id'], DEBUG_VERSION_TO_PROBE, str(possible_versions)) + W
	if VERBOSITY >= VERBOSE and matches > 0:
		print "  - response matches %d records"%(matches) #, versions.pprint(possible_versions) )
	elif VERBOSITY >= INFO and matches > 0:
		print "  - vector says: %s"%(versions.pprint(possible_versions) )

	# if the vector is marked to not be able to judge certain versions, add them regardlessly
	if 'unjudgeable' in vector:
		possible_versions = versions.union(possible_versions, vector['unjudgeable'] )
		if VERBOSITY >= VERBOSE:
			print "  - The vector is marked to always include problematic versions"

	# build the intersection between the versions that this vector found and those of the other ones	
	if possible_versions and possible_versions_already_found != None:
			possible_versions = versions.intersect(possible_versions, possible_versions_already_found)
	

	return possible_versions

#################################################################################
## Fingerprinting
#################################################################################

def fingerprint(url, use_vectors=None):
	
	if use_vectors:
		possible = None
		for v in vectors.vectors:
			if use_vectors and str(v['id']) in use_vectors:
				possible = execute( url, v, possible )
				if VERBOSITY >= INFO:
					print "  - currently possible versions are", versions.pprint(possible)
	else:
		# choose currently good working vectors
		possible = execute(url, "piwikjs")
		if VERBOSITY >= INFO:
					print "  - currently possible versions are", versions.pprint(possible)
		possible = execute(url, "1001", possible)
		if VERBOSITY >= INFO:
					print "  - currently possible versions are", versions.pprint(possible)
		possible = execute(url, "1002", possible)
		if VERBOSITY >= INFO:
					print "  - currently possible versions are", versions.pprint(possible)
		if versions.is_subset(possible, versions.NOT_INSTALLABLE):
			pass
		
	
	if VERBOSITY > QUIET:
		print "made", requests_made, "requests (", requests_made_total, " total)"
		
	return possible
