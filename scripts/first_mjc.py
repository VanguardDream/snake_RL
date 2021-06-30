# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : BRM snake robot python simulation script

from numpy.core.fromnumeric import reshape, shape
import mujoco_py
import os
import math
import numpy as np

def radtodeg(rad):
    return rad * 180/math.pi

def degtorad(deg):
    return deg * math.pi/180

snake_xml = """

<mujoco model="snake_v210623">

    <compiler inertiafromgeom="true" angle="degree"/>

    <option timestep="0.005" iterations="50" tolerance="1e-10" solver="Newton" jacobian="dense" cone="pyramidal"/>

    <size nconmax="500" njmax="2000" nstack="10000"/>

    <visual>
        <map force="0.1" zfar="30"/>
        <rgba haze="0.15 0.25 0.35 1"/>
        <quality shadowsize="2048"/>
        <global offwidth="800" offheight="800"/>
    </visual>

    <asset>
        <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="512"/> 

        <texture name="texplane" type="2d" builtin="checker" rgb1=".2 .3 .4" rgb2=".1 0.15 0.2" width="512" height="512" mark="cross" markrgb=".8 .8 .8"/>  

        <texture name="texgeom" type="cube" builtin="flat" mark="cross" width="127" height="1278" 
            rgb1="0.8 0.6 0.4" rgb2="0.8 0.6 0.4" markrgb="1 1 1" random="0.01"/>  

        <material name="matplane" reflectance="0.3" texture="texplane" texrepeat="1 1" texuniform="true"/>

        <material name="matgeom" texture="texgeom" texuniform="true" rgba="0.8 0.6 .4 1"/>
    </asset>

    <worldbody>

        <geom name="floor" pos="0 0 0" size="0 0 .25" type="plane" material="matplane" condim="3"/>

        <light directional="false" diffuse=".2 .2 .2" specular="0 0 0" pos="0 0 5" dir="0 0 -1" castshadow="false"/>

        <body name="head" pos="0 0 0.1">
            <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
            <freejoint name="root"/>
            <geom size="0.02325 0.017 0.01425" type="box" />
            <body name="body1" pos="-0.012 0 0">
                <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                <joint name="joint1" type="hinge" pos="0 0 0" axis="0 1 0" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                <geom size="0.02325 0.01425 0.017" pos="-0.0565 0 0" type="box" />
                <body name="body2" pos="-0.0685 0 0">
                    <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                    <joint name="joint2" type="hinge" pos="0 0 0" axis="0 0 1" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                    <geom size="0.02325 0.017 0.01425" pos="-0.0565 0 0" type="box" />
                    <body name="body3" pos="-0.0685 0 0">
                        <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                        <joint name="joint3" type="hinge" pos="0 0 0" axis="0 1 0" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                        <geom size="0.02325 0.01425 0.017" pos="-0.0565 0 0" type="box" />
                        <body name="body4" pos="-0.0685 0 0">
                            <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                            <joint name="joint4" type="hinge" pos="0 0 0" axis="0 0 1" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                            <geom size="0.02325 0.017 0.01425" pos="-0.0565 0 0" type="box" />
                            <body name="body5" pos="-0.0685 0 0">
                                <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                <joint name="joint5" type="hinge" pos="0 0 0" axis="0 1 0" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                <geom size="0.02325 0.01425 0.017" pos="-0.0565 0 0" type="box" />
                                <body name="body6" pos="-0.0685 0 0">
                                    <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                    <joint name="joint6" type="hinge" pos="0 0 0" axis="0 0 1" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                    <geom size="0.02325 0.017 0.01425" pos="-0.0565 0 0" type="box" />
                                    <body name="body7" pos="-0.0685 0 0">
                                        <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                        <joint name="joint7" type="hinge" pos="0 0 0" axis="0 1 0" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                        <geom size="0.02325 0.01425 0.017" pos="-0.0565 0 0" type="box" />
                                        <body name="body8" pos="-0.0685 0 0">
                                            <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                            <joint name="joint8" type="hinge" pos="0 0 0" axis="0 0 1" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                            <geom size="0.02325 0.017 0.01425" pos="-0.0565 0 0" type="box" />
                                            <body name="body9" pos="-0.0685 0 0">
                                                <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                                <joint name="joint9" type="hinge" pos="0 0 0" axis="0 1 0" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                                <geom size="0.02325 0.01425 0.017" pos="-0.0565 0 0" type="box" />
                                                <body name="body10" pos="-0.0685 0 0">
                                                    <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                                    <joint name="joint10" type="hinge" pos="0 0 0" axis="0 0 1" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                                    <geom size="0.02325 0.017 0.01425" pos="-0.0565 0 0" type="box" />
                                                    <body name="body11" pos="-0.0685 0 0">
                                                        <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                                        <joint name="joint11" type="hinge" pos="0 0 0" axis="0 1 0" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                                        <geom size="0.02325 0.01425 0.017" pos="-0.0565 0 0" type="box" />
                                                        <body name="body12" pos="-0.0685 0 0">
                                                            <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                                            <joint name="joint12" type="hinge" pos="0 0 0" axis="0 0 1" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                                            <geom size="0.02325 0.017 0.01425" pos="-0.0565 0 0" type="box" />
                                                            <body name="body13" pos="-0.0685 0 0">
                                                                <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                                                <joint name="joint13" type="hinge" pos="0 0 0" axis="0 1 0" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                                                <geom size="0.02325 0.01425 0.017" pos="-0.0565 0 0" type="box" />
                                                                <body name="body14" pos="-0.0685 0 0">
                                                                    <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                                                    <joint name="joint14" type="hinge" pos="0 0 0" axis="0 0 1" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                                                    <geom size="0.02325 0.017 0.01425" pos="-0.0565 0 0" type="box" />
                                                                    <body name="tail" pos="-0.0685 0 0">
                                                                        <inertial pos="-0.0565 0 0" quat="0 0.707107 0 0.707107" mass="0.1" diaginertia="0.0000194 0.0000174 0.0000115" />
                                                                        <joint name="joint15" type="hinge" pos="0 0 0" axis="0 1 0" limited="true" range="-90 90" damping="0.6" stiffness="0" armature="0.05" />
                                                                        <geom size="0.02325 0.01425 0.017" pos="-0.0565 0 0" type="box" />
                                                                    </body>
                                                                </body>
                                                            </body>
                                                        </body>
                                                    </body>
                                                </body>
                                            </body>
                                        </body>
                                    </body>
                                </body>
                            </body>
                        </body>
                    </body>
                </body>
            </body>
        </body>
    </worldbody>

    <actuator>
        <position name="servo_1" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint1" kp="4"/>
        <position name="servo_2" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint2" kp="4"/>
        <position name="servo_3" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint3" kp="4"/>
        <position name="servo_4" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint4" kp="4"/>
        <position name="servo_5" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint5" kp="4"/>
        <position name="servo_6" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint6" kp="4"/>
        <position name="servo_7" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint7" kp="4"/>
        <position name="servo_8" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint8" kp="4"/>
        <position name="servo_9" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint9" kp="4"/>
        <position name="servo_10" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint10" kp="4"/>
        <position name="servo_11" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint11" kp="4"/>
        <position name="servo_12" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint12" kp="4"/>
        <position name="servo_13" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint13" kp="4"/>
        <position name="servo_14" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint14" kp="4"/>
        <position name="servo_15" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.0 3.0" gear="1" joint="joint15" kp="4"/>

    </actuator>
</mujoco>

"""

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

def getMotionCol(M,i):
    return M[:,i].reshape(M.shape[0],1)


#Joint angle function
def P_vertical(slot):
    return np.array([[d_amp * math.cos(slot/10 + degtorad(d_amp))],
                        [0],
                        [d_amp * math.cos(slot/10 + 3 * degtorad(d_amp))],
                        [0],
                        [d_amp * math.cos(slot/10 + 5 * degtorad(d_amp))],
                        [0],
                        [d_amp * math.cos(slot/10 + 7 * degtorad(d_amp))],
                        [0],
                        [d_amp * math.cos(slot/10 + 9 * degtorad(d_amp))],
                        [0],
                        [d_amp * math.cos(slot/10 + 11 * degtorad(d_amp))],
                        [0],
                        [d_amp * math.cos(slot/10 + 13 * degtorad(d_amp))],
                        [0],
                        [d_amp * math.cos(slot/10 + 15 * degtorad(d_amp))],
                        [0]],dtype='float'
    )
# theta_vertical = np.array([[d_amp * math.sin((2 * math.pi / 8)*k + degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8)*k + 3 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8)*k + 5 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8)*k + 7 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8)*k + 9 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8)*k + 11 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8)*k + 13 * degtorad(d_amp))],
#                     [0],
#                     [d_amp * math.sin((2 * math.pi / 8)*k + 15 * degtorad(d_amp))],
#                     [0]],np.float
# )

snake = mujoco_py.load_model_from_xml(snake_xml)
simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

#Select gait if we select vertical -> gait slot is 8.
t = 0
k = 0
tau = 1 # time coefficient larger -> slower motion 0 < tau < inf
G = np.zeros((16,1))
while True:
   
    P = P_vertical(k)
    m_k = getMotionCol(m_vertical,(k%8)).T
    g = np.round(np.diagonal((np.dot(P,m_k))),decimals=2).reshape((16,1))
    G = G + g

    for motor_idx in range(15):
            simulator.data.ctrl[motor_idx] = round(degtorad(G[motor_idx].item()) * 0.1,4)
            
    # simulator.data.ctrl[0] = G[0]
    # simulator.data.ctrl[1] = G[1]
    # simulator.data.ctrl[2] = G[2]
    # simulator.data.ctrl[3] = G[3]
    # simulator.data.ctrl[4] = G[4]
    # simulator.data.ctrl[5] = G[5]
    # simulator.data.ctrl[6] = G[6]
    # simulator.data.ctrl[7] = G[7]
    # simulator.data.ctrl[8] = G[8]
    # simulator.data.ctrl[9] = G[9]
    # simulator.data.ctrl[10] = G[10]
    # simulator.data.ctrl[11] = G[11]
    # simulator.data.ctrl[12] = G[12]
    # simulator.data.ctrl[13] = G[13]
    # simulator.data.ctrl[14] = G[14]
    # simulator.data.ctrl[15] = G[15]

    simulator.step()
    sim_viewer.render()

    if t%tau == 0:
        k = k + 1

    if(t%1000 == 0):
        print(simulator.get_state())

    if(t%5000 == 0):
        simulator.reset()

    if t > 100 and os.getenv('TESTING') is not None:
        break

    t = t + 1

