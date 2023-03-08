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
        # k-th slot
        self.k = 0

        # Action Space
        self.action_space = spaces.Box(low= -3.0, high= 3.0, shape=(14,))

        # Observation Space
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(49,), dtype=np.float64) # k slot and 48 sensordatas


        MujocoEnv.__init__(self, os.path.join(__model_location__,'snake_circle_alligned.xml'), frame_skip, observation_space= self.observation_space, **kwargs)

    def _get_obs(self):
        slot = np.array(self.k)
        sensors = self.data.sensordata[0:48]
        observation = np.hstack((slot, sensors))

        return observation

    def step(self, action):
        xy_position_before = self.data.qpos[0:2].copy()
        self.do_simulation(action, self.frame_skip)
        self.k = self.k + 1
        xy_position_after = self.data.qpos[0:2].copy()

        xy_velocity = (xy_position_after - xy_position_before) / self.dt
        x_velocity, y_velocity = xy_velocity

        forward_reward = x_velocity

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

        return observation, reward, False, False, info

    def reset_model(self):
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