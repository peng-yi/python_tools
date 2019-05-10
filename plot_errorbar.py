import pylab

file1 = open("1200K/mfpt","r")
file2 = open("1200K2/mfpt","r")
X1=[]
X2=[]
Y1=[]
Y2=[]
Z1=[]
Z2=[]
for line in file1.readlines():
   x, y, z, r = line.split()
   X1.append(int(float(x)))
   Y1.append(float(y))
   Z1.append(float(r))
file1.close()

for line in file2.readlines():
   x, y, z, r = line.split()
   X2.append(int(float(x)))
   Y2.append(float(y))
   Z2.append(float(r))
file2.close()

file1 = open("1250K/mfpt","r")
file2 = open("1250K2/mfpt","r")
X3=[]
X4=[]
Y3=[]
Y4=[]
Z3=[]
Z4=[]
for line in file1.readlines():
   x, y, z, r = line.split()
   X3.append(int(float(x)))
   Y3.append(float(y))
   Z3.append(float(r))
file1.close()

for line in file2.readlines():
   x, y, z, r = line.split()
   X4.append(int(float(x)))
   Y4.append(float(y))
   Z4.append(float(r))
file2.close()

pylab.figure(1200)
pylab.errorbar(X1, Y1, yerr=Z1, label="1200K, 100,000 atoms")
#pylab.plot(X1, Y1, 'bo', label="1200K, 100,000 atoms")
pylab.errorbar(X2, Y2, yerr=Z2, label="1200K, 50,000 atoms")
#pylab.plot(X2, Y2, 'rs', label="1200K, 50,000 atoms")
pylab.xlim([0, 100])
pylab.ylim([0, 1.50])
pylab.xlabel("n_max")
pylab.ylabel("Time (ns)")
pylab.title("Mean First Passage Time (10 samples)")
pylab.legend(loc="best")

pylab.figure("1250")
pylab.errorbar(X3, Y3, yerr=Z3, label="1250K, 100,000 atoms")
#pylab.plot(X3, Y3, 'bo', label="1250K, 100,000 atoms")
pylab.errorbar(X4, Y4, yerr=Z4, label="1250K, 50,000 atoms")
#pylab.plot(X4, Y4, 'rs', label="1250K, 50,000 atoms")
pylab.xlim([0, 100])
pylab.ylim([0, 10.0])
pylab.xlabel("n_max")
pylab.ylabel("Time (ns)")
pylab.title("Mean First Passage Time (10 samples)")
pylab.legend(loc="best")

pylab.show()
