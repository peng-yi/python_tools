#!/software/apps/anaconda/5.2/python/2.7/bin/python
# program: fitprofile.py
#
# purpose: fit composition profile to erf functions
#
# update: 12/8/2018
#
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import sys

#---- default values of constants used in the program ------------------------#
timeunit = 1
timeend = 5e6
timeinterval = 1e6
#-----------------------------------------------------------------------------#

def rect(x, A, C, sig1, mu1, sig2, mu2):
   B=0
   return A*(np.erf((x-mu1)/sig1) + np.erf(-(x-mu2)/sig2))/2 + C

argv = sys.argv

filename = argv[1]
colx = int(float(argv[2]))-1 	# first column in python datastructure is 0, not 1
coly = int(float(argv[3]))-1 
if (len(argv) > 4):
   timeinterval = int(float(argv[4]))
   timeend = int(float(argv[5]))

# Set up plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set(xlabel=r'X ($\rm{\AA}$)', ylabel=r'Ni composition')

clr = ['k', 'r', 'b','c','m', 'g']
iclr =0

time = 0
fin = open(filename, "r")
for line in fin.readlines():
   data=line.split()

   if len(data)>1:
      if not data[0].isdigit(): 			# first line of record
	 b = [filter(str.isdigit, i) for i in data]
	 time=int(float(b[0])/timeunit)
	 if time > timeend:
	    break
	 count = 0
	 output = 1
	 x=[]
	 y=[]
      else:
	 count += 1
	 x.append(float(data[colx]))
	 y.append(float(data[coly]))

   elif time%timeinterval==0 and output==1: 		# output only every certain steps
         output = 0
         x=np.asarray(x)
         y=np.asarray(y)
	 init_vals = [-0.3, 0.65, 15, 25, 15, 65]
	 #(A, C, sig1, mu1, sig2, mu2)

	 #param, covar = curve_fit(rect, x, y, p0=init_vals)
	 #print time, param
	 #slope1 = abs(param[0]/param[2])
	 #slope2 = abs(param[0]/param[4])
	 #print "%d, %f, %f" %(time, slope1, slope2)

	 #yfit = rect(x, param[0], param[1], param[2], param[3], param[4], param[5])
	 ax.plot(x, y, 'o-', label=str(time/250000)+'ns',color=clr[iclr])
	 #plt.plot(x, yfit, '-',label=str(time),linewidth=1.5, color=clr[iclr])
	 iclr += 1
	 iclr = iclr%6

fin.close()

ax.text(0.5,0.85, 'T=1200K\n'+r'd=35$\rm{\AA}$', horizontalalignment='center',bbox=dict(boxstyle='round',fc='w',alpha=0.5,pad=0.5),transform=ax.transAxes,size=18)

#textx=6
#texty=3000
#ax.annotate("", xy=(4.5,2000), xytext=(textx,texty),arrowprops=dict(fc='r',shrink=0.1))
#ax.text(textx,texty,'martensitic transformation',color='r',size=16)

ax.xaxis.label.set_size(20)
ax.yaxis.label.set_size(20)
ax.title.set_size(20)

ax.legend(loc='best',shadow=False,prop={'size':14})
plt.tight_layout()
plt.savefig("out.png",dpi=300)
plt.show()
exit(1)
