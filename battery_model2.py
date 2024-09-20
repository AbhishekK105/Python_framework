# -*- coding: utf-8 -*-
"""
Created on Mon May  9 15:54:21 2022

@author: s345001
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import json

from math import ceil
from scipy.interpolate import PchipInterpolator
from scipy.integrate import solve_ivp, simpson, trapezoid
from scipy.optimize import fsolve


import warnings
warnings.filterwarnings("ignore", message='The iteration is not making good progress')
warnings.filterwarnings("ignore", message='RuntimeWarning: invalid value encountered in true_divide')


# def V_OC_2003(SOC): # 179.71 Wh/kg
#     return -1.031 * np.exp(-35 * SOC) + 3.685 + 0.2156 * SOC - 0.1178 * SOC ** 2 + 0.3201 * SOC ** 3

# def V_OC_2006(SOC): # 93.0769 Wh/kg
#     return -0.5863 * np.exp(-21.9 * SOC) + 3.414 + 0.1102 * SOC - 0.1718 * np.exp(-0.008/(1-SOC))


def V_OC_2014(SOC): # 133 Wh/kg
    return 13.91 * SOC ** 6 - 35.62 * SOC ** 5 + 29.61 * SOC **4 - 5.232 * SOC ** 3 - 3.959 * SOC **2 + 2.023 * SOC + 3.502


# def R0_2003(SOC): # 179.71 Wh/kg
#     return 0.5162 * np.exp(-24.37 * SOC) + 0.07446

def R0_2014(SOC): # 133 Wh/kg
    return 0.01483 * SOC**2 - 0.02518*SOC +0.1036

def Rth_2014(SOC):
    return -1.212 * np.exp(-0.03383 * SOC) + 1.258

def Cth_2014(SOC):
    Rth = Rth_2014(SOC)
    tau = 2.151 * np.exp(2.132 * SOC) + 27.2
    return tau/Rth

def V_OC_2011(SOC):
    return -0.1558*SOC**3 + 0.625*SOC**2 + 0.0776*SOC + 3.643

def R0_2011(SOC):
    return 0.0082*SOC**3 - 0.0113*SOC**2 +0.003*SOC + 0.0114

def Rth_2011(SOC):
    return 0.036 * SOC **3 + 0.0551*SOC**2 - 0.0251*SOC + 0.0103

def Cth_2011(SOC):
    return 82419*SOC**3 - 119776*SOC**2 + 50522*SOC + 7415.9


def V_ocp(DOD):
    return V_OC_2011(1-DOD)

def R0(DOD):
    return R0_2011(1-DOD) #/ 33.366

def Rth(DOD):
    return Rth_2011(1-DOD) #/ 8.9865

def Cth(DOD):
    return Cth_2011(1-DOD) #* (38/7)

class battery_cell_ODE:
    def __init__(self, en_density, cell_capacity, 
                 nom_tension, aging_data):
        
        # tspan is in seconds
        self.capacity = cell_capacity
        self.nominal_tension = nom_tension
        self.en_density = en_density
        
        self.mass = (nom_tension * cell_capacity)/en_density
        # self.heat_capacity = heat_capacity #J/(Kg K)
        # self.cell_surface = cell_surface
        # self.h_cool = h_cool
        
        
        # Aging model data
        self.days        = [0]
        self.cycles      = [0]
        self.Q_through   = [0]
        
        self.Ef_cal = [1]
        self.Ef_cyc = [1]
        
        self.Rg_cal = [1]
        self.Rg_cyc = [1]
        
        self.E_fade_hist = [1]
        self.R_grow_hist = [1]
        
        
        
        # self.delta_DOD = aging_data['Delta_DOD']
        # self.V_rms     = aging_data['V_rms']
        # self.T_store   = aging_data['T_store']
        # self.SOC_store = aging_data['SOC_store']
        
        # self.V_store   = V_ocp(1 - self.SOC_store)
        
        # self.n_cycles  = aging_data['Flights per Day'] * aging_data['Operational Days'] * 2
        # self.n_days    = aging_data['Operational Days']
        
        # #Calendar Aging Parameters
        # self.alpha_C = (7.543 * self.V_store - 23.75)* 1e6 * np.exp(-6976/self.T_store)
        # self.alpha_R = (5.270 * self.V_store - 16.32)* 1e5 * np.exp(-5986/self.T_store)

        # #Cycle Aging Parameters
        # self.beta_C = 7.3481e-3 * (self.V_rms - 3.667) **2 + 7.6001e-4 + 4.0811e-3 * self.delta_DOD
        # self.beta_R = 2.1531e-4 * (self.V_rms - 3.725) **2 + 1.5211e-5 + 2.7981e-4 * self.delta_DOD
        
        
        self.history = {
            'V' : [],
            'I' : [],
            'V_cap': [],
            'V_OC' : [],
            'dod' : [],
            't' : [],
            'R0' : [],
            'Rth' : [],
            'P_loss' : [],
            'P' : []
            }
        
        self.history_total = {
            'V' : [],
            'I' : [],
            'V_cap': [],
            'V_OC' : [],
            'dod' : [],
            't' : [],
            'R0' : [],
            'Rth' : [],
            'P_loss' : [],
            'P' : []
            }
        
    
    def update_aging(self, aging_data, day_step):
        # Aging model data
        dod   = np.array(self.history['dod'])
        V_dis = np.array(self.history['V'])
        I_dis = np.array(self.history['I'])
        t_dis = np.array(self.history['t'])/3600
        
        delta_DOD = dod.max() - dod.min()
        V_rms     = np.sqrt((V_dis**2).mean())
        
        T_store   = aging_data['T_store']
        V_store   = V_ocp(dod.min())
        
        n_cycles  = aging_data['Flights per Day'] * day_step * 2
        n_days    = self.days[-1] + day_step

        Q_cycle   = trapezoid(I_dis, t_dis)
        Q_total   = self.Q_through[-1] + n_cycles * Q_cycle

        #Calendar Aging Parameters
        alpha_C = (7.543 * V_store - 23.75)* 1e6 * np.exp(-6976/T_store)
        alpha_R = (5.270 * V_store - 16.32)* 1e5 * np.exp(-5986/T_store)

        #Cycle Aging Parameters
        beta_C = 7.348e-3 * (V_rms - 3.667) **2 + 7.600e-4 + 4.081e-3 * delta_DOD
        beta_R = 2.153e-4 * (V_rms - 3.725) **2 + 1.521e-5 + 2.798e-4 * delta_DOD
        
        
        #Update impedance factors
        E_fade = 1 - alpha_C*(n_days**0.75) - beta_C * np.sqrt(Q_total)
        R_grow = 1 + alpha_R*(n_days**0.75) + beta_R * Q_total
        
        self.Ef_cal.append(-alpha_C*(n_days**0.75))
        self.Ef_cyc.append(-beta_C * np.sqrt(Q_total))
        
        self.Rg_cal.append(alpha_R*(n_days**0.75))
        self.Rg_cyc.append(beta_R * Q_total)
        
        self.E_fade_hist.append(E_fade)
        self.R_grow_hist.append(R_grow)
        self.days.append(day_step + self.days[-1])
        self.cycles.append(n_cycles + self.cycles[-1])
        self.Q_through.append(Q_total)
    
    def run_ODE(self, tspan, P_profile,
                initial_val=None, 
                add_history=False, 
                scheme='RK45',
                degraded=False):
        # Constant power draw
        self.P = P_profile
        self.V = [0,]
        self.I = [0,]
        
        #self.T = [0,]
        
        # Initial conditions are V_cap and DOD
        if initial_val is not None:
            x0 = initial_val
        else:
            x0 = np.array([0,0])
        
        #  Call the solver and store the results in class variables
        self.sol = solve_ivp(self._equations, (tspan[0], tspan[-1]), x0, t_eval = tspan,
                             method=scheme, args=(degraded, ))
        self.t = self.sol.t
        self.V_cap = self.sol.y[0,:]
        self.dod = self.sol.y[1,:]
        #self.T = self.sol.y[2,:]
        
        #  Loop over the times and capacitor voltages and calculate the battery's voltage at each point.
        #  The results are stored in the list V.
        
        self.V = []
        self.I = []
        
        # if degraded:
        #     E_fade   = 1 - self.alpha_C*self.n_days**0.75 - self.beta_C * np.sqrt(self.n_cycles * self.Q_cycle)
        #     R_growth = 1 + self.alpha_R*self.n_days**0.75 + self.beta_R * self.n_cycles * self.Q_cycle
            
        #     print(E_fade, R_growth)
        
        for i, t in enumerate(self.sol.t):
            if i == 0:
                y = fsolve(self._alg_system, [0,0], args = (self.V_cap[i], t, self.dod[i], degraded))
            else:
                y = fsolve(self._alg_system, [self.V[-1], self.I[-1]], args = (self.V_cap[i], t, self.dod[i], degraded))

            self.V.append( y[0] )
            self.I.append( y[1])
            i = i + 1
        
        self.V_OC  = V_ocp(self.dod)
        self.R_0   = R0(self.dod)
        self.R_th  = Rth(self.dod)
        
        self.P_loss = (self.R_0 * np.array(self.I) ** 2) + (self.V_cap **2 / self.R_th )
        
        if add_history:
            self.history['V'] += self.V
            self.history['I'] += self.I
            self.history['V_cap'] += self.V_cap.tolist()
            self.history['V_OC'] += self.V_OC.tolist()
            self.history['dod'] += self.dod.tolist()
            self.history['t'] += self.t.tolist()
            self.history['R0'] += self.R_0.tolist()
            self.history['Rth'] += self.R_th.tolist()
            self.history['P_loss'] += self.P_loss.tolist()
            self.history['P'] += self.P(self.t).tolist()
            #self.history['T'] += self.T.tolist()
    
    def reset_history(self):
        self.history = {
            'V' : [],
            'I' : [],
            'V_cap': [],
            'V_OC' : [],
            'dod' : [],
            't' : [],
            'R0' : [],
            'Rth' : [],
            'P_loss' : [],
            'P' : [],
            #'T' : []
            }
        
        
        
    #  Define the differential equations    
    def _equations(self, t, x, degraded):
            
        V_cap = x[0]
        dod = x[1]
        #T = x[2]
        
        #  At each t, we need to calculate the current based on the constraint equation.
        y = fsolve(self._alg_system, [self.V[-1], self.I[-1]], args = (V_cap, t, dod, degraded))
        
        self.V.append(y[0])
        self.I.append(y[1])
        
        I = y[1]
        
        R1 = Rth(dod)
        C1 = Cth(dod)
        
        Total_cap = self.capacity
        
        #R_0 = R0(dod)
        if degraded:
            R1 *= self.R_grow_hist[-1]
            C1 *= self.E_fade_hist[-1]
            Total_cap *= self.E_fade_hist[-1]
            
            
        
        #Q_loss = R_0 * (I ** 2) + (V_cap ** 2)/R1
        
        return( [- V_cap / (R1 * C1) + I / C1,
            I  / 3600 / Total_cap,
            #Q_loss/(self.mass * self.heat_capacity)
            ] )

    def _alg_system(self, x, V_cap, t, dod, degraded):
            
        res = np.zeros(2)
            
        V  = x[0]
        I  = x[1]
        
        U_ocp = V_ocp(dod)
        R_0 = R0(dod)
        
        if degraded:
            R_0 *= self.R_grow_hist[-1]
      
        
        res[0] = -V +  U_ocp - V_cap - I * R_0
        res[1] = I * V - self.P(t)
        return res

class Battery_Pack:
    
    def __init__(self, en_density, cell_capacity, 
                 nom_tension, sys_tension, aging_data):
        # Data of the battery pack
        self.cell_capacity              = cell_capacity # Ah
        self.sys_tension                = sys_tension   # V
        self.cell_nominal_tension       = nom_tension   # V
        self.en_density                 = en_density    # Wh/kg
        #self.cell_heat_capacity         = cell_heat_capacity #J/(Kg K)
        
        # Connections
        self.N_series   = ceil(sys_tension/nom_tension)
        self.N_bank     = 0
        self.mass       = 0 # kg
        
        # Aging
        self.aging_data = aging_data
        
        self.cell       = battery_cell_ODE(self.en_density, 
                                           self.cell_capacity, 
                                           self.cell_nominal_tension,
                                           self.aging_data,
                                           #self.cell_heat_capacity
                                           )
        
        self.cell_mass  = self.cell.mass
        
        
        
        # Output Data
        self.t = []
        self.V = []
        self.I = []
        
        self.t   = None
        self.eff = None
        
        self.eff_fun = None
        #self.T_batt = []
        
        
    def size(self, target_dod, max_capacity, P_points, t_points, 
             dod_begin=0, verbose=False):
        
        self.cell.reset_history()
        
        k = 1.5

        k_b = 1
        k_t = 2
        
        dod_end = 0
        
        i = 0
        
        #for k in np.linspace(1.2,3,10):
        while abs(dod_end - target_dod) > 0.01:
            
            N_bank  = ceil(max_capacity * k / self.cell_capacity)
            
            P_cell = np.array(P_points) / (self.N_series * N_bank)
            dt = np.array(t_points) - t_points[0]
            p_profile = PchipInterpolator(dt, P_cell)
            
            if dod_begin > 0:
                x0 = np.array([0, dod_begin])
            else:
                x0 = None
            
            #  Define our time span and run the simulation
            # tspan = np.linspace(dt[0], dt[-1], 100) 
            self.cell.reset_history()
            
            self.cell.run_ODE(t_points, p_profile, add_history=True, 
                              scheme='RK45', initial_val=x0)
            
            dod_end = self.cell.dod[-1]
            
            if i < 2:
                if  (dod_end- target_dod) > 0:
                    k_b = k
                else:
                    k_t = k
                    
                k = 0.5 * (k_t + k_b)
            
            # # if np.array(self.cell.history['V']).min() < 2.7:
            # #     self.N_series = ceil(self.N_series*1.05)
            # #     print(self.N_series)
            else:
                #alpha = 0.8*np.exp(- i / 10)
                k = k - (target_dod - dod_end)*0.4
                
            # Smoothing
            #k = k * (1-alpha) + k_new * alpha
            if verbose:
                print(f'k :{k:.3f}, dod {dod_end:.4f}, error {(dod_end - target_dod):.4f}')
            #print(f'k :{k:.3f}, dod {dod_end:.4f}')
            
            i += 1
            
            if i > 10 and (dod_end - target_dod) < 0:
                break
        
        
        
        self.N_bank = N_bank
        self.mass = 1.25 * self.cell.mass * self.N_series * N_bank
        
        self.pack_nom_tension = self.cell_nominal_tension * self.N_series
        self.pack_capacity    = self.cell_capacity * self.N_bank
        
        self.DOD = np.array(self.cell.history['dod']) 
        
        self.V    = np.array(self.cell.history['V']) * self.N_series
        self.V_OC = np.array(self.cell.history['V_OC']) * self.N_series
        
        self.I = np.array(self.cell.history['I']) * self.N_bank
        self.t = np.array(self.cell.history['t'])
        #self.eff = np.clip(p_profile(dt).round(5) / (np.array(self.cell.history['I']) * np.array(self.cell.history['V_OC'])), 0, 1)
        
        self.P_loss = np.array(self.cell.history['P_loss']) * (self.N_series * self.N_bank)
        self.P_batt = (self.V * self.I).round(5)
        self.eff = np.nan_to_num((self.P_batt / (self.P_batt + self.P_loss)))

        self.eff_fun = PchipInterpolator(t_points, self.eff)
        

        self.aging_data['Delta_DOD'] = dod_end - dod_begin
        self.aging_data['V_rms']     = np.sqrt((np.array(self.cell.history['V'])**2).mean())
        self.aging_data['Discharge per Cycle'] = max_capacity / N_bank
        self.pack_cycle_discharge = max_capacity
        
        #self.cell.update_aging(self.aging_data)

        
        #self.T_batt = self.cell.history['T']
        
    def calculate(self, P_pts, t_pts, n_step=100, dod_begin=0):
        assert(self.N_bank > 0)
        
        self.cell.reset_history()
        
        P_cell = P_pts / (self.N_series * self.N_bank)
        
        p_profile = PchipInterpolator(t_pts, P_cell)
        #dt = np.linspace(t_pts[0], t_pts[-1], n_step)
        
        if dod_begin > 0:
            x0 = np.array([0, dod_begin])
        else:
            x0 = None
        
        
        self.cell.run_ODE(t_pts, p_profile, add_history=True, initial_val=x0)
        self.DOD = np.array(self.cell.history['dod'])
        
        self.V    = np.array(self.cell.history['V']) * self.N_series
        self.V_OC = np.array(self.cell.history['V_OC']) * self.N_series
        
        self.I = np.array(self.cell.history['I']) * self.N_bank
        self.t = np.array(self.cell.history['t'])
        
        
        self.P_loss = np.array(self.cell.history['P_loss']) * (self.N_series * self.N_bank)
        self.P_batt = (self.V * self.I).round(5)
        self.eff = np.nan_to_num((self.P_batt / (self.P_batt + self.P_loss)))
        self.eff_fun = PchipInterpolator(self.t, self.eff)
        
        self.P_loss = np.array(self.cell.history['P_loss']) * (self.N_series * self.N_bank)
        
    def calculate_degraded(self, P_pts, t_pts, dod_begin=0):
        assert(self.N_bank > 0)
        
        #cycle_stepping = np.arange(0, days, day_step)
        
        #for day in cycle_stepping:
        self.cell.reset_history()
    
        P_cell = P_pts / (self.N_series * self.N_bank)
        
        p_profile = PchipInterpolator(t_pts, P_cell)
        #dt = np.linspace(t_pts[0], t_pts[-1], n_step)
        
        if dod_begin > 0:
            x0 = np.array([0, dod_begin])
        else:
            x0 = None
    
        self.cell.run_ODE(t_pts, p_profile, add_history=True, 
                              scheme='RK45', initial_val=x0, degraded=True)
        
        self.DOD = np.array(self.cell.history['dod'])
        
        self.V    = np.array(self.cell.history['V']) * self.N_series
        self.V_OC = np.array(self.cell.history['V_OC']) * self.N_series
        
        self.I = np.array(self.cell.history['I']) * self.N_bank
        self.t = np.array(self.cell.history['t'])
        
        
        self.P_loss = np.array(self.cell.history['P_loss']) * (self.N_series * self.N_bank)
        self.P_batt = (self.V * self.I).round(5)
        self.eff = np.nan_to_num((self.P_batt / (self.P_batt + self.P_loss)))
        self.eff_fun = PchipInterpolator(self.t, self.eff)
        
        self.P_loss = np.array(self.cell.history['P_loss']) * (self.N_series * self.N_bank)
        
    def update_aging(self, day_step):
        self.cell.update_aging(self.aging_data, day_step)
        
