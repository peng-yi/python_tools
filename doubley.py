#!/software/apps/anaconda/5.2/python/2.7/bin/python
# program: doubley.py
#
# purpose: plot two y's
#
# update: 12/4/2018, 1/30/2019
#
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker
import math
import os
import sys

if len(sys.argv) < 5:
    print "Usage: python doubley.py infile colx coly1 coly2"
    sys.exit(1)

argv = sys.argv
filename = argv[1]
colx = int(float(argv[2]))
coly1 = int(float(argv[3]))
coly2 = int(float(argv[4]))

print filename, colx, coly1, coly2

X  = []
Y1 = []
Y2 = []

fin = open(filename,"r")
for line in fin.readlines():
   data = line.split()

   if data[1].replace('.','').isdigit():
      X.append(float(data[colx-1]))
      Y1.append(float(data[coly1-1]))
      Y2.append(float(data[coly2-1]))

fin.close()

X = np.asarray(X)
X /= 250000
Y1 = np.asarray(Y1)
Y2 = np.asarray(Y2)
#Y2 /= 1e4   # convert pressure unit from bar to GPa

#---- Make double-Y plot
#
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(X, Y1, '-', marker='s', color='b', linewidth=2)
#ax1.set_xlabel('X ('+r'$\rm{\AA}$'+')', fontsize=18)
ax1.set_xlabel('Time (ns)', fontsize=18)
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Nmax (atoms)', color='b',fontsize=18)
ax1.tick_params('y', colors='b',length=6,labelsize=12)
#ax1.set(ylim=[0.0, 20])
ax1.set_yscale("log")

#ax.tick_params(which='major',length=6,labelsize=10)
#ax.tick_params(which='minor',length=3)
#ax.tick_params(direction='in',which='both',labelright='on')

if coly2 > 0: 
   ax2 = ax1.twinx()
   ax2.plot(X, Y2, '-', marker='o',color='r', linewidth=2)
   ax2.set_ylabel('2ndNmax (atoms)', color='r', fontsize=18)
   ax2.tick_params('y', colors='r',length=6,labelsize=12)
   ax2.set_yscale("log")

ax1.text(0.5,0.85, 'd = 20'+r'$\rm{\AA}$ (run5)', horizontalalignment='center',bbox=dict(boxstyle='round',fc='w',alpha=0.5,pad=0.5),transform=ax1.transAxes,size=18)

fig.tight_layout()
plt.savefig('output.png',dpi=300)
plt.show()
