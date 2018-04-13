# program: modify_datalmp.py
#
# purpose: Modify LAMMPS data file to select atoms
#
# update: 1/29/2018
#

import sys
import os

if len(sys.argv) < 3:
   print "Usage: python selectatoms.py inputFile outputFile [natoms0] [ntypes0]"
   sys.exit(1)

argv=sys.argv

inputFile = argv[1]
outputFile = argv[2]

if len(sys.argv) > 3:
   natoms0 = int(float(argv[3]))
   ntypes0 = int(float(argv[4]))
else:
   natoms0 = 0
   ntypes0 = 0

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
lines = [0,0]

for line in fin.readlines():
   count += 1
   llist = line.split()

   if count == 1:
      fout.write(line)
      fout.write('\n')

   #if count == 3:
   if 'atoms' in llist:
      natoms_original = int(float(llist[0]))
      fout.write('natoms atoms\n')

   #if count == 4:
   if 'types' in llist:
      ntypes = int(float(llist[0]))
      fout.write('ntypes atom types\n')
      fout.write('\n')

   if 'xlo' in llist or 'ylo' in llist or 'zlo' in llist or 'xy' in llist:
      fout.write(line);

   if 'Atoms' in llist:
      fout.write('\n')
      fout.write('Atoms\n')
      fout.write('\n')
      lines = [count+1, count+1+natoms_original]
      
   if lines[0]!=lines[1] and count > lines[0] and count <= lines[-1]: 
      for i in range(len(llist)):
	 if "." in llist[i]:
	    llist[i]=float(llist[i])
	 else:
	    llist[i]=int(float(llist[i]))

      x = llist[2]
      y = llist[3]
      z = llist[4]

      if (x-50)**2+(z-85)**2 <15**2:   	# atom selection criterion

	    natoms += 1
	    llist[0] = natoms

	    write_str = "%-7d %1d" %(llist[0]+natoms0, llist[1]+ntypes0)
	    for i in range(2, 5):
	       write_str += " %10.6f" %(llist[i])
	    fout.write(write_str + '\n')

fin.close()
fout.close()

# change the number of atoms in the modified dump file
#command = "sed -i '%d s/%d/%d/' %s" %(4, count-9, natoms, outputFile)
command = "sed -i 's/%s/%d/' %s" %('natoms', natoms+natoms0, outputFile)
os.system(command)
command = "sed -i 's/%s/%d/' %s" %('ntypes', ntypes+ntypes0, outputFile)
os.system(command)

sys.exit(0)
