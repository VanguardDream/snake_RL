# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : BRM snake robot python simulation script

from numpy.core.fromnumeric import reshape, shape
import os
import math
import numpy as np
import time

def radtodeg(rad):
    return rad * 180/math.pi

def degtorad(deg):
    return deg * math.pi/180

def getNumofSlot(gait_type):
    if gait_type == 0: #Vertical
        return int(8)
    elif gait_type == 1: #Sinuous
        return int(16)
    else: # For now sidewind
        return int(16)

#Gait parameters
l_amp = 30; # lateral amplitude
l_phase = 150; # lateral phase
d_amp = 30; # dorsal amplitude
d_phase = 150; # dorsal phase

#Gait motion matirces
m_vertical = np.array([[1,0,0,0,0,0,0,0],
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

m_sinuous = np.eye(16)

m_sidewind = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],dtype='float')

def getMotionCol(gait,i):
    if gait == 0:
        return m_vertical[:,i].reshape(m_vertical.shape[0],1)
    elif gait == 1:
        return m_sinuous[:,i].reshape(m_sinuous.shape[0],1)
    else:
        return m_sidewind[:,i].reshape(m_sidewind.shape[0],1)


#Joint angle function
def P_vertical(slot):
    return np.array([[d_amp * math.sin((2 * math.pi / 8) * slot + degtorad(d_amp))],
                    [0],
                    [d_amp * math.sin((2 * math.pi / 8) * slot + 3 * degtorad(d_amp))],
                    [0],
                    [d_amp * math.sin((2 * math.pi / 8) * slot + 5 * degtorad(d_amp))],
                    [0],
                    [d_amp * math.sin((2 * math.pi / 8) * slot + 7 * degtorad(d_amp))],
                    [0],
                    [d_amp * math.sin((2 * math.pi / 8) * slot + 9 * degtorad(d_amp))],
                    [0],
                    [d_amp * math.sin((2 * math.pi / 8) * slot + 11 * degtorad(d_amp))],
                    [0],
                    [d_amp * math.sin((2 * math.pi / 8) * slot + 13 * degtorad(d_amp))],
                    [0],
                    [d_amp * math.sin((2 * math.pi / 8) * slot + 15 * degtorad(d_amp))],
                    [0]], dtype='float')

def P_sinuous(slot):
    return np.array([[d_amp * math.sin((2 * math.pi / 8) * slot + 0 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 1.5 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 2 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 2.5 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 4 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 3.5 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 6 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 4.5 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 8 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 5.5 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 10 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 6.5 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 12 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 7.5 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 14 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 8.5 * degtorad(l_amp))],
                        ],dtype='float')
                        


def calculte_P(gait, slot):
    if gait == 0: #Vertical
        return P_vertical(slot)

    elif gait == 1: # Sinuous
        return P_sinuous(slot)
    else :
        return 0

# Select gait if we select vertical -> gait slot is 8.
t = 0
k = 0
tau = 1 # time coefficient larger -> slower motion 0 < tau < inf
gait = 1 # Vertical -> 0, Sinuous -> 1, Sidewind -> 2

while True:
   
    P = P_vertical(float(k)/10)
    if(k % getNumofSlot(gait) == 0): # Very first of gait step.
        P = calculte_P(gait,k/10) # Calculate joint angles for this gait stride.


    m_k = getMotionCol(gait,(k%getNumofSlot(gait))).T
    g = np.round(np.diagonal((np.dot(P,m_k))),decimals=2).reshape((16,1))

    print(m_k)

    ### Control specificated motor by M matrix.
    spec_motor = np.nonzero(g)

    for idx in spec_motor:
        # Commnad motor here
        k = k 

    # print(degtorad(G[0].item()))
    time.sleep(0.75)

    t = t + 1
    k = (k + 1)