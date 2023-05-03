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
mw_air = air.mw(T=t1, p=p1) 
    #molecular weight of H2 at STP
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
excess = 0.3
    #excess value for iso_octane

    
def kilograms_iso(excess_percent):
    #kg of iso-octane reuired for stoichiometric combustion
    moles_iso = n_iso
    molecular_weight_iso = mw_iso
    kg = moles_iso*molecular_weight_iso*excess_percent/1000
    return kg
    
# %%
###################
#      INTAKE     #
###################

def intake(t1, p1):
    cv_air = air.cv(T=t1, p=p1)
    #volume specific heat at temperature t1
    cp_air = air.cp(T=t1, p=p1)
    #volume specific heat at temperature t1
    gamma = cp_air/cv_air
    #finding gamma. Basicaly the same as assumed value
    s_air = air.s(T=t1, p=p1)
    #air entropy at state point 1
    h_air = air.h(T=t1, p=p1)
    #air enthlpy at state point 1
    return cv_air, cp_air, gamma, s_air, h_air

#%%
###################
#   COMPRESSION   #
###################

gamma_avg = 1.3912

def compression(t1, p1):
    p2 = p1 * r ** gamma_avg
        #Finding stage 2 pressure through pressure ratio
    t2 = t1 * r**(gamma_avg-1)
        #Finding stage 2 temp through adiabatic compression
    cv_air_2 = air.cv(T=t2, p=p2)
        #volume specific heat at temperature t2
    cp_air_2 = air.cp(T=t2, p=p2)
        #volume specific heat at temperature t1
    gamma_air_2 = cp_air_2/cv_air_2
        #finding gamma. Basicaly the same as assumed value

    s_air_2 = air.s(T=t2, p=p2)
        #air entropy at state point 2
    h_air_2 = air.h(T=t2, p=p2)
        #H2 enthalpy at state point 2
    
    return cv_air_2, cp_air_2, gamma_air_2, s_air_2, h_air_2, p2, t2
        #specific work required for compression

#wc = h_air_2 - h_air_1
#%%
###################
#   COMBUSTION    #
###################

def combustion(t2, p2, kg_iso, kg_air, Q):
    cv_air_avg = 0.8735
    t3 = t2 + Q*kg_iso/(kg_air*cv_air_avg)
    p3 = p2*(t3/t2)

    cv_air_3 = air.cv(T=t3, p=p3)
    cp_air_3 = air.cp(T=t3, p=p3)
    h_air_3 = air.h(T=t3, p=p3)
    s_air_3 = air.s(T=t3, p=p3)

    gamma_air_3 = cp_air_3/cv_air_3
    return cv_air_3, cp_air_3, gamma_air_3, s_air_3, h_air_3, p3, t3
#%%
###################
#     EXHAUST     #
###################
def exhaust(t3, p3, gamma_air_3):
    p4 = p3*r**(-gamma_air_3)
    t4 = t3*r**(1-gamma_air_3)

    cv_air_4 = air.cv(T=t4, p=p4)
    cp_air_4 = air.cp(T=t4, p=p4)
    h_air_4 = air.h(T=t4, p=p4)
    s_air_4 = air.s(T=t4, p=p4)
    
    gamma_air_4 = cp_air_4/cv_air_4
    return cv_air_4, cp_air_4, gamma_air_4, s_air_4, h_air_4, p4, t4

# %%

def power(t1, t2, t3, t4, cv_air_1, cv_air_2, cv_air_3, cv_air_4):
    cv_avg = (cv_air_1+cv_air_2+cv_air_3+cv_air_4)/4
    W = cv_avg*( (t3-t2)-(t4-t1) )

    P_spec = W*rpm/60
    P = P_spec*(kg_air)
    print(f'kW = {P}')
    return P
#%%
###################
#     VOLUME      #
###################
'''
#DEPRECATED FOR NOW. TOTAL VOLUME

l = 20
t_12 = np.linspace(t1, t2, l)
t_23 = np.linspace(t2, t3, l)
t_34 = np.linspace(t3, t4, l)
t_14 = np.linspace(t1, t4[0], l)

v1_air = air.v(T=t1, s=s_air_1)
v2_air = air.v(T=t2, s=s_air_2)
v3_air = air.v(T=t3, s=s_air_3)
v4_air = air.v(T=t4, s=s_air_4)

v1 = (v1_air*kg_air)*1e6
v2 = (v2_air*kg_air)*1e6
v3 = (v3_air*kg_air)*1e6
v4 = (v4_air*kg_air)*1e6

v12_air = air.v(T=t_12, s=s_air_1)
v23_air = air.v(T=t2, s=s_air_2[0])
v34_air = air.v(T=t_34, s=s_air_4)
v41_air = air.v(T=t4, s=s_air_4[0])

v12 = (v12_air*kg_air)*1e6
v23 = (v23_air*kg_air)*1e6
v34 = (v34_air*kg_air)*1e6
v41 = (v41_air*kg_air)*1e6

p12 = air.p(T=t_12, s=s_air_1)/1000
p23 = air.p(T=t_23, v=v23_air)/1000
p34 = air.p(T=t_34, s=s_air_3)/1000
p41 = air.p(T=t_14, v=v41_air)/1000

fig1 = plt.figure()
plt.plot(v12, p12,'r--',linewidth=1.5)
plt.plot([v23,v23],[p2/1000,p3/1000],'r',linewidth=1.5)
plt.plot(v34, p34,'r--',linewidth=1.5)
plt.plot([v41[0],v41[0]],[p4[0]/1000,p1/1000],'r',linewidth=1.5)

plt.annotate('1',xy=(v1,p1/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
plt.annotate('2',xy=(v2,p2/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
plt.annotate('3',xy=(v3,p3/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         
plt.annotate('4',xy=(v4,p4/1000),horizontalalignment='left', verticalalignment='top', fontsize=20)         

plt.plot(v1, p1/1000, marker="o", label = f'V1 = {v1[0]:.2f}[cc]\nP1 = {p1/1000:.2f}[kPa]')
plt.plot(v2, p2/1000, marker="o", label = f'V2 = {v2[0]:.2f}[cc]\nP2 = {p2/1000:.2f}[kPa]')
plt.plot(v3, p3/1000, marker="o", label = f'V3 = {v3[0]:.2f}[cc]\nP3 = {p3/1000:.2f}[kPa]')
plt.plot(v4, p4/1000, marker="o", label = f'V4 = {v4[0]:.2f}[cc]\nP4 = {p4[0]/1000:.2f}[kPa]')

plt.grid()
plt.legend()

plt.xlabel('Volume [cc]')
plt.ylabel('Pressure [kPa]')
plt.title(f'80cc Iso-Octane-Air {np.round((excess-1)*100)}% excess Otto Cycle Simulation P-V')
plt.savefig(f'Iso-octane_graphs/P-V_total_{np.round((excess-1)*100)}%_excess.png')
'''
# %%

###################
#   SPECIFIC VOL  #
###################

def SV(excess,t1, p1, points):
    kg_iso = kilograms_iso(excess)
    cv_air_1, cp_air_1, gamma_1, s_air_1, h_air_1 = intake(t1, p1)
    cv_air_2, cp_air_2, gamma_2, s_air_2, h_air_2, p2, t2 = compression(t1, p1)
    cv_air_3, cp_air_3, gamma_3, s_air_3, h_air_3, p3, t3 = combustion(t2, p2, kg_iso, kg_air, Q)
    cv_air_4, cp_air_4, gamma_4, s_air_4, h_air_4, p4, t4 = exhaust(t3, p3, gamma_3)
    P = power(t1, t2, t3, t4, cv_air_1, cv_air_2, cv_air_3, cv_air_4)
    
    l = points
    
    t_12 = np.linspace(t1, t2, l)
    t_23 = np.linspace(t2, t3, l)
    t_34 = np.linspace(t3, t4, l)
    t_14 = np.linspace(t1, t4, l)
    
    v12_air = air.v(T=t_12, s=s_air_1)
    v23_air = air.v(T=t2,   s=s_air_2)
    v34_air = air.v(T=t_34, s=s_air_4)
    v41_air = air.v(T=t4,   s=s_air_4)
    
    v12_sp = (v12_air)
    v23_sp = (v23_air)
    v34_sp = (v34_air)
    v41_sp = (v41_air)

    v1_air = air.v(T=t1, s=s_air_1)
    v2_air = air.v(T=t2, s=s_air_2)
    v3_air = air.v(T=t3, s=s_air_3)
    v4_air = air.v(T=t4, s=s_air_4)

    v1_sp = (v1_air)
    v2_sp = (v2_air)
    v3_sp = (v3_air)
    v4_sp = (v4_air)
    
    p12 = air.p(T=t_12, s=s_air_1)/1000
    p23 = air.p(T=t_23, v=v23_air)/1000
    p34 = air.p(T=t_34, s=s_air_3)/1000
    p41 = air.p(T=t_14, v=v41_air)/1000
    
    return v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, \
        p1, p2, p3, p4, p12, p23, p34, p41, t1, t2, t3, t4, t_12, t_23, t_34, t_14,\
            s_air_1, s_air_2, s_air_3, s_air_4, kg_iso, P

excesses = np.array([1, 0.5, 0.25])

fig2 = plt.figure()
c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41,\
        t1, t2, t3, t4, t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_iso, P= SV(e, t1, p1, 20)
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
plt.title(f'80cc Iso-Octane-Air Otto Cycle Simulation P-v')
plt.ylim(-100,10000)
plt.savefig(f'Iso-octane_graphs/P-V_specific.png')
# %%
###################
#       TEMP      #
###################
fig3 = plt.figure()

excesses = np.array([1, 0.5, 0.25])
c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41,\
        t1, t2, t3, t4, t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_iso, P = SV(e, t1, p1, 20)
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

#PLOTTING

plt.xlabel('Temperature [K]')
plt.ylabel('Pressure [kPa]')
plt.title(f'80cc Iso-Octane-Air Otto Cycle Simulation P-T')

plt.grid()
plt.legend()
plt.xlim(0,5000)
plt.ylim(0,10000)

plt.savefig(f'Iso-octane_graphs/P-T.png')
# %%
###################
#     ENTROPY     #
###################

fig4 = plt.figure()

c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41,\
        t1, t2, t3, t4, t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_iso, P = SV(e, t1, p1, 20)
    if c == 0:
        color = 'r'
        plt.plot(s_air_1, t1, marker="o", label = f'T1 = {t1:.2f}[K]\ns1 = {s_air_1[0]:.2f}[kJ/kg]')
        plt.plot(s_air_2, t2, marker="o", label = f'T2 = {t2:.2f}[K]\ns2 = {s_air_2[0]:.2f}[kJ/kg]')
        plt.plot(s_air_3, t3, marker="o", label = f'T3 = {t3:.2f}[K]\ns3 = {s_air_3[0]:.2f}[kJ/kg]')
        plt.plot(s_air_4, t4, marker="o", label = f'T4 = {t4[0]:.2f}[K]\ns4 = {s_air_4[0]:.2f}[kJ/kg]')   
        
        plt.annotate('1',xy=(s_air_1, t1),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('2',xy=(s_air_2, t2),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('3',xy=(s_air_3, t3),horizontalalignment='left', verticalalignment='top', fontsize=20)         
        plt.annotate('4',xy=(s_air_4, t4),horizontalalignment='left', verticalalignment='top', fontsize=20)         
         
    elif c==1:
        color = 'b'
    else:
        color = 'g'

    air_s_14 = air.s(T=t_14, v=v41_sp)
    air_s_23 = air.s(T=t_23, v=v23_sp)
    plt.plot([s_air_1[0],s_air_2[0]],[t1,t2],f'{color}',linewidth=1.5,  label=f'{e*100}% of Stoichiometric')
    plt.plot([s_air_3[0],s_air_4[0]],[t3,t4[0]],f'{color}',linewidth=1.5)
    plt.plot(air_s_14,t_14,f'{color}--',linewidth=1.5)
    plt.plot(air_s_23,t_23,f'{color}--',linewidth=1.5)    
    c+=1

#LINES


plt.ylabel('Temperature [K]')
plt.xlabel('Specific Entropy [kJ/K kg]')
plt.title(f'80cc Iso-Octane-Air Otto Cycle Simulation P-T')
plt.grid()
plt.legend()

plt.ylim(0,5000)

plt.savefig(f'Iso-octane_graphs/T-S.png')
# %%
###################
#     RUNTIME     #
###################
fig5 = plt.figure()


c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41,\
        t1, t2, t3, t4, t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_iso, P = SV(e, t1, p1, 20)
    if c == 0:
        color = 'r'       
    elif c==1:
        color = 'b'
    else:
        color = 'g' 
    duty_cycle = np.linspace(0.1,1,100)
    rps = 6000/60
    m_dot_iso = kg_iso*rps*duty_cycle
    rho_iso = 690 #[kg/m3]
    tank_vol = 1 #[liters]
    m_tot_iso = rho_iso*tank_vol/1000
    runtime = (m_tot_iso/m_dot_iso)/60
    plt.plot(duty_cycle, runtime/60, label=f'{e*100}% of Stoichiometric')
    c+=1


plt.xlabel('Duty Cycle')
plt.ylabel('Runtime [hr]')
plt.title(f'Runtime, Iso-Octane Air with Duty Cycle \n 1 Liter Tank')
plt.grid()
plt.ylim(0,15)
plt.xlim(0.1,1)
plt.legend()
plt.savefig(f'Iso-octane_graphs/runtime_duty_cycle.png')

# %%
fig6 = plt.figure

c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41,\
        t1, t2, t3, t4, t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_iso, P = SV(e, t1, p1, 20)
    if c == 0:
        color = 'r'       
    elif c==1:
        color = 'b'
    else:
        color = 'g' 
    avg_rpm = np.linspace(1000,6000,100)
    rps = avg_rpm/60
    rho_iso = 690 #[kg/m3]
    tank_vol = 1 #[liters]
    m_tot_iso = rho_iso*tank_vol/1000
    m_dot_iso_a = kg_iso*rps
    runtime = (m_tot_iso/m_dot_iso_a)/60
    
    plt.plot(avg_rpm, runtime/60, label=f'{e*100}% of Stoichiometric')
    c+=1


plt.plot(avg_rpm, runtime)
plt.xlabel('Average RPM')
plt.ylabel('Runtime [hr]')
plt.title(f'Runtime, Iso-Octane Air at Given RPM \n 1 Liter Tank')
plt.grid()
plt.ylim(0,8)
plt.xlim(1000,6000)
plt.legend()
plt.savefig(f'Iso-octane_graphs/runtime_rpm.png')
# %%
fig7 = plt.figure()

c = 0
for e in excesses:
    v12_sp, v23_sp, v34_sp, v41_sp, v1_sp, v2_sp, v3_sp, v4_sp, p1, p2, p3, p4, p12, p23, p34, p41,\
        t1, t2, t3, t4, t_12, t_23, t_34, t_14, s_air_1, s_air_2, s_air_3, s_air_4, kg_iso, P = SV(e, t1, p1, 20)
    if c == 0:
        color = 'r'       
    elif c==1:
        color = 'b'
    else:
        color = 'g' 

    plt.plot(e, P,'o', label=f'Power={np.round(P,2)}kW \n {e*100}% of Stoichiometric')
    
    print(f'Iso-Oct per Cycle at {np.round(e*100)}% of stoich = {kg_iso} [kg]')
    
plt.xlabel('Percent Iso-octane of Stoichiometric')
plt.ylabel('Power [kW]')
plt.title('Power Versus Percent Iso-Octane of Stoichiometric')
plt.grid()
plt.legend()
plt.savefig(f'Iso-octane_graphs/power_v_e.png')
# %%
