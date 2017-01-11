# program: thermo.py
#
# purpose:
#
# update: 7/3/2016
#

import os
import pylab
import sys

if len(sys.argv) < 4:
   print "Usage: python thermo.py #1 #2 filename"
   sys.exit(1)

argv=sys.argv

first = int(float(argv[1]))
last = int(float(argv[2]))
inputFile = argv[3]

for i in range(first, last+1):
   folder = "run"+str(i)+"/"

   name = folder+inputFile
   output = folder+"thermo"

   file = open(name, "r")
   fileout = open(output, "w")

   nfield = 0

   while True:
      line = file.readline()		# read a line
      list = line.split()		# parse a line

      if (len(line)==0):		# EOF (End-Of-File)
	 break
      elif len(list)>1:			# line contains more than one field
	 if list[0] == "Step":		# title line
	    nfield = len(list)
	    #print line,			# print the title line
	    fileout.write(line)
	    break
   
   previous = -1

   while True:
      line = file.readline()		# continue reading
      list = line.split()

      if (len(line)==0):		# EOF (End-Of-File)
	 break
      elif len(list) == nfield and list[0].isdigit() and float(list[0])>float(previous):
	 #print line,
	 fileout.write(line)
	 previous = list[0]

   file.close()
