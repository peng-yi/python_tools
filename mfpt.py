# program: mfpt.py
#
# purpose:
#
# update: 7/3/2016
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
    print "Usage: python mfpt.py number1 number2"
    sys.exit(1)
argv = sys.argv

first = int(float(argv[1]))
last  = int(float(argv[2]))

# read raw data from files
rawdata={}

for i in range(first, last+1):
    folder = "run" + str(i) + "/"
    name = folder + "mfpt"

    os.system("grep nuclei " + folder + "output.0 > nuclei0")
    os.system("sort -n -u -k2 nuclei0 >nuclei")
    os.system("searchfirst nuclei 2 5 0 1 0 >mfpt")
    os.system("mv nuclei mfpt " + folder)
    
    file = open(name,"r")
    for line in file.readlines():
       x, y = line.split()
       x = int(float(x))
       y = float(y)
       if x not in rawdata.keys():
	  rawdata[x]=[y]
       else:
	  rawdata[x].append(y)

# calculate mean and standard deviation
Mean=[]
Std=[]
Sterr=[]
for key in rawdata.keys():
    mean, std = getMeanAndStd(rawdata[key])
    Mean.append(mean*4e-6)
    Std.append(std*4e-6)
    Sterr.append(std/math.sqrt(10)*4e-6)

# output statistics
out = open("mfpt", "w")
for i in xrange(len(rawdata)):
    out.write("%d %f %f %f\n" %(rawdata.keys()[i], Mean[i], Std[i], Sterr[i])) 
out.close()    

# make plot
#pylab.errorbar(rawdata.keys(), Mean, yerr=Std)
pylab.plot(rawdata.keys(), Mean, 'bo')
pylab.xlim([0, 100])
pylab.xlabel("n_max")
pylab.ylabel("Time (ns)")
pylab.title("Mean First Passage Time")
pylab.legend(("legend",))
pylab.show()

