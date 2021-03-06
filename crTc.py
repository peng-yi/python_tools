# program: crTc.py
#
# purpose:
#
# update: 7/3/2016
#

import pylab
import os.path
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
    print "Usage: python crTc.py number1 number2"
    sys.exit(1)
argv = sys.argv

first = int(float(argv[1]))
last  = int(float(argv[2]))

# read raw data from files
time = []
compos = []
timestep = 4e-6   	# ns
nmax = 100
t0 = 400     		# K
#rate = 50           	# K/ns, + for heating, - for cooling
rate = 50          	# K/ns, + for heating, - for cooling

for i in range(first, last+1):
    name = "run"+str(i)+"/mfpt"
    
    if not os.path.isfile(name):
       continue

    file = open(name,"r")
    for line in file.readlines():
       x, y = line.split()
       if float(x) >= nmax:
	  time.append(float(y))
	  break
 
    file.close()	  

    name = "run"+str(i)+"/nuclei"		# search file nuclei
    if not os.path.isfile(name):
       continue
    file = open(name,"r")
    for line in file.readlines():
       element = line.split()
       if float(element[4]) >= nmax:   	# when nmax is greater than the threshold
	  compos.append(float(element[6]))
	  break

    file.close()	  

# calculate mean and standard deviation
for i in range(len(time)):
    time[i] *= timestep
    time[i] = t0 + time[i]*rate		

mean, std = getMeanAndStd(time)
mean = round(mean,2)
std = round(std,2)
print mean, std

compos_mean, compos_std = getMeanAndStd(compos)
print compos_mean, compos_std

# output statistics
#out = open("mfpt", "w")
#for i in xrange(len(rawdata)):
#    out.write("%d %f %f\n" %(rawdata.keys()[i], Mean[i], Std[i])) 
#out.close()    

# make plot
#pylab.errorbar(rawdata.keys(), Mean, yerr=Std)
pylab.hist(time, 10, label="mean="+str(mean)+"K, std="+str(std)+"K")
pylab.xlabel("Nucleation Temperature (K)")
pylab.ylabel("Probability (arb.)")
pylab.title("Nucleation Temperature (10 samples)\ncooling rate 50K/ns, 100,000 atoms")
pylab.legend(loc='best')
pylab.show()

