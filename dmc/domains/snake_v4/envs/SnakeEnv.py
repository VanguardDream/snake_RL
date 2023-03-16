__author__ = ["Bongsub Song"]

import numpy as np
import os
import pathlib

from gymnasium import spaces
from gymnasium import utils
from gymnasium.envs.mujoco import MujocoEnv

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

    def __init__(self, frame_skip = 10, **kwargs) -> None:
        # Action Space
        self.action_space = spaces.Box(low= 0.0, high= 3.0, shape=(14,), dtype=np.float32)

        # Observation Space
        _slot_space = [1] * 14
        _accelerometer_space = [100] * 3
        _gyro_space = [20] * 3
        _joint_pos_space = [1.58] * 14
        _joint_vel_space = [8.4] * 14
        _joint_torque_space = [3.0] * 14
        _head_quat_space = [1.0] * 4

        __max_spaces = np.array(_slot_space + _accelerometer_space + _gyro_space + _joint_pos_space + _head_quat_space)
        __min_spaces = -1 * __max_spaces.copy()

        self.observation_space = spaces.Box(low=__min_spaces, high=__max_spaces, shape=(38,), dtype=np.float32) # M_col and 48 sensordatas -> 14 + 48 => 62

        # Create mujoco env instance
        MujocoEnv.__init__(self, os.path.join(__model_location__,'snake_circle_contact.xml'), frame_skip, observation_space= self.observation_space, **kwargs)

        # Physics variables
        self.k = 0
        self.action_frequency = 0.1
        self.timestep = self.model.opt.timestep
        self.time = self.data.time

        # Make gait motion matrix
        ### Gait parameters
        b = 0
        b2 = 0

        a = np.radians(15)
        a2 = np.radians(45)

        e_d1 = np.radians(45)
        e_l1 = np.radians(45)

        e_d2 = 1
        e_l2 = 1

        # delta = np.radians(45) # for sidewinding
        delta = np.radians(0) # for serpenoid

        t_range = np.arange(0, np.lcm(np.lcm(e_d2,e_l2), 2) * np.pi, self.action_frequency).transpose()

        joint_pos = serpenoid(t_range, b, b2, a, a2, e_d1, e_d2, e_l1, e_l2, delta)
        joint_vel = np.diff(joint_pos) * (1 / self.action_frequency)
        joint_tor = np.diff(joint_vel) * (1 / self.action_frequency)

        self.M_matrix = joint_tor.copy()

        for i in range(np.shape(self.M_matrix)[0]):
            for  j in range(np.shape(self.M_matrix)[1]):
                if self.M_matrix[i][j] > np.amax(joint_tor[i,:]) * 0.75:
                    self.M_matrix[i][j] = 1
                elif self.M_matrix[i][j] < np.amin(joint_tor[i,:]) * 0.75:
                    self.M_matrix[i][j] = -1
                else:
                    self.M_matrix[i][j] = 0

    def _get_obs(self):
        _slot = self.M_matrix[:,self.k].copy()
        _sensors = self.data.sensordata[0:20].copy()
        # _sensors = self.data.sensordata[0:48].copy()

        # _pos = self.data.sensordata[6:20].copy()
        _vel = self.data.sensordata[20:34].copy()
        # _tor = self.data.sensordata[34:48].copy()
        _quat = self.data.sensordata[48:52].copy()
        observation = np.hstack((_slot, _sensors, _quat)).astype(np.float32).copy()
        return observation

    def step(self, action):
        action = action * self.M_matrix[:,self.k]

        # xy_position_before = self.data.qpos[0:2].copy()
        xy_position_before = self.data.xpos[1][0:2].copy()

        self.do_simulation(action, self.frame_skip)

        self.k = np.mod(self.k + 1, np.shape(self.M_matrix)[1])

        # xy_position_after = self.data.qpos[0:2].copy()
        xy_position_after = self.data.xpos[1][0:2].copy()

        xy_velocity = (xy_position_after - xy_position_before) / self.dt
        x_velocity, y_velocity = xy_velocity

        observation = self._get_obs()
        forward_reward = 0
        # forward_reward = xy_position_after[0] - np.abs(xy_position_after[1])
        # forward_reward = x_velocity - np.abs(y_velocity)
        # forward_reward = 0.5 * xy_position_after[0] - ((np.abs(xy_position_after[1])+0.15) / (np.abs(xy_position_before[0]) + 0.15) -1) * xy_position_before[0]
        
        terminated = False
        terminated_reward = 0
        if (round(self.data.time / self.timestep) /10) > 10 * np.shape(self.M_matrix)[1]: #Check! MuJoCo 10 Sim-step -> RL 1 action step!
            terminated_reward = 15 * xy_position_after[0] - 5 * np.abs(xy_position_after[1])
            terminated = True

        info = {
            "reward_fwd": forward_reward,
            "x_position": xy_position_after[0],
            "y_position": xy_position_after[1],
            "distance_from_origin": np.linalg.norm(xy_position_after, ord=2),
            "x_velocity": x_velocity,
            "y_velocity": y_velocity,
            "forward_reward": forward_reward,
            "next_gait_slot" : observation[0:14].copy(),
            "accelerometer" : observation[14:17].copy(),
            "gyro" : observation[17:20].copy(),
            "joint_position" : observation[20:34].copy(),
            "head_orientation" : observation[-4:]
        }

        reward = forward_reward + terminated_reward

        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, False, info

    def reset_model(self):
        self.k = 0
        
        noise_low = -0.03
        noise_high = 0.03

        qpos = self.init_qpos + self.np_random.uniform(
        low=noise_low, high=noise_high, size=self.model.nq
        )
        qvel = self.init_qvel + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nv
        )

        self.set_state(qpos, qvel)

        observation = self._get_obs()
        return observation