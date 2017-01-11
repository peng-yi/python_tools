import os

old = '1050'
new = '1150'

for i in range(1, 11):
   folder = "run"+str(i)+"/"
   name = folder + "job.scr"

   os.system("sed 's/" + old + "/" + new + "/' " + name +" > t")
   os.system("mv t " + name)

