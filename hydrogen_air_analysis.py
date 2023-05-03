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
    
mw_air = air.mw(T=t1, p=p1) #molecular weight of air at STP
mw_H2 = H2.mw(T=t1, p=p1) #molecular weight of H2 at STP
# %%

#quick calculation to get molar fractions

def kilograms(excess_percent):
    air_part = 1
    hydrogen = 0.21*2 * excess_percent
        #hydrogen will be two times the moles of oxygen present
    total = air_part + hydrogen
    air_fraction = air_part/total
    H2_fraction = hydrogen/total
    
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
    return kg_H2, kg_air
# %%

###################
#     INTAKE      #
###################


def intake(excess_percent, t1, p1):
    
    kg_H2, kg_air = kilograms(excess_percent)
    
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
    s_1 = (s_H2_1*kg_H2+s_air_1*kg_air)/(kg_air+kg_H2)
    '''
    v1_air = air.v(T=t1, p=p1)
    v1_H2 = H2.v(T=t1, p=p1)
    v1_tot = v1_air+v1_H2
    '''
    gamma_1 = (gamma_air_1*kg_air+gamma_H2_1*kg_H2)/(kg_H2+kg_air)
    
    return cv_air_1, cp_air_1, gamma_1, s_air_1, h_air_1, cv_H2_1, cp_H2_1, s_H2_1, h_H2_1, s_1 
#%%

###################
#   COMPRESSION   #
###################

gamma_avg = 1.391217

def compression(excess_percent, t1, p1):
    kg_H2, kg_air = kilograms(excess_percent)
    p2 = p1 * r ** gamma_avg #gamma_avg
        #Finding stage 2 pressure through pressure ratio
    t2 = t1 * r**(gamma_avg-1)
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

    s_2 = (s_H2_2*kg_H2+s_air_2*kg_air)/(kg_air+kg_H2)

    gamma_2 = (gamma_air_2*kg_air+gamma_H2_2*kg_H2)/(kg_H2+kg_air)
    
    return cv_air_2, cp_air_2, gamma_2, s_air_2, h_air_2, cv_H2_2, cp_H2_2, s_H2_2, h_H2_2, s_2, t2, p2
#%%
###################
#   COMBUSTION    #
###################

def combustion(excess_percent, t2, p2):
    kg_H2, kg_air = kilograms(excess_percent)
    cv_air_avg = 0.8735
    cv_H2_avg = 11.5

    t3 = t2 + Q*(kg_H2)/(kg_air*cv_air_avg)
    p3 = p2*(t3/t2)

    cv_air_3 = air.cv(T=t3, p=p3)
    cp_air_3 = air.cp(T=t3, p=p3)
    h_air_3 = air.h(T=t3, p=p3)
    s_air_3 = air.s(T=t3, p=p3)

    cv_H2_3 = H2.cv(T=t3, p=p3)
    cp_H2_3 = H2.cp(T=t3, p=p3)
    s_H2_3 = H2.s(T=t3, p=p3)
    h_H2_3 = H2.h(T=t3, p=p3)

    #cv_air_avg = (cv_air_3+cv_air_2)/2
    #cv_H2_avg = (cv_H2_3+cv_H2_2)/2

    s_3 = (s_H2_3*kg_H2+s_air_3*kg_air)/(kg_air+kg_H2)

    gamma_air_3 = cp_air_3/cv_air_3
    gamma_H2_3 = cp_H2_3/cv_H2_3

    gamma_3 = (gamma_air_3*kg_air+gamma_H2_3*kg_H2)/(kg_H2+kg_air)
    return cv_air_3, cp_air_3, gamma_3, s_air_3, h_air_3, cv_H2_3, cp_H2_3, s_H2_3, h_H2_3, s_3, t3, p3
#%%
###################
#     EXHAUST     #
###################

def exhaust(excess_percent, t3, p3, gamma_3):
    kg_H2, kg_air = kilograms(excess_percent)
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

    s_4 = (s_H2_4*kg_H2+s_air_4*kg_air)/(kg_air+kg_H2)

    gamma_air_4 = cp_air_4/cv_air_4
    gamma_H2_4 = cp_H2_4/cv_H2_4

    gamma_4 = (gamma_air_4*kg_air+gamma_H2_4*kg_H2)/(kg_H2+kg_air)

    #gamma_avg_34 = (gamma_3+gamma_4)/2
    return cv_air_4, cp_air_4, gamma_4, s_air_4, h_air_4, cv_H2_4, cp_H2_4, s_H2_4, h_H2_4, s_4, t4, p4
# %%
def power(excess_percent, t1, t2, t3, t4, cv_air_1, cv_air_2, cv_air_3, cv_air_4):
    kg_H2, kg_air = kilograms(excess_percent)
    cv_avg = (cv_air_1+cv_air_2+cv_air_3+cv_air_4)/4
    W = cv_avg*( (t3-t2)-(t4-t1) )

    P_spec = W*rpm/60
    P = P_spec*(kg_air + kg_H2)
    print(f'kW = {P}')
    return P

#%%
'''
###################
#     VOLUME      #
###################

fig1 = plt.figure()
plt.plot(v12, p12,'r--',linewidth=1.5)
plt.plot([v23,v23],[p2/1000,p3/1000],'r',linewidth=1.5)
plt.plot(v34, p34,'r--',linewidth=1.5)
plt.plot([v41[0],v41[0]],[p4[0]/1000,p1/1000],'r',linewidth=1.5)

plt.annotate('1',xy=(v1,p1/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
plt.annotate('2',xy=(v2,p2/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
plt.annotate('3',xy=(v3,p3/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
plt.annotate('4',xy=(v4,p4/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
'''
#plt.plot(v1, p1/1000, marker="o", label = f'V1 = {v1[0]:.2f}[cc]\nP1 = {p1/1000:.2f}[kPa]')
#plt.plot(v2, p2/1000, marker="o", label = f'V2 = {v2[0]:.2f}[cc]\nP2 = {p2/1000:.2f}[kPa]')
#plt.plot(v3, p3/1000, marker="o", label = f'V3 = {v3[0]:.2f}[cc]\nP3 = {p3/1000:.2f}[kPa]')
#plt.plot(v4, p4/1000, marker="o", label = f'V4 = {v4[0]:.2f}[cc]\nP4 = {p4[0]/1000:.2f}[kPa]')
'''
plt.grid()
plt.legend()

plt.xlabel('Volume [cc]')
plt.ylabel('Pressure [kPa]')
plt.title(f'80cc Hydrogen-Air {np.round((excess-1)*100)}% excess Otto Cycle Simulation P-V')
plt.savefig(f'Hydrogen-Air_graphs/P-V_{np.round((excess-1)*100)}_excess.png')
'''
#%%
###################
#   SPECIFIC VOL  #
###################

def SV(excess, t1, p1, points):
    kg_H2, kg_air = kilograms(excess)
    
    cv_air_1, cp_air_1, gamma_1, s_air_1, h_air_1, cv_H2_1, cp_H2_1, s_H2_1, h_H2_1, s_1 = intake(excess, t1, p1)
    cv_air_2, cp_air_2, gamma_2, s_air_2, h_air_2, cv_H2_2, cp_H2_2, s_H2_2, h_H2_2, s_2, t2, p2 = compression(excess, t1, p1)
    cv_air_3, cp_air_3, gamma_3, s_air_3, h_air_3, cv_H2_3, cp_H2_3, s_H2_3, h_H2_3, s_3, t3, p3 = combustion(excess, t2, p2)
    cv_air_4, cp_air_4, gamma_4, s_air_4, h_air_4, cv_H2_4, cp_H2_4, s_H2_4, h_H2_4, s_4, t4, p4 = exhaust(excess, t3, p3, gamma_3)
    P = power(excess, t1, t2, t3, t4, cv_air_1, cv_air_2, cv_air_3, cv_air_4)
    
    l = points
    
    t_12 = np.linspace(t1, t2, l)
    t_23 = np.linspace(t2, t3, l)
    t_34 = np.linspace(t3, t4, l)
    t_14 = np.linspace(t1, t4, l)

    v1_air = air.v(T=t1, s=s_air_1)
    v2_air = air.v(T=t2, s=s_air_2)
    v3_air = air.v(T=t3, s=s_air_3)
    v4_air = air.v(T=t4, s=s_air_4)

    v1_H2 = H2.v(T=t1, s=s_H2_1)
    v2_H2 = H2.v(T=t2, s=s_H2_2)
    v3_H2 = H2.v(T=t3, s=s_H2_3)
    v4_H2 = H2.v(T=t4, s=s_H2_4)

    v1 = (v1_air*kg_air + v1_H2*kg_H2)*1e6
    v2 = (v2_air*kg_air + v2_H2*kg_H2)*1e6
    v3 = (v3_air*kg_air + v3_H2*kg_H2)*1e6
    v4 = (v4_air*kg_air + v4_H2*kg_H2)*1e6

    v12_air = air.v(T=t_12, s=s_air_1)
    v23_air = air.v(T=t2,   s=s_air_2)
    v34_air = air.v(T=t_34, s=s_air_4)
    v41_air = air.v(T=t4,   s=s_air_4)

    v12_H2 = H2.v(T=t_12, s=s_H2_1)
    v23_H2 = H2.v(T=t2,   s=s_H2_2)
    v34_H2 = H2.v(T=t_34, s=s_H2_4)
    v41_H2 = H2.v(T=t4,   s=s_H2_4)

    v12 = (v12_air*kg_air + v12_H2*kg_H2)*1e6
    v23 = (v23_air*kg_air + v23_H2*kg_H2)*1e6
    v34 = (v34_air*kg_air + v34_H2*kg_H2)*1e6
    v41 = (v41_air*kg_air + v41_H2*kg_H2)*1e6

    p12 = air.p(T=t_12, s=s_air_1)/1000
    p23 = air.p(T=t_23, v=v23_air)/1000
    p34 = air.p(T=t_34, s=s_air_3)/1000
    p41 = air.p(T=t_14, v=v41_air)/1000
    
    v12_sp = (v12_air*kg_air + v12_H2*kg_H2)/(kg_H2+kg_air)
    v23_sp = (v23_air*kg_air + v23_H2*kg_H2)/(kg_H2+kg_air)
    v34_sp = (v34_air*kg_air + v34_H2*kg_H2)/(kg_H2+kg_air)
    v41_sp = (v41_air*kg_air + v41_H2*kg_H2)/(kg_H2+kg_air)

    v1_sp = (v1_air*kg_air + v1_H2*kg_H2)/(kg_air+kg_H2)
    v2_sp = (v2_air*kg_air + v2_H2*kg_H2)/(kg_air+kg_H2)
    v3_sp = (v3_air*kg_air + v3_H2*kg_H2)/(kg_air+kg_H2)
    v4_sp = (v4_air*kg_air + v4_H2*kg_H2)/(kg_air+kg_H2)
    
    p12 = air.p(T=t_12, s=s_air_1)/1000
    p23 = air.p(T=t_23, v=v23_air)/1000
    p34 = air.p(T=t_34, s=s_air_3)/1000
    p41 = air.p(T=t_14, v=v41_air)/1000
    
    return v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, \
        p1, p2, p3, p4, p12, p23, p34, p41, t1, t2, t3, t4, t_12, t_23, t_34, t_14,\
            s_air_1, s_air_2, s_air_3, s_air_4, kg_H2, kg_air, s_1, s_2, s_3, s_4,\
                v12_air, v23_air, v34_air, v41_air, v12_H2, v23_H2, v34_H2, v41_H2, P

excesses = np.array([1, 0.5, 0.25])


fig2 = plt.figure()

c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41, t1, t2, t3, t4, \
        t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_H2, kg_air, s_1, s_2, s_3, s_4, \
            v12_air, v23_air, v34_air, v41_air, v12_H2, v23_H2, v34_H2, v41_H2, P = SV(e, t1, p1, 20)
    if c == 0:
        color = 'r'
        plt.annotate('1',xy=(v1_sp,p1/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('2',xy=(v2_sp,p2/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('3',xy=(v3_sp,p3/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('4',xy=(v4_sp,p4/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         

        plt.plot(v1_sp, p1/1000, marker="o", label = f'V1 = {v1_sp[0]:.2f}[$m^3$]\nP1 = {p1/1000:.2f}[kPa]')
        plt.plot(v2_sp, p2/1000, marker="o", label = f'V2 = {v2_sp[0]:.2f}[$m^3$]\nP2 = {p2/1000:.2f}[kPa]')
        plt.plot(v3_sp, p3/1000, marker="o", label = f'V3 = {v3_sp[0]:.2f}[$m^3$]\nP3 = {p3/1000:.2f}[kPa]')
        plt.plot(v4_sp, p4/1000, marker="o", label = f'V4 = {v4_sp[0]:.2f}[$m^3$]\nP4 = {p4[0]/1000:.2f}[kPa]')
    elif c==1:
        color = 'b'
    else:
        color = 'g'

    plt.plot(v12_sp, p12,f'{color}--',linewidth=1.5, label=f'{e*100}% of Stoichiometric')
    plt.plot([v23_sp,v23_sp],[p2/1000,p3/1000],f'{color}',linewidth=1.5)
    plt.plot(v34_sp, p34,f'{color}--',linewidth=1.5)
    plt.plot([v41_sp[0],v41_sp[0]],[p4[0]/1000,p1/1000],f'{color}',linewidth=1.5)
    
    c+=1

plt.grid()
plt.legend()

plt.xlabel(r'Specific Volume [$m^3$/kg]')
plt.ylabel('Pressure [kPa]')
plt.title(f'80cc Hydrogen-Air Otto Cycle Simulation P-v')
plt.ylim(-100,10000)
plt.savefig(f'Hydrogen-Air_graphs/P-V_specific.png')
#%%
###################
#       TEMP      #
###################

#PLOTTING
fig3 = plt.figure()

excesses = np.array([1, 0.5, 0.25])
c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41, t1, t2, t3, t4, \
        t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_H2, kg_air, s_1, s_2, s_3, s_4, \
            v12_air, v23_air, v34_air, v41_air, v12_H2, v23_H2, v34_H2, v41_H2, P = SV(e, t1, p1, 20)
    if c == 0:
        color = 'r'
        plt.plot(t1, p1/1000, marker="o", label = f'T1 = {t1:.2f}[K]\nP1 = {p1/1000:.2f}[kPa]')
        plt.plot(t2, p2/1000, marker="o", label = f'T2 = {t2:.2f}[K]\nP2 = {p2/1000:.2f}[kPa]')
        plt.plot(t3, p3/1000, marker="o", label = f'T3 = {t3:.2f}[K]\nP3 = {p3/1000:.2f}[kPa]')
        plt.plot(t4, p4/1000, marker="o", label = f'T4 = {t4[0]:.2f}[K]\nP4 = {p4[0]/1000:.2f}[kPa]')

        plt.annotate('1',xy=(t1,p1/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('2',xy=(t2,p2/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('3',xy=(t3,p3/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('4',xy=(t4,p4/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
    elif c==1:
        color = 'b'
    else:
        color = 'g'
    plt.plot(t_12, p12,f'{color}--',linewidth=1.5, label=f'{e*100}% of Stoichiometric')
    plt.plot(t_23, p23,f'{color}--',linewidth=1.5)
    plt.plot(t_34, p34,f'{color}--',linewidth=1.5)
    plt.plot(t_14, p41,f'{color}--',linewidth=1.5)
    c+=1
    
plt.xlabel('Temperature [K]')
plt.ylabel('Pressure [kPa]')
plt.title(f'80cc Hydrogen-Air Otto Cycle Simulation P-T')

plt.grid()
plt.legend()
plt.xlim(0,5000)
plt.ylim(0,10000)

plt.savefig(f'Hydrogen-Air_graphs/P-T.png')
#%%
###################
#     ENTROPY     #
###################
fig4 = plt.figure()

excesses = np.array([1, 0.5, 0.25])
c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41, t1, t2, t3, t4, \
        t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_H2, kg_air, s_1, s_2, s_3, s_4, \
            v12_air, v23_air, v34_air, v41_air, v12_H2, v23_H2, v34_H2, v41_H2, P = SV(e, t1, p1, 20)
    if c == 0:
        color = 'r'

        plt.plot(s_1, t1, marker="o", label = f'T1 = {t1:.2f}[K]\ns1 = {s_1[0]:.2f}[kJ/kg]')
        plt.plot(s_2, t2, marker="o", label = f'T2 = {t2:.2f}[K]\ns2 = {s_2[0]:.2f}[kJ/kg]')
        plt.plot(s_3, t3, marker="o", label = f'T3 = {t3:.2f}[K]\ns3 = {s_3[0]:.2f}[kJ/kg]')
        plt.plot(s_4, t4, marker="o", label = f'T4 = {t4[0]:.2f}[K]\ns4 = {s_4[0]:.2f}[kJ/kg]')
        
        plt.annotate('1',xy=(s_1, t1),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('2',xy=(s_2, t2),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('3',xy=(s_3, t3),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('4',xy=(s_4, t4),horizontalalignment='left', verticalalignment='top', fontsize=20)         
    elif c==1:
        color = 'b'
    else:
        color = 'g'

    air_s_14 = air.s(T=t_14, v=v41_air)
    air_s_23 = air.s(T=t_23, v=v23_air)

    H2_s_14 = H2.s(T=t_14, v=v41_H2)
    H2_s_23 = H2.s(T=t_23, v=v23_H2)
    
    plt.plot([s_1[0],s_2[0]],[t1,t2],f'{color}',linewidth=1.5)
    plt.plot([s_3[0],s_4[0]],[t3,t4[0]],f'{color}',linewidth=1.5)
    
    gas_14 = (air_s_14*kg_air+H2_s_14*kg_H2)/(kg_air+kg_H2)
    plt.plot(gas_14,t_14,f'{color}--',linewidth=1.5)

    gas_23 = (air_s_23*kg_air+H2_s_23*kg_H2)/(kg_air+kg_H2)
    plt.plot(gas_23,t_23,f'{color}--',linewidth=1.5)

    c+=1

plt.ylabel('Temperature [K]')
plt.xlabel('Specific Entropy [kJ/K kg]')
plt.title(f'80cc Hydrogen-Air Otto Cycle Simulation T-S')
plt.grid()
plt.legend()

plt.ylim(0,5000)

plt.savefig(f'Hydrogen-Air_graphs/T-S.png')
# %%

###################
#     RUNTIME     #
###################
fig5 = plt.figure()

excesses = np.array([1, 0.5, 0.25])
c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41, t1, t2, t3, t4, \
        t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_H2, kg_air, s_1, s_2, s_3, s_4, \
            v12_air, v23_air, v34_air, v41_air, v12_H2, v23_H2, v34_H2, v41_H2, P = SV(e, t1, p1, 20)
    if c == 0:
        color = 'r'       
    elif c==1:
        color = 'b'
    else:
        color = 'g' 

    duty_cycle = np.linspace(0.1,1,100)
    rps = 6000/60
    m_dot_H2 = kg_H2*rps*duty_cycle

    tank_vol = 6 #[liters]
    tank_pressure = 345 #[bar]
    tank_size = tank_pressure*tank_vol/1.01325 #[liters at stp]
    m_tot_H2 = H2.d(T=t1, p=p1)*tank_size/1000
    runtime = (m_tot_H2/m_dot_H2)/60
    plt.plot(duty_cycle, runtime/60, label=f'{e*100}% of Stoichiometric')
    c+=1
    
plt.xlabel('Duty Cycle')
plt.ylabel('Runtime [hr]')
plt.title(f'Runtime, Hydrogen-Ai with Duty Cycle \n 6 liter, 350 bar tank')
plt.grid()
plt.ylim(0,15)
plt.xlim(0.1,1)
plt.legend()
plt.savefig(f'Hydrogen-Air_graphs/runtime_duty_cycle.png')
# %%
fig6 = plt.figure()

excesses = np.array([1, 0.5, 0.25])
c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41, t1, t2, t3, t4, \
        t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_H2, kg_air, s_1, s_2, s_3, s_4, \
            v12_air, v23_air, v34_air, v41_air, v12_H2, v23_H2, v34_H2, v41_H2, P = SV(e, t1, p1, 20)
    if c == 0:
        color = 'r'       
    elif c==1:
        color = 'b'
    else:
        color = 'g' 


    avg_rpm = np.linspace(1000,6000,100)
    rps = avg_rpm/60
    m_dot_H2 = kg_H2*rps
    runtime = (m_tot_H2/m_dot_H2)/60
    plt.plot(avg_rpm, runtime/60, label=f'{e*100}% of Stoichiometric')
    c+=1
    
plt.xlabel('Average RPM')
plt.ylabel('Runtime [hr]')
plt.grid()
plt.legend()
plt.title(f'Runtime, Hydrogen-Air at given RPM \n 6 liter, 350 bar tank')
plt.ylim(0,8)
plt.xlim(1000,6000)
plt.savefig(f'Hydrogen-Air_graphs/runtime_rpm.png')
# %%
fig7 = plt.figure()

c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41, t1, t2, t3, t4, \
        t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_H2, kg_air, s_1, s_2, s_3, s_4, \
            v12_air, v23_air, v34_air, v41_air, v12_H2, v23_H2, v34_H2, v41_H2, P = SV(e, t1, p1, 20)
    if c == 0:
        color = 'r'       
    elif c==1:
        color = 'b'
    else:
        color = 'g' 

    plt.plot(e, P,'o', label=f'Power={np.round(P,2)}kW \n {e*100}% of Stoichiometric')
    
    print(f'Hydrogen per Cycle at {np.round(e*100)}% of stoich = {kg_H2} [kg]')
    
plt.xlabel('Percent Hydrogen of Stoichiometric')
plt.ylabel('Power [kW]')
plt.title('Power Versus Percent Hydrogen of Stoichiometric')
plt.grid()
plt.legend()
plt.savefig(f'Hydrogen-Air_graphs/power_v_e.png')
# %%
