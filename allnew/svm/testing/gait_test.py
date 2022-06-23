# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : Snake robot dynamics gait test code

import sys
sys.path.append("../")

import gait
import mujoco_py
import numpy as np
import random
import pytictoc as tictoc

snake = mujoco_py.load_model_from_path("../snake.xml")

simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

#Simulation Setup
_total_time = 1400
_num_iter = 10

gait_type = 1

# gait_param = np.array([39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1]) #initial params
# gait_param = np.array([39, 258, 0, 28, 86, 0, 1])

#################### From Matlab gait param ###############
gait_param = np.array([0,   344,     3,    11,   344,    -1,     4])



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
    # gait_vector[1] = random.randint(0,85) # Dorsal Amp
    # gait_vector[2] = random.randint(0,359)  # Dorsal Phase
    # gait_vector[3] = random.randint(-10,10) # Dorsal Nu
    # gait_vector[4] = random.randint(0,85) # Lateral Amp
    # gait_vector[5] = random.randint(0,359)  # Lateral Phase
    # gait_vector[6] = random.randint(-10,10) # Lateral Nu
    # gait_vector[7] = random.randint(1,5) # Tau

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
        accum_obs_data = np.append(accum_obs_data, simulator.data.sensordata[:-4]) # If use frame orientation sensor (this sensor is allign to global frame)

        # Additional data
        position_head = np.array(simulator.data.get_body_xpos('head'))
        accum_obs_data = np.append(accum_obs_data, position_head)

        position_com = np.array([simulator.data.get_body_xpos(x) for x in link_names]).mean(axis=0)
        accum_obs_data = np.append(accum_obs_data, position_com)

        # orientaion_head = np.array(simulator.data.get_body_xquat('head')) # If use just head link frame (this sensor is not allign to global frame)
        orientaion_head = np.array(simulator.data.sensordata[-4:]) # If use frame orientation sensor (this sensor is allign to global frame)
        accum_obs_data = np.append(accum_obs_data, orientaion_head)

        orientaion_com = np.array([simulator.data.get_body_xquat(x) for x in link_names]).mean(axis=0)
        accum_obs_data = np.append(accum_obs_data, orientaion_com)

        try:
            simulator.step()
        except:
            print("Mujoco Exception raised! at gait vector : " + str(gait_vector))
            break
        sim_viewer.render()

    accum_obs_data = np.reshape(accum_obs_data, (-1,64))

    # make data array to decimal 4 places
    accum_obs_data = np.around(accum_obs_data, decimals=4)

    # print(np.shape(accum_obs_data))

    _tic_iter.toc()
    _tic_proc.toc()
    print("%d Iteration Done! - (Total elapsed time is %3f) "%(_+1, _tic_proc.tocvalue()),end="\r")

print("Simulation is terminated correctly.")