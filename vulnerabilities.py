#!/usr/bin/env python

from versions import before, between, intersect

# format: [ version list, title, link ]
vulnerabilities = [
[
	before("0.4.5"),
	"Piwik Cookie Unserialize() Vulnerability",
	"https://www.sektioneins.de/en//advisories/advisory-032009-piwik-cookie-unserialize-vulnerability.html"
],
[
	between("1.2","1.4"),
	"Piwik 1.5 Security Advisory",
	"http://piwik.org/blog/2011/06/piwik-1-5-security-advisory/"
],
[
	before("1.0"),
	"Piwik 1.1 Security Advisory",
	"http://piwik.org/blog/2011/01/piwik-1-1-security-advisory/"
],
[
	["0.5.4"],
	"Piwik APS 0.5.4 Security Advisory",
	"http://piwik.org/blog/2010/08/piwik-0-5-4-remix-by-parallels-security-advisory/"
],
[
	["1.9.2"],
	"Malicious Code in Official 1.9.2 Archive",
	"http://piwik.org/blog/2012/11/security-report-piwik-org-webserver-hacked-for-a-few-hours-on-2012-nov-26th/"
],
[
	before("0.4.5"),
	"Shocking News in PHP Exploitation",
	"http://piwik.org/blog/2009/12/piwik-response-to-shocking-news-in-php-exploitation/"
],
[
	["0.2.35", "0.2.36", "0.2.37", "0.4", "0.4.1", "0.4.2", "0.4.3"],
	"Piwik 0.4.4, response to Secunia Advisory SA37078",
	"http://piwik.org/blog/2009/10/piwik-response-to-secunia-advisory-sa37078/"
],
[
	before("0.2.32"),
	"Piwik 0.2.33, response to CVE-2009-1085",
	"http://piwik.org/blog/2009/04/piwik-response-to-cve-2009-1085/"
],
[
	between("0.6", "0.6.3"),
	"Piwik 0.6.4 Security Advisory CVE-2010-2786",
	"http://piwik.org/blog/2010/07/piwik-0-6-4-security-advisory/"
],
[
	between("0.1.6", "0.5.5"),
	"Piwik 0.6 - Security Advisory to CVE-2010-1453",
	"http://piwik.org/blog/2010/04/piwik-0-6-security-advisory/"
]
]

def get_list(list_of_versions):
	list_of_vulns = []
	for v in vulnerabilities:
		affected = intersect(list_of_versions, v[0])
		if affected:
			list_of_vulns.append([ affected, v[1], v[2] ])
	return list_of_vulns
