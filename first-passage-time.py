#!/software/apps/anaconda/5.2/python/2.7/bin/python
# program: first-passage-time.py
#
# purpose: compute the first passage time of certain property
#
# update: 12/10/2018
#

from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
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

def func_fpt(x, tau, Z, x0):
    return 0.5*tau*(1+np.erf(Z*(x-x0)))

def func_fptG(x, tau, Z, x0, k, Zg):
    return 0.5*tau*(1+np.erf(Z*(x-x0))) + 0.5*k*(x-x0)*(1+np.erf(Zg*(x-x0)))

# end of helper code
# --------------------------------------

# --------------------------------------
# constants  
timeunit = 250000
# --------------------------------------

if len(sys.argv) < 6:
    print "Usage: python first-passage-time.py string filename coltime coldata dn"
    sys.exit(1)

argv = sys.argv
string = argv[1]
name = argv[2]
colx = int(float(argv[3]))-1
coly = int(float(argv[4]))-1
dn = int(float(argv[5]))

# get current working directory
cwd = os.getcwd()   	

# get subfolder names
subfolders = [ i for i in os.listdir(cwd) if os.path.isdir(i) and string in i]

subfolders = [filter(str.isdigit, i) for i in subfolders]

tmp = [int(float(i)) for i in subfolders]
tmp = sorted(tmp, reverse=False)

subfolders = ['run'+str(i) for i in tmp]

clr = ['k','r','b','c','m','g']
x0 = []
tau= []
Z = []
iclr = 0
for folder in subfolders:
   filename = folder + '/' + name

   print filename

   if not os.path.isfile(filename) or os.path.getsize(filename)==0:
      os.chdir(cwd)
      continue

   x=[]
   y=[]
   fin = open(filename,"r")

   for line in fin.readlines():
      data = line.split()
      if data[colx].replace('.','').isdigit():
	 x.append(float(data[colx]))
	 y.append(float(data[coly]))

   fin.close()

   y0=0
   fpx=[]
   fpy=[]
   for i in range(0,len(y),dn):
      if y[i] > y0:
	 y0 = y[i]
	 fpx.append(y[i])
	 fpy.append(x[i])

   fpx=np.asarray(fpx)
   fpy=np.asarray(fpy)
   init_vals = [1e6, 1.0, 5.0]
   #(tau, Z, x0)
   xmax = 200
   x = np.asarray([i for i in fpx if i <= xmax])
   y = fpy[:len(x)]

   lb = (0,0,0)
   ub = (np.inf, np.inf, np.inf)
   param, covar = curve_fit(func_fpt, x, y, bounds=(lb, ub), p0=init_vals)
   print param
   #print "%d, %f, %f" %(time, slope1, slope2)
   tau.append(param[0])
   Z.append(param[1])
   x0.append(param[2])

   plt.plot(x, y/timeunit, 'o', color=clr[iclr])

   fitx = np.linspace(0,xmax,xmax+1)
   fity = func_fpt(fitx, param[0], param[1], param[2])

   plt.plot(fitx, fity/timeunit, '-', label=str(folder),color=clr[iclr],linewidth=1.2)
   iclr += 1
   iclr = iclr %len(clr)

print sum(tau)/len(tau), sum(Z)/len(Z), sum(x0)/len(x0)

#plt.xlim([0, 150])
plt.xlabel(r'n$_{\rm{max}}$',fontsize=20)
plt.ylabel("first passage time (ns)",fontsize=20)
plt.title("First Passage Time",fontsize=20)
plt.legend(loc=1,shadow=False,prop={'size':14})
plt.savefig('mfpt.png',dpi=300)
plt.show()

