# © 2022 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Date : 2022-01-04 (YYYYMMDD)
# Description : Gait class for snake RL jupyter notebook this gait code is forked from "Gait-lambda.py" on 4th Jan. 

import math
import numpy as np

class gait:
    def __init__(self, gait,d_amp = 30, d_phase = 150, d_lam = 1,l_amp = 30, l_phase = 150, l_lam = 1, tau = 1):
        #Gait selection
        self.gait = gait
        
        #Gait parameters
        self.d_amp = d_amp # dorsal amplitude
        self.d_phase = d_phase # dorsal phase
        self.d_lam = d_lam

        self.l_amp = l_amp # lateral amplitude
        self.l_phase = l_phase # lateral phase
        self.l_lam = l_lam
        self.tau = int(tau); #time coefficient

        #Gait motion matirces
        self.m_vertical = np.array([[1,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,0],
                                    [0,1,0,0,0,0,0],
                                    [0,0,0,0,0,0,0],
                                    [0,0,1,0,0,0,0],
                                    [0,0,0,0,0,0,0],
                                    [0,0,0,1,0,0,0],
                                    [0,0,0,0,0,0,0],
                                    [0,0,0,0,1,0,0],
                                    [0,0,0,0,0,0,0],
                                    [0,0,0,0,0,1,0],
                                    [0,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,1],
                                    [0,0,0,0,0,0,0]],dtype='int')

        self.m_sinuous = np.eye(14)

        self.m_sidewind = np.array([[0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                                    [0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                                    [0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                                    [0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                                    [0,0,0,0,0,0,0,0,0,0,0,0,1,0]],dtype='int')

    def setParams(self, gait = 1,d_amp = 30, d_phase = 150, d_lam = 1,l_amp = 30, l_phase = 150, l_lam = 1, tau = 1):
        self.gait = gait
        self.d_amp = d_amp
        self.d_phase = d_phase
        self.d_lam = d_lam
        self.l_amp = l_amp
        self.l_phase = l_phase
        self.l_lam = l_lam
        self.tau = tau

    def radtodeg(self, rad):
        return rad * 180/math.pi

    def degtorad(self, deg):
        return deg * math.pi/180

    def getNumofSlot(self,gait_type):
        if gait_type == 0: #Vertical
            return int(7)
        elif gait_type == 1: #Sinuous
            return int(14)
        else: # For now sidewind
            return int(14)

    def P_vertical(self, slot): 
        return np.array([[self.d_amp * math.sin((2 * math.pi / 8) * slot + self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 1 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 2 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 2 * self.l_lam  * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 3 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 3 * self.l_lam  * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 4 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 4 * self.l_lam  * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 5 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 5 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 6 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 6 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 7 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 7 * self.l_lam * self.degtorad(self.l_phase))]
                            ],dtype='float')

    def P_sinuous(self,slot):
        return np.array([[self.d_amp * math.sin((2 * math.pi / 8) * slot + self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 1 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 2 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 2 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 3 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 3 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 4 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 4 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 5 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 5 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 6 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 6 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 7 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 7 * self.l_lam * self.degtorad(self.l_phase))]
                            ],dtype='float')

    def P_sidewind(self,slot): 
        return np.array([[self.d_amp * math.cos(slot + 1 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.cos(slot + 1 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.cos(slot + 2 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.cos(slot + 2 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.cos(slot + 3 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.cos(slot + 3 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.cos(slot + 4 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.cos(slot + 4 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.cos(slot + 5 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.cos(slot + 5 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.cos(slot + 6 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.cos(slot + 6 * self.l_lam * self.degtorad(self.l_phase))],
                            [self.d_amp * math.cos(slot + 7 * self.d_lam * self.degtorad(self.d_phase))],
                            [self.l_amp * math.cos(slot + 7 * self.l_lam * self.degtorad(self.l_phase))]
                            ],dtype='float')

    
    def calculate_P(self, slot):
        if self.gait == 0: #Vertical
            return self.P_vertical(slot)

        elif self.gait == 1: # Sinuous
            return self.P_sinuous(slot)

        else :
            return self.P_sidewind(slot)

    def getMotionCol(self,i):
        if self.gait == 0:
            return self.m_vertical[:,i].reshape(self.m_vertical.shape[0],1)
        elif self.gait == 1:
            return self.m_sinuous[:,i].reshape(self.m_sinuous.shape[0],1)
        else:
            return self.m_sidewind[:,i].reshape(self.m_sidewind.shape[0],1)

    def generate(self, i) -> np.ndarray:

        k = math.floor(i/self.tau)
        P = self.calculate_P(float(k)/10) # Calculate joint angles for this gait stride.

        m_k = self.getMotionCol((k%self.getNumofSlot(self.gait))).T # Get motion vector for motor selection.

        g = np.round(np.diagonal((np.dot(P,m_k))),decimals=2).reshape((14,1))

        ### Control specificated motor by M matrix.
        return g