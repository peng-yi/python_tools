#!/software/apps/anaconda/5.2/python/2.7/bin/python
#
# Syntax: python contour-field.py filename columnid
#
# author: Peng Yi @ JHU
#
# date: 11/17/2018, 2/15/2019
#

#from matplotlib.mlab import griddata
import scipy.interpolate
import matplotlib.pyplot as plt
import numpy as np
import sys

argv = sys.argv

if len(sys.argv) < 3:
    print "Usage: python contour-2d.py filename datacol"
    sys.exit(1)

filename = argv[1]
colz = int(float(argv[2]))-1  	# first column in python datastructure is 0, not 1

x, y, z = np.genfromtxt(filename, unpack=True, usecols=(0,1,colz))
#print x
#print y 
#print z
#exit(1)

#z = z*100
xll = np.amin(x, axis=0); xul = np.amax(x, axis=0); yll = np.amin(y, axis=0); yul = np.amax(y, axis=0)

zmin = np.amin(z)
zmax = np.amax(z)

#Nx=128; Ny=128
Nx=24; Ny=12
xi = np.linspace(xll, xul, Nx)
yi = np.linspace(yll, yul, Ny)
zi = scipy.interpolate.griddata((x,y), z, (xi[None, :], yi[:, None]), method='cubic')

#levels=np.arange(-1.0, 1.01, 0.2)
levels=[-4.1]
contours = plt.contour(xi, yi, zi, levels=levels, linewidth=1, colors='black')

#-- Collect contour path coordinates
p=contours.collections[0].get_paths()[0]
v = p.vertices
print v.T
xx = v[:,0]
yy = v[:,1]
print xx
print yy
plt.plot(yy,xx)
plt.show()
# 2nd path
p=contours.collections[0].get_paths()[1]
v = p.vertices
xx = v[:,0]
yy = v[:,1]
print xx
print yy
plt.plot(yy,xx)
plt.show()

#-- Plot setup
plt.clabel(contours, inline=True, fontsize=8)
plt.imshow(zi, extent=[xll, xul, yll, yul], origin='lower', cmap=plt.cm.jet, alpha=0.9)
plt.xlabel(r'$X (\AA)$', fontsize=16)
plt.ylabel(r'$Z (\AA)$', fontsize=16)
#plt.clim(-1.05, 1.05)
plt.clim(zmin, zmax)
#plt.ylim(10, 196)
#plt.colorbar(ticks=[0.03, 0.06, 0.09, 0.12, 0.15])
#plt.colorbar(ticks=[3, 6, 9, 12, 15])
plt.colorbar(ticks=[-1, -0.5, 0, 0.5, 1.0])
plt.savefig('be3.png', format='png', dpi=400, bbox_inches='tight')
plt.show()

