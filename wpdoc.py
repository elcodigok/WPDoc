#!/usr/bin/env python

import os
import sys

from optparse import OptionParser
from optparse import OptionGroup

class registerWordPress():
        def __init__(self, directory, verbose=False):
                self.directory = os.path.abspath(directory)
                self.mode_verbose = verbose
        
        def showObject(self):
                for r, d, f in os.walk(self.directory):
                        print "Show PATH: %s" %(r)
                        

def cmdLineParser():
	"""Implementation to WPDoc."""
	
	usage = "usage: python %prog [options]"
	version = 0.1
	parser = OptionParser(usage, version=version)
	parser.add_option("-v", "--verbose", action="store_true",
					  dest="verbose", default=False,
					  help="Verbose.")
	target = OptionGroup(parser, "Target", "At least one of these options has to be provided to define the Directory Work.")
	target.add_option("-d", "--dir", dest="path", help="**REQUIRED** -"
					  " Working Directory", metavar="DIRECTORY")

	parser.add_option_group(target)

	(options, args) = parser.parse_args()

	if options.path is None:
		parser.print_help()
		sys.exit()

        options.path = os.path.abspath(options.path)
        
        if os.path.exists(options.path):
                registerWordPress(options.path, False).showObject()

if __name__ == "__main__":
	cmdLineParser()
