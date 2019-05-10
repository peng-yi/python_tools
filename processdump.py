#!/software/apps/anaconda/5.2/python/2.7/bin/python
# Program: processdump.py
#
# Process the LAMMPS dump file
#
# Syntax: python processdump.py inputfilename outputfilename
#
# Author: Peng Yi @ JHU
#
# Created: 11/29/2018
#

import matplotlib.pyplot as plt
import math
import os
import sys

# --------------------------------------
# Helper code

def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
       tot += (x-mean)**2
    std = (tot/len(X))**0.5
    return mean, std

# end of helper code
# --------------------------------------

if len(sys.argv) < 3:
    print "Usage: python processdump.py infile outfile"
    sys.exit(1)
argv = sys.argv

infile = argv[1]
outfile = argv[2]

fin = open(infile,"r")
fout = open(outfile,"w")

for line in fin.readlines():
    data = line.split()

    # convert triclinic box to orthorgonal
    if 'xy' in data:
       data.remove('xy')
       data.remove('xz')
       data.remove('yz')

    if len(data)==3 and math.fabs(float(data[2]))<1e-6:
       del data[2]
    
    outline = data[0]
    for i in range(1,len(data)):
       outline += " " + data[i]
    outline += "\n"
    fout.write(outline)

fin.close()
fout.close()

