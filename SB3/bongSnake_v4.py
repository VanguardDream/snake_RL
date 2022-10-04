# © 2022 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Date : 2022-09-29 (YYYYMMDD)
# Version : 2022-08-04
# Description : Bong Snake Env for Gym with torque gait class

import mujoco_py
import numpy as np
from space_enums import *
from gym import utils
from gym.spaces import *
from gym.envs.mujoco import mujoco_env

from scipy.spatial.transform import Rotation as Rot

class bongEnv_v4(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(
        self,
        xml_file="snake_circle.xml",
        healthy_reward=1.0,
        terminate_when_unhealthy=True,
        healthy_roll_range=(-45,45),
        healthy_pitch_range=(-30,30),
        healthy_yaw_range=(-45,45),
        render_option = False,
    ):
        self._healthy_reward = healthy_reward
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._healthy_roll_range = healthy_roll_range
        self._healthy_pitch_range = healthy_pitch_range
        self._healthy_yaw_range = healthy_yaw_range
        self._mujoco_exception_occured = False

        #Render Option
        self.render_option = render_option

        #Spaces
        self.action_space = MultiDiscrete([3,3,3,3,3, 3,3,3,3,3, 3,3,3,3]) # {0,1,2} 세트임..
        self.observation_space = Box(-np.ones(14),np.ones(14)) 
        
        ### 원노트 2022년 9월 30일 노트 확인 + 모든 데이터 0~1 정규화 진행할 것
        # 위치 값 제약 -10m ~ 10m
        # 각도 -3.14 ~ 3.14

        #Parent class initialize
        utils.EzPickle.__init__(**locals())
        mujoco_env.MujocoEnv.__init__(self, xml_file, 10,observation_space=self.observation_space)
        
        if self.render_option:
            self.viewer = mujoco_py.MjViewer(self.sim)
        



        


    @property
    def healthy_reward(self):
        return (
            float(self.is_healthy or self._terminate_when_unhealthy)
            * self._healthy_reward
        )

    def control_cost(self, action):
        control_cost = np.linalg.norm(action)
        return control_cost

    @property
    def is_healthy(self):
        healthy_check = True
        state = self._get_obs()

        qCoM_w, qCoM_x, qCoM_y, qCoM_z = state[ENUM_OBSERVATION.quat_com_w.value], state[ENUM_OBSERVATION.quat_com_x.value], state[ENUM_OBSERVATION.quat_com_y.value], state[ENUM_OBSERVATION.quat_com_z.value]
        roll, pitch, yaw = self._quat2euler(qCoM_w, qCoM_x, qCoM_y, qCoM_z)

        if roll < self._healthy_roll_range[0] or roll > self._healthy_roll_range[1]:
            healthy_check = False

        # if yaw < self._healthy_yaw_range[0] or roll > self._healthy_yaw_range[1]:
        #     healthy_check = False

        if self._mujoco_exception_occured:
            healthy_check = False

        return healthy_check

    @property
    def done(self):
        done = not self.is_healthy
        return done

    def step(self, action):
        obs_before = self._get_obs().copy()

        self.do_simulation(action, self.frame_skip)

        obs_after = self._get_obs().copy()

        # later, could apply contact cost here
        ###

        #Reward Calculation
        x_vel, y_vel = (obs_after - obs_before)[ENUM_OBSERVATION.pos_com_x.value : ENUM_OBSERVATION.pos_com_y.value + 1]
        forward_reward = x_vel - (1.2 * abs(y_vel)) # 추후 계수 추가할 것
        healthy_reward = self.healthy_reward
        failure_panalty = 15
        control_panalty = 0.1 * np.linalg.norm((np.array(action[:7]) - np.array([6, 4, 3, 6, 4, 3, 4])) , 1)

        step_return = forward_reward + healthy_reward - control_panalty

        if not self.is_healthy:
            step_return = step_return - failure_panalty

        done = self.done

        if self.render_option == True:
            # print(self.gait.get_gait_params())
            # print(Rot.from_quat([obs_after[ENUM_OBSERVATION.quat_com_x.value], obs_after[ENUM_OBSERVATION.quat_com_y.value], obs_after[ENUM_OBSERVATION.quat_com_z.value], obs_after[ENUM_OBSERVATION.quat_com_w.value]]).as_euler('XYZ',degrees=True))
            pass
        info = {
            "reward_forward": forward_reward,
            "reward_contact": 0,
            "reward_survive": healthy_reward,
        }

        return obs_after, step_return, done, info

    def _get_obs(self, controller_input:np.ndarray = np.zeros(3), action:np.ndarray = np.zeros(14), before_obs:np.ndarray = np.zeros(1)):
        _sensor_data = self.sim.data.sensordata
        
        # if _sensor_data[48:52].sum() < 0.1:
        #     return  np.zeros(72)

        link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']
        
        _obs_data = np.array([])

        # CoM position
        position_com = np.array([self.sim.data.get_body_xpos(x) for x in link_names]).mean(axis=0)
        _obs_data = np.append(_obs_data, position_com)                       # 3

       # CoM orientation
        orientaions_com = np.reshape(_sensor_data[48:],(-1,4)).copy()  
        orientaions_com[:, [0, 1, 2, 3]] = orientaions_com[:, [1, 2, 3, 0]]

        try:
            rot_com = Rot.from_quat(orientaions_com.copy())
            orientaion_com = rot_com.mean().as_quat()
        except:
            print('zero quat exception occured! is initialized now?')
            orientaion_com = Rot([0,0,0,1])

        rpy_com = Rot.as_euler(orientaion_com,'XYZ')

        _obs_data = np.append(_obs_data, rpy_com)                             # 3

        # CoM velocity
        vel_com = (position_com - before_obs[0:3]) / (0.01 * self.frame_skip)
        _obs_data = np.append(_obs_data, vel_com)                             # 3

        # CoM angular velocity
        avel_com = (rpy_com - before_obs[4:7]) / (0.01 * self.frame_skip)
        _obs_data = np.append(_obs_data,avel_com)                             # 3

        # Joint position
        _obs_data = np.append(_obs_data, _sensor_data[6:20])                  # 14

        # Joint velocity
        _obs_data = np.append(_obs_data, _sensor_data[20:34])                 # 14

        # Action
        _obs_data = np.append(_obs_data, action)                              # 14

        # Controller axis
        _obs_data = np.append(_obs_data, controller_input)                    # 3

        return _obs_data

    def reset_model(self):

        if self.render_option:
            observation = self._get_obs()
            if (observation[ENUM_OBSERVATION.quat_com_x.value : ENUM_OBSERVATION.quat_com_x.value + 1] != [0,0,0,0]).all():
                print(Rot.from_quat([observation[ENUM_OBSERVATION.quat_com_x.value], observation[ENUM_OBSERVATION.quat_com_y.value], observation[ENUM_OBSERVATION.quat_com_z.value], observation[ENUM_OBSERVATION.quat_com_w.value]]).as_euler('XYZ',True))

        self._mujoco_exception_occured = False

        qpos = self.init_qpos
        qvel = self.init_qvel
        self.set_state(qpos, qvel)

        observation = self._get_obs()

        if self.render_option == True:
            print("Reset!",end='')
            print(self.gait.get_gait_params())
            
        return observation


    def do_simulation(self, action, n_frames):

        for _ in range(n_frames):
            self.sim.data.ctrl[:] = action

            try:
                self.sim.step()
            except:
                print("Mujoco Exception raised!")
                break

            if self.render_option:
                if self.viewer is not None:
                    self.viewer.render()