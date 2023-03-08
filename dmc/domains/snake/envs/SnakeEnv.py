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
    "render_fps": 25,
    }

    def __init__(self, frame_skip = 4, **kwargs) -> None:
        # Action Space
        self.action_space = spaces.Box(low= -3.0, high= 3.0, shape=(14,))

        # Observation Space
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(62,), dtype=np.float64) # M_col and 48 sensordatas -> 14 + 48 => 62

        # Create mujoco env instance
        MujocoEnv.__init__(self, os.path.join(__model_location__,'snake_circle_alligned.xml'), frame_skip, observation_space= self.observation_space, **kwargs)

        # Physics variables
        self.k = 0
        self.action_frequency = 0.1
        self.timestep = self.model.opt.timestep
        self.time = self.data.time

        # Make gait motion matrix
        ### Gait parameters
        b = 0
        b2 = 0

        a = np.radians(30)
        a2 = np.radians(15)

        e_d1 = np.radians(15)
        e_l1 = np.radians(15)

        e_d2 = 1
        e_l2 = 1

        delta = np.radians(45)

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
        slot = self.M_matrix[:,self.k]
        sensors = self.data.sensordata[0:48]
        observation = np.hstack((slot, sensors))

        return observation

    def step(self, action):
        
        xy_position_before = self.data.qpos[0:2].copy()
        self.do_simulation(action, self.frame_skip)
        self.k = np.mod(self.k + 1, np.shape(self.M_matrix)[1])

        xy_position_after = self.data.qpos[0:2].copy()

        xy_velocity = (xy_position_after - xy_position_before) / self.dt
        x_velocity, y_velocity = xy_velocity

        forward_reward = x_velocity - np.abs(xy_position_after[1])

        observation = self._get_obs()
        reward = forward_reward
        info = {
            "reward_fwd": forward_reward,
            "x_position": xy_position_after[0],
            "y_position": xy_position_after[1],
            "distance_from_origin": np.linalg.norm(xy_position_after, ord=2),
            "x_velocity": x_velocity,
            "y_velocity": y_velocity,
            "forward_reward": forward_reward,
        }

        if self.render_mode == "human":
            self.render()

        terminated = False
        if round(self.data.time / self.timestep) > 10 * np.shape(self.M_matrix)[1]:
            terminated = True

        return observation, reward, terminated, False, info

    def reset_model(self):
        self.k = 0
        
        noise_low = -0.05
        noise_high = 0.05

        qpos = self.init_qpos + self.np_random.uniform(
        low=noise_low, high=noise_high, size=self.model.nq
        )
        qvel = self.init_qvel + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nv
        )

        self.set_state(qpos, qvel)

        observation = self._get_obs()
        return observation