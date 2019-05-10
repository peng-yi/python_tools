#!/cm/shared/apps/Intel/python/2.7.10/bin/python
#
# Plot data from files, using given labels as legend
#
# Peng Yi, 8/20/18, 1/30/2019
#
import matplotlib.pyplot as plt
import sys
import numpy as np

if len(sys.argv) < 3:
    print "Usage: python plotfile.py file1 label1 file2 label2... colx coly"
    sys.exit(1)

argv = sys.argv
argc = len(argv)

colx = int(float(argv[argc-2]))-1
coly = int(float(argv[argc-1]))-1

fig = plt.figure()

for i in range(1, len(argv)-2, 2):
   x1 = []
   y1 = []
   print i
   filename = argv[i]
   label = argv[i+1]

   print filename
   fi = open(filename,"r")

   for line in fi.readlines():
       data = line.split()
       if data[0]!='#':
	  x1.append(data[colx])
	  y1.append(data[coly])

   fi.close()
   ax = fig.add_subplot(111)
   ax.plot(x1, y1, label=label)
   #plt.plot(x1, y1,'-', markevery=20, label='lid')

plt.xlabel("Temperature (K)")
plt.ylabel("Gibbs free energy (eV)")
plt.legend(loc="upper right")
plt.title('Free energy')
#plt.xlim(1000,1900)
plt.savefig('foo.png')
plt.show()
