# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 15:21:09 2021

@author: stijn.overmeen
"""

'''
Check rewritten formula of colebrook_white
'''

import numpy as np

#user-defined variables:
Q=0.025                                      #known discharge [m3/s]
V_MAX_OPTIONS=[0.1,0.5,1,1.5]                #initial max velocity [m/s]
D_OPTIONS=[0.25,0.315,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0] #diameter [m]

def initial_values():
    q=Q                 #discharge [m3/s]
    vmax=V_MAX          #initial max velocity [m/s]
    k=0.003             #assumption from Rioned
    g=9.81              #gravitational acceleration [m/s2]
    vi=1.007*(10**-6)     #kinematic viscosity [m2/s]

    return q,vmax,k,g,vi

def s(g,D,k,vi,vmax):
    #isolation of S found at https://civilweb-spreadsheets.com/drainage-design-spreadsheets/pipe-flow-calculator/colebrook-white-equation/    
    Scalc=vmax**2/(8*g*D*(np.log10((k/(3.7*D))+((6.28*vi)/(vmax*D))**0.89))**2)
    
    return Scalc
    
def v(g,D,k,vi,Scalc):
    vcalc=-2*np.sqrt(2*g*D*Scalc)*np.log10((k/(3.7*D))+((2.5*vi)/(D*np.sqrt(2*g*D*Scalc))))
    
    return vcalc

if __name__ == "__main__":
    for V_MAX in V_MAX_OPTIONS:
        q,vmax,k,g,vi=initial_values()
        list_of_velocities=[];list_of_errors=[]
        for D in D_OPTIONS:
            Scalc=s(g,D,k,vi,vmax)
            vcalc=v(g,D,k,vi,Scalc)
            error=((vcalc-V_MAX)/V_MAX)*100
            list_of_velocities.append(vcalc);list_of_errors.append(error);
            print('v_max = 'f"{V_MAX}"' and v_calc = 'f"{vcalc:.4f}"'. Error is 'f"{error:.4f}"' %')         