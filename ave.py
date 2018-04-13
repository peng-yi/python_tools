#!/cm/shared/apps/Intel/python/2.7.10/bin/python
# program: ave.py
#
# purpose:
#
# update: 7/3/2016
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
    print "Usage: python ave.py filename"
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

#print "Mean = ", Mean
#print "Std = ", Std

# output
out = open("stat", "a")
out.write("%.4f %.4f %.4f %.4f %.4f %.4f\n" %(Mean[8], Std[8], Mean[9], Std[9], Mean[10], Std[10])) 
out.close()    
