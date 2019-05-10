#!/cm/shared/apps/Intel/python/2.7.10/bin/python
# program: colSplit.py
#
# purpose: convert one column of data evenly into several columns
#
# author: Peng Yi @ JHU
#
# update: 4/15/2018, 11/17/2018
#

import matplotlib.pyplot as plt
import math
import os
import sys

# --------------------------------------
# Helper code

# end of helper code
# --------------------------------------

if len(sys.argv) < 2:
    print "Usage: python rowcolumn.py filename rownumber"
    sys.exit(1)
argv = sys.argv

filename = argv[1]
rownumber = int(float(argv[2]))

# read raw data from files
rawdata=[]

count = 0
infile = open(filename,"r")
for line in infile.readlines():
    #data = line.split()
    line = line.rstrip("\n")      # remove "\n" from the line

    if len(line) > 0:
       if (count < rownumber):  	# first column
	  rawdata.append(line)  
       else:
	  rawdata[count%rownumber] += ("   " + line)
    else:
       break

    count += 1
infile.close()

print "total "+str(count)+" lines data."

# output
out = open("output", "w")
for i in range(rownumber):
   out.write(rawdata[i]+"\n")
out.close()    
