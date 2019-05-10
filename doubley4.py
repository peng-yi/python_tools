#!/software/apps/anaconda/5.2/python/2.7/bin/python
# program: doubley4.py
#
# purpose: plot two y's, 4 subplots
#
# update: 12/4/2018
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

fig = plt.figure(figsize=(20,15))
st = fig.suptitle("800K",fontsize=20)

#files=['900Kd25','900Kd15','900Kd12','900Kd10']
files=['800Kd25','800Kd15','800Kd12','800Kd10']
label=['25','15','12','10']

for i in range(4):
   filename = files[i]

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
   Y1 = np.asarray(Y1)
   Y2 = np.asarray(Y2)
   Y2 /= 1e4   # convert pressure unit from bar to GPa
   
   #---- Make double-Y plot
   #
   ax1 = fig.add_subplot(220+i+1)
   ax1.plot(X, Y1, '-', marker='s', color='b', linewidth=2)
   ax1.set_xlabel('X ('+r'$\rm{\AA}$'+')', fontsize=14)
   # Make the y-axis label, ticks and tick labels match the line color.
   ax1.set_ylabel('Composition', color='b',fontsize=14)
   ax1.tick_params('y', colors='b',length=6,labelsize=12)
   #ax.tick_params(which='major',length=6,labelsize=10)
   #ax.tick_params(which='minor',length=3)
   #ax.tick_params(direction='in',which='both',labelright='on')
   
   ax2 = ax1.twinx()
   ax2.plot(X, Y2, '-', marker='o',color='r', linewidth=2)
   #ax2.set_ylabel('Number of atoms in bin', color='r', fontsize=14)
   ax2.set_ylabel('Pressure (GPa)', color='r', fontsize=14)
   ax2.tick_params('y', colors='r',length=6,labelsize=12)
   
   ax1.text(0.5,0.75, 'd = '+label[i]+r'$\rm{\AA}$', horizontalalignment='center',bbox=dict(boxstyle='round',fc='w',alpha=0.5,pad=0.5),transform=ax1.transAxes,size=18)

   i += 1

fig.tight_layout(pad=1.4, w_pad=2, h_pad=2)
st.set_y(0.95)
fig.subplots_adjust(top=0.90)
plt.savefig('output.png',dpi=300)
plt.show()
