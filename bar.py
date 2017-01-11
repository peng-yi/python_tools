import pylab

files=["run8/profile", "run9/profile", "run10/profile"]
clr=['r','g','b']
lbl=["45%-55%","35%-65%","25%-75%"]
ticks=range(0, 11)
for i in range(len(ticks)):
   ticks[i] /= 10.0

for i in range(3):
   X1=[]
   Y1=[]
   Z1=[]
   file = open(files[i], "r")
   for line in file.readlines():
      list = line.split()
      print list[0]
      if list[0].isdigit():
	 X1.append(float(list[1]))
	 Y1.append(float(list[5]))

   file.close()

   pylab.figure(i)
   pylab.bar(X1, Y1, align='center', width=10, label=lbl[i], color=clr[i], alpha=0.5)
   pylab.ylim([0, 1])
   pylab.yticks(ticks)
   pylab.xlabel("x dimension (Angstrom)")
   pylab.ylabel("Ni composition")
   pylab.legend(loc='best')

pylab.show()

#pylab.figure(1200)
#pylab.errorbar(X1, Y1, yerr=Z1, label="1200K, 100,000 atoms")
#pylab.plot(X1, Y1, 'bo', label="1200K, 100,000 atoms")
#pylab.errorbar(X2, Y2, yerr=Z2, label="1200K, 100,000 atoms")
#pylab.plot(X2, Y2, 'rs', label="1200K, 50,000 atoms")
#pylab.xlim([0, 100])
#pylab.ylim([0, 1.50])
#pylab.xlabel("n_max")
#pylab.ylabel("Time (ns)")
#pylab.title("Mean First Passage Time (10 samples)")
#pylab.legend(loc="best")

#pylab.show()
