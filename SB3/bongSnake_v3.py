# © 2022 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Date : 2022-08-04 (YYYYMMDD)
# Version : 2022-08-04
# Description : Bong Snake Env for Gym

import mujoco_py
import numpy as np
import gait
import math
from space_enums import *
from gym import utils
from gym.spaces import *
from gym.envs.mujoco import mujoco_env

from scipy.spatial.transform import Rotation as Rot

class bongEnv_v3(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(
        self,
        xml_file="snake.xml",
        healthy_reward=1.0,
        terminate_when_unhealthy=True,
        healthy_roll_range=(-45,45),
        healthy_pitch_range=(-30,30),
        healthy_yaw_range=(-45,45),
        gait_params=(1, 39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1),
        render_option = False,
    ):

        self._healthy_reward = healthy_reward
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._healthy_roll_range = healthy_roll_range
        self._healthy_pitch_range = healthy_pitch_range
        self._healthy_yaw_range = healthy_yaw_range
        self._mujoco_exception_occured = False

        ## For custom env
        self.gait = gait.gait(gait_params[0] 
            ,gait_params[1] 
            ,gait_params[2] 
            ,gait_params[3] 
            ,gait_params[4] 
            ,gait_params[5] 
            ,gait_params[6] 
            ,gait_params[7]
        )

        self.state_k = 0
        self.gait_type = gait_params[0]
        self.state_gait = np.array(gait_params[1:])


        #Render Option
        self.render_option = render_option

        #Parent class initialize
        utils.EzPickle.__init__(**locals())
        mujoco_env.MujocoEnv.__init__(self, xml_file, 5)
        
        if self.render_option:
            self.viewer = mujoco_py.MjViewer(self.sim)
        

        box_min = [ 0,	0,  0, 	0, 	0, 	-10, 	0, 	0, 	-10, 	1, 	-1000, 	-1000, 	-1000, 	-100, 	-100, 	-100, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-np.inf, 	-np.inf, 	-np.inf, 	-np.inf, 	-np.inf, 	-np.inf, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1]
        box_max = [ np.inf, 10, 	1, 	90, 	360, 	10, 	90, 	360, 	10, 	6, 	1000, 	1000, 	1000, 	100, 	100, 	100, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	np.inf, 	np.inf, 	np.inf, 	np.inf, 	np.inf, 	np.inf, 	1, 	1, 	1, 	1, 	1, 	1, 	1, 	1]

        self.action_space = MultiDiscrete([11,7,5,11,7,5,3])
        self.observation_space = Box(np.array(box_min),np.array(box_max), dtype=np.float32)
        


    @property
    def healthy_reward(self):
        return (
            float(self.is_healthy or self._terminate_when_unhealthy)
            * self._healthy_reward
        )

    def control_cost(self, obs:np.ndarray, ctrls:np.ndarray):
        control_cost = np.linalg.norm((obs[20:34] - ctrls))
        return control_cost

    def makeAction(self, action):
        if np.shape(action)[0] > 10:
            return 0

        _before_gait_params = self.gait.get_gait_params()

        d_action = np.array(action)
        d_action = d_action - np.array([6, 4, 3, 6, 4, 3, 2])
        d_action = d_action * np.array([5, 10, 1, 5, 10, 1, 1])

        _after_gait_params = _before_gait_params + np.append([0], d_action)
        _after_gait_params[1::] = np.clip(_after_gait_params[1::],a_min=[-85,0,-10,-85,0,-10,1], a_max=[[85,360,10,85,360,10,6]])

        self.gait.setParams(_after_gait_params[0], _after_gait_params[1], _after_gait_params[2], _after_gait_params[3], _after_gait_params[4], _after_gait_params[5], _after_gait_params[6], _after_gait_params[7])

    @property
    def is_healthy(self):
        healthy_check = True
        state = self._get_obs()

        qCoM_w, qCoM_x, qCoM_y, qCoM_z = state[68], state[69], state[70], state[71]
        roll, pitch, yaw = self._quat2euler(qCoM_w, qCoM_x, qCoM_y, qCoM_z)

        if abs(roll) > math.radians(60):
            healthy_check = False

        # if abs(yaw) > math.radians(30):
        #     healthy_check = False

        if self._mujoco_exception_occured:
            healthy_check = False

        return healthy_check

    @property
    def done(self):
        done = not self.is_healthy
        return done

    def step(self, action):
        obs_before = self._get_obs()

        skip_tau_scale = int(self.gait.get_gait_params()[-1])

        self.do_simulation(action, self.frame_skip * 14 * skip_tau_scale)

        obs_after = self._get_obs()

        # later, could apply contact cost here
        ###

        #Reward Calculation
        x_vel, y_vel = (obs_after - obs_before)[ENUM_OBSERVATION.pos_com_x.value : ENUM_OBSERVATION.pos_com_y.value + 1]
        forward_reward = 80 * x_vel - 80 * y_vel # 추후 계수 추가할 것
        healthy_reward = self.healthy_reward
        failure_panalty = 20

        step_return = forward_reward + healthy_reward

        if not self.is_healthy:
            step_return = step_return - failure_panalty

        done = self.done

        observation = obs_after

        info = {
            "reward_forward": forward_reward,
            "reward_contact": 0,
            "reward_survive": healthy_reward,
            "x_position": obs_after[0],
            "y_position": obs_after[1],
            "distance_from_origin": np.linalg.norm(obs_after[0:2], ord=2),
            "x_velocity": obs_after[2],
            "y_velocity": obs_after[3],
            "forward_reward": forward_reward,
        }

        return observation, step_return, done, info

    def _get_obs(self):
        
        if self.sim.data.sensordata[48:52].sum() < 0.1:
            return  np.zeros(72)

        joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
        link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']
        
        _obs_data = np.array([])
        t = self.state_k

        # Total 72 elements
        _obs_data = np.append(_obs_data, t)                                     # 1
        _obs_data = np.append(_obs_data, [self.gait.get_stride_ratio(t)])       # 1
        _obs_data = np.append(_obs_data, self.gait.get_gait_params())           # 8
        _obs_data = np.append(_obs_data, self.sim.data.sensordata[:48])         # 48

        position_head = np.array(self.sim.data.get_body_xpos('head'))
        _obs_data = np.append(_obs_data, position_head)                         # 3

        position_com = np.array([self.sim.data.get_body_xpos(x) for x in link_names]).mean(axis=0)
        _obs_data = np.append(_obs_data, position_com)                          # 3

        orientaion_head = np.array(self.sim.data.sensordata[-4:])
        _obs_data = np.append(_obs_data, orientaion_head)                       # 4

        orientaions_com = np.reshape(self.sim.data.sensordata[48:],(-1,4)).copy()
        orientaions_com[:, [0, 1, 2, 3]] = orientaions_com[:, [1, 2, 3, 0]]
        rot_com = Rot.from_quat(orientaions_com)
        orientaion_com = rot_com.mean().as_quat()
        orientaion_com[0], orientaion_com[1], orientaion_com[2], orientaion_com[3] = orientaion_com[3], orientaion_com[0], orientaion_com[1], orientaion_com[2]
        
        _obs_data = np.append(_obs_data, orientaion_com)                        # 4

        return _obs_data

    def _quat2euler(self, w, x, y, z):
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = np.arctan2(t0, t1)
    
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = np.arcsin(t2)
    
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = np.arctan2(t3, t4)

        return roll_x, pitch_y, yaw_z

    def reset_model(self):
        self.state_k = 0
        self._mujoco_exception_occured = False

        qpos = self.init_qpos
        qvel = self.init_qvel
        self.set_state(qpos, qvel)

        observation = self._get_obs()

        return observation


    def do_simulation(self, action, n_frames):
        joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
        
        self.makeAction(action)

        for _ in range(n_frames):
            joint_goal = self.gait.generate(self.state_k)
            selected_motor_index = self.gait.commandIdx(self.state_k)

            for idx in selected_motor_index:
                    # Commnad motor here
                    self.sim.data.ctrl[idx] = self.gait.degtorad(joint_goal[idx])
            
            self.state_k = self.state_k + 1

            try:
                self.sim.step()
            except:
                print("Mujoco Exception raised! at gait vector : " + str(self.gait.get_gait_params()))
                break

            if self.render_option:
                if self.viewer is not None:
                    self.viewer.render()