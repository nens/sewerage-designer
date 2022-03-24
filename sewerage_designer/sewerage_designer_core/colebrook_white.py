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

from bisect import bisect_left, bisect_right
import math
from .constants import *

#user-defined variables:
D_OPTIONS=[0.25,0.315,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0] #diameter [m]
D_OPTIONS_INFILTRATIE = [0.4,0.6,0.8,1.2]

# constants
K=0.003             #assumption from Rioned
G=9.81              #gravitational acceleration [m/s2]
VI=1.007*10**-6     #kinematic viscosity [m2/s]

class ColebrookWhite:
    
    def __init__(self, q, Smax, sewerage_type, v_max):
        self.q=q                 #discharge [m3/s]
        self.vmax=v_max #initial max velocity [m/s]
        self.Smax=Smax          #max hydraulic gradient [-]

        # Options for diameters are dependent on the sewerage type
        if sewerage_type == INFILTRATIEVOORZIENING:
            self.d_options = D_OPTIONS_INFILTRATIE
        else:
            self.d_options = D_OPTIONS
        
        
        # Define initial diameter
        self.D_precise = self.calculate_diameter()        
        self.D_design = self.find_closest_diameter(self.D_precise)
        
        
    def calculate_diameter(self):        
        D=2*math.sqrt((self.q)/(self.vmax*math.pi))
        return D

    def find_closest_diameter(self, diameter):
        pos = bisect_left(self.d_options, diameter)
        if pos == 0:
            return self.d_options[0]
        if pos == len(self.d_options):
            return self.d_options[-1]
        before = self.d_options[pos - 1]
        after = self.d_options[pos]
        if after - diameter < diameter - before:
            return after
        else:
            return before    
            
    def calc_vmax(self):
        vmax=self.q/(math.pi*(self.D_design/2)**2)
        return vmax
    
    def increase_diameter(self):
        self.D_design = self.d_options[bisect_right(self.d_options, self.D_design)]
        
    def colebrook_white(self):
        #vcalc=(-2*np.sqrt(2*g*D*Smax))*np.log((k/(3.7*D))+((2.5*vi)/(D*np.sqrt(2*g*D*Smax))))
        #isolation of S found at https://civilweb-spreadsheets.com/drainage-design-spreadsheets/pipe-flow-calculator/colebrook-white-equation/    
        Scalc=self.vmax**2/(8*G*self.D_design*(math.log10((K/(3.7*self.D_design))+((6.28*VI)/(self.vmax*self.D_design))**0.89))**2)  
        return Scalc
    
    def iterate_diameters(self):
        print('intial velocity='f"{self.vmax}")
        print('q='f"{self.q}")
        print('first guess D='f"{self.D_precise}")
        print('D_design='f"{self.D_design}")
        self.vmax = self.calc_vmax() #compute vmax corresponding to D_design before computing Scalc
        print('calc_vmax='f"{self.vmax}")
        Scalc = self.colebrook_white()
        print('Scalc='f"{Scalc}")
        
        while Scalc > self.Smax and self.D_design != self.d_options[-1]:
            print('Scalc='f"{Scalc}")
            print('Smax='f"{self.Smax}")
            self.increase_diameter()
            print('increase_diameter:D_design='f"{self.D_design}")
            self.vmax = self.calc_vmax()
            print('calc_vmax='f"{self.vmax}")
            Scalc = self.colebrook_white()
            print('colebrook_white_Scalc='f"{Scalc}")

        return self.D_design,self.vmax

        
