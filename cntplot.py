#!/software/apps/anaconda/5.2/python/2.7/bin/python
# program: cntplot.py
#
# purpose: plot formation energy of a cylindrical nucleus with composition step change at r0
#
# update: 4/30/2019

import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from scipy.special import erf

if len(sys.argv) < 2:
    print("Usage: python cntplot.py option")
    sys.exit(1)

argv = sys.argv

option = argv[1]    # 'step' or 'erf'

#t=np.arange(0.1, 8.0, 0.1)

r = np.linspace(0, 40, 1001)
r0  = 10.0
dr = r[1]-r[0]
print(r0, dr)

inverfw = 100.0
sigma1 = 10.0
sigma2 = 4.0

dg1 = -1.0
dg2 = -0.2

if option == 'step':
   surface1 = (sigma1 * 2*np.pi*(r+0.5*dr))[r<r0]
   surface2 = (sigma2 * 2*np.pi*(r+0.5*dr))[r>=r0]
   surface = np.concatenate((surface1, surface2))
   plt.plot(r, surface)
   plt.show()

   bulk1 = (dg1 * np.pi*(r+0.5*dr)**2) [r<r0]
   bulk2 = (dg2 * np.pi*((r+0.5*dr)**2-(r0+0.5*dr)**2) + dg1 * np.pi*(r0+0.5*dr)**2) [r>=r0]
   bulk = np.concatenate((bulk1, bulk2))
   plt.plot(r, bulk)
   plt.show()

elif option == 'erf':
   avesigma = (sigma1+sigma2)/2.0
   dsigma = sigma2-sigma1

   sig_r = avesigma + 0.5 * dsigma * erf(inverfw * np.log((r+0.5*dr)/r0))
   surface = sig_r * np.pi * (r+0.5*dr) * 2
   plt.plot(r, surface)
   plt.show()

   avedg = (dg1 + dg2)/2.0
   ddg = dg2 - dg1

   dg_r = avedg + 0.5 * ddg * erf(inverfw * np.log((r+0.5*dr)/r0))

   tmp = dg_r * 2*np.pi*(r+0.5*dr) * dr
   bulk = np.cumsum(tmp)
   plt.plot(r, bulk)
   plt.show()

#plt.plot(t, P)
plt.plot(r, surface+bulk)
#plt.xlim(0,40)
plt.show()
