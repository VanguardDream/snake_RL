# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : BRM snake robot python simulation script

from time import sleep
from Cython.Shadow import NULL
from numpy.core.fromnumeric import reshape, shape
import mujoco_py
import os
import math
import random
import numpy as np
import datetime

def radtodeg(rad):
    return rad * 180/math.pi

def degtorad(deg):
    return deg * math.pi/180

def getNumofSlot(gait_type):
    if gait_type == 0: #Vertical
        return int(8)
    elif gait_type == 1: #Sinuous
        return int(15)
    else: # For now sidewind
        return int(15)

def randomize_param():
    global l_amp
    global l_phase
    global d_amp
    global d_phase
    global tau

    l_amp = random.randint(0, 900) / 10
    l_phase = random.randint(0,3600) / 10
    d_amp = random.randint(0, 900) / 10
    d_phase = random.randint(0,3600) / 10
    tau = random.randint(1,20)


#load model from path
snake = mujoco_py.load_model_from_path("../description/mujoco/snake_allign.xml")

#Gait parameters 37.9, 269.6,
d_amp = 57.8; # dorsal amplitude
d_phase = 284.2; # dorsal phase
l_amp = 9.6; # lateral amplitude
l_phase = 324.8; # lateral phase

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

m_sinuous = np.eye(15)

m_sidewind = np.array([[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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

# m_sidewind = np.array([[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                         [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
#                         [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0],
#                         [0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],
#                         [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
#                         [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
#                         [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0],
#                         [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
#                         [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
#                         [0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0],
#                         [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
#                         [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
#                         [0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0],
#                         [0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1], 
#                         [0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0]
#                         ],dtype='float')

def getMotionCol(gait,i):
    if gait == 0:
        return m_vertical[:,i].reshape(m_vertical.shape[0],1)
    elif gait == 1:
        return m_sinuous[:,i].reshape(m_sinuous.shape[0],1)
    else:
        return m_sidewind[:,i].reshape(m_sidewind.shape[0],1)


#Joint angle function
# def P_vertical(slot):
#     return np.array([[d_amp * math.sin((2 * math.pi / 8) * slot + degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8) * slot + 3 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8) * slot + 5 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8) * slot + 7 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8) * slot + 9 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8) * slot + 11 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8) * slot + 13 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8) * slot + 15 * degtorad(d_amp))]
#                     ], dtype='float')

def P_vertical(slot):    #20210715 P함수 변형 테스트
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
                        ],dtype='float')

def P_sinuous(slot): #Original P
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
                        ],dtype='float')

# def P_sinuous(slot): # Original P - side - P함수 변형 테스트 20210728
#     return np.array([[d_amp * math.sin((2 * math.pi / 8) * slot + 0.5 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 0 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 1.5 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 1 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 2.5 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 2 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 3.5 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 3 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 4.5 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 4 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 5.5 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 5 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 6.5 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 6 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 7.5 * degtorad(d_amp))],
#                         ],dtype='float')

def P_sidewind(slot): # Original P side
    return np.array([[d_amp * math.sin((2 * math.pi / 8) * slot + 0.5 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 0 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 1.5 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 1 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 2.5 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 2 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 3.5 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 3 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 4.5 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 4 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 5.5 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 5 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 6.5 * degtorad(d_amp))],
                        [l_amp * math.sin((math.pi / 8) * slot + 6 * degtorad(l_amp))],
                        [d_amp * math.sin((2 * math.pi / 8) * slot + 7.5 * degtorad(d_amp))],
                        ],dtype='float')

# def P_sidewind(slot):    #20210715 P함수 변형 테스트
#     return np.array([[d_amp * math.sin((2 * math.pi / 8) * slot + 0 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 1.5 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 2 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 2.5 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 4 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 3.5 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 6 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 4.5 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 8 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 5.5 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 10 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 6.5 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 12 * degtorad(d_amp))],
#                         [l_amp * math.sin((math.pi / 8) * slot + 7.5 * degtorad(l_amp))],
#                         [d_amp * math.sin((2 * math.pi / 8) * slot + 14 * degtorad(d_amp))],
#                         ],dtype='float')

def calculte_P(gait, slot):
    if gait == 0: #Vertical
        return P_vertical(slot)

    elif gait == 1: # Sinuous
        return P_sinuous(slot)
    else :
        return P_sidewind(slot)

# snake = mujoco_py.load_model_from_xml(snake_pipe)
simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

# Select gait if we select vertical -> gait slot is 8.
t = 0
k = 0
tau = 3 # time coefficient larger -> slower motion 0 < tau < inf
gait = 1 # Vertical -> 0, Sinuous -> 1, Sidewind -> 2

# Variable for cost(loss) function
delta_x = 0
delta_y = 0
accum_theta = 0

# Simulation model info
joint_names = simulator.model.joint_names[1:]

t_before = datetime.datetime.now()

while True:
   

    P = calculte_P(gait,float(k)/10)
    # if(k % getNumofSlot(gait) == 0): # Very first of gait step.
    #     P = calculte_P(gait,k/10) # Calculate joint angles for this gait stride.

    m_k = getMotionCol(gait,(k%getNumofSlot(gait))).T
    g = np.round(np.diagonal((np.dot(P,m_k))),decimals=2).reshape((15,1)).flatten()

    spec_motor = []
    ### Control specificated motor by M matrix.
    spec_motor = np.nonzero(g)

    # For just debugging
    # os.system('clear')
    # print(g)
    # print(spec_motor[0])
    # print(type(spec_motor))
    # sleep(0.8)

    for idx in spec_motor:
        # Commnad motor here
        if not(len(idx) == 0):
            simulator.data.ctrl[idx] = degtorad(g[idx])
        
    # for motor_idx in range(15):
    #         simulator.data.ctrl[motor_idx] = round(degtorad(G[motor_idx].item()),4)
            
    #Accumulate joint angular displacement
    for name in joint_names:
        accum_theta = accum_theta + abs(simulator.data.get_joint_qpos(name))

    simulator.step()
    sim_viewer.render()

    if t%tau == 0:
        k = k + 1

    if(t%1000 == 0):
        # print("Accumulated joint displacement. :  %f" %accum_theta)
        # print("dX : %lf, dY : %lf" %(simulator.data.get_body_xpos('head')[0],simulator.data.get_body_xpos('head')[1]))
        pass

    if(t%5000 == 0):
        #save sim data
        delta_x = simulator.data.get_body_xpos('head')[0]
        delta_y = simulator.data.get_body_xpos('head')[1]
        accum_theta

        #Calculate Cost here
        J = 10 * delta_x - 5 * delta_y - 0.0003 * accum_theta
        # print("Loss is : %lf" %J)
        print(J)

        simulator.reset()
        
        t = 0
        k = 0

        delta_x = 0
        delta_y = 0
        accum_theta = 0

        t_after = datetime.datetime.now()
        print('excution time : ')
        print(t_after - t_before)

        t_before = t_after

    if t > 100 and os.getenv('TESTING') is not None:
        break

    t = t + 1
