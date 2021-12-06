# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 11:07:10 2021

@author: stijn.overmeen
"""

'''
Discharge q is known
Velocity v is a maximum limit
Diameter D is computed as: D=2*sqrt((pi*Q)/V)
Next up, it is checked whether this diameter does not lead to a too large of a hydraulic gradient S
We use Colebrook-White equation for this, with the following variable settings:
    k=0.003 (assumed from Rioned)
    g=9.81
    v=1.007 × 10^-6 (kinematic viscoisty of water at 20 degrees Celcius)

If S_calc (colebrook_white) > S_max with max v, redefine D and calculate again.

Possible diameters are: 250,315,400,500,600,700,etc..
'''
import numpy as np

#user-defined variables:
Q=0.025                 #known discharge [m3/s]
V_MAX=0.5               #initial max velocity [m/s]
S_MAX=1/400             #max hydraulic gradient [-]
D_OPTIONS=[0.25,0.315,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0] #diameter [m]

def initial_values():
    q=Q                 #discharge [m3/s]
    vmax=V_MAX          #initial max velocity [m/s]
    Smax=S_MAX          #max hydraulic gradient [-]
    k=0.003             #assumption from Rioned
    g=9.81              #gravitational acceleration [m/s2]
    vi=1.007*10**-6     #kinematic viscosity [m2/s]

    return q,vmax,Smax,k,g,vi

def calc_D(q,vmax):
    D=2*np.sqrt((np.pi*q)/vmax)
    
    return D

def calc_vmax(q,D):
    vmax=(np.pi*q)/(D/2)**2
    
    return vmax

def find_diameter(D):
    temp=[]
    for d in D_OPTIONS:
        if d<D:
            continue
        else:
            temp.append(d) #temp list, for in case D_OPTIONS is not in ascending order
    if temp:
        D=min(temp)
    else:
        raise Exception('Diameter found is bigger than all the pre-defined possibilities!')

    return D

def increase_diameter(D):
    temp=[]
    for d in D_OPTIONS:
        if d>D:
            temp.append(d) #temp list, for in case D_OPTIONS is not in ascending order
        else:
            continue
    if temp:
        D=min(temp)
    else:
        raise Exception('Cannot increase diameter anymore!')
    
    return D

def colebrook_white(g,D,k,vi,vmax):
    #vcalc=(-2*np.sqrt(2*g*D*Smax))*np.log((k/(3.7*D))+((2.5*vi)/(D*np.sqrt(2*g*D*Smax))))
    #isolation of S found at https://civilweb-spreadsheets.com/drainage-design-spreadsheets/pipe-flow-calculator/colebrook-white-equation/    
    Scalc=vmax**2/(8*g*D*(np.log10((k/(3.7*D))+((6.28*vi)/(vmax*D))**0.89))**2)
        
    return Scalc

if __name__ == "__main__":
    q,vmax,Smax,k,g,vi=initial_values()
    D=calc_D(q,vmax)
    print('Initial calculated diameter = 'f"{D*1000:.0f}"' mm.')
    D=find_diameter(D)
    print('Closest avalaible diameter = 'f"{D*1000:.0f}"' mm.')
    Scalc=colebrook_white(g,D,k,vi,vmax)
    response=''
    while response!='break':
        if Scalc>Smax:
            print('Diameter 'f"{D*1000:.0f}"' mm is too small.')
            print('Hydraulic gradient = 'f"{Scalc:.4f}"', while max = 'f"{Smax:.4f}"'.')
            print('Increasing diameter and recalculating vmax...')
            D=increase_diameter(D)
            print('');print('Trying again with D = 'f"{D*1000:.0f}"' mm.')
            vmax=calc_vmax(q,D)
            Scalc=colebrook_white(g,D,k,vi,vmax)
        else:
            print('Optimal diameter found: 'f"{D*1000:.0f}"' mm.')
            print('Hydraulic gradient = 'f"{Scalc:.4f}"', while max = 'f"{Smax:.4f}"'.')
            response='break'

  