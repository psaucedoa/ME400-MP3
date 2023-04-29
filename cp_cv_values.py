#%%
import numpy as np
import pyromat as pm
import matplotlib.pyplot as plt
import pandas as pd
#%%
cpTemps = np.linspace(298,1000,500)
air     = pm.get('ig.air')
H2      = pm.get('ig.H2')
cp_air  = air.cp(T=cpTemps)
cv_air  = air.cv(T=cpTemps)
cp_H2   = H2.cp(T=cpTemps)
cv_H2   = H2.cv(T=cpTemps)
#%%
fig1 = plt.figure()
plt.plot(cpTemps, cp_air, 'b')
plt.title(r'$C_p$ of Air at Standard Atmosphere')
plt.xlabel('Temperature [K]')
plt.ylabel(r'$C_p$')
plt.grid()

fig2 = plt.figure()
plt.plot(cpTemps, cv_air, 'b--')
plt.title(r'$C_v$ of Air at Standard Atmosphere')
plt.xlabel('Temperature [K]')
plt.ylabel(r'$C_v$')
plt.grid()

fig3 = plt.figure()
plt.plot(cpTemps, cp_H2, 'r')
plt.title(r'$C_p$ of H2 at Standard Atmosphere')
plt.xlabel('Temperature [K]')
plt.ylabel(r'$C_p$')
plt.grid()

fig2 = plt.figure()
plt.plot(cpTemps, cv_H2, 'r--')
plt.title(r'$C_v$ of H2 at Standard Atmosphere')
plt.xlabel('Temperature [K]')
plt.ylabel(r'$C_v$')
plt.grid()
# %%
air_zipped  = list(zip(cpTemps, cp_air, cv_air))
h2_zipped   = list(zip(cpTemps, cp_H2, cv_H2))
# %%
dict_air = {'Temperature [K]':cpTemps, 'cp air': cp_air, 'cv air': cv_air}
air_df = pd.DataFrame(dict_air)
air_df.to_csv('air.csv')

# %%
dict_H2 = {'Temperature [K]':cpTemps, 'cp H2': cp_H2, 'cv H2': cv_H2}
H2_df = pd.DataFrame(dict_H2)
H2_df.to_csv('H2.csv')
# %%
