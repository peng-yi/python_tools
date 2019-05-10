#!/software/apps/anaconda/5.2/python/2.7/bin/python
# program: extractThermo.py
#
# purpose: go to subfolders, extract thermodynamic output from LAMMPS log file
#
# Author: Peng Yi @ JHU
#
# update: 7/3/2016, 11/17/2018, 12/1/2018
#

import os
import pylab
import sys

if len(sys.argv) < 2:
   print "Usage: python thermo.py infilename"
   sys.exit(1)

argv=sys.argv

infile = argv[1] 		# LAMMPS log file

output = "thermodata"

#---- Find subfolders
#
cwd = os.getcwd()   					# get the current working directory
subfolders = [ i for i in os.listdir(cwd) if os.path.isdir(i)] 	# get subfolder names

for folder in subfolders:

   os.chdir(folder)
 
   if not os.path.isfile(infile):
      os.chdir(cwd)
      continue

   fin = open(infile, "r")
   fout = open(output, "w")

   nfield = 0

   while True:
      line = fin.readline()		# read a line
      data = line.split()		# parse a line

      if (len(line)==0):		# EOF (End-Of-File)
	 break
      elif len(data)>1:			# line contains more than one field
	 if data[0] == "Step":		# title line
	    nfield = len(data)
	    #print line,			# print the title line
	    fout.write(line)
	    break

   previous = -1

   while True:
      line = fin.readline()		# continue reading
      data = line.split()

      if (len(line)==0):		# EOF (End-Of-File)
	 break
      elif len(data) == nfield and data[0].isdigit() and float(data[0])>float(previous):
	 #print line,
	 fout.write(line)
	 previous = data[0]

   fin.close()
   fout.close()

   os.chdir(cwd)
