import horcrux_terrain_v1
import gymnasium as gym
import numpy as np
import pandas as pd

import os
import pathlib
import time
import mediapy as media

from gymnasium.utils.save_video import save_video

#camera names : com, ceiling, head_mount
# (30,30,40,40,0) # serpentine
# (45,45,10,10,45) # sidewinding
# (0,0,30,30,90) # rolling
# (30,30,40,40,90) # helix
env = gym.make("horcrux_terrain_v1/sand-v1", 
               terminate_when_unhealthy = False, 
               render_mode = "human", 
               render_camera_name = 'ceiling', 
               use_gait = True,
               gait_params = (30,30,15,15,0)
               ,) 
_ = env.reset()

step_starting_index = 0
episode_index = 8
video_prefix = "PPO_20240126-0.28.1"
frames = []
datas = {"joint_pos":np.empty((0,14)),
         "joint_vel":np.empty((0,14)),
         "head_quat":np.empty((0,4)),
         "head_ang_vel":np.empty((0,3)),
         "head_lin_acc":np.empty((0,3)),
         "motion_vector":np.empty((0,14)),
         "head_rpy":np.empty((0,3)),
         "com_rpy":np.empty((0,3)),

         "x_disp":np.empty((0,1)),
         "y_disp":np.empty((0,1)),
         "origin_disp":np.empty((0,1)),
         "x_vel":np.empty((0,1)),
         "y_vel":np.empty((0,1)),
         "reward_forward":np.empty((0,1)),
         "reward_healthy":np.empty((0,1)),
         "reward_ctrl":np.empty((0,1)),
         "reward_side":np.empty((0,1)),
         "reward_unhealthy":np.empty((0,1)),
         }
for j in range(1):
    for i in range(300):
        # random = np.random.random(14) * 2
        random = np.ones(14) * 0.7

        obs, rew, terminated, _, info = env.step(random)

        if terminated:
            env.reset()
            print("terminated")

        # if i % 300 == 0:
        #     env.reset()
            
        # datas['joint_pos'] = np.vstack((datas['joint_pos'], info['joint_pos'])).tolist()
        # datas['joint_vel'] = np.vstack((datas['joint_vel'], info['joint_vel'])).tolist()
        # datas['head_quat'] = np.vstack((datas['head_quat'], info['head_quat'])).tolist()
        # datas['head_ang_vel'] = np.vstack((datas['head_ang_vel'], info['head_ang_vel'])).tolist()
        # datas['head_lin_acc'] = np.vstack((datas['head_lin_acc'], info['head_lin_acc'])).tolist()
        # datas['motion_vector'] = np.vstack((datas['motion_vector'], info['motion_vector'])).tolist()
        # datas['head_rpy'] = np.vstack((datas['head_rpy'], info['head_rpy'])).tolist()
        # datas['com_rpy'] = np.vstack((datas['com_rpy'], info['com_rpy'])).tolist()

        # datas['x_disp'] = np.vstack((datas['x_disp'], info['x_displacement'])).tolist()
        # datas['y_disp'] = np.vstack((datas['y_disp'], info['y_displacement'])).tolist()
        # datas['origin_disp'] = np.vstack((datas['origin_disp'], info['distance_from_origin'])).tolist()
        # datas['x_vel'] = np.vstack((datas['x_vel'], info['x_velocity'])).tolist()
        # datas['y_vel'] = np.vstack((datas['y_vel'], info['y_velocity'])).tolist()
        # datas['reward_forward'] = np.vstack((datas['reward_forward'], info['reward_forward'])).tolist()
        # datas['reward_healthy'] = np.vstack((datas['reward_healthy'], info['reward_healthy'])).tolist()
        # datas['reward_ctrl'] = np.vstack((datas['reward_ctrl'], info['reward_ctrl'])).tolist()
        # datas['reward_side'] = np.vstack((datas['reward_side'], info['reward_side'])).tolist()
        # datas['reward_unhealthy'] = np.vstack((datas['reward_unhealthy'], info['reward_unhealthy'])).tolist()
            
        pixels = env.render()

        frames.append(pixels)

    env.reset()
exit()

save_video(frames,"./videos", name_prefix=video_prefix, fps=env.metadata["render_fps"], step_starting_index = step_starting_index, episode_index = episode_index)

env.close()


import datetime
__now_str = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
savedata_pos = pd.DataFrame(datas['joint_pos'], columns=['POS_1',
                                                         'POS_2',
                                                         'POS_3',
                                                         'POS_4',
                                                         'POS_5',
                                                         'POS_6',
                                                         'POS_7',
                                                         'POS_8',
                                                         'POS_9',
                                                         'POS_10',
                                                         'POS_11',
                                                         'POS_12',
                                                         'POS_13',
                                                         'POS_14'
                                                         ])
savedata_vel = pd.DataFrame(datas['joint_vel'], columns=['VEL_1',
                                                         'VEL_2',
                                                         'VEL_3',
                                                         'VEL_4',
                                                         'VEL_5',
                                                         'VEL_6',
                                                         'VEL_7',
                                                         'VEL_8',
                                                         'VEL_9',
                                                         'VEL_10',
                                                         'VEL_11',
                                                         'VEL_12',
                                                         'VEL_13',
                                                         'VEL_14'
                                                         ])
savedata_h_quat = pd.DataFrame(datas['head_quat'], columns=['qw', 'qx', 'qy', 'qz'])
savedata_h_a_vel = pd.DataFrame(datas['head_ang_vel'], columns=['angular_vel_r', 'angular_vel_p', 'angular_vel_y'])
savedata_h_l_acc = pd.DataFrame(datas['head_lin_acc'], columns=['linear_acc_x', 'linear_acc_y', 'linear_acc_z'])
savedata_m_Vec = pd.DataFrame(datas['motion_vector'], columns=['Motion_vec_1',
                                                               'Motion_vec_2',
                                                               'Motion_vec_3',
                                                               'Motion_vec_4',
                                                               'Motion_vec_5',
                                                               'Motion_vec_6',
                                                               'Motion_vec_7',
                                                               'Motion_vec_8',
                                                               'Motion_vec_9',
                                                               'Motion_vec_10',
                                                               'Motion_vec_11',
                                                               'Motion_vec_12',
                                                               'Motion_vec_13',
                                                               'Motion_vec_14'
                                                               ])
savedata_h_rpy = pd.DataFrame(datas['head_rpy'], columns=['head_roll', 'head_pitch', 'head_yaw'])
savedata_c_rpy = pd.DataFrame(datas['com_rpy'], columns=['com_roll', 'com_pitch', 'com_yaw'])

savedata_x_disp = pd.DataFrame(datas['x_disp'], columns=['x_disp'])
savedata_y_disp = pd.DataFrame(datas['y_disp'], columns=['y_disp'])
savedata_o_disp = pd.DataFrame(datas['origin_disp'], columns=['origin_disp'])
savedata_x_vel = pd.DataFrame(datas['x_vel'], columns=['x_vel'])
savedata_y_vel = pd.DataFrame(datas['y_vel'], columns=['y_vel'])
savedata_r_for = pd.DataFrame(datas['reward_forward'], columns=['reward_forward'])
savedata_r_health = pd.DataFrame(datas['reward_healthy'], columns=['reward_healthy'])
savedata_r_ctrl = pd.DataFrame(datas['reward_ctrl'], columns=['reward_ctrl'])
savedata_r_side = pd.DataFrame(datas['reward_side'], columns=['reward_side'])
savedata_r_uhealth = pd.DataFrame(datas['reward_unhealthy'], columns=['reward_unhealthy'])


integrated_data = pd.concat([savedata_pos, savedata_vel, savedata_h_quat, savedata_h_a_vel, savedata_h_l_acc, savedata_m_Vec, savedata_h_rpy, savedata_c_rpy, savedata_x_disp, savedata_y_disp, savedata_o_disp, savedata_x_vel, savedata_y_vel, savedata_r_for, savedata_r_health, savedata_r_ctrl, savedata_r_side, savedata_r_uhealth], axis=1)

integrated_data.to_csv('./'+__now_str+'integrated.csv')