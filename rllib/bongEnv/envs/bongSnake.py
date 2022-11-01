# gym 0.23.1 compatible

import numpy as np

from gym import utils
from gym.envs.mujoco import MujocoEnv


from gym.spaces import Box
from gym.spaces import MultiDiscrete
from scipy.spatial.transform import Rotation as Rot

DEFAULT_CAMERA_CONFIG = {
    "trackbodyid": 1,
    "distance": 4.0,
    "lookat": np.array((0.0, 0.0, 2.0)),
    "elevation": -20.0,
}


def mass_center(model, data):
    mass = np.expand_dims(model.body_mass, axis=1)
    xpos = data.xipos
    return (np.sum(mass * xpos, axis=0) / np.sum(mass))[0:2].copy()


class bongEnv(MujocoEnv, utils.EzPickle):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
        "render_fps": 60,
    }
    def __init__(
        self,
        forward_reward_weight=5,
        ctrl_direction_weight=3,
        ctrl_cost_weight=0.05,
        terminate_when_unhealthy=True,
        healthy_roll_range=(-5.0, 5.0),
        reset_noise_scale=1e-2,
        controller_input = (1.0, 0, 0),
        **kwargs
    ):
        utils.EzPickle.__init__(
            self,
            forward_reward_weight,
            ctrl_cost_weight,
            terminate_when_unhealthy,
            healthy_roll_range,
            reset_noise_scale,
            controller_input,
            **kwargs
        )

        self._forward_reward_weight = forward_reward_weight
        self._ctrl_direction_weight = ctrl_direction_weight
        self._ctrl_cost_weight = ctrl_cost_weight
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._healthy_roll_range = healthy_roll_range

        self._reset_noise_scale = reset_noise_scale

        self._controller_input = controller_input
        self.is_healthy = True

        observation_space = Box(
            low=-np.inf, high=np.inf, shape=(58,)
        )

        self._input_command_verbose = False
        for _key, _value in kwargs.items():
            if 'print_input_command' in kwargs.keys():
                if  kwargs.get('print_input_command') == True:
                    self._input_command_verbose = True



        # MujocoEnv.__init__(
        #     self, "snake_circle.xml", 10, observation_space=observation_space,**kwargs
        # )


        # gym v0.23.1
        MujocoEnv.__init__(
            self, "snake_circle.xml", 5
        )

        self.action_space = MultiDiscrete([3,3,3,3,3, 3,3,3,3,3, 3,3,3,3])

        print(f'Initiating bongSnake Env with ctrl : {controller_input}')


    def control_cost(self, action):
        control_cost = self._ctrl_cost_weight * np.sum(np.square(self.data.ctrl))
        return control_cost

    @property
    def terminated(self):
        terminated = (not self.is_healthy) if self._terminate_when_unhealthy else False
        return terminated

    def _get_obs(self, controller_input:np.ndarray = np.zeros(3), before_obs:np.ndarray = np.zeros(57)):

        _sensor_data = self.data.sensordata
        link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']

        # CoM position -> #3
        position_com = self.data.geom_xpos[1::].mean(axis=0)              # 3

       # CoM orientation -> #4
        orientaions_com = np.reshape(_sensor_data[48:],(-1,4)).copy()  
        # orientaions_com = np.reshape(_sensor_data[48:52],(-1,4)).copy()  
        orientaions_com[:, [0, 1, 2, 3]] = orientaions_com[:, [1, 2, 3, 0]]
        try:
            rot_com = Rot.from_quat(orientaions_com.copy())
            rpy_com = rot_com.mean().as_quat()

        except:
            print('zero quat exception occured! is initialized now?')
            rpy_com = Rot([0,0,0,1])

        # CoM velocity -> #3
        vel_com = (position_com - before_obs[0:3]) / self.dt 

        # CoM angular velocity -> #3
        # avel_com = (rpy_com - before_obs[3:6]) / self.dt # Angular vel from euler Not recommended
        b_quat = Rot(before_obs[4:8])
        a_quat = Rot(rpy_com)

        diff_quat = (b_quat.inv() * a_quat)
        avel_com = diff_quat.as_euler('XYZ')

        # Joint position -> #14
        joint_position = _sensor_data[6:20]

        # Joint velocity -> #14
        joint_vel = _sensor_data[20:34]

        # Joint torque -> #14
        joint_frc = _sensor_data[34:48]

        # Controller axis -> #3
        input = controller_input

        return np.concatenate(
            (
                position_com, #0 1 2
                rpy_com, # 3 4 5 6
                vel_com, # 7 8 9
                avel_com, # 10 11 12
                joint_position, # 13 ~ 26
                joint_vel, # 27 ~ 40
                joint_frc, # 41 ~ 54
                input # 55 ~ 57                
            ), dtype=np.float32
        )


    def step(self, action):
        _before_obs = self._get_obs(controller_input=self._controller_input)
        self.do_simulation(action, self.frame_skip)
        observation = self._get_obs(controller_input=self._controller_input, before_obs=_before_obs)

        xy_position_after = observation[0:2]
        xy_velocity = observation[6:8]
        x_velocity, y_velocity = xy_velocity
        yaw_velocity = observation[11]

        self.is_healthy = self._healthy_roll_range[0] < observation[3] < self._healthy_roll_range[1]
        ctrl_cost = self.control_cost(action)

        # forward_reward = self._forward_reward_weight * x_velocity
        # ctrl_direction_cost = self._ctrl_direction_weight * ((self._controller_input[0] - x_velocity) + (self._controller_input[1] - yaw_velocity) + (self._controller_input[2] - y_velocity))
        
        """
        Direction Normalize
        """
        try:
            _norm_input = self._controller_input / np.linalg.norm(np.array(self._controller_input),2)
            _obsvel = np.append(xy_velocity, yaw_velocity)
            _norm_obsvel = _obsvel / np.linalg.norm(_obsvel, 2)

            """
            Vector Projection
            """
            _proj_vector = (np.dot(_norm_obsvel, _norm_input) / np.dot(_norm_input, _norm_input)) * _norm_input
        except:
            _norm_input = np.array([0, 0, 0])
            _norm_obsvel = _obsvel / np.linalg.norm(_obsvel, 2)
            _proj_vector = np.array([0, 0, 0])

        ctrl_direction_cost = self._ctrl_direction_weight * np.linalg.norm((_norm_input - _norm_obsvel),1)

        forward_reward = self._forward_reward_weight * np.dot(_norm_input, _proj_vector)
        rewards = forward_reward

        # costs = ctrl_cost + ctrl_direction_cost
        
        costs = ctrl_direction_cost

        reward = rewards - costs

        if self._input_command_verbose:
            # print(f'Reward info : _norm_input : {_norm_input}, _norm_obsvel : {_norm_obsvel}, _proj_vetor {_proj_vector}')
            # print(f'Reward info : ctrl_direction_cost : {ctrl_direction_cost}, forward_reward : {forward_reward}, ctrl_cost {ctrl_cost}')
            pass

        terminated = self.terminated
        info = {
            "reward_linvel": forward_reward,
            "reward_quadctrl": -ctrl_cost,
            "x_position": observation[0],
            "y_position": observation[1],
            "distance_from_origin": np.linalg.norm(xy_position_after, ord=2),
            "x_velocity": x_velocity,
            "y_velocity": y_velocity,
            "yaw_ang_velocity" : observation[11],
            "norm_input" : _norm_input,
            "norm_obs_vel" : _obsvel,
            "projection_vector" : _proj_vector,
            "forward_reward": forward_reward,
        }

        # if self.render_mode == "human":
        #     self.render()
        return observation, reward, terminated, info

    def reset_model(self):
        noise_low = -self._reset_noise_scale
        noise_high = self._reset_noise_scale

        # noise_low = 0
        # noise_high = 0

        qpos = self.init_qpos + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nq
        )
        qvel = self.init_qvel + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nv
        )
        self.set_state(qpos, qvel)

        # rand_input = np.random.randint([-4, -4, -4],[4, 4, 4]) / 4

        rand_input = np.array([0, 0, 0])

        while np.linalg.norm(rand_input,2) == 0:
            rand_input = np.random.randint([-4, -4, -4],[4, 4, 4]) / 4

        self._controller_input = rand_input

        if self._input_command_verbose:
            print('Reset input cmd to : '+str(rand_input))
        before_obs = self._get_obs()
        observation = self._get_obs(controller_input=self._controller_input, before_obs=before_obs)

        return observation

    # def viewer_setup(self):
    #     assert self.viewer is not None
    #     for key, value in DEFAULT_CAMERA_CONFIG.items():
    #         if isinstance(value, np.ndarray):
    #             getattr(self.viewer.cam, key)[:] = value
    #         else:
    #             setattr(self.viewer.cam, key, value)

    def do_simulation(self, ctrl, n_frames):
        self.sim.data.ctrl[:] = 1.9 * (ctrl - 1)
        for _ in range(n_frames):
            self.sim.step()