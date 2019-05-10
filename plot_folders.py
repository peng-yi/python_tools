#!/software/apps/anaconda/5.2/python/2.7/bin/python
# program: plot_folders.py
#
# purpose: plot same file in multi folders sharing the same string in their folder names
#
# update: 12/20/2017, 12/1/2018, 1/30/2019
#

import matplotlib.pyplot as mp
import matplotlib.ticker as ticker
import math
import os
import sys
import numpy as np

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
    print("Usage: python plot_folders.py string filename colx coly")
    print("       string is the common string in folder names")
    print("       filename is the name of the file in folders")
    sys.exit(1)

argv = sys.argv
string = argv[1]
name = argv[2]
colx = int(float(argv[3]))
coly = int(float(argv[4]))

# --------------------------------------
# Get names of folder and sort them
# --------------------------------------

# get current working directory
cwd = os.getcwd()   	

# get subfolder names
subfolders = [ i for i in os.listdir(cwd) if os.path.isdir(i) and string in i]

# find numbers in subfolder names
nums = [filter(str.isdigit, i) for i in subfolders]

# find prefix before the number in subfolder names
prefix = ''.join([i for i in subfolders[0] if not i.isdigit()])

# sort the numbers
tmp = [int(float(i)) for i in nums]
tmp = sorted(tmp, reverse=True)

# sort the subfolders based on the numbers
subfolders = [prefix + str(i) for i in tmp]

# ---- Set up plot
fig = mp.figure()
ax = fig.add_subplot(111)

clr = ['k', 'r', 'b','c','m', 'g']
iclr = 0


for folder in subfolders:
   filename = folder + '/' + name

   print filename

   if not os.path.isfile(filename):
      os.chdir(cwd)
      continue

   fin = open(filename, 'r')

   X = []
   Y = []
   for line in fin.readlines():
      data = line.split()

      if data[1].replace(".","").isdigit():
	 x = float(data[colx-1])
	 y = float(data[coly-1])
	 X.append(x)
	 Y.append(y)

   X=np.asarray(X)
   #X/=250000
   #X*=float(filter(str.isdigit,folder))
   Y=np.asarray(Y)
   ax.plot(X, Y, label=folder, color=clr[iclr], linewidth=1.2)
   iclr += 1
   iclr = iclr%len(clr)

#ax.set(xlim=[0.0, None])
#ax.set(ylim=[0.0, None])
#ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
#ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_ticks_position('both')
ax.tick_params(which='major',length=6,labelsize=10)
ax.tick_params(which='minor',length=3)
ax.tick_params(direction='in',which='both',labelright='on')

#ax.set(title='spherical nucleus, no gradient', xlabel='Time (ns)', ylabel=r'$\frac{\mathrm{Nucleus\ size}}{\mathrm{Nucleus\ size @ t=0}}$')
#label = [r'r=5$\math{\AA}$',r'r=10$\mathrm{\AA}$',r'r=15$\mathrm{\AA}$',r'r=20$\mathrm{\AA}$',r'r=25$\mathrm{\AA}$',r'r=30$\mathrm{\AA}$']

ax.set(title=r'NiAl nucleation, P=0Pa', xlabel=r'Time (ns)/gradient', ylabel=r'n$_{max}$')
ax.xaxis.label.set_size(20)
ax.yaxis.label.set_size(20)
ax.title.set_size(20)

#ax.text(0.05,0.85, 'T=900K\n'+r'd=12$\AA$', horizontalalignment='left',bbox=dict(boxstyle='round',fc='w',alpha=0.5,pad=0.5),transform=ax.transAxes,size=18)
#textx=10
#texty=6000
#ax.annotate("", xy=(8.8,6700), xytext=(textx,texty),arrowprops=dict(fc='r',shrink=0.1))
#ax.text(textx,texty,'martensitic transformation',color='r',size=16)

legend = ax.legend(loc='best',shadow=False,prop={'size':10})
frame = legend.get_frame()
frame.set_facecolor('0.95')

for label in legend.get_texts():
   label.set_fontsize('large')

for label in legend.get_lines():
   label.set_linewidth(1.5)

mp.tight_layout()
mp.savefig('output.png',dpi=300)
mp.show()
exit(0)
