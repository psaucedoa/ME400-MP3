#%%
import numpy as np
import pyromat as pm
import matplotlib.pyplot as plt
import pandas as pd
# %%
#Force the unit system into kJ,kg,KPa,K
pm.config['unit_energy'] = 'kJ'
pm.config['unit_matter'] = 'kg'
pm.config['unit_pressure'] = 'Pa'
pm.config['unit_temperature'] = 'K'

rpm     = 6000          #operating revolutions per minute
cc      = 80            #[cc] engine size
vol_l   = 80/1000       #[L] engine volume in liters
vol     = vol_l/1000    #[m^3] engine volume in meters cubed
r       = 6             #compression ratio
t1      = 298.15        #[K] ambient operating temp
Q       = 44430         #[kJ/kg]
p1      = 101325        #[kPa] operating pressure (ambient)
R       = 8.314         #[J/mol] universal gas constant

#%%
air     = pm.get('ig.air') 
    #getting ideal gas air data from Pyromat

rho_air = air.d(T=t1, p=p1) 
    #density of oxygen at STP
# %%
mw_air = air.mw(T=t1, p=p1) #molecular weight of H2 at STP

n = p1*vol/(R*t1) 
    #idela gas law to find number of moles

kg_air = mw_air*n/1000
    #weight of O2 will be molar weight x moles

mw_iso = 12*8 + 18*1
    #molecular weight of iso-octane

n_O2 = 0.21*n
    #moles of oxygen present in air
    
n_iso = n_O2/12.5
    #moles of iso-octane required for stoichiometric combustion

kg_iso = n_iso*mw_iso/1000
    #kg of iso-octane reuired for stoichiometric combustion
# %%
###################
#   COMPRESSION   #
###################

cv_air_1 = air.cv(T=t1, p=p1)
    #volume specific heat at temperature t1
cp_air_1 = air.cp(T=t1, p=p1)
    #volume specific heat at temperature t1
gamma_air_1 = cp_air_1/cv_air_1
    #finding gamma. Basicaly the same as assumed value

s_air_1 = air.s(T=t1, p=p1)
    #air entropy at state point 1
h_air_1 = air.h(T=t1, p=p1)
    #air enthlpy at state point 1

gamma_avg = 1.364

p2 = p1 * r ** gamma_avg
    #Finding stage 2 pressure through pressure ratio
t2 = t1 * r**(gamma_avg-1)
    #Finding stage 2 temp through adiabatic compression

cv_air_2 = air.cv(T=t2, p=p2)
    #volume specific heat at temperature t2
cp_air_2 = air.cp(T=t2, p=p2)
    #volume specific heat at temperature t1
gamma_air_2 = cp_air_1/cv_air_2
    #finding gamma. Basicaly the same as assumed value

s_air_2 = air.s(T=t2, p=p2)
    #air entropy at state point 2
h_air_2 = air.h(T=t2, p=p2)
    #H2 enthalpy at state point 2

wc = h_air_2 - h_air_1
    #specific work required for compression


fuel_air = kg_iso / kg_air
t3 = t2 + Q*kg_iso/(0.835*kg_air)
p3 = p2*(t3/t2)

cv_air_3 = air.cv(T=t3, p=p3)
cp_air_3 = air.cv(T=t3, p=p3)
h_3 = air.cv(T=t3, p=p3)
s_3 = air.cv(T=t3, p=p3)
#%%
p4 = p3*r**(-gamma_avg)
t4 = t3*r**(1-gamma_avg)

cv_air_4 = air.cv(T=t4, p=p4)
cp_air_4 = air.cv(T=t4, p=p4)
h_4 = air.cv(T=t4, p=p4)
s_4 = air.cv(T=t4, p=p4)

cv_avg = (cv_air_1+cv_air_2+cv_air_3+cv_air_4)/4
# %%
W = cv_avg*( (t3-t2)-(t4-t1) )

P_spec = W*rpm/60
P = P_spec*(kg_air)
print(P)
#%%


#PLOTTING
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
