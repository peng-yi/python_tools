#!/software/apps/anaconda/5.2/python/2.7/bin/python
# Program: ave.py
#
# Calculate the mean and standard deviation of columns of data
#
# Syntax: python ave.py filename col#1 col#2 ...
#
# output: file "results"
#
# Author: Peng Yi @ JHU
#
# update: 7/3/2016, 7/19/2018, 11/17/2018
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

if len(sys.argv) < 2:
    print "Usage: python ave.py filename col1 col2 col3 ..."
    sys.exit(1)
argv = sys.argv

filename = argv[1]

# read raw data from files
rawdata=[]

file = open(filename,"r")
for line in file.readlines():
    data = line.split()

    if len(rawdata) == 0:
       for i in range(len(data)):
	  rawdata.append([])

    for i in range(len(data)):
       rawdata[i].append(float(data[i]))

# calculate mean and standard deviation
Mean=[]
Std=[]

for i in range(len(rawdata)):
    mean, std = getMeanAndStd(rawdata[i])
    Mean.append(mean)
    Std.append(std)
    #Mean.append(str(round(mean,4)))
    #Std.append(str(round(std,4)))

# output
out = open("results", "a")
out.write("Averaging cols of file \"" + filename + "\"\n")

for i in range(2,len(argv)):
   col = int(argv[i])-1
   out.write("Col#%d: %8.4f +- %3.4f\n" %(col+1, Mean[col], Std[col]))

out.close()    
