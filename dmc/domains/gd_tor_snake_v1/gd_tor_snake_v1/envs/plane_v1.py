from typing import Dict, Optional, Tuple, Union
from gymnasium.envs.mujoco.mujoco_env import DEFAULT_SIZE

import numpy as np

from gymnasium import utils
from gymnasium.envs.mujoco import MujocoEnv
from gymnasium.spaces import Box, Space

DEFAULT_CAMERA_CONFIG = {
    "distance": 4.0,
}


class PlaneWorld(MujocoEnv, utils.EzPickle):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
    }
    def __init__(
            self, 
            model_path, 
            frame_skip: int = 5, 
            default_camera_config: Dict[str, Union[float, int]] = DEFAULT_CAMERA_CONFIG,
            forward_reward_weight: float = 1,
            ctrl_cost_weight: float = 0.5,
            healthy_reward: float = 1.0,
            main_body: Union[int, str] = 1,
            healthy_roll_range: Tuple[float, float] = (-100, -100),
            contact_force_range: Tuple[float, float] = (-1.0, 1.0),
            reset_noise_scale: float = 0.1,
            **kwargs,
        ):
            utils.EzPickle.__init__(
                self,
                model_path,
                frame_skip,
                default_camera_config,
                forward_reward_weight,
                ctrl_cost_weight,
                healthy_reward,
                main_body,
                healthy_roll_range,
                contact_force_range,
                reset_noise_scale,
                **kwargs,                
            )

            self._forward_reward_weight = forward_reward_weight
            self._ctrl_cost_weight = ctrl_cost_weight
            self._healthy_reward = healthy_reward
            self._healthy_roll_range = healthy_roll_range
            self._contact_force_range = contact_force_range
            self._reset_noise_scale = reset_noise_scale
            self._main_body = main_body

            MujocoEnv.__init__(
                  self,
                  model_path,
                  frame_skip,
                  observation_space = None, # define later
                  default_camera_config = default_camera_config,
                  **kwargs,
            )

            self.metadata = {
                "render_modes": [
                    "human",
                    "rgb_array",
                    "depth_array",
                ],
                "render_fps": int(np.round(1.0 / self.dt)),
            }

            obs_size = self.data.sensordata.size

            self.observation_space = Box(
                  low=-40, high= 40, shape=(obs_size,), dtype=np.float64
            )

            self.observation_structure = {
                  "jpos":self.data.sensordata[:14],
                  "jvel":self.data.sensordata[14:28],
                  "head_orientation":self.data.sensordata[28:32],
                  "head_angvel":self.data.sensordata[32:35],
                  "head_linacc":self.data.sensordata[35:38],
            }

    pass