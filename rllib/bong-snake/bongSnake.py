# © 2022 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Date : 2022-03-04 (YYYYMMDD)
# Version : 2022-03-18
# Description : Bong Snake Env for Gym

from curses.ascii import ctrl
from turtle import st
import mujoco_py
import numpy as np
import gait
import math
from gym import utils
from gym.spaces import *
from gym.envs.mujoco import mujoco_env


DEFAULT_CAMERA_CONFIG = {
    "distance": 4.0,
}


class bongEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    """
    Description

    Actoin space:
    | Num | Action               | Control Min   | Control Max    | Name (in corresponding gait class) | Joint | Unit |
    |-----|----------------------|---------------|----------------|---------------------------------------|-------|------|
    | 0   | dorsal amplitute     | -85  | 85    | d_amp           | hinge | degree |
    | 1   | dorsal phase         |   0  | 360   | d_phase         | hinge | degree |
    | 2   | dorsal lambda        | -10  | 10    | d_lam           | hinge | dimensionless |
    | 3   | lateral amplitude    | -85  | 85    | l_amp           | hinge | degree |
    | 4   | lateral phase        |   0  | 360   | l_phase         | hinge | degree |
    | 5   | lateral lambda       | -10  | 10    | l_lam           | hinge | dimensionless |
    | 6   | tau                  |   1  | 6     | tau             | hinge | dimensionless |


    Observation space:
    | Num | Observation                                                     | Min                   | Max                | Name (in corresponding XML file) | Joint | Unit |
    |-----|-----------------------------------------------------------------|----------------------|--------------------|-----------|------|----------------|
    | 0   | x-coordinate of the body CoM                                    | -Inf                 | Inf                | all       | free | position (m)   |
    | 1   | y-coordinate of the body CoM                                    | -Inf                 | Inf                | all       | free | position (m)   |
    | 2   | x-coordinate velocity of the body CoM                           | -Inf                 | Inf                | all       | free | velocity (m/s) |
    | 3   | y-coordinate velocity of the body CoM                           | -Inf                 | Inf                | all       | free | velocity (m/s) |
    | 4   | x-coordinate velocity of the head link                          | -Inf                 | Inf                | head      | free | velocity (m/s) |
    | 5   | y-coordinate velocity of the head link                          | -Inf                 | Inf                | head      | free | velocity (m/s) |
    | 6   | x-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 7   | y-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 8   | z-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 9   | w-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 10  | x-orientation of the body CoM                                   | -Inf                 | Inf                | all       | free | angle (rad) |
    | 11  | y-orientation of the body CoM                                   | -Inf                 | Inf                | all       | free | angle (rad) |
    | 12  | z-orientation of the body CoM                                   | -Inf                 | Inf                | all       | free | angle (rad) |
    | 13  | w-orientation of the body CoM                                   | -Inf                 | Inf                | all       | free | angle (rad) |
    | 14  | roll angular velocity of the head link                          | -Inf                 | Inf                | head      | free | angular velocity (rad/s) |
    | 15  | pitch angular velocity of the head link                         | -Inf                 | Inf                | head      | free | angular velocity (rad/s) |
    | 16  | yaw angular velocity of the head link                           | -Inf                 | Inf                | head      | free | angular velocity (rad/s) | 
    | 17  | roll angular velocity of the body CoM                           | -Inf                 | Inf                | all       | free | angular velocity (rad/s) |
    | 18  | pitch angular velocity of the body CoM                          | -Inf                 | Inf                | all       | free | angular velocity (rad/s) |
    | 19  | yaw angular velocity of the body CoM                            | -Inf                 | Inf                | all       | free | angular velocity (rad/s) |   
    | 20  | angle of the joint1                                             | -Inf                 | Inf                | joint1    | hinge | angle (rad) |
    | 21  | angle of the joint2                                             | -Inf                 | Inf                | joint2    | hinge | angle (rad) |
    | 22  | angle of the joint3                                             | -Inf                 | Inf                | joint3    | hinge | angle (rad) |
    | 23  | angle of the joint4                                             | -Inf                 | Inf                | joint4    | hinge | angle (rad) |
    | 24  | angle of the joint5                                             | -Inf                 | Inf                | joint5    | hinge | angle (rad) |
    | 25  | angle of the joint6                                             | -Inf                 | Inf                | joint6    | hinge | angle (rad) |
    | 26  | angle of the joint7                                             | -Inf                 | Inf                | joint7    | hinge | angle (rad) |
    | 27  | angle of the joint8                                             | -Inf                 | Inf                | joint8    | hinge | angle (rad) |
    | 28  | angle of the joint9                                             | -Inf                 | Inf                | joint9    | hinge | angle (rad) |
    | 29  | angle of the joint10                                            | -Inf                 | Inf                | joint10   | hinge | angle (rad) |
    | 30  | angle of the joint11                                            | -Inf                 | Inf                | joint11   | hinge | angle (rad) |
    | 31  | angle of the joint12                                            | -Inf                 | Inf                | joint12   | hinge | angle (rad) |
    | 32  | angle of the joint13                                            | -Inf                 | Inf                | joint13   | hinge | angle (rad) |
    | 33  | angle of the joint14                                            | -Inf                 | Inf                | joint14   | hinge | angle (rad) | 
    | 34  | angular velocity of the joint1                                  | -Inf                 | Inf                | joint1    | hinge | angle (rad) |
    | 35  | angular velocity of the joint2                                  | -Inf                 | Inf                | joint2    | hinge | angle (rad) |
    | 36  | angular velocity of the joint3                                  | -Inf                 | Inf                | joint3    | hinge | angle (rad) |
    | 37  | angular velocity of the joint4                                  | -Inf                 | Inf                | joint4    | hinge | angle (rad) |
    | 38  | angular velocity of the joint5                                  | -Inf                 | Inf                | joint5    | hinge | angle (rad) |
    | 39  | angular velocity of the joint6                                  | -Inf                 | Inf                | joint6    | hinge | angle (rad) |
    | 40  | angular velocity of the joint7                                  | -Inf                 | Inf                | joint7    | hinge | angle (rad) |
    | 41  | angular velocity of the joint8                                  | -Inf                 | Inf                | joint8    | hinge | angle (rad) |
    | 42  | angular velocity of the joint9                                  | -Inf                 | Inf                | joint9    | hinge | angle (rad) |
    | 43  | angular velocity of the joint10                                 | -Inf                 | Inf                | joint10   | hinge | angle (rad) |
    | 44  | angular velocity of the joint11                                 | -Inf                 | Inf                | joint11   | hinge | angle (rad) |
    | 45  | angular velocity of the joint12                                 | -Inf                 | Inf                | joint12   | hinge | angle (rad) |
    | 46  | angular velocity of the joint13                                 | -Inf                 | Inf                | joint13   | hinge | angle (rad) |
    | 47  | angular velocity of the joint14                                 | -Inf                 | Inf                | joint14   | hinge | angle (rad) |


    Agent State Space
    * Gait Parameters (+ k-value, - gait type) -> 8
    * Head Link x-y velocity -> 2
    * Head Link Orientation -> 4
    * Body Orientation -> 4
    * Head Link Angular Velocity -> 3
    * Joint Position -> 14
    * Joint Angular Velocity -> 14
    = Total = 49 elements

    | Num | Description                                                     | Min                  | Max                | Name (in corresponding XML file) | Joint | Unit |
    | 0   | Time step k                                                     |   0                  | Inf                | simulation time step
    | 1   | Dorsal Amplitude                                                |  -85                 | 85                 | Gait Params
    | 2   | Dorsal Phase                                                    |   0                  | 360                | Gait Params
    | 3   | Dorsal Lambda                                                   |  -10                 | 10                 | Gait Params
    | 4   | Lateral Amplitude                                               |  -85                 | 85                 | Gait Params
    | 5   | Lateral Phase                                                   |   0                  | 360                | Gait Params
    | 6   | Lateral Lambda                                                  |  -10                 | 10                 | Gait Params
    | 7   | tau                                                             |   1                  | 6                  | Gait Params
    | 8   | x-coordinate velocity of the head link                          | -Inf                 | Inf                | head      | free | velocity (m/s) |
    | 9   | y-coordinate velocity of the head link                          | -Inf                 | Inf                | head      | free | velocity (m/s) |
    | 10  | x-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 11  | y-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 12  | z-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 13  | w-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 14  | x-orientation of the body CoM                                   | -Inf                 | Inf                | all       | free | angle (rad) |
    | 15  | y-orientation of the body CoM                                   | -Inf                 | Inf                | all       | free | angle (rad) |
    | 16  | z-orientation of the body CoM                                   | -Inf                 | Inf                | all       | free | angle (rad) |
    | 17  | w-orientation of the body CoM                                   | -Inf                 | Inf                | all       | free | angle (rad) |
    | 18  | roll angular velocity of the head link                          | -Inf                 | Inf                | head      | free | angular velocity (rad/s) |
    | 19  | pitch angular velocity of the head link                         | -Inf                 | Inf                | head      | free | angular velocity (rad/s) |
    | 20  | yaw angular velocity of the head link                           | -Inf                 | Inf                | head      | free | angular velocity (rad/s) | 
    | 21  | angle of the joint1                                             | -Inf                 | Inf                | joint1    | hinge | angle (rad) | 
    | 22  | angle of the joint2                                             | -Inf                 | Inf                | joint2    | hinge | angle (rad) |
    | 23  | angle of the joint3                                             | -Inf                 | Inf                | joint3    | hinge | angle (rad) |
    | 24  | angle of the joint4                                             | -Inf                 | Inf                | joint4    | hinge | angle (rad) |
    | 25  | angle of the joint5                                             | -Inf                 | Inf                | joint5    | hinge | angle (rad) |
    | 26  | angle of the joint6                                             | -Inf                 | Inf                | joint6    | hinge | angle (rad) |
    | 27  | angle of the joint7                                             | -Inf                 | Inf                | joint7    | hinge | angle (rad) |
    | 28  | angle of the joint8                                             | -Inf                 | Inf                | joint8    | hinge | angle (rad) |
    | 29  | angle of the joint9                                             | -Inf                 | Inf                | joint9    | hinge | angle (rad) |
    | 30  | angle of the joint10                                            | -Inf                 | Inf                | joint10   | hinge | angle (rad) |
    | 31  | angle of the joint11                                            | -Inf                 | Inf                | joint11   | hinge | angle (rad) |
    | 32  | angle of the joint12                                            | -Inf                 | Inf                | joint12   | hinge | angle (rad) |
    | 33  | angle of the joint13                                            | -Inf                 | Inf                | joint13   | hinge | angle (rad) |
    | 34  | angle of the joint14                                            | -Inf                 | Inf                | joint14   | hinge | angle (rad) | 
    | 35  | angular velocity of the joint1                                  | -Inf                 | Inf                | joint1    | hinge | angle (rad) |
    | 36  | angular velocity of the joint2                                  | -Inf                 | Inf                | joint2    | hinge | angle (rad) |
    | 37  | angular velocity of the joint3                                  | -Inf                 | Inf                | joint3    | hinge | angle (rad) |
    | 38  | angular velocity of the joint4                                  | -Inf                 | Inf                | joint4    | hinge | angle (rad) |
    | 39  | angular velocity of the joint5                                  | -Inf                 | Inf                | joint5    | hinge | angle (rad) |
    | 40  | angular velocity of the joint6                                  | -Inf                 | Inf                | joint6    | hinge | angle (rad) |
    | 41  | angular velocity of the joint7                                  | -Inf                 | Inf                | joint7    | hinge | angle (rad) |
    | 42  | angular velocity of the joint8                                  | -Inf                 | Inf                | joint8    | hinge | angle (rad) |
    | 43  | angular velocity of the joint9                                  | -Inf                 | Inf                | joint9    | hinge | angle (rad) |
    | 44  | angular velocity of the joint10                                 | -Inf                 | Inf                | joint10   | hinge | angle (rad) |
    | 45  | angular velocity of the joint11                                 | -Inf                 | Inf                | joint11   | hinge | angle (rad) |
    | 46  | angular velocity of the joint12                                 | -Inf                 | Inf                | joint12   | hinge | angle (rad) |
    | 47  | angular velocity of the joint13                                 | -Inf                 | Inf                | joint13   | hinge | angle (rad) |
    | 48  | angular velocity of the joint14                                 | -Inf                 | Inf                | joint14   | hinge | angle (rad) |

    !! Environment space and Agent state space are not subset of the any env sets. !!

    """

    def __init__(
        self,
        xml_file="/home/bong/projects/snake_RL/rllib/bong-snake/asset/snake.xml",
        ctrl_cost_weight=0.5,
        contact_cost_weight=5e-4,
        healthy_reward=1.0,
        terminate_when_unhealthy=True,
        healthy_roll_range=(-45,45),
        healthy_pitch_range=(-30,30),
        healthy_yaw_range=(-45,45),
        contact_force_range=(-1.0, 1.0),
        reset_noise_scale=0.1,
        exclude_current_positions_from_observation=False,
        gait_params=(1, 39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1)
    ):
        utils.EzPickle.__init__(**locals())

        self._ctrl_cost_weight = ctrl_cost_weight
        self._contact_cost_weight = contact_cost_weight

        self._healthy_reward = healthy_reward
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._healthy_roll_range = healthy_roll_range
        self._healthy_pitch_range = healthy_pitch_range
        self._healthy_yaw_range = healthy_yaw_range

        self._contact_force_range = contact_force_range

        self._reset_noise_scale = reset_noise_scale

        self._exclude_current_positions_from_observation = (
            exclude_current_positions_from_observation
        )

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
        limit_min = [-85,0,-10,-85,0,-10,1]
        limit_max = [85,360,10,85,360,10,6]


        self.state_k = 0
        self.gait_type = gait_params[0]
        self.state_gait = np.array(gait_params[1:])
        self.custom_state = 0

        mujoco_env.MujocoEnv.__init__(self, xml_file, 5)

        self.action_space = Box(np.array(limit_min),np.array(limit_max), dtype=np.integer)
        self.observation_space = Box(np.ones(46,) * -np.inf, np.ones(46,) * np.inf, dtype=np.float32)

        self.viewer = mujoco_py.MjViewer(self.sim)
        
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
    def contact_forces(self):
        raw_contact_forces = self.sim.data.cfrc_ext
        min_value, max_value = self._contact_force_range
        contact_forces = np.clip(raw_contact_forces, min_value, max_value)
        return contact_forces

    @property
    def contact_cost(self):
        contact_cost = self._contact_cost_weight * np.sum(
            np.square(self.contact_forces)
        )
        return contact_cost

    @property
    def is_healthy(self):
        healthy_check = True
        state = self.state_vector()

        qCoM_x, qCoM_y, qCoM_z, qCoM_w = state[14], state[15], state[16], state[17]
        roll, pitch, yaw = self._quat2euler(qCoM_w, qCoM_x, qCoM_y, qCoM_z)

        if abs(roll) > math.radians(75):
            healthy_check = False

        if abs(yaw) > math.radians(60):
            healthy_check = False

        return healthy_check

    @property
    def done(self):
        # done = not self.is_healthy if self._terminate_when_unhealthy else False
        done = not self.is_healthy
        return done

    def step(self, action):
        obs_before = self._get_obs()

        skip_tau_scale = int(action[-1])

        ctrl_cost = self.do_simulation(action, self.frame_skip * 14 * skip_tau_scale)

        obs_after = self._get_obs()


        self.custom_state = self._get_custom_state(obs_after).copy()


        # later, could apply contact cost here
        ###

        #Reward Calculation
        x_vel, y_vel = (obs_after - obs_before)[0:2]
        forward_reward = x_vel - 0.4 * y_vel # 추후 계수 추가할 것
        healthy_reward = self.healthy_reward

        rewards = forward_reward + healthy_reward
        costs = 0.001 * ctrl_cost

        reward = rewards + costs

        if '_healthy_roll_range' in locals():
            done = self.done
        else:
            done = False

        observation = self._get_obs()
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

        if self._exclude_current_positions_from_observation:
            pass

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
        noise_low = -self._reset_noise_scale
        noise_high = self._reset_noise_scale

        # qpos = self.init_qpos + self.np_random.uniform(
        #     low=noise_low, high=noise_high, size=self.model.nq
        # )
        # qvel = (
        #     self.init_qvel
        #     + self._reset_noise_scale * self.np_random.standard_normal(self.model.nv)
        # )

        qpos = self.init_qpos
        qvel = self.init_qvel
        self.set_state(qpos, qvel)

        observation = self._get_obs()

        return observation

    def viewer_setup(self):
        for key, value in DEFAULT_CAMERA_CONFIG.items():
            if isinstance(value, np.ndarray):
                getattr(self.viewer.cam, key)[:] = value
            else:
                setattr(self.viewer.cam, key, value)

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
            if self.viewer is not None:
                self.viewer.render()

        return accum_qvels

    def reset(self):
        self.state_k = 0
        self.sim.reset()
        return super().reset()