#!/usr/bin/env python

import hashlib
import os
import sys
import time

from datetime import datetime
from optparse import OptionParser
from optparse import OptionGroup
from sqlobject import *


class wpProject(SQLObject):
    name = StringCol(length=100)
    directory = StringCol(length=255)
    dbdirectory = StringCol(length=255)
    description = StringCol(default=None)
    url = StringCol(length=255, default=None)
    created = DateTimeCol(default=DateTimeCol.now)


class wpRevision(SQLObject):
    name = StringCol(length=100)
    notes = StringCol(default='')
    created = DateTimeCol(default=DateTimeCol.now)


class wpObject(SQLObject):
    name = StringCol(length=100)
    path = StringCol(length=255)
    objecttype = EnumCol(enumValues=['file', 'directory'])
    uid = IntCol()
    gid = IntCol()
    size = IntCol()
    sha256 = StringCol(length=255, default=None)
    content = StringCol(default=None)
    created = DateTimeCol(default=DateTimeCol.now)
    revision = ForeignKey('wpRevision')


class registerDatabase():
    def __init__(self, database):
        self.database = database

    def connectDatabase(self):
        self.connection_string = 'sqlite:' + self.database
        self.connection = connectionForURI(self.connection_string)
        sqlhub.processConnection = self.connection

    def isNewDatabase(self):
        if os.path.exists(self.database):
            self.connectDatabase()
        else:
            self.connectDatabase()
            wpProject.createTable()
            wpRevision.createTable()
            wpObject.createTable()

    def saveData(self, name, directory, url, dbdirectory):
        wpProject(
            name=name, directory=directory,
            url=url, dbdirectory=dbdirectory
            )


class registerWordPress():
    def __init__(self, directory, revision, verbose=False):
        self.extensions = [".eot", ".ttf", ".woff", ".png", ".gif", ".jpg", ".jpeg", ".swf", ".xap", ".gz"]
        self.directory = os.path.abspath(directory)
        self.mode_verbose = verbose
        self.count_directory = 0
        self.count_file = 0
        self.revision = revision

    def showObject(self):
        for r, d, f in os.walk(self.directory):
            print "Show PATH Directory: %s" % (r)
            # print "Show STAT Directory: %s" % (os.stat(r))
            uid = os.stat(r).st_uid
            gid = os.stat(r).st_gid
            size = os.stat(r).st_size
            # print "Show STATVFS Directory: %s" % (os.statvfs(r))
            # print "Show GETSIZE Directory: %s" % (os.path.getsize(r))
            # print "Show GETATIME Directory: %s" % (
            # datetime.fromtimestamp(
            # os.path.getatime(r)).strftime('%Y-%m-%d %H:%M:%S'))
            # print "Show MODIFIED TIME Directory: %s" % (
            # datetime.fromtimestamp(
            # os.path.getmtime(r)).strftime('%Y-%m-%d %H:%M:%S'))
            # print "Show CREATED TIME Directory: %s" % (
            # datetime.fromtimestamp(
            # os.path.getctime(r)).strftime('%Y-%m-%d %H:%M:%S'))
            self.count_directory += 1
            wpObject(name=r, path=r, objecttype='directory',
                     uid=uid, gid=gid, size=size, revision=self.revision)

            for wpfile in f:
                print "\tShow PATH File: %s" % (r + "/" + wpfile)
                # print "\tShow STAT File: %s" % (os.stat(r + "/" + wpfile))
                uid = os.stat(r + "/" + wpfile).st_uid
                gid = os.stat(r + "/" + wpfile).st_gid
                size = os.stat(r + "/" + wpfile).st_size
                # print "\tShow STATVFS File: %s" % (
                # os.statvfs(r + "/" + wpfile))
                # print "\tShow GETSIZE File: %s" % (
                # os.path.getsize(r + "/" + wpfile))
                # print "\tShow GETATIME File: %s" % (
                # datetime.fromtimestamp(
                # os.path.getatime(r + "/" + wpfile)).strftime(
                # '%Y-%m-%d %H:%M:%S'))
                # print "\tShow MODIFIED TIME File: %s" % (
                # datetime.fromtimestamp(
                # os.path.getmtime(r + "/" + wpfile)).strftime(
                # '%Y-%m-%d %H:%M:%S'))
                # print "\tShow CREATED TIME File: %s" % (
                # datetime.fromtimestamp(
                # os.path.getctime(r + "/" + wpfile)).strftime(
                # '%Y-%m-%d %H:%M:%S'))

                openedFile = open(r + "/" + wpfile, "r")
                readFile = openedFile.read()
                openedFile.close()

                sha256Hash = hashlib.sha256(readFile)
                sha256Hashed = sha256Hash.hexdigest()
                
                extension = os.path.splitext(wpfile)[1]
                if extension in self.extensions:
                    readFile = ""

                wpObject(name=wpfile, path=r+"/"+wpfile, objecttype='file',
                         uid=uid, gid=gid, size=size, sha256=sha256Hashed,
                         content=readFile,revision=self.revision)

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
        self.url = ""

    def setName(self):
        name = raw_input("WPDoc:Project:Name > ")
        self.name = name

    def getName(self):
        return self.name

    def setDirectoy(self):
        directory = raw_input("WPDoc:Project:PATH > ")
        self.directory = directory

    def getDirectory(self):
        return self.directory

    def setDbDirectory(self, path_db):
        self.dbdirectory = path_db
        print "WPDoc:Project:db > %s" % (self.getDbDirectory())

    def getDbDirectory(self):
        return self.dbdirectory

    def setDescription(self):
        description = raw_input("WPDoc:Project:Description > ")
        self.description = description

    def getDescription(self):
        return self.description

    def setUrl(self):
        url = raw_input("WPDoc:Project:URL > ")
        self.url = url

    def getUrl(self):
        return self.url


def cmdLineParser():
    """Implementation to WPDoc."""
    usage = "usage: python %prog [options]"
    version = 0.1
    parser = OptionParser(usage, version=version)
    parser.add_option("-v", "--verbose", action="store_true",
                      dest="verbose", default=False,
                      help="Verbose.")
    target = OptionGroup(
        parser, "Target",
        "At least one of these options has to be provided to" +
        " define the Directory Work.")
    target.add_option("--db", dest="database",
                      help="**REQUIRED** - Database Example project.db")
    target.add_option("--new", action="store_true",
                      dest="new", help="New proyect for WPDoc.")
    target.add_option("--revision", action="store_true",
                      dest="revision", help="Revision all files and directory")
    parser.add_option_group(target)

    (options, args) = parser.parse_args()
    if options.database is None:
        parser.print_help()
        sys.exit()

    options.database = os.path.abspath(options.database)

    if options.new:
        my_database = registerDatabase(options.database)
        my_database.isNewDatabase()
        my_project = classProject(False)
        my_project.setDbDirectory(options.database)
        my_project.setName()
        my_project.setDirectoy()
        my_project.setUrl()
        my_database.saveData(
            my_project.getName(), my_project.getDirectory(),
            my_project.getUrl(), my_project.getDbDirectory()
            )

    if options.revision:
        if options.new:
            my_revision = wpRevision(name="Revision 1", notes="")
            registerWordPress(
                my_project.getDirectory(), my_revision
            ).showObject()
        else:
            print "Other revision."
            my_database = registerDatabase(options.database)
            my_database.connectDatabase()
            p = wpProject.get(1).directory
            print p
            


if __name__ == "__main__":
    cmdLineParser()
