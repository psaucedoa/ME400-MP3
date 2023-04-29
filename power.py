#%%
import numpy as np
import pyromat as pm
import matplotlib.pyplot as plt
import pandas as pd
# %%
#Force the unit system into kJ,kg,KPa,K
pm.config['unit_energy'] = 'kJ'
pm.config['unit_matter'] = 'kg'
pm.config['unit_pressure'] = 'kPa'
pm.config['unit_temperature'] = 'K'

rpm     = 6000          #operating revolutions per minute
cc      = 80            #[cc] engine size
vol_l   = 80/1000       #[L] engine volume in liters
vol     = vol_l/1000    #[m^3] engine volume in meters cubed
gamma   = 1.4           #assuming diatomic ideal
r       = 6             #compression ratio
t1      = 298.15        #[K] ambient operating temp
Q       = 120000        #[kj/kg]
p1      = 101.325        #[kPa] operating pressure (ambient)
R       = 8314          #[kJ/mol] universal gas constant

H2      = pm.get('ig.H2') #getting ideal has H2 data from Pyromat
O2      = pm.get('ig.O2') #getting ideal has O2 data from Pyromat

#%%
rho_H2 = H2.d(T=298.15, p=p1) #density of hydrogen at STP
rho_O2 = O2.d(T=298.15, p=p1) #density of oxygen at STP
# %%
mw_H2 = H2.mw(T=298.15, p=p1) #molecular weight of H2 at STP
mw_O2 = O2.mw(T=298.15, p=p1) #molecular weight of H2 at STP
af_ratio = mw_O2 / (2*mw_H2 ) #air fuel ratio
# %%
n = p1*vol/(R*t1) 
#idela gas law to find number of moles

mol_H2 = 2*n/3 
#two thrids of those moles will be H2

P_partial_H2 = p1*2/3
#partial pressure of H2 is 2/3 total pressure

kg_H2 = mw_H2*mol_H2
#weight of H2 will be molar weight x moles

kg_O2 = mw_O2*mol_H2/2
#weight of O2 will be molar weight x moles

# %%
###################
#   COMPRESSION   #
###################

cv_H2_1 = H2.cv(T=t1, p=p1)
    #volume specific heat at temperature t1
cv_O2_1 = O2.cv(T=t1, p=p1)
    #volume specific heat at temperature t1
cv_1 = cv_H2_1*(kg_H2/(kg_O2+kg_H2)) + cv_O2_1*(kg_O2/(kg_H2+kg_O2))
    #weighted average value of cv

cp_H2_1 = H2.cp(T=t1, p=p1)
    #volume specific heat at temperature t1
cp_O2_1 = O2.cp(T=t1, p=p1)
    #volume specific heat at temperature t1
cp_1 = cp_H2_1*(kg_H2/(kg_O2+kg_H2)) + cp_O2_1*(kg_O2/(kg_H2+kg_O2))
    #weighted average value of cv

gamma_H2_1 = cp_H2_1/cv_H2_1
gamma_O2_1 = cp_O2_1/cv_O2_1
gamma_1 = gamma_H2_1*(kg_H2/(kg_O2+kg_H2)) + gamma_O2_1*(kg_O2/(kg_H2+kg_O2))
#finding gamma. Basicaly the same as assumed value

s_H2_1 = H2.s(T=t1, p=p1)
    #H2 entropy at state point 1
s_O2_1 = O2.s(T=t1, p=p1)
    #O2 entropy at state point 1
s_1 = s_H2_1*(kg_H2/(kg_O2+kg_H2)) + s_O2_1*(kg_O2/(kg_H2+kg_O2))
    #weighted average entropy at state point 2

h_H2_1 = H2.h(T=t1, p=p1)
    #H2 enthalpy at state point 1
h_O2_1 = O2.h(T=t1, p=p1)
    #O2 enthlpy at state point 1
h_1 = h_H2_1*(kg_H2/(kg_O2+kg_H2)) + h_O2_1*(kg_O2/(kg_H2+kg_O2))
    #weighted average enthalpy at state point 1

p2 = p1 * r ** 1.3366
    #Finding stage 2 pressure through pressure ratio
t2 = t1 * r**(1.3366-1)
    #Finding stage 2 temp through adiabatic compression

cv_H2_2 = H2.cv(T=t2, p=p2)
    #volume specific heat at temperature t2
cv_O2_2 = O2.cv(T=t2, p=p2)
    #volume specific heat at temperature t2
cv_2 = cv_H2_2*(kg_H2/(kg_O2+kg_H2)) + cv_O2_2*(kg_O2/(kg_H2+kg_O2))
    #weighted average value of cv

cp_H2_2 = H2.cp(T=t2, p=p2)
    #volume specific heat at temperature t1
cp_O2_2 = O2.cp(T=t2, p=p2)
    #volume specific heat at temperature t1
cp_2 = cp_H2_2*(kg_H2/(kg_O2+kg_H2)) + cp_O2_2*(kg_O2/(kg_H2+kg_O2))
    #weighted average value of cv

gamma_H2_2 = cp_H2_1/cv_H2_2
gamma_O2_2 = cp_O2_1/cv_O2_2
gamma_2 = gamma_H2_2*(kg_H2/(kg_O2+kg_H2)) + gamma_O2_2*(kg_O2/(kg_H2+kg_O2))
#finding gamma. Basicaly the same as assumed value

s_H2_2 = H2.s(T=t2, p=p2)
    #H2 entropy at state point 2
s_O2_2 = O2.s(T=t2, p=p2)
    #O2 entropy at state point 2
s_2 = s_H2_2*(kg_H2/(kg_O2+kg_H2)) + s_O2_2*(kg_O2/(kg_H2+kg_O2))
    #weighted average entropy at state point 2

h_H2_2 = H2.h(T=t2, p=p2)
    #H2 enthalpy at state point 2
h_O2_2 = O2.h(T=t2, p=p2)
    #O2 enthlpy at state point 2
h_2 = h_H2_2*(kg_H2/(kg_O2+kg_H2)) + h_O2_2*(kg_O2/(kg_H2+kg_O2))
    #weighted average enthalpy at state point 2



wc = h_2 - h_1
    #specific work required for compression


fuel_air = 2*mw_H2 / mw_O2
t3 = t2 + fuel_air*Q/cv_2
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
