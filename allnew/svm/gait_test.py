# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : Snake robot dynamics SVM code

import gait
import mujoco_py
import numpy as np


#load model from path
# snake = mujoco_py.load_model_from_path("./snake.xml")
snake = mujoco_py.load_model_from_path("./snake_circle.xml") # Triangular frame
# -> 향 후 지형 랜덤 초기화 기능을 추가할 수 있을 것

# mujoco-py
simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

#Simulation Setup
_total_time = 1680
# _total_time = 10

_num_iter = 3

# gait_type = 2
# # gait_param = np.array([39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1]) #initial params
# # gait_param = np.array([30,    69,     3,    48,   133,     2,     2]) # 우연하게 얻은 로테이션 -> 1
# # gait_param = np.array([10,   116,     1,    48,    98,     1,     2]) # gait 2 회전
# gait_param = np.array([10,   107,     5,    55,    91,    -7,     2]) # gait 2회전 2

gait_type = 3
gait_param = np.array([1,     1,    14,    12,    19,   -27,     1]) # gait 2회전 2

# gait_param = np.array([52.76,	319.65,	1.99,	72.07,	262.95,	7.91,	1])
gait_gen = gait.gait(gait_type, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4], gait_param[5], gait_param[6])
joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']



# while(True):
for _ in range(_num_iter):
    _rolled_check = False
    
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

        # print(np.around(simulator.data.ctrl, decimals=2))
        simulator.step()
        sim_viewer.render()

        position_com = np.array([simulator.data.get_body_xpos(x) for x in link_names]).mean(axis=0)

    cost = position_com[0] - abs(position_com[1])
    print("J : { %f }"%(cost))
    print(gait_gen.m_sinuous)
print("\n Simulation is terminated correctly.")



