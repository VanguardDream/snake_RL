from typing import Dict, Optional, Tuple, Union
from gymnasium.envs.mujoco.mujoco_env import DEFAULT_SIZE
from horcrux_terrain_v1.envs.gait import Gait

import numpy as np
import os
import pathlib
import pkg_resources

from gymnasium import utils
from gymnasium.envs.mujoco import MujocoEnv
from gymnasium.spaces import Box

from scipy.spatial.transform import Rotation

from collections import deque

DEFAULT_CAMERA_CONFIG = {}

# __pkg_dir__ = pathlib.Path(os.path.dirname(__file__))
# __resource_dir__ = os.path.join(__pkg_dir__.parent,'resources')
# __mjcf_model_path__ = os.path.join(__resource_dir__, 'horcrux_sand.xml')

__mjcf_model_path__ = pkg_resources.resource_filename("horcrux_terrain_v1", "resources/horcrux_plane.xml")

class MovingAverageFilter3D:
    def __init__(self, window_size=20):
        self.window_size = window_size
        self.x_queue = deque(maxlen=window_size)
        self.y_queue = deque(maxlen=window_size)
        self.z_queue = deque(maxlen=window_size)

    def update(self, new_x, new_y, new_z):
        self.x_queue.append(new_x)
        self.y_queue.append(new_y)
        self.z_queue.append(new_z)

        avg_x = np.mean(self.x_queue) if self.x_queue else 0.0
        avg_y = np.mean(self.y_queue) if self.y_queue else 0.0
        avg_z = np.mean(self.z_queue) if self.z_queue else 0.0

        return avg_x, avg_y, avg_z

class PlaneJoyWorld(MujocoEnv, utils.EzPickle):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
        "render_fps" : 10 # For gymnasium 0.28.1
    }
    def __init__(
            self, 
            model_path = __mjcf_model_path__,
            frame_skip: int = 20, 
            default_camera_config: Dict[str, Union[float, int]] = DEFAULT_CAMERA_CONFIG,
            forward_reward_weight: float = 60,
            termination_reward: float = 0,
            side_cost_weight:float = 60,
            ctrl_cost_weight: float = 0,
            rotation_norm_cost_weight: float = 0.1,
            rotation_orientation_cost_weight: float = 0.05,
            unhealthy_cost_weight: float = 1,
            healthy_reward: float = 2,
            main_body: Union[int, str] = 2,
            render_camera_name = "ceiling",
            terminate_when_unhealthy: bool = True,
            unhealthy_max_steps: int = 30,
            healthy_roll_range: Tuple[float, float] = (-45, 45),
            terminating_roll_range: Tuple[float, float] = (-120, 120),
            contact_force_range: Tuple[float, float] = (-1.0, 1.0),
            reset_noise_scale: float = 0.1,
            use_gait: bool = True,
            use_friction_chg: bool = False,
            joy_input_random: bool = True,
            joy_input: Union[float, float, float] = (0, 0, 0), # X axis velocity, Y axis velocity, Yaw angular velocity
            gait_params: Tuple[float, float, float, float, float] = (30, 30, 40, 40, 0),
            **kwargs,
    ):
        utils.EzPickle.__init__(
            self,
            model_path,
            frame_skip,
            default_camera_config,
            forward_reward_weight,
            termination_reward,
            side_cost_weight,
            ctrl_cost_weight,
            rotation_norm_cost_weight,
            unhealthy_cost_weight,
            healthy_reward,
            main_body,
            render_camera_name,
            terminate_when_unhealthy,
            unhealthy_max_steps,
            healthy_roll_range,
            terminating_roll_range,
            contact_force_range,
            reset_noise_scale,
            use_gait,
            use_friction_chg,
            joy_input_random,
            joy_input,
            gait_params,
            **kwargs,                
        )

        self._forward_reward_weight = forward_reward_weight
        self.termination_reward = termination_reward
        self._side_cost_weight = side_cost_weight
        self._ctrl_cost_weight = ctrl_cost_weight
        self._rotation_norm_cost_weight = rotation_norm_cost_weight
        self._rotation_orientation_cost_weight = rotation_orientation_cost_weight
        self._unhealthy_cost_weight = unhealthy_cost_weight
        self._healthy_reward = healthy_reward
        self._healthy_roll_range = healthy_roll_range
        self._terminating_roll_range = terminating_roll_range
        self._contact_force_range = contact_force_range
        self._reset_noise_scale = reset_noise_scale
        self._main_body = main_body
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._use_gait = use_gait
        self._use_friction_chg = use_friction_chg
        self._gait = Gait(gait_params)
        self._gait_params = gait_params
        self._k = 0
        self._unhealthy_max_steps = unhealthy_max_steps
        self._unhealth_steps = 0
        self._robot_body_names = ["link1","link2","link3","link4","link5","link6","link7","link8","link9","link10","link11","link12","link13","link14","link15"]
        self._n_step = 0
        self._initial_com = np.array([0,0,0])
        self._initial_rpy = np.array([0,0,0])
        self._initial_head_rpy = np.array([0,0,0])
        self._cur_euler_ypr = np.array([0,0,0])
        self._joy_input = np.array(joy_input)
        self._joy_input_random = joy_input_random

        _temporal_param = max(self._gait_params[2], self._gait_params[3])
        _period = int(np.ceil((_temporal_param) / (2 * np.pi))) * 2
        self._mov_mean = MovingAverageFilter3D(window_size=_period)


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

        obs_size = self.data.sensordata.size + 14 + 3 ## Motion vector + Joy input

        self.observation_space = Box(
                low=-np.inf, high= np.inf, shape=(obs_size,)
        )

        self.action_space = Box(
                low=0, high=2.7, shape=(14,)
        )

        self.motion_vector = np.array([0] * 14)
        self.observation_structure = {
                "jpos":self.data.sensordata[:14], #14
                "jvel":self.data.sensordata[14:28], #14
                "jtor":self.data.sensordata[28:42], #14
                "link_contacts_top":self.data.sensordata[42:56], #14
                "link_contacts_bot":self.data.sensordata[56:70], #14
                "head_orientation":self.data.sensordata[70:74], #4
                "head_angvel":self.data.sensordata[74:77], #3
                "head_linacc":self.data.sensordata[77:80], #3
                "motion_vector":self.motion_vector, #14
                "joy_input":self._joy_input, #3
        }

    @property
    def healthy_reward(self):          
            return self.is_healthy * self._healthy_reward
    
    @property
    def is_healthy(self):
            y, p, r = self._cur_euler_ypr
            min_r, max_r = self._healthy_roll_range
            is_healthy = min_r <= r <= max_r
            return is_healthy
    
    @property
    def is_terminated(self):
            y, p, r = self._cur_euler_ypr
            t_min_r, t_max_r = self._terminating_roll_range
            is_not_over = t_min_r <= r <= t_max_r

            is_done = False
            if is_not_over:
                self._unhealth_steps = 0
            else:
                self._unhealth_steps += 1

            if self._unhealth_steps >= self._unhealthy_max_steps:
                is_done = True

            return is_done
    
    def control_cost(self, action):
         control_cost = self._ctrl_cost_weight * np.sum(action)
         return control_cost
            
    def step(self, action):
        com_pos_before = self.get_robot_com().copy()
        com_rpy_before = self.get_robot_rot().copy()
        head_pos_before = self.data.body('link1').xpos.copy()
        head_quat_before = self.data.body(self._main_body).xmat.copy()
        head_quat_before = np.reshape(head_quat_before, (3,3)).copy()

        if self._n_step == 0:   
            self._initial_rpy = com_rpy_before.copy()
            self._initial_com = com_pos_before.copy()
            self._initial_head_rpy = Rotation.from_matrix(head_quat_before).as_rotvec(True).copy()

        motion_vector = self.motion_vector.copy()
        direction_action = (action * motion_vector).copy()

        self.do_simulation(direction_action, self.frame_skip)

        com_pos_after = self.get_robot_com().copy()
        com_rpy_after = self.get_robot_rot().copy()
        head_pos_after = self.data.body('link1').xpos.copy()
        head_quat_after = self.data.body(self._main_body).xmat.copy()
        head_quat_after = np.reshape(head_quat_after, (3,3)).copy()

        self._n_step += 1

        ## 각종 Transformation matrix 생성
        # 원점의 Transformation matrix
        T_0 = np.eye(4)
        T_0[:3, :3] = Rotation.from_rotvec(self._initial_rpy,True).as_matrix()
        # T_0[:3, 3] = self._initial_com
        T_0[:3, 3] = com_pos_before

        # Before의 Transformation matrix
        T_1 = np.eye(4)
        T_1[:3, :3] = Rotation.from_rotvec(com_rpy_before,True).as_matrix()
        T_1[:3, 3] = com_pos_before

        # After의 Transformation matrix
        T_2 = np.eye(4)
        T_2[:3, :3] = Rotation.from_rotvec(com_rpy_after,True).as_matrix()
        T_2[:3, 3] = com_pos_after

        # # Head Before의 Transformation matrix
        # T_head_1 = np.eye(4)
        # T_head_1[:3, :3] = Rotation.from_matrix(head_quat_before).as_matrix()
        # T_head_1[:3, 3] = head_pos_before

        # # Head After의 Transformation matrix
        # T_head_2 = np.eye(4)
        # T_head_2[:3, :3] = Rotation.from_matrix(head_quat_after).as_matrix()
        # T_head_2[:3, 3] = head_pos_after

        # Transformation matrix of CoM between two steps
        d_T = np.linalg.inv(T_1) @ T_2
        d_T_p = d_T[:3, 3]
        d_T_r = d_T[:3, :3]

        # # 원점과 T2의 step
        d_T0 = np.linalg.inv(T_0) @ T_2
        d_T0_p = d_T0[:3, 3]
        d_T0_r = d_T0[:3, :3]

        # # Head Before와 Head After의 step
        # d_T_head = np.linalg.inv(T_head_1) @ T_head_2
        # d_T_head_p = d_T_head[:3, 3]
        # d_T_head_r = d_T_head[:3, :3]

        #### Reward를 위한 선형 변위 정의
        ## CoM의 Step에서의 변위로 구하기
        # x_disp = d_T_p[0]
        # y_disp = d_T_p[1]

        # ## Origin과 Step after를 통해서 구하기
        x_disp = d_T0_p[0]
        y_disp = d_T0_p[1]

        ## Head의 변위로 구하기
        # x_disp = d_T_head_p[0]
        # y_disp = d_T_head_p[1]

        ## CoM 좌표 그래로 사용
        # x_disp = com_pos_after[0] - com_pos_before[0]
        # y_disp = com_pos_after[1] - com_pos_before[1]

        #### Reward를 위한 회전 변위 정의

        # 회전의 노름 (회전의 크기)
        euler_r = Rotation.from_matrix(d_T_r).as_euler('ZYX',False).copy()
        norm_r = np.linalg.norm(np.array([euler_r[1], euler_r[2]])).copy()
        self._cur_euler_ypr = Rotation.from_matrix(d_T0_r).as_euler('ZYX',True).copy()

        #### Reward 계산을 위한 변수 설정
        tmp_x_vel = x_disp / self.dt
        tmp_y_vel = y_disp / self.dt
        tmp_yaw_vel = euler_r[0] / self.dt

        x_vel, y_vel, yaw_vel = self._mov_mean.update(tmp_x_vel, tmp_y_vel, tmp_yaw_vel)

        # ## Gait changing...
        self._k += 1
        self.motion_vector = self._gait.getMvec(self._k)
        
        observation = self._get_obs(motion_vector)
        reward, reward_info = self._get_rew(x_vel, y_vel, self._joy_input[0], self._joy_input[1], action, norm_r, yaw_vel, self._joy_input[2])
        terminated = self.is_terminated and self._terminate_when_unhealthy

        if self.render_mode == "human":
            self.render()

        if self._n_step >= 6000:
            terminated = True

        if terminated:
            terminated_forward = 0
            # Termination reward
            if self.termination_reward > 0:
                T_origin = np.eye(4)
                T_origin[:3, 3] = self._initial_com
                T_origin[:3, :3] = Rotation.from_rotvec(self._initial_rpy,True).as_matrix()

                d_T_origin = np.linalg.inv(T_origin) @ T_2
                d_T_origin_p = d_T_origin[:3, 3]

                # terminated_forward = d_T_origin_p[0] * 150
                # 종료 보상 안씀
                terminated_forward = 0

            if self.render_mode == "human":
                print(terminated_forward)

            reward = reward + terminated_forward

        info = {
            "x_displacement": x_disp,
            "y_displacement": y_disp,
            "distance_from_origin": np.linalg.norm(self.data.qpos[0:2], ord=2),
            "x_velocity": x_vel,
            "y_velocity": y_vel,
            "yaw_velocity": yaw_vel,
            "joint_pos": observation[:14].copy(),
            "joint_vel": observation[-41:-27].copy(),
            "head_quat": observation[-27:-23].copy(),
            "head_ang_vel": observation[-23:-20].copy(),
            "head_lin_acc": observation[-20:-17].copy(),
            "motion_vector": observation[-17:-3].copy(),
            "joy_input": observation[-3:].copy(),
            # "head_rpy": rpy_after,
            "com_pos": com_pos_before,
            # "com_rpy": com_rpy_after,
            "com_ypr": self._cur_euler_ypr,
            "step_ypr": euler_r,
            # "step_p": np.transpose(d_T0_p),
            "init_rpy": self._initial_rpy,
            "init_com": self._initial_com,
            "init_head_rpy":self._initial_head_rpy,
            **reward_info,
        }

        # truncation=False as the time limit is handled by the `TimeLimit` wrapper added during `make`
        return observation, reward, terminated, False, info

    def _get_rew(self, x_vel, y_vel, joy_x, joy_y, action, norm_r, yaw_vel, joy_r):
        _v_vel = np.array([x_vel, y_vel])
        _v_joy = np.array([joy_x, joy_y])
        _scale_k = 0.7 # 실제 뱀로봇 속도와 조이스틱 범위 스케일링을 위한 계수
        _beta = 1 # 크기 차이에 대한 민감도를 조절하는 계수
        _scale_r = 1.5 # 회전에 대한 스케일을 조절하는 계수
        _alpha = 1 # 회전에 대한 민감도를 조절하는 계수

        if np.linalg.norm(_v_joy) < 1e-1:
            forward_direction_reward = self._forward_reward_weight * (1 / (1 + np.linalg.norm(_v_vel)))
        else:
            forward_direction_reward = self._forward_reward_weight * np.dot(_v_vel, _v_joy) / (np.linalg.norm(_v_vel) * np.linalg.norm(_v_joy) + 1e-6)

        
        forward_magnitude_reward = self._forward_reward_weight * np.exp(-_beta * np.abs(np.linalg.norm(_v_vel) - _scale_k * np.linalg.norm(_v_joy)))
        rot_reward = self._forward_reward_weight * np.exp(-_alpha * np.abs(yaw_vel - _scale_r * joy_r))
        healthy_reward = self.healthy_reward

        rewards = forward_direction_reward + forward_magnitude_reward + rot_reward + healthy_reward

        ctrl_cost = self.control_cost(action)
        unhealthy_cost = self.is_terminated * self._unhealthy_cost_weight
        rot_cost = self._rotation_norm_cost_weight * norm_r

        costs = ctrl_cost + unhealthy_cost + rot_cost
        reward = rewards - costs

        reward_info = {
             "reward_forward_direction":forward_direction_reward,
             "reward_forward_magnitude":forward_magnitude_reward,
             "reward_rotation":rot_reward,
             "reward_healthy":healthy_reward,
             "reward_ctrl":-ctrl_cost,
             "reward_unhealthy":-unhealthy_cost,
             "reward_rotation":-rot_cost,
        }

        return reward, reward_info


    def _get_obs(self, mVec : np.ndarray):
        tmp = self.data.sensordata.copy()
        tmp[42:56] = (tmp[42:56]>1).astype(int)
        tmp[56:70] = (tmp[56:70]>1).astype(int)
        return np.concatenate((tmp.flatten(), mVec, self._joy_input), dtype=np.float32)
    
    def reset_model(self):
        # Unhealthy step reset
        self._n_step = 0
        self._k = 0
        self._unhealth_steps = 0
        self._initial_rpy = np.array([0,0,0])
        self._initial_head_rpy = np.array([0,0,0])
        self._initial_com = np.array([0,0,0])
        self._cur_euler_ypr = np.array([0,0,0])

        _temporal_param = max(self._gait_params[2], self._gait_params[3])
        _period = int(np.ceil((_temporal_param) / (2 * np.pi))) * 2
        self._mov_mean = MovingAverageFilter3D(window_size=_period)


        # Gait reset
        if not(self._use_gait):
            a = np.random.randint(15, 46)
            b = np.random.randint(15, 46)
            c = np.random.randint(10, 71)
            d = np.random.randint(10, 71)
            e = np.random.randint( -46, 46)

            self._gait = Gait((a, b, c, d, e))

        # Joy input reset
        if self._joy_input_random:
            self._joy_input = np.array([0, 0, 0])
            while np.linalg.norm(self._joy_input) < 0.2:  # 너무 작은 값 방지

                theta = np.random.uniform(0, 2 * np.pi)  # [0, 2π] 범위의 랜덤 각도
                r = np.sqrt(np.random.uniform(0, 1))  # 제곱근 샘플링을 통해 균등한 분포 생성
                x = r * np.cos(theta)
                y = r * np.sin(theta)

                self._joy_input = np.array([x, y, np.random.uniform(-1, 1)])

        # System reset
        noise_low = -0.05
        noise_high = 0.05
        xpos_low = 0
        xpos_high = 0

        qpos = self.init_qpos + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nq
        )

        # random_rpy = [0, 0, float(self.np_random.uniform(low=-180,high=180,size=1))]
        # random_rpy = np.array(random_rpy)
        # _reset_rotation = Rotation.from_rotvec(random_rpy,True).as_quat()
        # qpos[3:7] = [_reset_rotation[3], _reset_rotation[0], _reset_rotation[1], _reset_rotation[2]]

        qvel = (
            self.init_qvel
            + 0.01 * self.np_random.standard_normal(self.model.nv)
        )
        x_xpos = self.np_random.uniform(low=xpos_low, high=xpos_high)
        y_xpos = self.np_random.uniform(low=xpos_low, high=xpos_high)

        qpos[0] = x_xpos
        qpos[1] = y_xpos

        if self._use_friction_chg:
            u_slide = round(np.random.uniform(low=0.5, high = 1.0),3)
            u_torsion = round(np.random.uniform(low=0.01, high = 0.06),3)
            u_roll = round(np.random.uniform(low=0.001, high = 0.03),3)
            self.model.geom('floor').friction = [u_slide, u_torsion, u_roll]

        self.set_state(qpos, qvel)

        observation = self._get_obs(np.array([1] * 14))

        return observation
    
    def get_robot_com(self)->np.ndarray:
        accum_x = 0
        accum_y = 0
        accum_z = 0
        len_names = len(self._robot_body_names)

        for name in self._robot_body_names:
            x, y, z = self.data.body(name).xpos
            accum_x = accum_x + x
            accum_y = accum_y + y
            accum_z = accum_z + z

        return np.array([accum_x / len_names, accum_y / len_names, accum_z / len_names])

    def get_robot_rot(self)->np.ndarray:
        com_roll = 0
        com_pitch = 0
        com_yaw = 0

        robot_quats = np.empty((0,4))
        for name in self._robot_body_names:
            robot_quats = np.vstack((robot_quats, self.data.body(name).xquat.copy()))

        robot_quats = robot_quats[:, [1, 2, 3, 0]]
        robot_rot = Rotation(robot_quats)

        com_roll, com_pitch, com_yaw = robot_rot.mean().as_rotvec(True)

        return np.array([com_roll, com_pitch, com_yaw])
