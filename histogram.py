#!/software/apps/anaconda/5.2/python/2.7/bin/python
# Program: histogram.py
#
# Calculate the mean and standard deviation of columns of data
#
# Syntax: python histogram.py filename1 filename2 col
#
# output: file "results", histogram figure file output.png
#
# Author: Peng Yi @ JHU
#
# update: 3/27/2019
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
    print "Usage: python histogram.py filename1 filename2 filename3 col"
    sys.exit(1)
argv = sys.argv

filenames = [argv[1], argv[2], argv[3]]
col = int(float(argv[4]))-1
colors=['b','r','k']
labels=filenames

fig = plt.figure()

for counter, filename in enumerate(filenames):

   ax  = fig.add_subplot(111)

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

   ax.hist(rawdata[col], bins=20, facecolor=colors[counter], alpha=0.5, label=labels[counter], normed=0)

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

for i in range(4,len(argv)):
   col = int(argv[i])-1
   out.write("Col#%d: %8.4f +- %3.4f\n" %(col+1, Mean[col], Std[col]))

out.close()    


#ax.set_title('Histogram of $q_6$ for all atom (after 100ps)', fontsize=18)
#ax.set_xlabel('$q_6$', fontsize=18)
ax.set_title('Histogram of displacement for all atom (after 1ns)', fontsize=18)
ax.set_xlabel('displacement ('+r'$\rm{\AA}$'+')', fontsize=18)
ax.set_ylabel('Number of atoms', fontsize=18)
ax.set_yscale("log")
#ax.set_ylim([0, 800])
legend = ax.legend(loc='best',shadow=False,prop={'size':10})
frame = legend.get_frame()
frame.set_facecolor('0.95')

for label in legend.get_texts():
   label.set_fontsize('large')

for label in legend.get_lines():
   label.set_linewidth(1.5)

fig.tight_layout()
plt.savefig("output.png",dpi=300)
plt.show()
