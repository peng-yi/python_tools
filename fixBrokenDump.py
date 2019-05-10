#!/software/apps/anaconda/5.2/python/2.7/bin/python
# Program: fixBrokenDump.py
#
# Fix LAMMPS dump file, remove broken snapshots (1) missing atom output (2) mixed first line
#
# Syntax: python fixBrokenDump.py inputfilename outputfilename
#
# Author: Peng Yi @ JHU
#
# Created: 12/3/2018
#

import matplotlib.pyplot as plt
import math
import os
import sys
import subprocess

# --------------------------------------
# Helper code

# end of helper code
# --------------------------------------

if len(sys.argv) < 3:
    print "Usage: python fixBrokenDump.py infile outfile"
    sys.exit(1)
    
argv = sys.argv

infile = argv[1]
outfile = argv[2]

#---- clean the line containing ITEM: TIMESTEP 
#
command = "awk '{if ($0~\"TIME\") print \"ITEM: TIMESTEP\"; else print}' "+infile+" > "+outfile
os.system(command)
command = "mv " + outfile + " " + infile
os.system(command)
exit(1)

#---- Read the number of atoms, natoms
#
fin = open(infile,"r")
numnext = 0  		# flag, whether to read natoms
for line in fin.readlines():
    data = line.split()

    if "NUMBER" in data:
       numnext = 1
       continue
    if numnext:
       natoms = int(float(data[0]))
       break
fin.close()

#---- Find the starting line numbers for each snapshot
#
command1 = "cat -n " + infile
command2 = "grep TIME"
cmd1 = command1.split()
cmd2 = command2.split()
proc1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
proc2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stdin=proc1.stdout)

nline = []
for line in proc2.stdout.readlines():
   data = line.split()
   nline.append(int(float(data[0])))

#---- Find out total number of lines in the input file
#
command3 = "wc -l " + infile
cmd3 = command3.split()
proc3 = subprocess.Popen(cmd3, stdout=subprocess.PIPE)
for line in proc3.stdout.readlines():
   linetot = int(float(line.split()[0]))    	# total number of lines
   break

#print "Total number of atoms: ", natoms
#print "Starting line number for snaphots: ", nline
#print "Total number of lines in this dump file: ", linetot

#---- Line number matches, no need to fix
#
if linetot == len(nline) * (natoms+9):
   print "\nNo fix: dump file good.\n"
   exit(0)

# method 1
'''
nline.append(linetot+1)
fout = open(outfile,"w")
for i in range(len(nline)-1):
   if nline[i+1] - nline[i] == natoms+9:

      command = "awk \"{if (NR>="+str(nline[i])+" && NR<"+str(nline[i+1])+") print}\" " + infile + " >> " + outfile
      os.system(command)

exit(1)
'''

# method 2, about twice as faster than method 1
count = 0
record = 0

fin = open(infile,"r")
fout = open(outfile,"w")
for line in fin.readlines():
   
   if record == len(nline)-1:  				# last record
      if linetot - (nline[record]-1) == natoms +9: 	# last record is good
	 start = nline[record]-1
      else:
	 break
   elif nline[record+1] - nline[record] == natoms+9:
      start = nline[record]-1
   else:
      start = nline[record+1]-1

   #print count, start, record
   if count == start:
      fout.write("ITEM: TIMESTEP") 	# sometime this line is broken
   if count >= start:
      fout.write(line)

   count += 1

   if record < len(nline)-1 and count == nline[record+1]-1:
      record += 1


#out = subprocess.check_output(cmd2, stdin=proc1.stdout)
#for item in out:
#   data = item.split()   # every item is a letter, or space, or other single character, not a word
#   print data

fin.close()
fout.close()

command = "mv " + outfile + " " + infile
os.system(command)
print "\n" + infile + " fixed.\n"

