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

rpm     = 6000          #operating revolutions per minute
cc      = 80            #[cc] engine size
vol_l   = 80/1000       #[L] engine volume in liters
vol     = vol_l/1000    #[m^3] engine volume in meters cubed
r       = 6             #compression ratio
t1      = 298.15        #[K] ambient operating temp
Q       = 120000        #[kJ/kg]
p1      = 101325        #[kPa] operating pressure (ambient)
R       = 8.314         #[J/mol] universal gas constant

#%%

air     = pm.get('ig.air') 
    #getting ideal gas air data from Pyromat
rho_air = air.d(T=t1, p=p1) 
    #density of air at STP
    
H2      = pm.get('ig.H2')
rho_air = H2.d(T=t1, p=p1) 
    #density of hydrogen at STP
# %%

#quick calculation to get molar fractions
excess = 1.20
    #percent excess
air_part = 1
hydrogen = 0.21*2 * excess
    #hydrogen will be two times the moles of oxygen present
total = air_part + hydrogen
air_fraction = air_part/total
H2_fraction = hydrogen/total
#%%

mw_air = air.mw(T=t1, p=p1) #molecular weight of air at STP
mw_H2 = H2.mw(T=t1, p=p1) #molecular weight of H2 at STP

n = p1*vol/(R*t1) 
    #idela gas law to find number of moles

mol_air = air_fraction*n
mol_H2 = H2_fraction*n

P_partial_H2 = p1*H2_fraction
    #partial pressure of H2 is 2/3 total pressure
kg_H2 = mw_H2*mol_H2/1000
    #weight of H2 will be molar weight x moles
kg_air = mw_air*mol_air/(1000)
    #weight of air will be molar weight x moles
# %%

###################
#     INTAKE      #
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

cv_H2_1 = H2.cv(T=t1, p=p1)
    #volume specific heat at temperature t1
cp_H2_1 = H2.cp(T=t1, p=p1)
    #volume specific heat at temperature t1
gamma_H2_1 = cp_H2_1/cv_H2_1
    #finding gamma. Basicaly the same as assumed value
s_H2_1 = H2.s(T=t1, p=p1)
    #air entropy at state point 1
h_H2_1 = H2.h(T=t1, p=p1)
    #air enthlpy at state point 1
s_1 = (s_H2_1+s_air_1)/2

gamma_1 = (gamma_air_1+gamma_H2_1)/2
#%%

###################
#   COMPRESSION   #
###################

gamma_avg = 1.3944

p2 = p1 * r ** gamma_1 #gamma_avg
    #Finding stage 2 pressure through pressure ratio
t2 = t1 * r**(gamma_1-1)
    #Finding stage 2 temp through adiabatic compression

cv_air_2 = air.cv(T=t2, p=p2)
    #volume specific heat at temperature t2
cp_air_2 = air.cp(T=t2, p=p2)
    #volume specific heat at temperature t2
gamma_air_2 = cp_air_2/cv_air_2
    #finding gamma. Basicaly the same as assumed value
s_air_2 = air.s(T=t2, p=p2)
    #air entropy at state point 2
h_air_2 = air.h(T=t2, p=p2)
    #air enthlpy at state point 2

cv_H2_2 = H2.cv(T=t2, p=p2)
    #volume specific heat at temperature t2
cp_H2_2 = H2.cp(T=t2, p=p2)
    #volume specific heat at temperature t2
gamma_H2_2 = cp_H2_2/cv_H2_2
    #finding gamma. Basicaly the same as assumed value
s_H2_2 = H2.s(T=t2, p=p2)
    #air entropy at state point 2
h_H2_2 = H2.h(T=t2, p=p2)
    #air enthlpy at state point 2

s_2 = (s_H2_2+s_air_2)/2

wc = h_air_2 - h_air_1
    #specific work required for compression

gamma_2 = (gamma_air_2 + gamma_H2_2)/2

gamma_avg_12 = (gamma_1 + gamma_2)/2
#%%
###################
#   COMBUSTION    #
###################

cv_air_avg = 0.8735
cv_H2_avg = 11.5
#fuel_air = kg_H2 / kg_air
t3 = t2 + Q*(kg_H2/excess)/(kg_air*cv_air_avg + (kg_H2*excess-kg_H2)*cv_H2_avg)
p3 = p2*(t3/t2)

cv_air_3 = air.cv(T=t3, p=p3)
cp_air_3 = air.cp(T=t3, p=p3)
h_air_3 = air.h(T=t3, p=p3)
s_air_3 = air.s(T=t3, p=p3)

cv_H2_3 = H2.cv(T=t3, p=p3)
cp_H2_3 = H2.cp(T=t3, p=p3)
s_H2_3 = H2.s(T=t3, p=p3)
h_H2_3 = H2.h(T=t3, p=p3)

cv_air_avg = (cv_air_3+cv_air_2)/2
cv_H2_avg = (cv_H2_3+cv_H2_2)/2

s_3 = (s_H2_3+s_air_3)/2

gamma_air_3 = cp_air_3/cv_air_3
gamma_H2_3 = cp_H2_3/cv_H2_3

gamma_3 = (gamma_air_3+gamma_H2_3)/2
#%%
###################
#     EXHAUST     #
###################

gamma_avg_34 = 1.1368

p4 = p3*r**(-gamma_3)
t4 = t3*r**(1-gamma_3)

cv_air_4 = air.cv(T=t4, p=p4)
cp_air_4 = air.cp(T=t4, p=p4)
h_air_4 = air.h(T=t4, p=p4)
s_air_4 = air.s(T=t4, p=p4)

cv_H2_4 = H2.cv(T=t4, p=p4)
cp_H2_4 = H2.cp(T=t4, p=p4)
s_H2_4 = H2.s(T=t4, p=p4)
h_H2_4 = H2.h(T=t4, p=p4)

cv_avg = (cv_air_1+cv_air_2+cv_air_3+cv_air_4)/4

s_4 = (s_H2_4+s_air_4)/2

gamma_air_4 = cp_air_4/cv_air_4
gamma_H2_4 = cp_H2_4/cv_H2_4

gamma_4 = (gamma_air_4+gamma_H2_4)/2

#gamma_avg_34 = (gamma_3+gamma_4)/2
# %%
W = cv_avg*( (t3-t2)-(t4-t1) )

P_spec = W*rpm/60
P = P_spec*(kg_air + kg_H2)
print(P)
#%%


#PLOTTING
fig1 = plt.figure()
plt.plot(t1, p1/1000, marker="o", label = f'T1 = {t1:.2f}[K]\nP1 = {p1:.2f}[kJ/kg]')
plt.plot(t2, p2/1000, marker="o", label = f'T2 = {t2[0]:.2f}[K]\nP2 = {p2[0]:.2f}[kJ/kg]')
plt.plot(t3, p3/1000, marker="o", label = f'T3 = {t3[0]:.2f}[K]\nP3 = {p3[0]:.2f}[kJ/kg]')
plt.plot(t4, p4/1000, marker="o", label = f'T4 = {t4[0]:.2f}[K]\nP4 = {p4[0]:.2f}[kJ/kg]')
#plt.annotate(f'T1 = {t1:.2f}[K]\nP1 = {p1/1000:.2f}[kPa]',xy=(t1,p1/1000),horizontalalignment='left', verticalalignment='bottom', fontsize=10)  
plt.annotate('1',xy=(t1,p1/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         

plt.annotate('2',xy=(t2,p2/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
#plt.annotate(f'T2 = {t2[0]:.2f}[K]\nP2 = {p2[0]/1000:.2f}[kPa]',xy=(t2,p2/1000),horizontalalignment='left', verticalalignment='bottom', fontsize=10)  

plt.annotate('3',xy=(t3,p3/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
#plt.annotate(f'T3 = {t3[0]:.2f}[K]\nP3 = {p3[0]/1000:.2f}[kPa]',xy=(t3,p3/1000),horizontalalignment='right', verticalalignment='top', fontsize=10)  

plt.annotate('4',xy=(t4,p4/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
#plt.annotate(f'T4 = {t4[0]:.2f}[K]\nP4 = {p4[0]/1000:.2f}[kPa]',xy=(t4,p4/1000),horizontalalignment='left', verticalalignment='bottom', fontsize=10)  

plt.xlabel('Temperature [K]')
plt.ylabel('Pressure [kPa]')
plt.title('80cc Hydrogen-Air Otto Cycle Simulation P-T Diagram')
plt.grid()
plt.legend()
#%%
fig2 = plt.figure()

plt.plot(s_1, t1, marker="o", label = f'T1 = {t1:.2f}[K]\nP1 = {s_1[0]:.2f}[kJ/kg]')
plt.plot(s_2, t2, marker="o", label = f'T2 = {t2[0]:.2f}[K]\nP2 = {s_2[0]:.2f}[kJ/kg]')
plt.plot(s_3, t3, marker="o", label = f'T3 = {t3[0]:.2f}[K]\nP3 = {s_3[0]:.2f}[kJ/kg]')
plt.plot(s_4, t4, marker="o", label = f'T4 = {t4[0]:.2f}[K]\nP4 = {s_4[0]:.2f}[kJ/kg]')

plt.annotate('1',xy=(s_1, t1),horizontalalignment='left', verticalalignment='top', fontsize=20)         

plt.annotate('2',xy=(s_2, t2),horizontalalignment='left', verticalalignment='top', fontsize=20)         

plt.annotate('3',xy=(s_3, t3),horizontalalignment='left', verticalalignment='top', fontsize=20)         
#plt.annotate(f'T3 = {t3:.2f}[K]\nP3 = {s_3[0]:.2f}[kPa]',xy=(t3,s_3),horizontalalignment='right', verticalalignment='top', fontsize=10)  

plt.annotate('4',xy=(s_4, t4),horizontalalignment='left', verticalalignment='top', fontsize=20)         
#plt.annotate(f'T4 = {t4[0]:.2f}[K]\nP4 = {s_4[0]:.2f}[kPa]',xy=(t4,s_4),horizontalalignment='left', verticalalignment='baseline', fontsize=10)  

plt.ylabel('Temperature [K]')
plt.xlabel('Entropy [kJ/K]')
plt.title('80cc Hydrogen-Air Otto Cycle Simulation T-S Diagram')
plt.grid()
plt.legend()
# %%
