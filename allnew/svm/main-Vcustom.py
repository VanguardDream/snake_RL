# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : Snake robot dynamics SVM code

import gait
import mujoco_py
import numpy as np
import utils
import random
from scipy.spatial.transform import Rotation as Rot
import pytictoc as tictoc


#load model from path
# snake = mujoco_py.load_model_from_path("./snake.xml")
snake = mujoco_py.load_model_from_path("./snake_circle_variable.xml")
# -> 향 후 지형 랜덤 초기화 기능을 추가할 수 있을 것

# mujoco-py
simulator = mujoco_py.MjSim(snake)
# sim_viewer = mujoco_py.MjViewer(simulator)

#Simulation Setup
# _total_time = 1680
_total_time = 840
# _total_time = 10

_num_iter = 10

gait_type = 3
# gait_param = np.array([39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1]) #initial params
gait_param = np.array([39, 258, 0, 28, 86, 0, 1])
# Running time measure
_tic_proc = tictoc.TicToc()
_tic_iter = tictoc.TicToc()

# gait_param = np.array([52.76,	319.65,	1.99,	72.07,	262.95,	7.91,	1])
gait_gen = gait.gait(gait_type, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4], gait_param[5], gait_param[6])
joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']
site_names = ['s_head','s_link1','s_link2','s_link3','s_link4','s_link5','s_link6','s_link7','s_link8','s_link9','s_link10','s_link11','s_link12','s_link13','s_tail']

#Initiation
_tic_proc.tic()


# while(True):
for _ in range(_num_iter):
    _tic_iter.tic()
    _rolled_check = False
    
    gait_vector = [gait_type, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4], gait_param[5], gait_param[6]]
    gait_vector[1] = random.randint(1,15) # Dorsal Amp
    gait_vector[2] = random.randint(1,20)  # Frequency
    gait_vector[3] = random.randint(-36,36) # Phase
    gait_vector[4] = random.randint(1,15) # Lateral Amp
    gait_vector[5] = random.randint(1,20)  # Frequency
    gait_vector[6] = random.randint(-36,36) # Phase
    gait_vector[7] = random.randint(1,1) # Tau

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
        # position_head = np.array(simulator.data.get_body_xpos('head')) #원통 프레임 바디 축 틀어져서 사용안함!
        position_head = np.array(simulator.data.get_site_xpos('s_head'))
        accum_obs_data = np.append(accum_obs_data, position_head)

        # position_com = np.array([simulator.data.get_body_xpos(x) for x in link_names]).mean(axis=0) #원통 프레임 바디 축 틀어져서 사용안함!
        position_com = np.array([simulator.data.get_site_xpos(x) for x in site_names]).mean(axis=0)
        accum_obs_data = np.append(accum_obs_data, position_com)

        # orientaion_head = np.array(simulator.data.get_body_xquat('head')) # If use just head link frame (this sensor is not allign to global frame)
        orientaion_head = np.array(simulator.data.sensordata[-4:]) # If use frame orientation sensor (this sensor is allign to global frame)
        accum_obs_data = np.append(accum_obs_data, orientaion_head)

        # orientaion_com = np.array([simulator.data.get_body_xquat(x) for x in link_names]).mean(axis=0) # Do not use! this code just averaging coefficients of quaternion.
        orientaions_com = np.reshape(simulator.data.sensordata[48:],(-1,4)).copy()

        orientaions_com[:, [0, 1, 2, 3]] = orientaions_com[:, [1, 2, 3, 0]]
        rot_com = Rot.from_quat(orientaions_com)
        orientaion_com = rot_com.mean().as_quat()
        orientaion_com[0], orientaion_com[1], orientaion_com[2], orientaion_com[3] = orientaion_com[3], orientaion_com[0], orientaion_com[1], orientaion_com[2]
        accum_obs_data = np.append(accum_obs_data, orientaion_com)


        ## Healthy check
        [_roll, _pitch, _yaw] = rot_com.mean().as_euler('XYZ',degrees=True)

        if(abs(_roll) > 170 and (not _rolled_check)):
            # print("(Roll axis turned) ",end='')
            _rolled_check = True
            break

        try:
            simulator.step()
        except:
            print("Mujoco Exception raised! at gait vector : " + str(gait_vector))
            break
        # sim_viewer.render()

    accum_obs_data = np.reshape(accum_obs_data, (-1,64))
    # print(np.shape(accum_obs_data))

    # make data array to decimal 4 places
    accum_obs_data = np.around(accum_obs_data, decimals=4)

    accum_quat_com =  accum_obs_data[:,-4:].copy()
    accum_quat_com[:, [0, 1, 2, 3]] = accum_quat_com[:, [1, 2, 3, 0]]

    accum_rot = Rot.from_quat(accum_quat_com)
    avg_angle = accum_rot.mean().as_euler('XYZ',degrees=True)

    _tic_iter.toc()
    _tic_proc.toc()
    print("%d Iteration Done! - (Total elapsed time is %3f) "%(_+1, _tic_proc.tocvalue()),end="\r")

    if(abs(avg_angle[0]) > 7 or _rolled_check):
        # print("Rolling unhealthy! Gait Params : ",end='')
        # print(str(gait_vector) + "\t \t Average euler : " ,end=' ')

        # print(np.around(accum_rot.mean().as_euler('XYZ',degrees=True),decimals=2),end='\n')

        f = open("./error_log.txt",'a')
        _log = str()
        if _rolled_check:
            _log = _log + "(Roll axis turned) "

        _log = _log + "Rolling unhealthy! Gait Params : " + str(gait_vector) + "\t \t Average euler : " + str(np.around(accum_rot.mean().as_euler('XYZ',degrees=True),decimals=2)) + "\n"

        f.write(_log)
        f.close()
        continue

    utils.writeToMATeach(gait_vector,accum_obs_data)

print("\n Simulation is terminated correctly.")



