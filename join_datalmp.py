#!/cm/shared/apps/Intel/python/2.7.10/bin/python
# program: join_datalmp.py
#
# purpose: attach LAMMPS data files in x or y or z direction
#
# update: 1/29/2018, 11/16/2018
#

import sys
import os
import numpy as np

# --------------------------------------
# Helper code

# end of helper code
# --------------------------------------

if len(sys.argv) < 5:
   print "Usage: python join_datalmp.py inputFile1 inputFile2 outputFile direction [natoms0] [ntypes0]"
   sys.exit(1)

argv=sys.argv

inputFile1 = argv[1]
inputFile2 = argv[2]
outputFile = argv[3]
direction = argv[4]  	# direction = x or y or z

if len(sys.argv) > 5:
   natoms0 = int(float(argv[5]))
   ntypes0 = int(float(argv[6]))
else:
   natoms0 = 0
   ntypes0 = 0

if not os.path.isfile(inputFile1) or not os.path.isfile(inputFile2):
   print "Input file does NOT exist"
   sys.exit(1)

if os.path.isfile(outputFile):
   overwrite = raw_input("Output file exists, overwrite? (y/n) :")
   if overwrite == 'y':
      pass
   else:
      sys.exit(1)

fin1 = open(inputFile1, "r")
fin2 = open(inputFile2, "r")
fout = open(outputFile, "w")

natoms = 0   	# number of atoms chosen
xlo = []
xhi = []
ylo = []
yhi = []
zlo = []
zhi = []

for fin in [fin1, fin2]:

   count = 0         	# line count in input datalmp file
   lines = [0,0]

   for line in fin.readlines():
      count += 1
      llist = line.split()

      if count == 1:    				# Line #2
	 if fin == fin1:
	    fout.write(line)
	    fout.write('\n')

      if 'atoms' in llist:   				# Line #3
	 natoms_original = int(float(llist[0]))

	 if fin == fin1:
	    fout.write('natoms atoms\n')

      if 'types' in llist:    				# Line #4
	 ntypes = int(float(llist[0]))

	 if fin == fin1:
	    fout.write('ntypes atom types\n')
	    fout.write('\n')

	 if fin == fin2:
	    ntypes0 = ntypes

      if 'xlo' in llist:
	 xlo.append(float(llist[0]))
	 xhi.append(float(llist[1]))
	 if fin == fin1:
	    fout.write('#xlo #xhi xlo xhi\n')

      if 'ylo' in llist:
	 ylo.append(float(llist[0]))
	 yhi.append(float(llist[1]))
	 if fin == fin1:
	    fout.write('#ylo #yhi ylo yhi\n')

      if 'zlo' in llist:
	 zlo.append(float(llist[0]))
	 zhi.append(float(llist[1]))
	 if fin == fin1:
	    fout.write('#zlo #zhi zlo zhi\n')
	 
      if 'xy' in llist:
	 if fin == fin1:
	    fout.write(line);

      if 'Atoms' in llist:
	 lines = [count+1, count+1+natoms_original]

	 if fin == fin1:
	    fout.write('\n')
	    fout.write('Atoms\n')
	    fout.write('\n')
	 
      if lines[0]!=lines[1] and count > lines[0] and count <= lines[-1]: 

	 for i in range(len(llist)):
	    if "." in llist[i]:  		# with digit point
	       llist[i]=float(llist[i])
	    else:
	       llist[i]=int(float(llist[i]))

	 x = llist[2]
	 y = llist[3]
	 z = llist[4]

	 # atom output

	 if 1:
	       natoms += 1
	       llist[0] = natoms

	       write_str = "%-7d %1d" %(llist[0], llist[1]+ntypes0) 	# id and type

               if fin == fin2:
		  if direction == 'x':
		     x += xhi[0]
		  elif direction == 'y':
		     y += yhi[0]
		  elif direction == 'z':
		     z += zhi[0]

	       write_str += " %10.6f %10.6f %10.6f\n" %(x, y, z)
	       fout.write(write_str)
		         

	       '''
	       if direction == 'x':
		  if fin==fin1:
		     write_str += " %10.6f" %(llist[2])    		# x coordinate
		  elif fin==fin2:
		     write_str += " %10.6f" %(llist[2]+xhi[0])   

		  write_str += " %10.6f" %(llist[3])      		# y coordinate
		  write_str += " %10.6f" %(llist[4])    		# z coordinate

	       elif direction == 'y':
		  write_str += " %10.6f" %(llist[2])      		# x

		  if fin==fin1:
		     write_str += " %10.6f" %(llist[3])    		# y 
		  elif fin==fin2:
		     write_str += " %10.6f" %(llist[3]+yhi[0])    	 

		  write_str += " %10.6f" %(llist[4])    		# z

	       elif direction == 'z':
		  write_str += " %10.6f" %(llist[2])      		# x
		  write_str += " %10.6f" %(llist[3])      		# y
		  if fin==fin1:
		     write_str += " %10.6f" %(llist[4])    		# z 
		  elif fin==fin2:
		     write_str += " %10.6f" %(llist[4]+zhi[0]) 	# z 

	       fout.write(write_str + '\n')
	       '''

   fin.close()
fout.close()

# change the number of atoms in the modified dump file
#command = "sed -i '%d s/%d/%d/' %s" %(4, count-9, natoms, outputFile)

command = "sed -i 's/%s/%8.6f/' %s" %('#xlo', xlo[0], outputFile)
os.system(command)
command = "sed -i 's/%s/%8.6f/' %s" %('#ylo', ylo[0], outputFile)
os.system(command)
command = "sed -i 's/%s/%8.6f/' %s" %('#zlo', zlo[0], outputFile)
os.system(command)

if direction == 'x':
   command = "sed -i 's/%s/%8.6f/' %s" %('#xhi', sum(xhi), outputFile)
   os.system(command)
else:
   command = "sed -i 's/%s/%8.6f/' %s" %('#xhi', max(xhi), outputFile)
   os.system(command)

if direction == 'y':
   command = "sed -i 's/%s/%8.6f/' %s" %('#yhi', sum(yhi), outputFile)
   os.system(command)
else:
   command = "sed -i 's/%s/%8.6f/' %s" %('#yhi', max(yhi), outputFile)
   os.system(command)

if direction == 'z':
   command = "sed -i 's/%s/%8.6f/' %s" %('#zhi', sum(zhi), outputFile)
   os.system(command)
else:
   command = "sed -i 's/%s/%8.6f/' %s" %('#zhi', max(zhi), outputFile)
   os.system(command)

command = "sed -i 's/%s/%d/' %s" %('ntypes', ntypes+ntypes0, outputFile)
os.system(command)

command = "sed -i 's/%s/%d/' %s" %('natoms', natoms, outputFile)
os.system(command)

sys.exit(0)
