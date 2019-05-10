import matplotlib.pyplot as plt
import numpy as np

t=np.arange(0.1, 8.0, 0.1)

beta=1./t

A=-8.2269
B=-2.398

P = beta**(-1.25) * np.exp(-0.4759*beta**0.5) * (16.89+A*beta+B*beta**2)

l = beta**(-0.25) * (0.90735-0.27120*beta + 0.91784*beta**2 - 1.1627*beta**3 + 0.68012 *beta**4 - 0.15284*beta**5)

s = beta**(-0.25) * (0.908629 - 0.04151*beta + 0.514632*beta**2 - 0.70859*beta**3 + 0.428351*beta**4 - 0.095229*beta**5)

#plt.plot(t, P)
plt.plot(t, l)
plt.plot(t, s)
plt.ylim(0,1.0)
plt.show()
