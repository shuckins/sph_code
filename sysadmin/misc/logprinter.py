#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Name:        logprinter 
# Purpose:    
# This script is designed to view normal and compressed
# logs files, and provide the ability to print time
# passed between entries addresses.
#
# Author:      Samuel Huckins
#
# Started:     10/31/2007
# Copyright:   (c) 2007 Samuel Huckins
#-----------------------------------------------------------------------------
#
# For grabbing arguments passed:
import sys
import optparse
# For verifying filetype:
import mimetypes
# For opening compressed files
import tarfile
# For getting dates from the strings:
import time
# For finding sections of lines:
import re
#
class Main(object):
	"""I do everything"""

	def showWithoutDelta(self, filename):
		print "File: ", filename
		logfile = file(filename)
		try:
			while True:
				line = logfile.readline()
				if len(line) == 0:
					break
				print line,
		except IOError:
			print "Not a valid file. Try again."
		logfile.close()

	def showWithDelta(self, filename):
		print "File: ", filename
		print
		logfile = file(filename)
		curline = 0
		lastdate = ()
		try:
			for line in logfile.readlines():
				datestamp = re.search("\[(.*)\ \+|\-{4}]", line)
				secsfromepoch = time.mktime(time.strptime(datestamp.group(1), "%d/%b/%Y:%H:%M:%S"))
				if curline == 0:
					delta = datestamp.group(1)
					lastdate = secsfromepoch
					curline += 1
					print line,
					print "   ", delta
				else:
					delta = (secsfromepoch - lastdate)
					lastdate = secsfromepoch
					curline += 1
					if delta <> 1 and delta < 60 or delta > -60:
						timeunit = "seconds pass..."
					if delta > 60 or delta < -60:
						divided = divmod (delta, 60) 
						delta = divided[0], "minutes, ", divided[1], " seconds"
						timeunit = " pass..."
					elif delta == 1:
						timeunit = "second passes..."
					print line,
					print "   ", delta, timeunit
		except IOError:
			print "Not a valid file. Try again."
		logfile.close()

	def parseOptions(self, args):
		"""Parse options passed if any, accessible via self.options:"""
		self.parser = optparse.OptionParser()
		self.parser.add_option("-d", "--showwithdelta", dest="showdelta", 
			help="Print file passed along with delta "
			"of times between entries.", action="store_true" )
		self.options, self.args = self.parser.parse_args(args=args)

	def main(self):
		self.parseOptions(sys.argv[1:])
		if not self.args:
			print "Have to pass a filename!"
			sys.exit()
		filename = self.args[0]
		if self.options.showdelta:
			self.showWithDelta(filename)
		else:
			self.showWithoutDelta(filename)
		sys.exit()
#-----------------------------------------------------------------------------
def run():
	mainclass = Main()
	mainclass.main()

if __name__ == "__main__":
    run()
