from typing import Dict, Optional, Tuple, Union
from gymnasium.envs.mujoco.mujoco_env import DEFAULT_SIZE
from gd_tor_snake_v1.envs.gait import Gait

import numpy as np
import os
import pathlib

from gymnasium import utils
from gymnasium.envs.mujoco import MujocoEnv
from gymnasium.spaces import Box
from numpy import float64
from numpy.typing import NDArray

from scipy.spatial.transform import Rotation

DEFAULT_CAMERA_CONFIG = {}

__pkg_dir__ = pathlib.Path(os.path.dirname(__file__))
__resource_dir__ = os.path.join(__pkg_dir__.parent,'resources')
__mjcf_model_path__ = os.path.join(__resource_dir__, 'env_snake_v1.xml')

class PlaneWorld(MujocoEnv, utils.EzPickle):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
        "render_fps":10 # For gymnasium 0.28.1
    }
    def __init__(
            self, 
            model_path = __mjcf_model_path__,
            frame_skip: int = 20, 
            default_camera_config: Dict[str, Union[float, int]] = DEFAULT_CAMERA_CONFIG,
            forward_reward_weight: float = 2,
            side_cost_weight:float = 1.1,
            ctrl_cost_weight: float = 0.1,
            healthy_reward: float = 0.1,
            main_body: Union[int, str] = 2,
            render_camera_name = "ceiling",
            terminate_when_unhealthy: bool = False,
            healthy_roll_range: Tuple[float, float] = (-100, 100),
            contact_force_range: Tuple[float, float] = (-1.0, 1.0),
            reset_noise_scale: float = 0.03,
            use_gait: bool = False,
            gait_params: Tuple[float, float, float, float, float] = (30, 30, 40, 40, 0),
            **kwargs,
    ):
        utils.EzPickle.__init__(
            self,
            model_path,
            frame_skip,
            default_camera_config,
            forward_reward_weight,
            side_cost_weight,
            ctrl_cost_weight,
            healthy_reward,
            main_body,
            render_camera_name,
            terminate_when_unhealthy,
            healthy_roll_range,
            contact_force_range,
            reset_noise_scale,
            use_gait,
            gait_params,
            **kwargs,                
        )

        self._forward_reward_weight = forward_reward_weight
        self._side_cost_weight = side_cost_weight
        self._ctrl_cost_weight = ctrl_cost_weight
        self._healthy_reward = healthy_reward
        self._healthy_roll_range = healthy_roll_range
        self._contact_force_range = contact_force_range
        self._reset_noise_scale = reset_noise_scale
        self._main_body = main_body
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._use_gait = use_gait
        self._gait = Gait(gait_params)
        self._k = 0
        self._robot_body_names = ["head","link1","link2","link3","link4","link5","link6","link7","link8","link9","link10","link11","link12","link13","tail"]

        MujocoEnv.__init__(
                self,
                model_path,
                frame_skip,
                width=1280,
                height=720,
                observation_space = None, # define later
                default_camera_config = default_camera_config,
                camera_name = render_camera_name,
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

        obs_size = self.data.sensordata.size + 14

        self.observation_space = Box(
                low=-np.inf, high= np.inf, shape=(obs_size,), dtype=np.float64
        )

        self.action_space = Box(
                low=0, high=1.5, shape=(14,), dtype=np.float32
        )

        self.motion_vector = np.array([0] * 14)
        self.observation_structure = {
                "jpos":self.data.sensordata[:14],
                "jvel":self.data.sensordata[14:28],
                "head_orientation":self.data.sensordata[28:32],
                "head_angvel":self.data.sensordata[32:35],
                "head_linacc":self.data.sensordata[35:38],
                "motion_vector":self.motion_vector,
        }

    @property
    def healthy_reward(self):
            return self.is_healthy * self._healthy_reward
    
    @property
    def is_healthy(self):
            _q_head_orientation = Rotation([self.data.sensordata[29],self.data.sensordata[30],self.data.sensordata[31],self.data.sensordata[28]])
            r, p, y = _q_head_orientation.as_rotvec(True)
            min_r, max_r = self._healthy_roll_range
            is_healthy = min_r <= r <= max_r
            return is_healthy
    
    def control_cost(self, action):
         control_cost = self._ctrl_cost_weight * np.sum(np.square(action))
         return control_cost
            
    def step(self, action):
        xy_head_pos_before = self.data.body(self._main_body).xpos[:2].copy()
        head_quat_before = self.data.body(self._main_body).xquat.copy()
        rpy_before = Rotation([head_quat_before[1], head_quat_before[2], head_quat_before[3], head_quat_before[0]]).as_rotvec(False)
        
        com_pos_before = self.get_robot_com()
        com_rpy_before = self.get_robot_rot()

        motion_vector = self.motion_vector
        direction_action = action * motion_vector

        self.do_simulation(direction_action, self.frame_skip)

        xy_head_pos_after = self.data.body(self._main_body).xpos[:2].copy()
        head_quat_after = self.data.body(self._main_body).xquat.copy()
        rpy_after = Rotation([head_quat_after[1], head_quat_after[2], head_quat_after[3], head_quat_after[0]]).as_rotvec(False)

        com_pos_after = self.get_robot_com()
        com_rpy_after = self.get_robot_rot()

        # ## Head based
        # forward_dist = np.linalg.norm(xy_head_pos_after - xy_head_pos_before)

        # d_yaw = rpy_after[2] - rpy_before[2]
        # x_disp = forward_dist * np.cos(d_yaw)
        # y_disp = forward_dist * np.sin(d_yaw)

        # x_vel = x_disp / self.dt
        # y_vel = y_disp / self.dt

        ## COM based
        forward_dist = np.linalg.norm(com_pos_after - com_pos_before)

        d_yaw = com_rpy_after[2] - com_rpy_before[2]
        x_disp = forward_dist * np.cos(d_yaw)
        y_disp = forward_dist * np.sin(d_yaw)

        x_vel = x_disp / self.dt
        y_vel = y_disp / self.dt
        
        if self._use_gait:
            self.motion_vector = self._gait.getMvec(self._k)
            self._k += 1
        else:
            self.motion_vector = np.random.choice([-1, 1], size=14)
        
        observation = self._get_obs(motion_vector)
        reward, reward_info = self._get_rew(x_vel, y_vel, action)
        terminated = (not self.is_healthy) and self._terminate_when_unhealthy
        info = {
            "x_displacement": x_disp,
            "y_displacement": y_disp,
            "distance_from_origin": np.linalg.norm(self.data.qpos[0:2], ord=2),
            "x_velocity": x_vel,
            "y_velocity": y_vel,
            **reward_info,
        }

        if self.render_mode == "human":
            self.render()
        # truncation=False as the time limit is handled by the `TimeLimit` wrapper added during `make`
        return observation, reward, terminated, False, info

    def _get_rew(self, x_vel, y_vel, action):
        forward_reward = x_vel * self._forward_reward_weight
        healthy_reward = self.healthy_reward

        rewards = forward_reward + healthy_reward

        ctrl_cost = self.control_cost(action)
        side_cost = np.abs(y_vel) * self._side_cost_weight

        costs = ctrl_cost + side_cost

        reward = rewards - costs

        reward_info = {
             "reward_forward":forward_reward,
             "reward_healthy":healthy_reward,
             "reward_ctrl":-ctrl_cost,
             "reward_side":-side_cost,
        }

        return reward, reward_info


    def _get_obs(self, mVec : np.ndarray):
          return np.concatenate((self.data.sensordata.flatten(), mVec))
    
    def reset_model(self):
        noise_low = -self._reset_noise_scale
        noise_high = self._reset_noise_scale

        qpos = self.init_qpos + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nq
        )
        qvel = (
            self.init_qvel
            + self._reset_noise_scale * self.np_random.standard_normal(self.model.nv)
        )
        self.set_state(qpos, qvel)

        observation = self._get_obs(np.array([0] * 14))

        return observation
    
    def get_robot_com(self)->np.ndarray:
        accum_x = 0
        accum_y = 0
        len_names = len(self._robot_body_names)

        for name in self._robot_body_names:
            x, y, _ = self.data.body(name).xpos
            accum_x = accum_x + x
            accum_y = accum_y + y

        return np.array([accum_x / len_names, accum_y / len_names])

    def get_robot_rot(self)->np.ndarray:
        com_roll = 0
        com_pitch = 0
        com_yaw = 0

        robot_quats = np.empty((0,4))
        for name in self._robot_body_names:
            robot_quats = np.vstack((robot_quats, self.data.body(name).xquat))

        robot_quats = robot_quats[:, [1, 2, 3, 0]]
        robot_rot = Rotation(robot_quats)

        com_roll, com_pitch, com_yaw = robot_rot.mean().as_rotvec(False)

        return np.array([com_roll, com_pitch, com_yaw])
