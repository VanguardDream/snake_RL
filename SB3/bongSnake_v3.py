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
        render_option = False
    ):

        self._healthy_reward = healthy_reward
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._healthy_roll_range = healthy_roll_range
        self._healthy_pitch_range = healthy_pitch_range
        self._healthy_yaw_range = healthy_yaw_range

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
        self.custom_state = 0


        #Render Option
        self.render_option = render_option

        #Parent class initialize
        utils.EzPickle.__init__(**locals())
        mujoco_env.MujocoEnv.__init__(self, xml_file, 5)
        
        if self.render_option:
            self.viewer = mujoco_py.MjViewer(self.sim)
        

        box_min = [ 0,	0, 	0, 	0, 	-10, 	0, 	0, 	-10, 	1, 	-1000, 	-1000, 	-1000, 	-100, 	-100, 	-100, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-2, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-100, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-10, 	-np.inf, 	-np.inf, 	-np.inf, 	-np.inf, 	-np.inf, 	-np.inf, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1]
        box_max = [ np.inf, 	1, 	90, 	360, 	10, 	90, 	360, 	10, 	6, 	1000, 	1000, 	1000, 	100, 	100, 	100, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	2, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	100, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	10, 	np.inf, 	np.inf, 	np.inf, 	np.inf, 	np.inf, 	np.inf, 	1, 	1, 	1, 	1, 	1, 	1, 	1, 	1]

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
        self.gait.setParams(self.gait_type, action[0], action[1], action[2], action[3], action[4], action[5], action[6])
        ctrls = self.gait.generate(self.state_k)
        
        self.state_k = self.state_k + 1
        return np.radians(ctrls)

    @property
    def is_healthy(self):
        healthy_check = True
        state = self.state_vector()

        qCoM_w, qCoM_x, qCoM_y, qCoM_z = state[14], state[15], state[16], state[17]
        roll, pitch, yaw = self._quat2euler(qCoM_w, qCoM_x, qCoM_y, qCoM_z)

        if abs(roll) > math.radians(60):
            healthy_check = False

        if abs(yaw) > math.radians(30):
            healthy_check = False

        return healthy_check

    @property
    def done(self):
        done = not self.is_healthy
        return done

    def step(self, action):
        obs_before = self._get_obs()

        skip_tau_scale = int(action[-1])

        ctrl_cost = 0

        self.do_simulation(action, self.frame_skip * 14 * skip_tau_scale)

        obs_after = self._get_obs()


        self.custom_state = self._get_custom_state(obs_after).copy()


        # later, could apply contact cost here
        ###

        #Reward Calculation
        x_vel, y_vel = (obs_after - obs_before)[0:2]
        forward_reward = 80 * x_vel - 80 * y_vel # 추후 계수 추가할 것
        healthy_reward = self.healthy_reward

        rewards = forward_reward + healthy_reward
        costs = 0.001 * ctrl_cost

        reward = rewards + costs

        done = self.done

        observation = obs_after

        info = {
            "reward_forward": forward_reward,
            "reward_ctrl": ctrl_cost,
            "reward_contact": 0,
            "reward_survive": healthy_reward,
            "x_position": obs_after[0],
            "y_position": obs_after[1],
            "distance_from_origin": np.linalg.norm(obs_after[0:2], ord=2),
            "x_velocity": obs_after[2],
            "y_velocity": obs_after[3],
            "forward_reward": forward_reward,
        }

        return observation, reward, done, info

    def _get_obs(self):
        joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
        link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']

        xy_position = np.array([self.get_body_com(x) for x in link_names]).mean(axis=0)[:2].copy()
        xy_velocity = np.array([self.data.get_body_xvelp(x) for x in link_names]).mean(axis=0)[:2].copy()

        xy_velocity_head = np.array(self.data.get_body_xvelp('head'))[:2].copy()

        orientaion_head = np.array(self.data.get_body_xquat('head')).copy()
        orientaion_com = np.array([self.data.get_body_xquat(x) for x in link_names]).mean(axis=0).copy()
        
        rpy_head = np.array(self.data.get_body_xvelr('head')).copy()
        rpy_com = np.array([self.data.get_body_xvelr(x) for x in link_names]).mean(axis=0).copy()

        theta = np.array([self.data.get_joint_qpos(x) for x in joint_names]).copy()
        dtheta = np.array([self.data.get_joint_qvel(x) for x in joint_names]).copy()

        observations = np.concatenate([xy_position.flat,
                                    xy_velocity.flat,
                                    xy_velocity_head.flat,
                                    orientaion_head.flat,
                                    orientaion_com.flat,
                                    rpy_head.flat,
                                    rpy_com.flat,
                                    theta.flat,
                                    dtheta.flat])

        return observations

    def _get_custom_state(self, obs:np.ndarray) -> np.ndarray:
        gaits = np.append(self.state_k,self.state_gait)

        states = np.concatenate([gaits.flat, obs[4:17].flat, obs[20::].flat])
        return states

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

        qpos = self.init_qpos
        qvel = self.init_qvel
        self.set_state(qpos, qvel)

        observation = self._get_obs()

        return observation

    def state_vector(self):
        return self.custom_state

    def do_simulation(self, action, n_frames):
        joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
        
        accum_qvels = 0

        for _ in range(n_frames):
            mujoco_ctrl = self.makeAction(action)

            spec_motor = np.nonzero(mujoco_ctrl)[0]

            for idx in spec_motor:
                # Commnad motor here
                self.sim.data.ctrl[idx] = mujoco_ctrl[idx]
            
            for name in joint_names:
                accum_qvels = accum_qvels + abs(self.sim.data.get_joint_qpos(name))

            self.sim.step()

            if self.render_option:
                if self.viewer is not None:
                    self.viewer.render()