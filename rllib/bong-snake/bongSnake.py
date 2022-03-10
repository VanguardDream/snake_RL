# © 2022 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Date : 2022-03-04 (YYYYMMDD)
# Description : Bong Snake Env for Gym

from curses import flash
from socket import gaierror
import numpy as np
import gait
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
    | Num | Observation                                                     | Min                | Max                | Name (in corresponding XML file) | Joint | Unit |
    |-----|-----------------------------------------------------------------|----------------|-----------------|----------------------------------------|-------|------|
    | 0   | x-coordinate of the body CoM                                    | -Inf                 | Inf                | head      | free | position (m)   |
    | 1   | y-coordinate of the body CoM                                    | -Inf                 | Inf                | head      | free | position (m)   |
    | 2   | x-coordinate velocity of the body CoM                           | -Inf                 | Inf                | head      | free | velocity (m/s) |
    | 3   | y-orientation velocity of the body CoM                          | -Inf                 | Inf                | head      | free | velocity (m/s) |
    | 4   | x-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 5   | y-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 6   | z-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 7   | w-orientation of the head link                                  | -Inf                 | Inf                | head      | free | angle (rad) |
    | 8   | x-orientation of the body CoM                                   | -Inf                 | Inf                | head      | free | angle (rad) |
    | 9   | y-orientation of the body CoM                                   | -Inf                 | Inf                | head      | free | angle (rad) |
    | 10  | z-orientation of the body CoM                                   | -Inf                 | Inf                | head      | free | angle (rad) |
    | 11  | w-orientation of the body CoM                                   | -Inf                 | Inf                | head      | free | angle (rad) |
    | 12  | roll angular velocity of the head link                          | -Inf                 | Inf                | head      | free | angular velocity (rad/s) |
    | 13  | pitch angular velocity of the head link                         | -Inf                 | Inf                | head      | free | angular velocity (rad/s) |
    | 14  | yaw angular velocity of the head link                           | -Inf                 | Inf                | head      | free | angular velocity (rad/s) | 
    | 15  | roll angular velocity of the body CoM                           | -Inf                 | Inf                | head      | free | angular velocity (rad/s) |
    | 16  | pitch angular velocity of the body CoM                          | -Inf                 | Inf                | head      | free | angular velocity (rad/s) |
    | 17  | yaw angular velocity of the body CoM                            | -Inf                 | Inf                | head      | free | angular velocity (rad/s) |   
    | 18  | angle of the joint1                                             | -Inf                 | Inf                | joint1    | hinge | angle (rad) |
    | 19  | angle of the joint2                                             | -Inf                 | Inf                | joint2    | hinge | angle (rad) |
    | 20  | angle of the joint3                                             | -Inf                 | Inf                | joint3    | hinge | angle (rad) |
    | 21  | angle of the joint4                                             | -Inf                 | Inf                | joint4    | hinge | angle (rad) |
    | 22  | angle of the joint5                                             | -Inf                 | Inf                | joint5    | hinge | angle (rad) |
    | 23  | angle of the joint6                                             | -Inf                 | Inf                | joint6    | hinge | angle (rad) |
    | 24  | angle of the joint7                                             | -Inf                 | Inf                | joint7    | hinge | angle (rad) |
    | 25  | angle of the joint8                                             | -Inf                 | Inf                | joint8    | hinge | angle (rad) |
    | 26  | angle of the joint9                                             | -Inf                 | Inf                | joint9    | hinge | angle (rad) |
    | 27  | angle of the joint10                                            | -Inf                 | Inf                | joint10   | hinge | angle (rad) |
    | 28  | angle of the joint11                                            | -Inf                 | Inf                | joint11   | hinge | angle (rad) |
    | 29  | angle of the joint12                                            | -Inf                 | Inf                | joint12   | hinge | angle (rad) |
    | 30  | angle of the joint13                                            | -Inf                 | Inf                | joint13   | hinge | angle (rad) |
    | 31  | angle of the joint14                                            | -Inf                 | Inf                | joint14   | hinge | angle (rad) | 
    | 32  | angular velocity of the joint1                                  | -Inf                 | Inf                | joint1    | hinge | angle (rad) |
    | 33  | angular velocity of the joint2                                  | -Inf                 | Inf                | joint2    | hinge | angle (rad) |
    | 34  | angular velocity of the joint3                                  | -Inf                 | Inf                | joint3    | hinge | angle (rad) |
    | 35  | angular velocity of the joint4                                  | -Inf                 | Inf                | joint4    | hinge | angle (rad) |
    | 36  | angular velocity of the joint5                                  | -Inf                 | Inf                | joint5    | hinge | angle (rad) |
    | 37  | angular velocity of the joint6                                  | -Inf                 | Inf                | joint6    | hinge | angle (rad) |
    | 38  | angular velocity of the joint7                                  | -Inf                 | Inf                | joint7    | hinge | angle (rad) |
    | 39  | angular velocity of the joint8                                  | -Inf                 | Inf                | joint8    | hinge | angle (rad) |
    | 40  | angular velocity of the joint9                                  | -Inf                 | Inf                | joint9    | hinge | angle (rad) |
    | 41  | angular velocity of the joint10                                 | -Inf                 | Inf                | joint10   | hinge | angle (rad) |
    | 42  | angular velocity of the joint11                                 | -Inf                 | Inf                | joint11   | hinge | angle (rad) |
    | 43  | angular velocity of the joint12                                 | -Inf                 | Inf                | joint12   | hinge | angle (rad) |
    | 44  | angular velocity of the joint13                                 | -Inf                 | Inf                | joint13   | hinge | angle (rad) |
    | 45  | angular velocity of the joint14                                 | -Inf                 | Inf                | joint14   | hinge | angle (rad) |

    Agent State Space
    * Gait Parameters (+ k-value, - gait type) -> 8
    * Head Link x-y velocity -> 2
    * Head Link Orientation -> 4
    * Head Link Angular Velocity -> 3
    * Joint Position -> 14
    * Joint Angular Velocity -> 14
    = Total = 45 elements

    !! Environment space and Agent state space are not subset of the any env sets. !!

    """

    def __init__(
        self,
        xml_file="/Users/bong/project/snake_RL/rllib/bong-snake/asset/snake.xml",
        ctrl_cost_weight=0.5,
        contact_cost_weight=5e-4,
        healthy_reward=1.0,
        terminate_when_unhealthy=True,
        healthy_z_range=(0.2, 1.0),
        healthy_r_range=(-120,120),
        healthy_y_range=(-45,45),
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
        self._healthy_z_range = healthy_z_range

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
        # self.state_gait = np.array(gait_params[1:])

        self.action_space = Box(np.array(limit_min),np.array(limit_max), dtype=np.integer)

        self.observation_space = Box(np.ones(46,) * -np.inf, np.ones(46,) * np.inf, dtype=np.float32)

        ##
        mujoco_env.MujocoEnv.__init__(self, xml_file, 5)

    @property
    def healthy_reward(self):
        return (
            float(self.is_healthy or self._terminate_when_unhealthy)
            * self._healthy_reward
        )

    def control_cost(self, action):
        control_cost = self._ctrl_cost_weight * np.sum(np.square(action))
        return control_cost

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
        state = self.state_vector()

        return is_healthy

    @property
    def done(self):
        done = not self.is_healthy if self._terminate_when_unhealthy else False
        return done

    def step(self, action):
        # joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
        # link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']

        # xy_position = np.array([self.get_body_com(x) for x in link_names]).mean(axis=0)[:2].copy()
        # xy_velocity = np.array([self.data.get_body_xvelp(x) for x in link_names]).mean(axis=0)[:2].copy()

        # orientaion_head = np.array([self.data.get_body_xquat('head')]).copy()
        # orientaion_com = np.array([self.data.get_body_xquat(x) for x in link_names]).mean(axis=0).copy()
        
        # rpy_head = np.array([self.data.get_body_xvelr('head')]).copy()
        # rpy_com = np.array([self.data.get_body_xvelr(x) for x in link_names]).mean(axis=0).copy()

        # theta = np.array([self.data.get_joint_qpos(x) for x in joint_names]).copy()
        # dtheta = np.array([self.data.get_joint_qvel(x) for x in joint_names]).copy()

        # obs_before = np.concatenate([xy_position.flat,
        #                             xy_velocity.flat,
        #                             orientaion_head.flat,
        #                             orientaion_com.flat,
        #                             rpy_head.flat,
        #                             rpy_com,
        #                             theta.flat,
        #                             dtheta.flat])

        obs_before = self._get_obs()

        # write action exporter code here

        self.do_simulation(action, self.frame_skip)

        obs_after = self._get_obs()

        # ctrl_cost = self.control_cost(action)
        # contact_cost = self.contact_cost

        #Reward Calculation
        x_vel, y_vel = (obs_after - obs_before)[0:1]
        forward_reward = x_vel + y_vel
        healthy_reward = self.healthy_reward

        rewards = forward_reward + healthy_reward
        costs = ctrl_cost + contact_cost

        reward = rewards - costs

        done = self.done
        # done = False

        observation = self._get_obs()
        info = {
            "reward_forward": forward_reward,
            "reward_ctrl": -ctrl_cost,
            "reward_contact": -contact_cost,
            "reward_survive": healthy_reward,
            "x_position": xy_position_after[0],
            "y_position": xy_position_after[1],
            "distance_from_origin": np.linalg.norm(xy_position_after, ord=2),
            "x_velocity": x_velocity,
            "y_velocity": y_velocity,
            "forward_reward": forward_reward,
        }

        return observation, reward, done, info

    def _get_obs(self):
        joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
        link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']

        xy_position = np.array([self.get_body_com(x) for x in link_names]).mean(axis=0)[:2].copy()
        xy_velocity = np.array([self.data.get_body_xvelp(x) for x in link_names]).mean(axis=0)[:2].copy()

        orientaion_head = np.array([self.data.get_body_xquat('head')]).copy()
        orientaion_com = np.array([self.data.get_body_xquat(x) for x in link_names]).mean(axis=0).copy()
        
        rpy_head = np.array([self.data.get_body_xvelr('head')]).copy()
        rpy_com = np.array([self.data.get_body_xvelr(x) for x in link_names]).mean(axis=0).copy()

        theta = np.array([self.data.get_joint_qpos(x) for x in joint_names]).copy()
        dtheta = np.array([self.data.get_joint_qvel(x) for x in joint_names]).copy()

        if self._exclude_current_positions_from_observation:
            pass

        observations = np.concatenate([xy_position.flat,
                                    xy_velocity.flat,
                                    orientaion_head.flat,
                                    orientaion_com.flat,
                                    rpy_head.flat,
                                    rpy_com,
                                    theta.flat,
                                    dtheta.flat])

        return observations

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

        qpos = self.init_qpos + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nq
        )
        qvel = (
            self.init_qvel
            + self._reset_noise_scale * self.np_random.standard_normal(self.model.nv)
        )
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

        return super().state_vector()