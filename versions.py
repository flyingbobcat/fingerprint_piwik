#!/usr/bin/env python

import re

VERSIONS = [
 '0.1.0',
 '0.1.1',
 '0.1.2',
 '0.1.3',
 '0.1.4',
 '0.1.5',
 '0.1.6',
 '0.1.7',
 '0.1.8',
 '0.1.9',
 '0.1.10',
 '0.2.1',
 '0.2.2',
 '0.2.3',
 '0.2.4',
 '0.2.5',
 '0.2.6',
 '0.2.7',
 '0.2.8',
 '0.2.9',
 '0.2.10',
 '0.2.11',
 '0.2.12',
 '0.2.13',
 '0.2.14',
 '0.2.16',
 '0.2.17',
 '0.2.18',
 '0.2.19',
 '0.2.20',
 '0.2.22',
 '0.2.23',
 '0.2.24',
 '0.2.25',
 '0.2.26',
 '0.2.27',
 '0.2.28',
 '0.2.29',
 '0.2.30',
 '0.2.31',
 '0.2.32',
 '0.2.33',
 '0.2.34',
 '0.2.35',
 '0.2.36',
 '0.2.37',
 '0.4.0',
 '0.4.1',
 '0.4.2',
 '0.4.3',
 '0.4.4',
 '0.4.5',
 '0.5.0',
 '0.5.1',
 '0.5.2',
 '0.5.3',
 '0.5.4',
 '0.5.5',
 '0.6.0',
 '0.6.1',
 '0.6.2',
 '0.6.3',
 '0.6.4',
 '0.7.0',
 '0.8.0',
 '0.9.0',
 '0.9.9',
 '1.0.0',
 '1.1.0',
 '1.1.1',
 '1.2.0',
 '1.2.1',
 '1.3.0',
 '1.4.0',
 '1.5.0',
 '1.5.1',
 '1.6.0',
 '1.7.0',
 '1.7.1',
 '1.8.0',
 '1.8.1',
 '1.8.2',
 '1.8.3',
 '1.8.4',
 '1.9.0',
 '1.9.1',
 '1.9.2',
 '1.10.0',
 '1.10.1',
 '1.11.0',
 '1.11.1',
 '1.12.0',
 '2.0.0',
 '2.0.1',
 '2.0.2',
 '2.0.3',
 '2.1.0',
 '2.1.1-b8',
 '2.1.1-b9',
 '2.1.1-b10',
 '2.1.1-b12',
 '2.2.0',
 '2.2.0-b13',
 '2.2.0-b14',
 '2.2.0-b15',
 '2.2.0-b16',
 '2.2.0-b18',
 '2.2.0-rc1',
 '2.2.0-rc2',
 '2.2.0-rc3',
 '2.2.0-rc4',
 '2.2.1',
 '2.2.1-b1',
 '2.2.1-b2',
 '2.2.1-b3',
 '2.2.1-b4',
 '2.2.1-rc1',
 '2.2.1-rc3',
 '2.2.2',
 '2.2.2-b1',
 '2.2.3-b1',
 '2.2.3-b4',
 '2.2.3-b6',
 '2.2.3-b7',
 '2.3.0',
 '2.3.0-rc1',
 '2.3.0-rc2',
 '2.3.0-rc3',
 '2.3.0-rc4',
 '2.4.0',
 '2.4.0-b2',
 '2.4.0-b3',
 '2.4.0-b5',
 '2.4.0-b6',
 '2.4.0-b7',
 '2.4.0-b8',
 '2.4.0-rc1',
 '2.4.1',
 '2.4.1-rc1',
 '2.5.0',
 '2.5.0-b1',
 '2.5.0-b2',
 '2.5.0-b3',
 '2.5.0-rc1',
 '2.5.0-rc3',
 '2.5.0-rc4',
 '2.6.0',
 '2.6.0-b1',
 '2.6.0-rc1',
 '2.6.0-rc2',
 '2.6.0-rc3',
 '2.6.0-rc4',
 '2.6.1',
 '2.6.1-b1',
 '2.7.0',
 '2.7.0-b1',
 '2.7.0-b3',
 '2.7.0-b4',
 '2.7.0-rc1',
 '2.7.0-rc2',
 '2.8.0',
 '2.8.0-b2',
 '2.8.0-b3',
 '2.8.0-rc1',
 '2.8.0-rc2',
 '2.8.1',
 '2.8.1-b1',
 '2.8.1-b2',
 '2.8.1-rc1',
 '2.8.2',
 '2.8.3',
 '2.9.0',
 '2.9.0-b1',
 '2.9.0-b2',
 '2.9.0-b3',
 '2.9.0-b4',
 '2.9.0-b5',
 '2.9.0-b6',
 '2.9.0-b7',
 '2.9.0-b8',
 '2.9.0-b9',
 '2.9.0-rc1',
 '2.9.0-rc2',
 '2.9.1',
 '2.9.1-b1',
 '2.9.1-b2',
 '2.10.0',
 '2.10.0-b1',
 '2.10.0-b2',
 '2.10.0-b3',
 '2.10.0-b4',
 '2.10.0-b5',
 '2.10.0-b6',
 '2.10.0-b7',
 '2.10.0-b8',
 '2.10.0-b9',
 '2.10.0-b10',
 '2.10.0-b11',
 '2.10.0-rc1',
 '2.10.0-rc2',
 '2.10.0-rc3',
 '2.10.0-rc4',
 '2.11.0',
 '2.11.0-b2',
 '2.11.0-b3',
 '2.11.0-b4',
 '2.11.0-b5',
 '2.11.0-b6',
 '2.11.0-b7',
 '2.11.0-rc1',
 '2.11.1',
 '2.11.1-b1',
 '2.11.1-b3',
 '2.11.1-rc1',
 '2.11.2',
 '2.11.2-b1',
 '2.11.2-b2',
 '2.11.2-b3',
 '2.11.2-rc1']
 
NOT_INSTALLABLE = [
 '0.1.0',
 '0.1.1',
 '0.1.2',
 '0.1.3',
 '0.1.4',
 '0.1.5',
 '0.1.6',
 '0.1.7',
 '0.1.8',
 '0.1.9',
 '0.1.10',
 '0.2.1',
 '0.2.2',
 '0.2.3',
 '0.2.4',
 '0.2.5',
 '0.2.6',
 '0.2.7',
 '0.2.8',
 '0.2.9',
 '0.2.10',
 '0.2.11',
 '0.2.12',
 '0.2.13',
 '0.2.14',
 '0.2.16',
 '0.2.17',
 '0.2.18',
 '0.2.19',
 '0.2.20',
 '0.2.22',
 '0.2.23',
 '0.2.24',
 '0.2.25',
 '0.2.26',
 '0.2.27',
 '0.2.28',
 '0.2.29',
 '0.2.30',
 '0.2.31',
 '0.2.32',
 '0.2.33',
 '0.2.34',
 '0.2.35',
 '0.2.36',
 '0.2.37',
 '0.4.0',
 '0.4.1',
 '1.8.1',
 '2.2.3-b7',
 '2.6.0',
 '2.6.0-rc3',
 '2.6.0-rc4',
 '2.9.0-b9',
 '2.10.0-rc2',
 '2.10.0-rc3']

def minors():
	return filter(lambda x: not _v2d(x)['build'] and not _v2d(x)['revision'], VERSIONS)

def extract_version(text,dont_check=False):
	'''Returns any version string found in text'''
	vre = re.compile(r"(\d\.\d{1,2}(?:\.\d{1,2})?(?:(?:-rc\d+)|(?:-b\d+))?)")
	matches = vre.findall(text)
	if matches:
		if dont_check:
			return matches[0]
		else:
			return check(matches[0])
	else:
		print text
		return []


def _v2d(verstr):
	'''Transform a string like 'a.b.c-d' to a dictionary'''
	parts = verstr.split(".")
	if len(parts) != 3:
		raise Exception("cannot create tuple from '%s': not a valid version string!"%verstr)
	a,b,t = parts
	major = int(a)
	minor = int(b)
	if "-" in t:
		c,d = t.split("-")
		build = int(c)
		revision = d
	else:
		build = int(t)
		revision = ""
	return {
		"major": major,
		"minor": minor,
		"build": build,
		"revision": revision
	}

def compare(v1,v2):
	if v1 == v2:
		return 0

	d1, d2 = _v2d(v1), _v2d(v2)
	if d1["major"] != d2["major"]:
		return cmp(d1["major"], d2["major"])
	else:
		if d1["minor"] != d2["minor"]:
				return cmp(d1["minor"], d2["minor"])
		else:
			if d1["build"] != d2["build"]:
					return cmp(d1["build"], d2["build"])
			else:
				if d1["revision"] != d2["revision"]:
#					print d1, d2
					if "rc" in d1["revision"] and "rc" in d2["revision"]:
						return cmp( int(d1["revision"][2:]), int(d2["revision"][2:]) )
					elif "b" in d1["revision"] and "b" in d2["revision"]:
						return cmp( int(d1["revision"][1:]), int(d2["revision"][1:]) )
					elif d1["revision"] == "" and  d2["revision"] != "":
						return -1
					elif d2["revision"] == "" and  d1["revision"] != "":
						return 1
					else:
						return cmp(d1["revision"], d2["revision"])
				else:
					raise Exception("Compare exception: v1!=v2 but compare(v1,v2)==0 !!")
def between(a, b):
	'''Creates a range [a...b] of known versions beginning with version a ending with version b.'''
	a, b = check(a), check(b)
	if not a in VERSIONS:
		raise Exception("%s is not a known version!"%a)
	if not b in VERSIONS:
		raise Exception("%s is not a known version!"%b)
	posA, posB = VERSIONS.index(a), VERSIONS.index(b)
	pos1, pos2 = (posA, posB) if posA <= posB else (posB, posA)
	return VERSIONS[pos1:pos2+1]

def intersect(a,b):
	'''return a all elements that are contained both in a and in b'''
	if a == None:
		return b
	if b == None:
		return a
	a, b = [check(x) for x in a], [check(x) for x in b]
	res = []
	for xa in a:
		if xa in b:
			res.append(xa)
	return sort(res)

def subtract(a,b):
	''' return all elements from a that are NOT in b'''
	a, b = [check(x) for x in a], [check(x) for x in b]
	res = []
	for x in a:
		if x not in b:
			res.append(x)
	return sort(res)

def union(a,b):
	'''return the union of a and b. Like addition with removal of duplicates'''
	a, b = [check(x) for x in a], [check(x) for x in b]
	res = []
	for x in a+b:
		if x not in res:
			res.append(x)
	return sort(res)

def inverse(l):
	l = [check(x) for x in l]
	res = []
	for x in VERSIONS:
		if x not in l:
			res.append(x)
	return x
	
def is_subset(subset, superset):
	'''Check if 'subset' is fully contained in 'superset'.'''
	for x in subset:
		if x not in superset:
			return False
	return True

def sort(l):
	l = [check(x) for x in l]
	return sorted(l,cmp=compare)[:]

def after(v,inclusive=True):
	v = check(v)
	if not v in VERSIONS:
		raise Exception("%s is not a known version!"%v)
	pos = VERSIONS.index(v)
	if inclusive:
		return VERSIONS[max(pos-1,0):]
	else:
		return VERSIONS[pos:]

def before(v,inclusive=True):
	v = check(v)
	if not v in VERSIONS:
		raise Exception("%s is not a known version!"%v)
	pos = VERSIONS.index(v)
	if inclusive:
		return VERSIONS[:min(pos+1,len(VERSIONS))]
	else:
		return VERSIONS[:pos]

def check(v):
	# complete full minor, e.g. '2.0' to '2.0.0"
	chunks = v.split(".")
	if len(chunks) == 2:
		v += ".0"

	if not v in VERSIONS:
		raise Exception("%s is not a known version!"%v)
	else:
		return v
def pprint(l):
	if isinstance(l,str):
		return l
	if len(l) <= 3:
		return ", ".join(l)
	l = sort(l)
#	print l
	
	new = []
	for i, current in enumerate(l):
		if i==0:
			new.append(current+",")
			lastadded = previous = current
			continue
		if i==len(l)-1:
			new.append(current)
			break
		
		# if current is one away from last and one away from the next, skip it
		next = l[i+1]
		if abs( VERSIONS.index(previous) - VERSIONS.index(current) ) == 1 and abs(VERSIONS.index(current) - VERSIONS.index(next) ) == 1:
			if new[-1] != "...,":
				new.append("...,")
			previous = current
			continue
			
		new.append(current+",")
		previous = current
	
	return " ".join(new)
	
#	new = [l[0]]
#	lastv = l[0]
#	for i in range(1,len(l)-1):
#		if abs( VERSIONS.index(lastv) - VERSIONS.index(l[i]) ) > 1:
#			new.extend( [lastv,",", l[i]] )
#		else:
#			if new[-1] != "...":
#				new.append("...")
#		lastv = l[i]
#	new.append(l[-1])
#	return " ".join(new)

if __name__ == '__main__':
	import random
	from pprint import pprint
	a = between("2.2.0","2.10.0-rc1")
	b = a[:]
	random.shuffle(b)
	c = sorted(b,cmp=compare)
	print a == c
