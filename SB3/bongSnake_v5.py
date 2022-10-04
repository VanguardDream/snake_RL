import numpy as np

from gym import utils
from gym.envs.mujoco import MujocoEnv
from gym.spaces import Box
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


class bongEnv_v5(MujocoEnv, utils.EzPickle):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
        "render_fps": 67,
    }
    def __init__(
        self,
        forward_reward_weight=1.25,
        ctrl_cost_weight=0.5,
        healthy_reward=1.0,
        terminate_when_unhealthy=True,
        healthy_roll_range=(-2.1, 2.1),
        reset_noise_scale=1e-2,
        controller_input = (0.99, 0, 0),
        **kwargs
    ):
        utils.EzPickle.__init__(
            self,
            forward_reward_weight,
            ctrl_cost_weight,
            healthy_reward,
            terminate_when_unhealthy,
            healthy_roll_range,
            reset_noise_scale,
            controller_input,
            **kwargs
        )

        self._forward_reward_weight = forward_reward_weight
        self._ctrl_cost_weight = ctrl_cost_weight
        self._healthy_reward = healthy_reward
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._healthy_roll_range = healthy_roll_range

        self._reset_noise_scale = reset_noise_scale

        self._controller_input = controller_input

        observation_space = Box(
            low=-1, high=1, shape=(57,), dtype=np.float64
        )

        MujocoEnv.__init__(
            self, "snake_circle.xml", 10, observation_space=observation_space, **kwargs
        )

    @property
    def healthy_reward(self):
        return (
            float(self.is_healthy or self._terminate_when_unhealthy)
            * self._healthy_reward
        )

    def control_cost(self, action):
        control_cost = self._ctrl_cost_weight * np.sum(np.square(self.data.ctrl))
        return control_cost

    @property
    def is_healthy(self):
        """
            BongEnv 오버라이드 Roll 불안정성 검증
        """
        # CoM orientation
        orientaions_com = np.reshape(self.data.sensordata[48:],(-1,4)).copy()  
        orientaions_com[:, [0, 1, 2, 3]] = orientaions_com[:, [1, 2, 3, 0]]

        try:
            rot_com = Rot.from_quat(orientaions_com.copy())
            orientaion_com = rot_com.mean().as_quat()
        except:
            print('zero quat exception occured! is initialized now?')
            orientaion_com = Rot([0,0,0,1])

        min_roll, max_roll = self._healthy_roll_range
        is_healthy = min_roll < orientaion_com[0] < max_roll

        return is_healthy

    @property
    def terminated(self):
        terminated = (not self.is_healthy) if self._terminate_when_unhealthy else False
        return terminated

    def _get_obs(self, controller_input:np.ndarray = np.zeros(3), c_action:np.ndarray = np.zeros(14), before_obs:np.ndarray = np.zeros(57)):

        _sensor_data = self.data.sensordata
        link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']

        # CoM position -> #3
        position_com = np.array([self.sim.data.get_body_xpos(x) for x in link_names]).mean(axis=0)                 # 3

       # CoM orientation -> #3
        orientaions_com = np.reshape(_sensor_data[48:],(-1,4)).copy()  
        orientaions_com[:, [0, 1, 2, 3]] = orientaions_com[:, [1, 2, 3, 0]]
        try:
            rot_com = Rot.from_quat(orientaions_com.copy())
            orientaion_com = rot_com.mean().as_quat()
        except:
            print('zero quat exception occured! is initialized now?')
            orientaion_com = Rot([0,0,0,1])
        rpy_com = Rot.as_euler(orientaion_com,'XYZ')

        # CoM velocity -> #3
        vel_com = (position_com - before_obs[0:3]) / self.dt

        # CoM angular velocity -> #3
        avel_com = (rpy_com - before_obs[4:7]) / self.dt

        # Joint position -> #14
        joint_position = _sensor_data[6:20]

        # Joint velocity -> #14
        joint_vel = _sensor_data[20:34]

        # Action -> #14
        action = c_action

        # Controller axis -> #3
        input = controller_input

        return np.concatenate(
            (
                position_com,
                rpy_com,
                vel_com,
                avel_com,
                joint_position,
                joint_vel,
                action,
                input
            )
        )

    def step(self, action):
        _before_obs = self._get_obs(controller_input=self._controller_input,c_action=action)
        self.do_simulation(action, self.frame_skip)
        observation = self._get_obs(controller_input=self._controller_input, c_action=action, before_obs=_before_obs)

        xy_velocity = observation[6:8]
        x_velocity, y_velocity = xy_velocity

        ctrl_cost = self.control_cost(action)

        forward_reward = self._forward_reward_weight * x_velocity
        healthy_reward = self.healthy_reward

        rewards = forward_reward + healthy_reward

        observation = self._get_obs()
        reward = rewards - ctrl_cost
        terminated = self.terminated
        info = {
            "reward_linvel": forward_reward,
            "reward_quadctrl": -ctrl_cost,
            "reward_alive": healthy_reward,
            "x_position": observation[0],
            "y_position": observation[1],
            "distance_from_origin": np.linalg.norm(xy_position_after, ord=2),
            "x_velocity": x_velocity,
            "y_velocity": y_velocity,
            "forward_reward": forward_reward,
        }

        if self.render_mode == "human":
            self.render()
        return observation, reward, terminated, False, info

    def reset_model(self):
        noise_low = -self._reset_noise_scale
        noise_high = self._reset_noise_scale

        qpos = self.init_qpos + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nq
        )
        qvel = self.init_qvel + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nv
        )
        self.set_state(qpos, qvel)

        observation = self._get_obs()
        return observation

    def viewer_setup(self):
        assert self.viewer is not None
        for key, value in DEFAULT_CAMERA_CONFIG.items():
            if isinstance(value, np.ndarray):
                getattr(self.viewer.cam, key)[:] = value
            else:
                setattr(self.viewer.cam, key, value)