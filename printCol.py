#!/cm/shared/apps/Intel/python/2.7.10/bin/python
# program: printCol.py
#
# purpose: print selected columns
#
# update: 4/15/2018
#

import os
import sys

# --------------------------------------
# Helper code

# end of helper code
# --------------------------------------

if len(sys.argv) < 2:
    print "Usage: python printCol.py filename col#1 col#2 col#3 ..."
    sys.exit(1)
argv = sys.argv

filename = argv[1]

# prepare for awk command
for i in range(2, len(argv)):
   if i == 2:
      line = "$" + argv[i]
   else:
      line += "\" \"$" + argv[i]

command = "awk '{print " + line +"}' " + filename
os.system(command)
#print command
#command = "sed -i '%d s/%d/%d/' %s" %(4, count-9, natoms, outputFile)
