from typing import Dict, Optional, Tuple, Union
from gymnasium.envs.mujoco.mujoco_env import DEFAULT_SIZE
from horcrux_terrain_v2.envs.gait import Gait

import numpy as np
import pkg_resources

from gymnasium import utils
from gymnasium.envs.mujoco import MujocoEnv
from gymnasium.spaces import Box

from scipy.spatial.transform import Rotation
from scipy.linalg import logm, expm

from collections import deque

DEFAULT_CAMERA_CONFIG = {}

__mjcf_model_path__ = pkg_resources.resource_filename("horcrux_terrain_v2", "resources/horcrux_plane.xml")

# __mjcf_model_path__ = 'horcrux_plane.xml'

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

class MovingAverageFilterQuaternion:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.w_queue = deque(maxlen=window_size)
        self.x_queue = deque(maxlen=window_size)
        self.y_queue = deque(maxlen=window_size)
        self.z_queue = deque(maxlen=window_size)

    def update(self, quat):
        if not (np.linalg.norm(quat) < 1e-8):
            self.w_queue.append(quat[0])
            self.x_queue.append(quat[1])
            self.y_queue.append(quat[2])
            self.z_queue.append(quat[3])
        else:
            self.w_queue.append(1)
            self.x_queue.append(0)
            self.y_queue.append(0)
            self.z_queue.append(0)

        _raw_quat = np.array([self.w_queue, self.x_queue, self.y_queue, self.z_queue]).T

        _rot = Rotation.from_quat(_raw_quat, scalar_first=True)

        _avg_rot = _rot.mean().as_quat(scalar_first=True)

        return _avg_rot

# class MovingAverageFilterQuaternion:
#     def __init__(self, window_size=10):
#         self.window_size = window_size
#         self.quat_queue = deque(maxlen=window_size)  # (x, y, z, w) 형식

#     def update(self, new_quat):  # new_quat: (x, y, z, w) or (4,) ndarray
#         # 부호 일관성 유지
#         if not (np.linalg.norm(new_quat) < 1e-8):
#             if self.quat_queue:
#                 last_quat = self.quat_queue[-1]
#                 if np.dot(last_quat, new_quat) < 0:
#                     new_quat = -new_quat

#             self.quat_queue.append(new_quat)
#         else:
#             self.quat_queue.append(np.array([1, 0, 0, 0]))

#         if len(self.quat_queue) < 2:
#             return Rotation.from_quat(self.quat_queue[-1], scalar_first=True).as_quat(scalar_first=True)  # 초기값은 그대로 반환

#         # 고유값 기반 평균
#         A = np.zeros((4, 4))
#         for q in self.quat_queue:
#             q = q / np.linalg.norm(q)
#             A += np.outer(q, q)
#         A /= len(self.quat_queue)

#         eigvals, eigvecs = np.linalg.eigh(A)
#         avg_quat = eigvecs[:, np.argmax(eigvals)]  # 최대 고유값의 고유벡터

#         if avg_quat[3] < 0:  # w<0이면 부호 반전
#             avg_quat = -avg_quat

#         # scipy는 (x, y, z, w) 형식 사용
#         rot_avg = Rotation.from_quat(avg_quat, scalar_first=True)

#         # print("Quaternion sequence (Euler angles):")
#         for q in self.quat_queue:
#             # print(R.from_quat(q).as_euler('XYZ', degrees=True))
#             pass

#         # print("Averaged (Euler):", rot_avg.as_euler('XYZ', degrees=True))

#         return rot_avg.as_quat(scalar_first=True)


class PlaneJoyWorld(MujocoEnv, utils.EzPickle):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
    }
    def __init__(
            self, 
            model_path = __mjcf_model_path__,
            frame_skip: int = 2, 
            gait_sampling_interval: float = 0.1,
            default_camera_config: Dict[str, Union[float, int]] = DEFAULT_CAMERA_CONFIG,
            forward_reward_weight: float = 60,
            rotation_reward_weight: float = 45,
            termination_reward: float = 0,
            side_cost_weight:float = 60,
            ctrl_cost_weight: float = 0,
            rotation_norm_cost_weight: float = 0.5,
            rotation_orientation_cost_weight: float = 0.05,
            unhealthy_cost_weight: float = 2,
            efficiency_reward_weight: float = 3,
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
            use_imu_window: bool = False,
            **kwargs,
    ):
        utils.EzPickle.__init__(
            self,
            model_path,
            frame_skip,
            gait_sampling_interval,
            default_camera_config,
            forward_reward_weight,
            rotation_reward_weight,
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
            use_imu_window,
            **kwargs,                
        )
        self._gait_sampling_interval = gait_sampling_interval
        self._forward_reward_weight = forward_reward_weight
        self._rotation_reward_weight = rotation_reward_weight
        self.termination_reward = termination_reward
        self._side_cost_weight = side_cost_weight
        self._ctrl_cost_weight = ctrl_cost_weight
        self._rotation_norm_cost_weight = rotation_norm_cost_weight
        self._rotation_orientation_cost_weight = rotation_orientation_cost_weight
        self._unhealthy_cost_weight = unhealthy_cost_weight
        self._efficiency_reward_weight = efficiency_reward_weight
        self._healthy_reward = healthy_reward
        self._healthy_roll_range = healthy_roll_range
        self._terminating_roll_range = terminating_roll_range
        self._contact_force_range = contact_force_range
        self._reset_noise_scale = reset_noise_scale
        self._main_body = main_body
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._use_gait = use_gait
        self._use_friction_chg = use_friction_chg
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
        self._use_imu_mov_mean = use_imu_window
        self._friction_information = [0, 0, 0]

        _temporal_param = max(self._gait_params[2], self._gait_params[3])
        _period = int(np.ceil((_temporal_param) / (2 * np.pi))) * 2
        # self._mov_mean_vels = MovingAverageFilter3D(window_size=_period)
        self._mov_mean_vels = MovingAverageFilter3D(window_size=5)

        # IMU data filter
        self._mov_mean_imu_vel = MovingAverageFilter3D(window_size=5)
        self._mov_mean_imu_acc = MovingAverageFilter3D(window_size=5)
        self._mov_mean_imu_quat = MovingAverageFilterQuaternion(window_size=5)

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

        self._gait = Gait(gait_params, sampling_t = gait_sampling_interval, frame_skip=self.frame_skip)

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
            y, r, p = self._cur_euler_ypr
            min_r, max_r = self._healthy_roll_range
            is_healthy = min_r <= r <= max_r
            return is_healthy
    
    @property
    def is_terminated(self):
            y, r, p = self._cur_euler_ypr
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
        head_quat_before = self.data.body(self._main_body).xmat.copy()
        head_quat_before = np.reshape(head_quat_before, (3,3)).copy()

        if self._n_step < 1:   
            self._initial_rpy = com_rpy_before.copy()
            self._initial_com = com_pos_before.copy()
            self._initial_head_rpy = Rotation.from_matrix(head_quat_before).as_rotvec(True).copy()

        motion_vector = self.motion_vector.copy()
        direction_action = (action * motion_vector).copy()

        self.do_simulation(direction_action, self.frame_skip)

        com_pos_after = self.get_robot_com().copy()
        com_rpy_after = self.get_robot_rot().copy()
        head_quat_after = self.data.body(self._main_body).xmat.copy()
        head_quat_after = np.reshape(head_quat_after, (3,3)).copy()

        self._n_step += 1

        ## 각종 Transformation matrix 생성
        # 원점의 Transformation matrix
        T_0 = np.eye(4)
        T_0[:3, :3] = Rotation.from_rotvec(self._initial_rpy,True).as_matrix()
        T_0[:3, 3] = com_pos_before

        # Before의 Transformation matrix
        T_1 = np.eye(4)
        T_1[:3, :3] = Rotation.from_rotvec(com_rpy_before,True).as_matrix()
        T_1[:3, 3] = com_pos_before

        # After의 Transformation matrix
        T_2 = np.eye(4)
        T_2[:3, :3] = Rotation.from_rotvec(com_rpy_after,True).as_matrix()
        T_2[:3, 3] = com_pos_after

        # Transformation matrix of CoM between two steps
        d_T = np.linalg.inv(T_1) @ T_2
        d_T_p = d_T[:3, 3]
        d_T_r = d_T[:3, :3]

        # # 원점과 T2의 step
        d_T0 = np.linalg.inv(T_0) @ T_2
        d_T0_p = d_T0[:3, 3]
        d_T0_r = d_T0[:3, :3]

        # ## Step before와 Step after를 통해서 구하기
        # x_disp = d_T_p[0]
        # y_disp = d_T_p[1]

        ## Origin과 Step after를 통해서 구하기
        # """
        # 학습 초기에는 이 방법을 통해서 속도를 구하는 것으로 변경했음. 학습 초기에는 뱀 로봇이 원하는 방향으로 잘 움직이지 않는데, 너무 타이트한 속도 조건을 요구하는 것으로 생각됨. 이후 어느정도 뱀 로봇이 조향 방향으로 움직이기 시작하면 Step을 통해서 구해진 속도를 사용하는 것으로 변경할 예정임.
        # """
        x_disp = d_T0_p[0]
        y_disp = d_T0_p[1]

        # 회전의 노름 (회전의 크기) 'ZYX' -> 마지막에 Roll축에 왜곡이 생겨서 다른 방법으로 바꿔야함.
        step_euler_ypr = Rotation.from_matrix(d_T_r).as_euler('ZYX',False).copy()
        self._cur_euler_ypr = Rotation.from_matrix(d_T0_r).as_euler('ZYX',True).copy()

        # 회전의 노름 (회전의 크기) 'ZXY' -> 왜곡 문제 해결을 위해서 XY 순서로 변경
        # step_euler_ypr = Rotation.from_matrix(d_T_r).as_euler('zyx',False).copy() #주의! Yaw Roll Pitch 순서로 저장됨
        # self._cur_euler_ypr = Rotation.from_matrix(d_T0_r).as_euler('zyx',True).copy() #주의! Yaw Roll Pitch 순서로 저장됨

        norm_r = np.linalg.norm(np.array([self._cur_euler_ypr[1], self._cur_euler_ypr[2]])).copy()

        #### Reward 계산을 위한 변수 설정
        tmp_x_vel = x_disp / self.dt
        tmp_y_vel = y_disp / self.dt
        tmp_yaw_vel = step_euler_ypr[0] / self.dt

        x_vel, y_vel, yaw_vel = self._mov_mean_vels.update(tmp_x_vel, tmp_y_vel, tmp_yaw_vel)

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

        info = {
            "step": self._n_step,
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
            "com_pos": com_pos_before,
            "com_ypr": self._cur_euler_ypr,
            "step_ypr": step_euler_ypr,
            "init_rpy": self._initial_rpy,
            "init_com": self._initial_com,
            "init_head_rpy":self._initial_head_rpy,
            "friction_coeff": self._friction_information,
            **reward_info,
        }

        # truncation=False as the time limit is handled by the `TimeLimit` wrapper added during `make`
        return observation, reward, False, terminated, info

    # def _get_rew(self, x_vel, y_vel, joy_x, joy_y, action, norm_r, yaw_vel, joy_r):
    #     """
    #     속도 범위까지 포함된 보상 함수
    #     """
    #     _v_vel = np.array([x_vel, y_vel])
    #     _v_joy = np.array([joy_x, joy_y])
    #     _scale_k = 0.7 # 실제 뱀로봇 속도와 조이스틱 범위 스케일링을 위한 계수
    #     _beta = 1 # 크기 차이에 대한 민감도를 조절하는 계수
    #     _scale_r = 1.5 # 회전에 대한 스케일을 조절하는 계수
    #     _alpha = 1 # 회전에 대한 민감도를 조절하는 계수

    #     if np.linalg.norm(_v_joy) < 1e-1:
    #         forward_direction_reward = self._forward_reward_weight * (1 / (1 + np.linalg.norm(_v_vel)))
    #     else:
    #         forward_direction_reward = self._forward_reward_weight * np.dot(_v_vel, _v_joy) / (np.linalg.norm(_v_vel) * np.linalg.norm(_v_joy) + 1e-6)

        
    #     forward_magnitude_reward = self._forward_reward_weight * np.exp(-_beta * np.abs(np.linalg.norm(_v_vel) - _scale_k * np.linalg.norm(_v_joy)))
    #     rot_reward = self._forward_reward_weight * np.exp(-_alpha * np.abs(yaw_vel - _scale_r * joy_r))
    #     healthy_reward = self.healthy_reward

    #     rewards = forward_direction_reward + forward_magnitude_reward + rot_reward + healthy_reward

    #     ctrl_cost = self.control_cost(action)
    #     unhealthy_cost = self.is_terminated * self._unhealthy_cost_weight
    #     rot_cost = self._rotation_norm_cost_weight * norm_r

    #     costs = ctrl_cost + unhealthy_cost + rot_cost
    #     reward = rewards - costs

    #     reward_info = {
    #          "reward_forward_direction":forward_direction_reward,
    #          "reward_forward_magnitude":forward_magnitude_reward,
    #          "reward_rotation":rot_reward,
    #          "reward_healthy":healthy_reward,
    #          "reward_ctrl":-ctrl_cost,
    #          "reward_unhealthy":-unhealthy_cost,
    #          "reward_rotation":-rot_cost,
    #     }

    #     return reward, reward_info

    # def _get_rew(self, x_vel, y_vel, joy_x, joy_y, action, norm_r, yaw_vel, joy_r):
    #     """
    #     운동 방향만 고려하는 보상함수
    #     """
    #     _v_vel = np.array([x_vel, y_vel])
    #     _v_joy = np.array([joy_x, joy_y])

    #     _linear_magnitude = np.linalg.norm(_v_vel)
    #     _angular_magnitude = np.linalg.norm(yaw_vel)

    #     linear_direction = 0
    #     rotation_direction = 0
    #     yaw_vel_cost_weight = 0

    #     if np.linalg.norm(_v_joy) < 1e-1:
    #         _rew_ctrl_cost_weight = 2 * self._ctrl_cost_weight/(np.linalg.norm(_v_joy) + 1e-1)
    #         linear_direction = 0
    #     else:
    #         _rew_ctrl_cost_weight = self._ctrl_cost_weight / (np.linalg.norm(_v_joy))
    #         linear_direction = self._forward_reward_weight * np.dot(_v_vel, _v_joy) / (np.linalg.norm(_v_vel) * np.linalg.norm(_v_joy) + 1e-6)

    #     if joy_r < 1e-1:
    #         rotation_direction = 0
    #         yaw_vel_cost_weight = 3
    #     else:
    #         rotation_direction = np.sign(joy_r * yaw_vel)

    #     linear_movement_reward = self._forward_reward_weight * linear_direction * _linear_magnitude
    #     angular_movement_reward = self._rotation_reward_weight * rotation_direction * _angular_magnitude * np.abs(joy_r)
        
    #     healthy_reward = self.healthy_reward

    #     rewards = linear_movement_reward + angular_movement_reward + healthy_reward

    #     ctrl_cost = _rew_ctrl_cost_weight * np.sum(action)
    #     unhealthy_cost = self.is_terminated * self._unhealthy_cost_weight
    #     orientation_cost = self._rotation_norm_cost_weight * norm_r
    #     yaw_vel_cost = yaw_vel_cost_weight * np.abs(yaw_vel)

    #     costs = ctrl_cost + unhealthy_cost + orientation_cost + yaw_vel_cost
    #     reward = rewards - costs

    #     reward_info = {
    #          "reward_linear_movement": linear_movement_reward,
    #          "reward_angular_movement": angular_movement_reward,
    #          "reward_healthy":healthy_reward,
    #          "reward_ctrl":-ctrl_cost,
    #          "reward_unhealthy":-unhealthy_cost,
    #          "reward_orientation": -orientation_cost,
    #          "reward_yaw_vel_cost": -yaw_vel_cost,
    #     }

    #     return reward, reward_info
    
    def _get_rew(self, x_vel, y_vel, joy_x, joy_y, action, norm_r, yaw_vel, joy_r):
        """
        ChatGPT 리팩토링 보상함수
        """
        _v_vel = np.array([x_vel, y_vel])
        _v_joy = np.array([joy_x, joy_y])

        # 벡터 크기
        vel_mag = np.linalg.norm(_v_vel)
        joy_mag = np.linalg.norm(_v_joy)
        yaw_mag = np.abs(yaw_vel)

        # 정렬 유사도 (선형)
        if joy_mag > 1e-1 and vel_mag > 1e-1:
            direction_similarity = np.dot(_v_vel, _v_joy) / (vel_mag * joy_mag + 5e-2)
            direction_similarity = np.clip(direction_similarity, 0, 1)
        else:
            direction_similarity = 0.0

        # 선형 움직임 보상
        linear_movement_reward = self._forward_reward_weight * direction_similarity * vel_mag

        # 회전 정렬 보상
        if np.abs(joy_r) > 1e-1 and yaw_mag > 1e-1:
            rotation_alignment = np.sign(joy_r * yaw_vel)
        else:
            rotation_alignment = 0.0

        angular_movement_reward = self._rotation_reward_weight * rotation_alignment * yaw_mag * np.abs(joy_r)

        # 조작 효율성 보상: 적은 조작으로 많은 이동을 유도
        if np.linalg.norm(action) > 1e-3:
            efficiency = direction_similarity * vel_mag / (np.linalg.norm(action) * 1e-2 + 1e-1)
        else:
            efficiency = 0.0

        efficiency_reward = self._efficiency_reward_weight * efficiency

        # 건강 보상
        healthy_reward = self.healthy_reward

        # 보상 총합
        rewards = linear_movement_reward + angular_movement_reward + efficiency_reward + healthy_reward

        # # 비용: 컨트롤, 자세, 회전, 비정상 상태
        # if joy_mag > 1e-1:
        #     ctrl_cost_weight = self._ctrl_cost_weight / joy_mag
        # else:
        #     ctrl_cost_weight = 2 * self._ctrl_cost_weight

        ctrl_cost = self._ctrl_cost_weight * np.sum(action) * (1 / 30)
        unhealthy_cost = self.is_terminated * self._unhealthy_cost_weight
        orientation_cost = self._rotation_norm_cost_weight * norm_r * (1 / 20)
        yaw_cost_weight = 3 if np.abs(joy_r) < 1e-2 else 0
        yaw_vel_cost = yaw_cost_weight * yaw_mag

        costs = ctrl_cost + unhealthy_cost + orientation_cost + yaw_vel_cost
        reward = rewards - costs

        reward_info = {
            "reward_linear_movement": linear_movement_reward,
            "reward_angular_movement": angular_movement_reward,
            "reward_efficiency": efficiency_reward,
            "reward_healthy": healthy_reward,
            "cost_ctrl": -ctrl_cost,
            "cost_unhealthy": -unhealthy_cost,
            "cost_orientation": -orientation_cost,
            "cost_yaw_vel": -yaw_vel_cost,
            "direction_similarity": direction_similarity,
            "rotation_alignment": rotation_alignment,
        }

        return reward, reward_info



    def _get_obs(self, mVec : np.ndarray):
        """
        Mujoco Sensor Tags
        "head_quat": observation[-10:-6].copy(),
        "head_ang_vel": observation[-6:-3].copy(),
        "head_lin_acc": observation[-3::].copy(),
        """

        tmp = self.data.sensordata.copy()

        if self._use_imu_mov_mean:
            tmp[-10:-6] = self._mov_mean_imu_quat.update((self.data.sensordata[-10].copy(), self.data.sensordata[-9].copy(), self.data.sensordata[-8].copy(), self.data.sensordata[-7].copy()))
            tmp[-6:-3] = self._mov_mean_imu_vel.update(self.data.sensordata[-6].copy(), self.data.sensordata[-5].copy(), self.data.sensordata[-4].copy())
            tmp[-3::] = self._mov_mean_imu_acc.update(self.data.sensordata[-3].copy(), self.data.sensordata[-2].copy(), self.data.sensordata[-1].copy())

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
        self._initial_com = np.array([-0.4795,0,0.0350])
        self._cur_euler_ypr = np.array([0,0,0])

        _temporal_param = max(self._gait_params[2], self._gait_params[3])
        _period = int(np.ceil((_temporal_param) / (2 * np.pi))) * 2

        # self._mov_mean_vels = MovingAverageFilter3D(window_size=_period)
        self._mov_mean_vels = MovingAverageFilter3D(window_size=5)

        self._mov_mean_imu_vel = MovingAverageFilter3D(window_size=5)
        self._mov_mean_imu_acc = MovingAverageFilter3D(window_size=5)
        self._mov_mean_imu_quat = MovingAverageFilterQuaternion(window_size=5)


        # Gait reset
        if not(self._use_gait):
            a = np.random.randint(15, 46)
            b = np.random.randint(15, 46)
            c = np.random.randint(10, 71)
            d = np.random.randint(10, 71)
            e = np.random.randint( -46, 46)

            self._gait = Gait((a, b, c, d, e), sampling_t = self._gait_sampling_interval, frame_skip=self._frame_skip)

        # Joy input reset
        if self._joy_input_random:
            self._joy_input = np.array([0, 0, 0])
            while np.linalg.norm(self._joy_input) < 0.5:  # 너무 작은 값 방지

                theta = np.random.uniform(0, 2 * np.pi)  # [0, 2π] 범위의 랜덤 각도
                r = np.sqrt(np.random.uniform(0, 1))  # 제곱근 샘플링을 통해 균등한 분포 생성
                x = r * np.cos(theta)
                y = r * np.sin(theta)

                # self._joy_input = np.array([x, y, np.random.uniform(-1, 1)]) # 회전 속도의 크기도 고려
                self._joy_input = np.array([x, y, 0]) # 회전안함

        # System reset
        # noise_low = -0.05
        # noise_high = 0.05
        noise_low = 0
        noise_high = 0
        noise_qvel = 0
        xpos_low = 0
        xpos_high = 0

        qpos = self.init_qpos + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nq
        )

        qvel = (
            self.init_qvel
            + noise_qvel * self.np_random.standard_normal(self.model.nv)
        )
        x_xpos = self.np_random.uniform(low=xpos_low, high=xpos_high)
        y_xpos = self.np_random.uniform(low=xpos_low, high=xpos_high)

        qpos[0] = x_xpos
        qpos[1] = y_xpos

        if self._use_friction_chg:
            u_slide = round(np.random.uniform(low=0.6, high = 0.8),2)
            u_torsion = round(np.random.uniform(low=0.013, high = 0.017),3)
            u_roll = round(np.random.uniform(low=0.0008, high = 0.0012),4)
            self.model.geom('floor').friction = [u_slide, u_torsion, u_roll]
            self._friction_information = [u_slide, u_torsion, u_roll]

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

    def get_robot_rot(self)->np.ndarray: #Chordal L2 method
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

    # def chordal_mean_rot(self)->np.ndarray: #Chordal L2 method
    #     com_roll = 0
    #     com_pitch = 0
    #     com_yaw = 0

    #     robot_quats = np.empty((0,4))
    #     for name in self._robot_body_names:
    #         robot_quats = np.vstack((robot_quats, self.data.body(name).xquat.copy()))

    #     robot_quats = robot_quats[:, [1, 2, 3, 0]]
    #     robot_rot = Rotation(robot_quats)

    #     com_roll, com_pitch, com_yaw = robot_rot.mean().as_rotvec(True)

    #     return np.array([com_roll, com_pitch, com_yaw])

    # def get_robot_rot(self)->np.ndarray: #Karcher method
    #     com_roll = 0
    #     com_pitch = 0
    #     com_yaw = 0

    #     robot_rots = []
    #     for name in self._robot_body_names:
    #         robot_quats = self.data.body(name).xquat.copy()
    #         link_rot = Rotation.from_quat(robot_quats, scalar_first=True)
    #         robot_rots.append(link_rot)

    #     mean_rot = self.log_exp_karcher_mean(robot_rots)

    #     com_roll, com_pitch, com_yaw = mean_rot.as_rotvec(True)

    #     return np.array([com_roll, com_pitch, com_yaw])
    
    # def log_exp_karcher_mean(self, rot_list, max_iter=100, tol=1e-6):
    #     R_mean = rot_list[0].as_matrix()
    #     for _ in range(max_iter):
    #         delta_sum = np.zeros((3, 3))
    #         for r in rot_list:
    #             delta = logm(r.as_matrix() @ R_mean.T)
    #             delta_sum += delta
    #         delta_avg = delta_sum / len(rot_list)
    #         norm = np.linalg.norm(delta_avg, ord='fro')
    #         R_mean = expm(delta_avg) @ R_mean
    #         if norm < tol:
    #             break
    #     return Rotation.from_matrix(R_mean)

    def do_simulation(self, ctrl, n_frames):
        return super().do_simulation(ctrl, n_frames)