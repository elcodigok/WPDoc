#!/usr/bin/env python

import hashlib
import os
import sys
import time

from datetime import datetime
from optparse import OptionParser
from optparse import OptionGroup
from sqlobject import *

class registerWordPress():
        def __init__(self, directory, verbose=False):
                self.directory = os.path.abspath(directory)
                self.mode_verbose = verbose
                self.count_directory = 0
                self.count_file = 0
        
        def showObject(self):
                for r, d, f in os.walk(self.directory):
                        print "Show PATH Directory: %s" %(r)
                        print "Show STAT Directory: %s" %(os.stat(r))
                        print "Show STATVFS Directory: %s" %(os.statvfs(r))
                        print "Show GETSIZE Directory: %s" %(os.path.getsize(r))
                        print "Show GETATIME Directory: %s" %(datetime.fromtimestamp(os.path.getatime(r)).strftime('%Y-%m-%d %H:%M:%S'))
                        print "Show MODIFIED TIME Directory: %s" % (datetime.fromtimestamp(os.path.getmtime(r)).strftime('%Y-%m-%d %H:%M:%S'))
                        print "Show CREATED TIME Directory: %s" %(datetime.fromtimestamp(os.path.getctime(r)).strftime('%Y-%m-%d %H:%M:%S'))
                        self.count_directory += 1
                        for wpfile in f:
                                print "\tShow PATH File: %s" %(r + "/" + wpfile)
                                print "\tShow STAT File: %s" %(os.stat(r + "/" + wpfile))
                                print "\tShow STATVFS File: %s" %(os.statvfs(r + "/" + wpfile))
                                print "\tShow GETSIZE File: %s" %(os.path.getsize(r + "/" + wpfile))
                                print "\tShow GETATIME File: %s" %(datetime.fromtimestamp(os.path.getatime(r + "/" + wpfile)).strftime('%Y-%m-%d %H:%M:%S'))
                                print "\tShow MODIFIED TIME File: %s" % (datetime.fromtimestamp(os.path.getmtime(r + "/" + wpfile)).strftime('%Y-%m-%d %H:%M:%S'))
                                print "\tShow CREATED TIME File: %s" %(datetime.fromtimestamp(os.path.getctime(r + "/" + wpfile)).strftime('%Y-%m-%d %H:%M:%S'))
                                
                                openedFile = open(r + "/" + wpfile)
                                readFile = openedFile.read()
                                
                                md5Hash = hashlib.md5(readFile)
                                md5Hashed = md5Hash.hexdigest()
                                
                                sha1Hash = hashlib.sha1(readFile)
                                sha1Hashed = sha1Hash.hexdigest()
                                
                                openedFile.close()
                                print "\tShow MD5 File: %s" % (md5Hashed)
                                print "\tShow SHA-1 File: %s" %(sha1Hashed)
                                
                                self.count_file += 1
                                print ("\t" + '-' * 67)
                                print 
                        print('-' * 75)
                        print
                print "Count Directory: %s" % (self.count_directory)
                print "Count File: %s" % (self.count_file)

class classProject():
        def __init__(self, verbose=False):
                self.verbose = verbose
                self.name = ""
                self.directory = ""
                self.description = ""
        
        def setName(self):
                name = raw_input("Name Project: ")
                self.name = name
        
        def getName(self):
                return self.name

def cmdLineParser():
	"""Implementation to WPDoc."""
	usage = "usage: python %prog [options]"
	version = 0.1
	parser = OptionParser(usage, version=version)
	parser.add_option("-v", "--verbose", action="store_true",
					  dest="verbose", default=False,
					  help="Verbose.")
	target = OptionGroup(parser, "Target", "At least one of these options has to be provided to define the Directory Work.")
	#target.add_option("-d", "--dir", dest="path", help="**REQUIRED** -"
					  #" Working Directory", metavar="DIRECTORY")
        target.add_option("--new", action="store_true", dest="new", help="New proyect for WPDoc.")
        
        target.add_option("--db", dest="database", help="**REQUIRED** - Database Example project.db")

	parser.add_option_group(target)

	(options, args) = parser.parse_args()

	if options.database is None:
		parser.print_help()
		sys.exit()

        #options.path = os.path.abspath(options.path)
        
        if options.new:
                classProject(False).setName()
        
        #if os.path.exists(options.path):
                #registerWordPress(options.path, False).showObject()

if __name__ == "__main__":
	cmdLineParser()
