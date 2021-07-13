# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : BRM snake robot gait class

import math
import numpy as np

class gait:
    def __init__(self, gait,d_amp = 30, d_phase = 150, l_amp = 30, l_phase = 150, tau = 1):
        #Gait selection
        self.gait = gait
        
        #Gait parameters
        self.l_amp = l_amp; # lateral amplitude
        self.l_phase = l_phase; # lateral phase
        self.d_amp = d_amp; # dorsal amplitude
        self.d_phase = d_phase; # dorsal phase
        self.tau = tau; #time coefficient

        #Gait motion matirces
        self.m_vertical = np.array([[1,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0],
                                [0,1,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0],
                                [0,0,1,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0],
                                [0,0,0,1,0,0,0,0],
                                [0,0,0,0,0,0,0,0],
                                [0,0,0,0,1,0,0,0],
                                [0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,1,0,0],
                                [0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,1,0],
                                [0,0,0,0,0,0,0,0], 
                                [0,0,0,0,0,0,0,1],
                                [0,0,0,0,0,0,0,0]],dtype='float')

        self.m_sinuous = np.eye(15)

        self.m_sidewind = np.array([[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                                [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                                [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1], 
                                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
                                ],dtype='float')

    def radtodeg(self, rad):
        return rad * 180/math.pi

    def degtorad(self, deg):
        return deg * math.pi/180

    def getNumofSlot(self,gait_type):
        if gait_type == 0: #Vertical
            return int(8)
        elif gait_type == 1: #Sinuous
            return int(15)
        else: # For now sidewind
            return int(15)

    def P_vertical(self,slot):
        return np.array([[self.d_amp * math.sin((2 * math.pi / 8) * slot + self.degtorad(self.d_amp))],
                        [0],
                        [self.d_amp * math.sin((2 * math.pi / 8) * slot + 3 * self.degtorad(self.d_amp))],
                        [0],
                        [self.d_amp * math.sin((2 * math.pi / 8) * slot + 5 * self.degtorad(self.d_amp))],
                        [0],
                        [self.d_amp * math.sin((2 * math.pi / 8) * slot + 7 * self.degtorad(self.d_amp))],
                        [0],
                        [self.d_amp * math.sin((2 * math.pi / 8) * slot + 9 * self.degtorad(self.d_amp))],
                        [0],
                        [self.d_amp * math.sin((2 * math.pi / 8) * slot + 11 * self.degtorad(self.d_amp))],
                        [0],
                        [self.d_amp * math.sin((2 * math.pi / 8) * slot + 13 * self.degtorad(self.d_amp))],
                        [0],
                        [self.d_amp * math.sin((2 * math.pi / 8) * slot + 15 * self.degtorad(self.d_amp))]
                        ], dtype='float')

    def P_sinuous(self,slot):
        return np.array([[self.d_amp * math.sin((2 * math.pi / 8) * slot + 0 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 1.5 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 2 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 2.5 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 4 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 3.5 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 6 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 4.5 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 8 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 5.5 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 10 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 6.5 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 12 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 7.5 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 14 * self.degtorad(self.d_amp))],
                            ],dtype='float')
                        
    def P_sidewind(self,slot):
        return np.array([[self.d_amp * math.sin((2 * math.pi / 8) * slot + 0.5 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 0 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 1.5 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 1 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 2.5 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 2 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 3.5 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 3 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 4.5 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 4 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 5.5 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 5 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 6.5 * self.degtorad(self.d_amp))],
                            [self.l_amp * math.sin((math.pi / 8) * slot + 6 * self.degtorad(self.l_amp))],
                            [self.d_amp * math.sin((2 * math.pi / 8) * slot + 7.5 * self.degtorad(self.d_amp))],
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

    def generate(self, i):

        k = math.floor(i/self.tau)
        P = self.calculate_P(float(k)/10) # Calculate joint angles for this gait stride.

        m_k = self.getMotionCol((k%self.getNumofSlot(self.gait))).T # Get motion vector for motor selection.

        g = np.round(np.diagonal((np.dot(P,m_k))),decimals=2).reshape((15,1))

        ### Control specificated motor by M matrix.
        return g