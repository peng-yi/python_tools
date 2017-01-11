import os
import pylab

const = 0.75

for i in range(7, 11):
   folder = "run"+str(i)+"/"

   name = folder+"nuclei"

   file = open(name, "r")

   x=[]
   y1=[]
   y2=[]
   y0=[]
   for line in file.readlines():
      list = line.split()
      if list[1].isdigit():
	 x.append(float(list[1])*4e-6)
	 y1.append(float(list[6]))
	 y2.append(float(list[21]))
	 y0.append(const)

   pylab.figure(i)
   pylab.plot(x, y1, 'b-', label="bcc phase")
   pylab.plot(x, y2, 'r-', label="fcc phase")
   pylab.plot(x, y0, 'g-', label="0.75")
   #pylab.xlim([0, 100])
   pylab.ylim([0.6, 0.9])
   pylab.xlabel("Time (ns)")
   pylab.ylabel("Ni composition of the largest nucleus")
   pylab.title("75Ni:25Al nucleation at T=1100K (sample #"+str(i)+")")
   pylab.legend(loc="best")

   file.close()

pylab.show()
