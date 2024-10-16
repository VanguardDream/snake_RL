# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : Snake robot dynamics gait test code

import sys
sys.path.append("../")

import gait
import mujoco_py
import numpy as np
import random
from scipy.spatial.transform import Rotation as Rot
import pytictoc as tictoc

snake = mujoco_py.load_model_from_path("../snake.xml")

simulator = mujoco_py.MjSim(snake)

#Simulation Setup
_render = True
if _render:
    sim_viewer = mujoco_py.MjViewer(simulator)

_total_time = 1400
_num_iter = 3

gait_type = 2

#################### From Matlab gait param ###############
gait_param = np.array([50,   208,     0,    67,   263,     8,     1])
# gait_param = np.array([0, 0, 0, 0, 0, 0, 1])

# Running time measure
_tic_proc = tictoc.TicToc()
_tic_iter = tictoc.TicToc()

# gait_param = np.array([52.76,	319.65,	1.99,	72.07,	262.95,	7.91,	1])
gait_gen = gait.gait(gait_type, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4], gait_param[5], gait_param[6])
joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']

#Initiation
_tic_proc.tic()


# while(True):
for _ in range(_num_iter):
    _tic_iter.tic()
    
    gait_vector = [gait_type, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4], gait_param[5], gait_param[6]]

    if 'gait_gen' in locals():
        del gait_gen


    gait_gen = gait.gait(gait_vector[0], gait_vector[1], gait_vector[2], gait_vector[3], gait_vector[4], gait_vector[5], gait_vector[6], gait_vector[7])

    simulator.reset()
    simulator.step()

    if 'accum_obs_data' in locals():
        try:
            del accum_obs_data
        except:
            print('Is there accum_obs_data variable? check it')

    accum_obs_data = np.array([])

    for t in range(_total_time):
        joint_goal = gait_gen.generate(t)
        selected_motor_index = gait_gen.commandIdx(t)

        for idx in selected_motor_index:
                # Commnad motor here
                simulator.data.ctrl[idx] = gait_gen.degtorad(joint_goal[idx])

         # MJCF Sensor data
        accum_obs_data = np.append(accum_obs_data, t)
        accum_obs_data = np.append(accum_obs_data, [gait_gen.get_stride_ratio(t)])
        accum_obs_data = np.append(accum_obs_data, simulator.data.sensordata[:48])  # If use frame orientation sensor (this sensor is allign to global frame)

        # Additional data
        position_head = np.array(simulator.data.get_body_xpos('head'))
        accum_obs_data = np.append(accum_obs_data, position_head)

        position_com = np.array([simulator.data.get_body_xpos(x) for x in link_names]).mean(axis=0)
        accum_obs_data = np.append(accum_obs_data, position_com)

        # orientaion_head = np.array(simulator.data.get_body_xquat('head')) # If use just head link frame (this sensor is not allign to global frame)
        orientaion_head = np.array(simulator.data.sensordata[-4:]) # If use frame orientation sensor (this sensor is allign to global frame)
        accum_obs_data = np.append(accum_obs_data, orientaion_head)

        # orientaion_com = np.array([simulator.data.get_body_xquat(x) for x in link_names]).mean(axis=0) # Do not use! this code just averaging coefficients of quaternion.
        orientaions_com = np.reshape(simulator.data.sensordata[52:],(-1,4))

        orientaions_com[:, [0, 1, 2, 3]] = orientaions_com[:, [1, 2, 3, 0]]
        rot_com = Rot.from_quat(orientaions_com)
        orientaion_com = rot_com.mean().as_quat()
        orientaion_com[0], orientaion_com[1], orientaion_com[2], orientaion_com[3] = orientaion_com[3], orientaion_com[0], orientaion_com[1], orientaion_com[2]
        accum_obs_data = np.append(accum_obs_data, orientaion_com)

        # ## Healthy check
        # [_roll, _pitch, _yaw] = rot_com.mean().as_euler('XYZ',degrees=True)

        # if(abs(_roll) > 165):
        #     print("Unhealy(Over rolling) is occured! at gait vector : " + str(gait_vector))
        #     _unhealth = True
        #     break

        try:
            simulator.step()
        except:
            print("Mujoco Exception raised! at gait vector : " + str(gait_vector))
            break

        if _render:
            sim_viewer.render()

    accum_obs_data = np.reshape(accum_obs_data, (-1,64))
    # print(np.shape(accum_obs_data))

    # make data array to decimal 4 places
    accum_obs_data = np.around(accum_obs_data, decimals=4)

    accum_quat_com =  accum_obs_data[:,-4:].copy()
    accum_quat_com[:, [0, 1, 2, 3]] = accum_quat_com[:, [1, 2, 3, 0]]

    accum_rot = Rot.from_quat(accum_quat_com)
    avg_angle = accum_rot.mean().as_euler('XYZ',degrees=True)

    if(abs(avg_angle[0]) > 7):
        print("Rolling unhealthy! Gait Params : ",end='')
        print(str(gait_vector) + "\t Average euler : " ,end=' ')
        print(accum_rot.mean().as_euler('XYZ',degrees=True),end='\n')

    _tic_iter.toc()
    _tic_proc.toc()
    print("%d Iteration Done! - (Total elapsed time is %3f) "%(_+1, _tic_proc.tocvalue()),end="\r")

print("Simulation is terminated correctly.")