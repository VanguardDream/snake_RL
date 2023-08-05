__author__ = ["Bongsub Song"]

import numpy as np
import pandas as pd
import os
import pathlib

from gymnasium import spaces
from gymnasium import utils
from gymnasium.envs.mujoco import MujocoEnv
from scipy.spatial.transform import Rotation

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = pathlib.Path(__location__)
__model_location__ = __location__.parent.parent.parent.joinpath('models')

def serpenoid(t, b, b2, a, a2, e_d1, e_d2, e_l1, e_l2, delta):
    #Hirose (1993) serpenoid curve implementations
    f1 = e_d2 * t
    f2 = e_l2 * t

    j_1 = b + a * np.sin(e_d1 + f1)
    j_2 = b2 + a2 * np.sin(e_l1 * 2 + f2 + delta)

    j_3 = b + a * np.sin(e_d1 * 3 + f1)
    j_4 = b2 + a2 * np.sin(e_l1 * 4 + f2 + delta)

    j_5 = b + a * np.sin(e_d1 * 5 + f1)
    j_6 = b2 + a2 * np.sin(e_l1 * 6 + f2 + delta)

    j_7 = b + a * np.sin(e_d1 * 7 + f1)
    j_8 = b2 + a2 * np.sin(e_l1 * 8 + f2 + delta)

    j_9 = b + a * np.sin(e_d1 * 9 + f1)
    j_10 = b2 + a2 * np.sin(e_l1 * 10 + f2 + delta)

    j_11 = b + a * np.sin(e_d1 * 11 + f1)
    j_12 = b2 + a2 * np.sin(e_l1 * 12 + f2 + delta)

    j_13 = b + a * np.sin(e_d1 * 13 + f1)
    j_14 = b2 + a2 * np.sin(e_l1 * 14 + f2 + delta)

    return np.array([j_1, j_2, j_3, j_4, j_5, j_6, j_7, j_8, j_9, j_10, j_11, j_12, j_13, j_14])

class SnakeEnv(MujocoEnv, utils.EzPickle):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
    "render_fps": 10,
    }

    def __init__(self, frame_skip = 10, **kwargs,) -> None:
        utils.EzPickle.__init__(self, frame_skip, **kwargs,)
        # Observation Space
        _slot_space = [1] * 14
        _accelerometer_space = [15] * 3
        _gyro_space = [6] * 3
        _joint_pos_space = [2.1] * 14
        _joint_vel_space = [10.4] * 14
        _joint_torque_space = [5.0] * 14
        _head_quat_space = [1.0] * 4

        __Rot_goal_orientation = Rotation.from_rotvec([0, 0, 0])

        self._goal_orientation = __Rot_goal_orientation.as_rotvec(degrees=True)
        self._robot_body_names = ["head","link1","link2","link3","link4","link5","link6","link7","link8","link9","link10","link11","link12","link13","tail"]

        self.__max_spaces = np.array(_slot_space + _accelerometer_space + _gyro_space + _joint_pos_space + _joint_vel_space + _joint_torque_space + _head_quat_space,dtype=np.float64)
        self.__min_spaces = -1 * self.__max_spaces.copy()

        self.observation_space = spaces.Box(low=self.__min_spaces, high=self.__max_spaces, shape=(66,),dtype=np.float64) # M_col and 48 sensordatas -> 14 + 48 => 62

        # Create mujoco env instance
        MujocoEnv.__init__(self, os.path.join(__model_location__,'snake_circle_contact_fixed_marker.xml'), frame_skip, observation_space= self.observation_space, **kwargs)

        # Action Space
        # self.action_space = spaces.Box(low= 0.0, high= 3.0, shape=(14,))
        self.action_space = spaces.MultiDiscrete(np.array([7]*14))

        # Physics variables
        self.k = 0
        self.action_frequency = 0.1
        self.timestep = self.model.opt.timestep
        self.time = self.data.time
        self.frame_skip = frame_skip

        # Make gait motion matrix
        ### Gait parameters
        b = 0
        b2 = 0

        a = 1
        a2 = 1

        e_d1 = np.radians(30)
        e_l1 = np.radians(30)

        e_d2 = 3
        e_l2 = 3

        # delta = np.radians(45) # for sidewinding
        delta = np.radians(0) # for serpenoid

        t_range = np.arange(0, np.lcm(np.lcm(e_d2,e_l2), 2) * np.pi, self.action_frequency).transpose()

        joint_pos = serpenoid(t_range, b, b2, a, a2, e_d1, e_d2, e_l1, e_l2, delta)
        joint_vel = np.diff(joint_pos.copy()) * (1 / self.action_frequency)
        joint_tor = np.diff(joint_vel.copy()) * (1 / self.action_frequency)

        self.M_matrix = joint_tor.copy()

        # print(np.shape(joint_pos))
        # print(np.shape(joint_vel))
        # print(np.shape(joint_tor))

        # for i in range(np.shape(self.M_matrix)[0]):
        #     for  j in range(np.shape(self.M_matrix)[1]):
        #         if self.M_matrix[i][j] > np.amax(joint_pos[i,:]) * 0.75:
        #             self.M_matrix[i][j] = 1
        #         elif self.M_matrix[i][j] < np.amin(joint_pos[i,:]) * 0.75:
        #             self.M_matrix[i][j] = -1
        #         else:
        #             self.M_matrix[i][j] = 0

        for i in range(np.shape(self.M_matrix)[0]):
            for  j in range(np.shape(self.M_matrix)[1]):
                if self.M_matrix[i][j] > 0:
                    self.M_matrix[i][j] = -1
                elif self.M_matrix[i][j] < 0:
                    self.M_matrix[i][j] = 1
                else:
                    self.M_matrix[i][j] = 0

        # dataframe_mat = pd.DataFrame(self.M_matrix)
        # dataframe_mat.to_csv('gait_mat.csv',index=False)

    def _get_obs(self):
        _slot = self.M_matrix[:,self.k].copy()
        # _sensors = self.data.sensordata[0:20].copy()
        _sensors = self.data.sensordata[0:48].copy()

        # _pos = self.data.sensordata[6:20].copy()
        # _vel = self.data.sensordata[20:34].copy()
        # _tor = self.data.sensordata[34:48].copy()
        _quat = self.data.sensordata[48:52].copy()
        observation = np.clip(np.hstack((_slot, _sensors, _quat)).copy(),a_min=self.__min_spaces, a_max=self.__max_spaces)
        return observation

    def step(self, action):
        action = 0.5 * (action) * self.M_matrix[:,self.k].copy()
        
        com_xy_position_before = self.get_robot_com()
        xy_position_before = self.data.xpos[1][0:2].copy()

        self.do_simulation(action, self.frame_skip)

        self.k = np.mod(self.k + 1, np.shape(self.M_matrix)[1])

        com_xy_position_after = self.get_robot_com()
        xy_position_after = self.data.xpos[1][0:2].copy()

        com_xy_velocity = (com_xy_position_after - com_xy_position_before) / self.dt
        com_x_velocity, com_y_velocity = com_xy_velocity
        xy_velocity = (xy_position_after - xy_position_before) / self.dt
        x_velocity, y_velocity = xy_velocity

        observation = self._get_obs()
        __model_sensordata = self.data.sensordata.copy()

        head_R = Rotation.from_quat([__model_sensordata[49], __model_sensordata[50], __model_sensordata[51], __model_sensordata[48]])
        head_rotvec = head_R.as_rotvec(degrees=True).copy()    

        forward_reward = x_velocity - 0.1 * np.abs(com_y_velocity)
        # torque_cost = 0.3 * np.linalg.norm(__model_sensordata[-3:],1).copy()

        orientation_reward = (1 / (np.abs(head_rotvec[2] - self._goal_orientation[2]) + 4))

        torque_cost = 0
              
        terminated = False
        terminated_reward = 0        

        self.data.qpos[-2:] = [com_xy_position_after[0], com_xy_position_after[1]]


        # print(np.shape(self.M_matrix)[1])
        if np.abs(head_rotvec[0]) > 80:
            terminated_reward = -10
            terminated = True

        if (np.round(self.data.time * 10)) >= 10 * np.shape(self.M_matrix)[1]: #Check! MuJoCo 10 Sim-step -> RL 1 action step!
            # terminated_reward = 50 * xy_position_after[0] - 30 * np.abs(xy_position_after[1])
            # print(self.data.time)
            terminated = True

        reward = forward_reward + orientation_reward + terminated_reward - torque_cost

        info = {
            "distance_from_origin": np.linalg.norm(xy_position_after, ord=2),
            "com_x_position": com_xy_position_after[0],
            "com_y_position": com_xy_position_after[1],
            "com_x_velocity": com_x_velocity,
            "com_y_velocity": com_y_velocity,
            "head_x_position": xy_position_after[0],
            "head_y_position": xy_position_after[1],
            "head_x_velocity": x_velocity,
            "head_y_velocity": y_velocity,
            "forward_reward": forward_reward,
            "terminated_reward" : terminated_reward,
            "head_torque_cost" : torque_cost,
            "next_gait_slot" : observation[0:14].copy(),
            "accelerometer" : __model_sensordata[0:3].copy(),
            "gyro" : __model_sensordata[3:6].copy(),
            "joint_position" : __model_sensordata[6:20].copy(),
            "joint_velocity" : __model_sensordata[20:34].copy(),
            "joint_torque" : __model_sensordata[34:48].copy(),
            "head_orientation" : __model_sensordata[48:52].copy(),
            "head_rotation" : head_rotvec,
            "head_torque" : __model_sensordata[-3:].copy(),
        }


        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, False, info

    def reset_model(self):
        self.k = 0
        
        noise_low = 0
        noise_high = 0

        qpos = self.init_qpos + self.np_random.uniform(
        low=noise_low, high=noise_high, size=self.model.nq
        )
        qvel = self.init_qvel + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nv
        )

        self.set_state(qpos, qvel)

        observation = self._get_obs()
        return observation
    
    def get_robot_com(self):
        accum_x = 0
        accum_y = 0
        len_names = len(self._robot_body_names)

        for name in self._robot_body_names:
            x, y, _ = self.data.body(name).xpos
            accum_x = accum_x + x
            accum_y = accum_y + y

        return np.array([accum_x / len_names, accum_y / len_names])