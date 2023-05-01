#%%
import numpy as np
import pyromat as pm
import matplotlib.pyplot as plt
import pandas as pd
# %%
pm.config['unit_energy'] = 'kJ'
pm.config['unit_matter'] = 'kg'
pm.config['unit_pressure'] = 'Pa'
pm.config['unit_temperature'] = 'K'

#%%
air = pm.get('ig.air')
t1 = 298.15
p1 = 101325
r = 6
s_air_1 = air.s(T=t1, p=p1)

#%%
def find_gamma(gamma):
    t2 = t1*r**(gamma-1)
    p2 = air.p(T=t2, s=s_air_1)
    gamma_return = np.log(p2/p1)/np.log(6)
    return gamma_return
# %%

y = np.linspace(1.391, 1.3915, 1000)

plt.plot(y, find_gamma(y))
plt.grid()
# %%

gamma_list = find_gamma(y)
for i in range(1000):
    if (abs(gamma_list[i]-y[i]) <=  0.000001):
        found = y[i]
        print(found, gamma_list[i], y[i])
# %%
t = np.linspace(300, 2000, 100)

plt.plot(t, air.s(T=t, p=p1))
# %%
