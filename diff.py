import numpy
import random
import pylab
import sys
import os

folders = []
compositions = []
os.system("ls -d */ > t")         # list folders in file t
file = open('t','r')
for line in file.readlines():
   list = line.split()
   folders.append(list[0])

   tmp = list[0][2:-1]
   compositions.append(int(float(tmp)))
   compositions.sort()

for compos in compositions:
   folder = "ni"+str(compos)+"/"
   file=folder+"msd.txt"
   os.system("cp "+file+" .")
   os.system("awk '{if ($1==3) print (NR-8)/5*0.1\" \"$2\" \"$3\" \"$4}' msd.txt >tt")
   os.system("cp tt "+folder)

   file = open(folder+"tt", "r")

   x = []
   y1 = []
   y2 = []
   y3 = []

   for line in file.readlines():
      list = line.split()
      try: 
	 #print list[0]
	 x.append(float(list[0]))
	 y1.append(float(list[1]))
	 y2.append(float(list[2]))
	 y3.append(float(list[3]))
      except:
	 continue

#   x = pylab.array(x)
#   y1 = pylab.array(y1)
#   y2 = pylab.array(y2)
#   y3 = pylab.array(y3)

   try:
      a, b = pylab.polyfit(x, y1, 1)
      print compos, a, b, 
      a, b = pylab.polyfit(x, y2, 1)
      print a, b, 
      a, b = pylab.polyfit(x, y3, 1)
      print a, b 
   except:
      print 'fell to here'

#   pylab.plot(x, y1)
#   pylab.plot(x, y2)
#   pylab.plot(x, y3)
#   pylab.show()

