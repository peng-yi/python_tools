#!/software/apps/anaconda/5.2/python/2.7/bin/python
# Program: reducedump.py
#
# Combine every two dump files
#
# Syntax: python combinedump.py i j
#
# Author: Peng Yi @ JHU
#
# Created: 1/10/2019
#

import matplotlib.pyplot as plt
import math
import os
import sys

DEBUG = False
# --------------------------------------
# Helper code

# end of helper code
# --------------------------------------

if len(sys.argv) < 3:
    print "Usage: python combinedump.py i j"
    sys.exit(1)
    
argv = sys.argv

first = int(float(argv[1]))
last  = int(float(argv[2]))

#---- find the length of each snapshot
firstfile = "dump." + str(first).zfill(4)
fin = open(firstfile, "r")
numnext = 0

for line in fin.readlines():
    data = line.split()

    if "NUMBER" in data:
       numnext = 1
       continue
    if numnext:
       natoms = int(float(data[0]))
       break

fin.close()
length = natoms+9

#---- combine every two dump files
for i in range(first, last+1, 2):
   s = str(i).zfill(4)
   t = str(i+1).zfill(4)
   #print(s,"{0:04d}".format(i))

   command = "tail -n +"+str(length+1)+" "+"dump."+t+" >> "+"dump."+s
   if not DEBUG:
      os.system(command)
   else:
      print command

   #---- don't need sleep, os.system() will wait
   #command = "sleep 1.0"
   #print command
   #if not DEBUG:
   #   os.system(command)

   command = "rm dump."+t
   if not DEBUG:
      os.system(command)
   else:
      print command

#---- rename files
for i in range(first+2, last+1, 2):
   s = str(i).zfill(4)
   t = str(i/2).zfill(4)

   command = "mv dump."+s+" dump."+t
   if not DEBUG:
      os.system(command)
   else:
      print command
