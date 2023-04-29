#%%
import numpy as np
import pyromat as pm
import matplotlib.pyplot as plt
import pandas as pd
# %%
rpm     = 6000          #operating revolutions per minute
cc      = 80            #[cc] engine size
vol_l   = 80/1000       #[L] engine volume in liters
vol     = vol_l/1000    #[m^3] engine volume in meters cubed
gamma   = 1.4           #assuming diatomic ideal
r       = 6             #compression ratio
t1      = 298.15        #[K] ambient operating temp
Q       = 120000        #[kj/kg]
p1      = 101325        #[pa] operating pressure (ambient)
bar1    = p1/100000     #[bar] operating pressure (ambient) bars
R       = 8314          #[kJ/mol] universal gas constant

H2      = pm.get('ig.H2') #getting ideal has H2 data from Pyromat
O2      = pm.get('ig.O2') #getting ideal has O2 data from Pyromat

#%%
rho_H2 = H2.d(T=298.15, p=bar1)
rho_O2 = O2.d(T=298.15, p=bar1)
# %%
mw_H2 = H2.mw(T=298.15, p=bar1)
mw_O2 = O2.mw(T=298.15, p=bar1)
af_ratio = mw_O2 / (2*mw_H2 )
# %%
n = p1*vol/(R*t1)

mol_H2 = 2*n/3
P_partial_H2 = p1*2/3
n_H2 = P_partial_H2*vol/(R*t1)
#vol_H2 = #(1/af_ratio) * vol
kg_H2 = mw_H2*n_H2

#vol_O2 = (af_ratio)/(af_ratio+1) * vol
kg_O2 = mw_O2*n_H2/2

# %%
gamma = 1.3
p2 = p1 * r**(gamma)
t2 = t1 * r**(gamma-1)
# %%
cv_H2 = H2.cv(T=900, p=bar1)
cv_O2 = O2.cv(T=900, p=bar1)
cv = cv_H2*(kg_H2/(kg_O2+kg_H2)) + cv_O2*(kg_O2/(kg_H2+kg_O2))


fuel_air = 2*mw_H2 / mw_O2
t3 = t2 + fuel_air*Q/cv_H2

p3 = p2*(t3/t2)
# %%
p4 = p3*r**(-gamma)
t4 = t3*r**(1-gamma)

# %%
W_H2 = cv_H2*( (t3-t2)-(t4-t1) )
# %%
P_spec_H2 = W_H2*rpm/60
P_H2 = P_spec_H2*(kg_H2)
# %%
W_O2 = cv_O2*( (t3-t2)-(t4-t1) )
P_spec_O2 = W_O2*rpm/60
P_O2 = P_spec_O2*(kg_O2)
# %%
W = cv*( (t3-t2)-(t4-t1) )
P_spec = W*rpm/60
P = P_spec*(kg_H2+kg_O2)
# %%


#PLOTTING

Wnet = W*(kg_H2+kg_O2)
p1 = p1
T1 = t1
pr = r
s1 = H2.s(T1, p1) + O2.s(T1,p1)


fig1 = plt.figure()
plt.plot(t1, p1/1000, marker="o")
plt.plot(t2, p2/1000, marker="o")
plt.plot(t3, p3/1000, marker="o")
plt.plot(t4, p4/1000, marker="o")
plt.annotate('T1=298.15 [K]\nP1=101.3',xy=(t1,p1/1000),horizontalalignment='left', verticalalignment='bottom', fontsize=10)  
plt.annotate('1',xy=(t1,p1/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         

plt.annotate('2',xy=(t2,p2/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
plt.annotate('T2=510.36 [K]\nP2=1040.67 [kPa]',xy=(t2,p2/1000),horizontalalignment='left', verticalalignment='bottom', fontsize=10)  

plt.annotate('3',xy=(t3,p3/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
plt.annotate('T1=1917.79 [K]\nP1=3910.52 [kPa]',xy=(t3,p3/1000),horizontalalignment='right', verticalalignment='top', fontsize=10)  

plt.annotate('4',xy=(t4,p4/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
plt.annotate('T1=1120.36 [K]\nP1=380.75',xy=(t4,p4/1000),horizontalalignment='left', verticalalignment='bottom', fontsize=10)  

plt.xlabel('Temperature [K]')
plt.ylabel('Pressure [kPa]')
plt.title('80cc Hydrogen-Oxygen Otto Cycle Simulation P-T Diagram')
plt.grid()
# %%
