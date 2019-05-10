import matplotlib.pyplot as plt
import numpy as np

# Data to plot.
L = 5.
step = L/10
x, y = np.meshgrid(np.arange(-L, L, step), np.arange(-L, L, step))

print x
print y

z = -y*(3*x**2 + y**2)/(x**2 + y**2)**2

cmap= plt.cm.get_cmap("rainbow")

#cs = plt.contour(x,y,z, colors='k')
cs = plt.contourf(x, y, z, cmap=cmap)

#CS = plt.contourf(x, y, z, 15, vmax=abs(z).max(), vmin=-abs(z).max())

plt.colorbar()
plt.title('stress field of an edge dislocation')
plt.xlabel('X')
plt.ylabel('Pxx')

plt.grid(c='k', ls='-', alpha=0.1)
plt.show()
