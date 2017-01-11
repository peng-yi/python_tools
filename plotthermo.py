import os
import pylab

const = 0.50

for i in range(1, 3):

   if i==1:
      name = 'cooling'
   if i==2:
      name = 'heating'

   file = open(name, "r")

   if i==1:
      x1=[]
      y1=[]
   if i==2:
      x2=[]
      y2=[]

   for line in file.readlines():
      list = line.split()
      if list[0].isdigit():
	 if i==1:
	    x1.append(float(list[1]))
            y1.append(float(list[3]))
	 if i==2:
	    x2.append(float(list[1]))
	    y2.append(float(list[3]))

   file.close()

#print x1[0],y1[0],x2[0],y2[0]
pylab.plot(x1, y1, 'b-', label="cooling")
pylab.plot(x2, y2, 'r-', label="heating")
#pylab.plot(x, y0, 'g-', label="0.75")
#pylab.xlim([0, 100])
#pylab.ylim([0.6, 0.9])
pylab.xlabel("Temp (K)")
pylab.ylabel("Potential Energy (eV)")
pylab.title("50Ni:50Al nucleation")
pylab.legend(loc="best")

pylab.show()
