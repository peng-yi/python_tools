# program: selectatoms.py
#
# purpose: Modify dump file to select atoms for VMD visualization
#          Type of atoms will be modified for coloring in VMD
#
# update: 5/14/2016
#

import sys
import os

if len(sys.argv) < 3:
   print "Usage: python selectatoms.py inputFile outputFile"
   sys.exit(1)

argv=sys.argv

inputFile = argv[1]
outputFile = argv[2]

if not os.path.isfile(inputFile):
   print "Input file does NOT exist"
   sys.exit(1)

if os.path.isfile(outputFile):
   overwrite = raw_input("Output file exists, overwrite? (y/n) :")
   if overwrite == 'y':
      pass
   else:
      sys.exit(1)

fin = open(inputFile, "r")
fout = open(outputFile, "w")

count = 0         	# line count in input dump file
natoms = 0   		# number of atoms chosen

for line in fin.readlines():
   count += 1
   if count <= 9:    	# first 9 lines are file head
      fout.write(line)
   else:
      list = line.split()
      for i in range(len(list)):
	 if "." in list[i]:
	    list[i]=float(list[i])
	 else:
	    list[i]=int(float(list[i]))

      if list[-1] == 1 or list[-1] == 5:     #	choice criterion
	 if list[4] > 20.0 and list[4] < 180:

	    natoms += 1
	    list[0] = natoms
	    list[1] = list[-1]

	    outline = "%-7d %1d" %(list[0], list[1])
	    for i in range(2, len(list)-1):
	       outline += " %10.6f" %(list[i])
	    outline += " %1d\n" %(list[-1])
	    fout.write(outline)

fin.close()
fout.close()

# change the number of atoms in the modified dump file
command = "sed -i '%d s/%d/%d/' %s" %(4, count-9, natoms, outputFile)
os.system(command)

sys.exit(0)
