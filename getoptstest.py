#!/bin/env python
#coding:utf-8
#

import getopt,sys

def usage():
	"""
The output  configuration file contents.

Usage: config.py [-d|--domain,[number|'m']] [-c|--cache,[allow|deny]]

Description
	-d,--domain	generate domain configuration,take 13 or 19 number,"m" is the second - tier cities.
	-c,--cache	configure cache policy. "allow" or "deny".
for example:
	python config.py -d 13
	python config.py -c allow
"""


def getopttest():
	try:
		options,args = getopt.getopt(sys.argv[1:],"d:c:v",["help","output="])
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(1)
	output = None
	verbose = False
	for o,a in options:
	#	print list((o,a))

		if o == "-v":
			verbose = True
		elif o in ("-h","--help"):
			#usage()
			print usage.__doc__
			sys.exit()
		elif o in ("-o","--output"):
			output = a
		else:
			assert False, "unhandled option"
if __name__ == "__main__":
	getopttest()

