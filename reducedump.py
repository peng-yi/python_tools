#!/software/apps/anaconda/5.2/python/2.7/bin/python
# Program: reducedump.py
#
# Process the LAMMPS dump file, keep one of every nfreq snapshot
#
# Syntax: python reducedump.py inputfilename outputfilename nfreq istart
#
# Author: Peng Yi @ JHU
#
# Created: 12/1/2018
# Updated: 5/10/2019
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

if len(sys.argv) < 5:
    print("Usage: python processdump.py infile outfile nfreq istart")
    print("       istart: 0 - keep the first configuration, then every nfreq conf.")
    print("       istart: 1 - keep the second configuration, then every nfreq conf.")
    print("       istart: ......")
    sys.exit(1)
    
argv = sys.argv

infile = argv[1]
outfile = argv[2]
nfreq = int(float(argv[3]))
nstart = int(float(argv[4]))

fin = open(infile,"r")
#fout = open(outfile,"w")

numnext = 0

for line in fin.readlines():
    data = line.split()

    if "NUMBER" in data:
       numnext = 1
       continue
    if numnext:
       natoms = int(float(data[0]))
       break

command = "awk \"{if (int((NR-1)/"+str(natoms+9)+")%"+str(nfreq)+"=="+str(nstart)+") print}\" " + infile + " > " + outfile
print command
os.system(command)

fin.close()
#fout.close()

