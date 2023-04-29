#%%
import numpy as np
import pyromat as pm
import matplotlib.pyplot as plt
import pandas as pd
#%%
H2O = pm.get('mp.H2O')

# %%
Temps = np.linspace(273.16,500,200)
T = Temps.reshape((Temps.size,1))
Press = np.linspace(1,3,200)
h_H2O = H2O.h(T=T)
s_H2O = H2O.s(T=T, p=Press)
#h_H2O_mp = H2O_mp.h(T=Temps, p=Press)
# %%
fig1 = plt.figure()
plt.plot(Temps, h_H2O)
plt.xlabel('Temperature [K]')
plt.ylabel('Enthalpy')
plt.title('Enthalpy of H2O wrt Temperature')
plt.grid()

fig2 = plt.figure()
plt.contourf(Temps, Press, s_H2O)
plt.colorbar()
plt.xlabel('Temperature [K]')
plt.ylabel('Pressure [Bar]')
plt.title('Entropy of H2O wrt Temperature and Pressure')
# %%
steam = pm.get('mp.H2O')
Tt,pt = steam.triple()
Tc,pc = steam.critical()
T = np.arange(Tt,Tc,2.5)
p = steam.ps(T)
dL,dV = steam.ds(T=T)
sL,sV = steam.ss(T=T)

fig3 = plt.figure()
plt.plot(sL,T,'k')
plt.plot(sV,T,'k')
plt.ylabel('Temperature [K]')
plt.xlabel('Entropy [kJ/kg/K]')

fig4 = plt.figure()
plt.plot(1./dL,p,'k')
plt.plot(1./dV,p,'k')
plt.yscale('log')
plt.xscale('log')
plt.ylabel('Pressure [bar]')
plt.xlabel(r'Volume [$m^3/kg$]')

h_vals = np.arange(0,3500)
hL, hV = steam.hs(T=T)

fig5 = plt.figure()
plt.plot(hL, p)
plt.plot(hV, p)
plt.yscale('log')
plt.ylabel('Pressure [bar]')
plt.xlabel('Enthalpy [kJ/kg]')
# %%r