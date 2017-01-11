# program: work.py
#
# purpose:
#
# update: 8/8/2016
#

import pylab
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
    print "Usage: python work.py number1 number2"
    sys.exit(1)
argv = sys.argv

data=[]
file=open('de','r')

line=file.readline()
list=line.split()
refdata=float(list[3])
print refdata

i=0
for line in file.readlines():
   list=line.split()
   if (i>0):
      data.append(float(list[3])-refdata)
   i+=1

print i
mean,std=getMeanAndStd(data)
print mean, std
