#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compareCorrelations.py
Created on Fri Oct 26 16:15:20 2018

@author: dariusalix-williams
d.alixwill@jhu.edu
"""
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import summary_table
from scipy.optimize import curve_fit
import scipy.optimize as opt
import numpy as np
import pandas as pd
# import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import os
import sys
import math
import peakutils
from sklearn.linear_model import LogisticRegression
from scipy.optimize import leastsq
from scipy import asarray as ar, exp

#sys.exit(0)
# Define file paths        
mainFilePath = os.getcwd().rsplit('/',2)[0]
#print(mainFilePath)
#sys.exit(0)
outFilePath = mainFilePath + '/figures/combined/'
inFilePath = mainFilePath + '/figures/npy/'
scriptFilePath = mainFilePath + '/scripts/'

kB = 8.6173303e-5

# Get density
matSystem = 'Cu64Zr36'
quenchRate = '5e11'
runNum = '5'
outFileName = inFilePath + matSystem + '--run_' + runNum + '--Q_' + quenchRate + '--'
rho = np.load(outFileName + 'rho.npy')

def logistic5(x, A, B, C, D, E): #
    #D = 1
    #E = 0
    return A*np.exp(B*(x-C))/(np.exp(B*(D*x-C))+1)+E

def linear(x, m, b):
    #b = 0
    return m*x + b

def poly(x, a, b, c):
    return a*x**2 + b*x + c

def gauss(x, A, B, C, D):

    return A*np.exp(-(x-B)**2/(2*C*C)) + D

def gl(x, sig, mu, m, A):
    
    return A*np.exp(-(x-mu)**2/(2*sig**2)) + m*x

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

# Make output dirpectory
if not os.path.exists(outFilePath):
    os.mkdir(outFilePath)


# Constants, Initialization of variables
Tbath = np.load(inFilePath + 'Cu64Zr36--run_0--Q_5e12--TBath.npy')
matSystem = 'Cu64Zr36'
quenchRate = ['5e12', '5e11', '5e10']
Runs = ['0123456789', '0123456789', '0123456789']
markers = ['o', '^', 's']
colors = ['red', 'orange', 'blue']
linestyles=[':','-.','--']
offset=[0,0.1,0.2]


# Fast Subsystem
fig = plt.figure()
for iQ, vQ in enumerate(quenchRate):
    
    outFileName = matSystem + '--runs_' + Runs[iQ] + '--Q_' + vQ + '--'
    gFave = np.load(inFilePath + outFileName + 'gFave.npy')
    gFstd = np.load(inFilePath + outFileName + 'gFstd.npy')
    
    plt.plot(Tbath[::5], gFave[::5]+offset[iQ], \
             marker=markers[iQ], markersize=4, \
             linestyle=linestyles[iQ],\
             color=colors[iQ], label=vQ)


#titleText = 'Fast DoFs Auto-Correlation'
#plt.title(titleText)
plt.xlabel(r'$T_{Res.} \hspace{0.5} [K] $')
plt.ylabel(r'$g_F \hspace{1} [eV^2 \cdot \AA^3]$')
axes = plt.gca()
axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#plt.legend(title=r'$\dot{T}$ [K/s]')
plt.legend(bbox_to_anchor = (1.04, 0.5), loc = 'center left', \
           title=r'$\dot{T}$ [K/s]')
plt.tight_layout()
figName = outFilePath + matSystem + '--runs_ALL--Q_ALL--gF_vs_T'
#plt.savefig(figName, dpi=200)
plt.close(fig)    
    

# Slow Subsystem
fig = plt.figure()
for iQ, vQ in enumerate(quenchRate):
    
    outFileName = matSystem + '--runs_' + Runs[iQ] + '--Q_' + vQ + '--'
    gSave = np.load(inFilePath + outFileName + 'gSave.npy')
    gSstd = np.load(inFilePath + outFileName + 'gSstd.npy')
    
    # Estimate initial values
    A0 = -0.0554 
    B0 = 0.01 # Slope of inflection point
    C0 = 1100 # Temperature near inflection point
    D0 = 0.97 # slope of right flange
    #D0 = 1
    E0 = 0 # vertical shift
    p0 = [A0, B0, C0, D0, E0]
    
    popt, pcov = opt.curve_fit(logistic5, Tbath, gSave, p0=p0, \
                 bounds=((-0.1, 0, np.amin(Tbath), 0.9, -.1), \
                         (0, 0.02, np.amax(Tbath), 1.0, .1)))
    
    
    plt.plot(Tbath[::5], gSave[::5], \
             marker=markers[iQ], markersize=4, \
             linestyle=linestyles[iQ],\
             color=colors[iQ], label=vQ)



#titleText = 'Slow DoFs Auto-Correlation'
#plt.title(titleText)
plt.xlabel(r'$T_{Res.} \hspace{0.5} [K] $')
plt.ylabel(r'$g_S \hspace{1} [eV^2 \cdot \AA^3]$')
axes = plt.gca()
axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.legend(bbox_to_anchor = (1.04, 0.5), loc = 'center left', \
           title=r'$\dot{T}$ [K/s]')
plt.tight_layout()
figName = outFilePath + matSystem + '--runs_ALL--Q_ALL--gS_vs_T--fit'
plt.savefig(figName, dpi=200)
plt.close(fig)  

sys.exit(0)

"""

Cross Correlation

"""
# Cross-Correlation
gXr_Coefs = np.zeros((3,5))
gXi_Coefs = np.zeros((3,4))

fig = plt.figure()
for iQ, vQ in enumerate(quenchRate):
    
    
    outFileName = matSystem + '--runs_' + Runs[iQ] + '--Q_' + vQ + '--'
    gXave = np.load(inFilePath + outFileName + 'gXave.npy')
    gXstd = np.load(inFilePath + outFileName + 'gXstd.npy')   
    
    # Estimate initial values
    A0 = -0.0554 
    B0 = 0.01 # Slope of inflection point
    C0 = 1100 # Temperature near inflection point
    D0 = 0.97 # slope of right flange
    #D0 = 1
    E0 = 0 # vertical shift
    p0 = [A0, B0, C0, D0, E0]
    
    popt, pcov = opt.curve_fit(logistic5, Tbath, gXave, p0=p0, \
                 bounds=((-0.1, 0, np.amin(Tbath), 0.9, -.1), \
                         (0, 0.02, np.amax(Tbath), 1.0, .1)))
    #popt, pcov = opt.curve_fit(linear, Tbath, gXave)
    #popt, pcov = opt.curve_fit(poly, Tbath, gXave)
    
    #p0 = [500, 800, -.1, 0.5]
    #popt, pcov = opt.curve_fit(gl, Tbath, gXave, p0=p0)
    
    gX_baseline = logistic5(Tbath, *popt)
    gXr_Coefs[iQ,:] = popt[:]
    
    #gX_baseline = linear(Tbath, *popt)
    #gX_baseline = poly(Tbath, *popt)
    
    
    #gX_baseline = gl(Tbath, *popt)
    
    plt.subplot(2,1,1)
    plt.title("(A)")
    plt.plot(Tbath[::10], gXave[::10], \
             marker=markers[iQ], markersize=4, \
             linestyle='None',\
             color=colors[iQ], label=vQ)
    
    plt.plot(Tbath, gX_baseline, label='fit', \
             color=colors[iQ], \
             linestyle=linestyles[iQ])
    plt.xlabel(r'$T_{Res.}$ [K]')
    plt.ylabel(r'$g_X$')
    
    
    gXave2 = gXave-gX_baseline
    
    A0 = np.abs(np.amin(gXave2) - np.amax(gXave2))
    B0 = Tbath[np.argmax(gXave2)]
    C0 = 10
    D0 = 0
    
    p02 = [A0, B0, C0, D0]
    
    popt, pcov = opt.curve_fit(gauss, Tbath, gXave2, p0=p02, \
                               bounds=((0, np.amin(Tbath), 0, 0),\
                                       (.2, np.amax(Tbath), 1750,1))) 
    gX_irrev = gauss(Tbath, *popt)
    
    # if C < 10, gauss equation cannot be determined,
    # use linear fit instead...
    if popt[2] < 10:
        popt[0] = 0
        popt[3] = np.mean(gXave2)
        gX_irrev = gauss(Tbath, *popt)
        
    gXi_Coefs[iQ,:] = popt[:]
    
    axes = plt.gca()
    axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.legend(bbox_to_anchor = (1.04, 0.5), loc = 'center left', \
           title=r'$\dot{T}$ [K/s]')
    plt.tight_layout()

    
    plt.subplot(2,1,2)
    plt.title("(B)")
    plt.plot(Tbath[::10], gXave2[::10], \
             marker=markers[iQ], markersize=4, \
             linestyle='None',\
             color=colors[iQ], label=vQ)
    
    plt.plot(Tbath, gX_irrev, label='fit', \
             linestyle=linestyles[iQ], color=colors[iQ])
    plt.xlabel(r'$T_{Res.}$ [K]')
    plt.ylabel(r"$g_X'$")
    axes = plt.gca()
    axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.legend(bbox_to_anchor = (1.04, 0.5), loc = 'center left', \
           title=r'$\dot{T}$ [K/s]')
    plt.tight_layout()

figName = outFilePath + matSystem + '--runs_ALL--Q_ALL--gX_vs_T--fit'
plt.savefig(figName, dpi=200)
plt.close(fig)  

# Plot smooth gX Cuvres
fig = plt.figure()
for iQ, vQ in enumerate(quenchRate):
    
    
    gXsmooth = logistic5(Tbath, *gXr_Coefs[iQ, :]) + gauss(Tbath, *gXi_Coefs[iQ, :])
    plt.plot(Tbath, gXsmooth, color=colors[iQ], label=vQ)
    
    
plt.xlabel(r'$T_{Res.}$ [K]')
plt.ylabel(r'$g_X$')    
plt.legend()
axes = plt.gca()
axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.savefig(outFilePath + matSystem + '-gX_smooth.png', dpi=200)
print(gXi_Coefs)