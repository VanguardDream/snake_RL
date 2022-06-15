# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : Snake robot dynamics SVM code

import gait
import mujoco_py
import numpy as np

#load model from path
snake = mujoco_py.load_model_from_path("./snake.xml")
# -> 향 후 지형 랜덤 초기화 기능을 추가할 수 있을 것

# mujoco-py
simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

#Simulation Loop

gait_param = np.array([39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1])
gait_param = np.array([52.76,	319.65,	1.99,	72.07,	262.95,	7.91,	1])

gait_gen = gait.gait(2, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4], gait_param[5], gait_param[6])

joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']

while(True):
    simulator.reset()

    for t in range(1000):
        joint_goal = gait_gen.generate(t)
        selected_motor_index = gait_gen.commandIdx(t)

        for idx in selected_motor_index:
                # Commnad motor here
                simulator.data.ctrl[idx] = gait_gen.degtorad(joint_goal[idx])

        simulator.step()
        sim_viewer.render()