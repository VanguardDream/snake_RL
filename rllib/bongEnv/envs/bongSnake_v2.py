# gym 0.23.1 compatible
import re
import numpy as np

from gym import utils
from gym.envs.mujoco import MujocoEnv
from gym.envs.bongEnv.gait import snake_gait


from gym.spaces import Box
from gym.spaces import Discrete
from scipy.spatial.transform import Rotation as Rot

DEFAULT_CAMERA_CONFIG = {
    "trackbodyid": 1,
    "distance": 4.0,
    "lookat": np.array((0.0, 0.0, 2.0)),
    "elevation": -20.0,
}

def center_orientation(data) -> np.ndarray:
    _sensor_data = data.sensordata
    orientaions_com = np.reshape(_sensor_data[48::],(-1,4)).copy()  
    orientaions_com[:, [0, 1, 2, 3]] = orientaions_com[:, [1, 2, 3, 0]]

    try:
        rot_com = Rot.from_quat(orientaions_com.copy())
        rpy_com = rot_com.mean().as_quat()
    except:
        rpy_com = [0,0,0,1]

    return rpy_com

class bongEnv_v2(MujocoEnv, utils.EzPickle):
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
        healthy_roll_range=(-2.0, 2.0),
        reset_noise_scale=1e-2,
        controller_input = (1.0, 0, 0),
        **kwargs
    ):
        utils.EzPickle.__init__(
            self,
            forward_reward_weight,
            ctrl_direction_weight,
            ctrl_cost_weight,
            terminate_when_unhealthy,
            healthy_roll_range,
            reset_noise_scale,
            controller_input,
            **kwargs
        )
        self.gait_gen = snake_gait()
        self.prior_action = np.zeros(14)

        self._forward_reward_weight = forward_reward_weight
        self._ctrl_direction_weight = ctrl_direction_weight
        self._ctrl_cost_weight = ctrl_cost_weight
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._healthy_roll_range = healthy_roll_range

        self._reset_noise_scale = reset_noise_scale

        self._controller_input = controller_input
        self.is_healthy = True

        observation_space = Box(
            low=-np.inf, high=np.inf, shape=(66,)
        )

        self._input_command_verbose = False
        for _key, _value in kwargs.items():
            if 'print_input_command' in kwargs.keys():
                if  kwargs.get('print_input_command') == True:
                    self._input_command_verbose = True

        # gym v0.23.1
        MujocoEnv.__init__(
            self, "snake_circle_alligned.xml", 2
        )

        self.action_space = Discrete(5, start= -2)

        print(f'Initiating bongSnake Env with ctrl : {controller_input}')

    @property
    def terminated(self):
        terminated = (not self.is_healthy) if self._terminate_when_unhealthy else False
        return terminated

    def _get_obs(self, controller_input:np.ndarray = np.zeros(3)):
        sim_state = self.sim.get_state().qpos # 21
        _sensor_data = self.data.sensordata
        joint_vel = _sensor_data[20:34] # 14
        joint_frc = _sensor_data[34:48] # 14
        next_joint = self.gait_gen.get_next_joints() # 14
        input = controller_input # 3

        return np.concatenate(
            (
                sim_state,
                joint_vel,
                joint_frc,
                next_joint,
                input
                # center_orientation(self.data)       # For debugging   
            ), dtype=np.float32
        )

    def step(self, action):

        sim_state_before = self.sim.get_state().qpos
        xy_position_before = sim_state_before[0:2]
        head_orientation_before = Rot([sim_state_before[4], sim_state_before[5], sim_state_before[6], sim_state_before[3]])
        com_orientation_before = Rot(center_orientation(self.data))

        self.do_simulation(action, self.frame_skip)
        observation = self._get_obs(controller_input=self._controller_input)

        sim_state_after = self.sim.get_state().qpos
        xy_position_after = sim_state_after[0:2]
        head_orientation_after = Rot([sim_state_after[4], sim_state_after[5], sim_state_after[6], sim_state_after[3]])
        com_orientation_after = Rot(center_orientation(self.data))

        xy_velocity = (xy_position_after - xy_position_before) / self.dt
        diff_com_quat = (com_orientation_before.inv() * com_orientation_after)

        yaw_velocity = diff_com_quat.as_euler('ZYX')[0]
        
        _norm_input = self._controller_input / np.linalg.norm(np.array(self._controller_input),2)
        _obsvel = np.append(xy_velocity, yaw_velocity)

        try:
            _norm_obsvel = _obsvel / np.linalg.norm(_obsvel, 2)
        except:
            _norm_obsvel = _obsvel

        _proj_vector = (np.dot(_norm_obsvel, _norm_input) / np.dot(_norm_input, _norm_input)) * _norm_input

        ### Healthy check
        self.is_healthy = self._healthy_roll_range[0] < head_orientation_after.as_euler('ZYX')[2] < self._healthy_roll_range[1]

        # ### Reward Version 1
        # ### Rewards
        # forward_reward = self._forward_reward_weight * np.dot(_norm_input, _proj_vector)
        # rewards = forward_reward

        # ### Costs
        # ctrl_direction_cost = self._ctrl_direction_weight * np.linalg.norm((_norm_input - _norm_obsvel),1)
        # healthy_cost = not(self.is_healthy) * 1500
        # costs = ctrl_direction_cost + healthy_cost

        # step_return = rewards - costs

        ### Reward Version 2
        ### Rewards
        forward_reward = np.dot(_obsvel, self._controller_input) * self._forward_reward_weight
        rewards = forward_reward

        ### Costs
        costs = 0

        step_return = rewards - costs

        if self._input_command_verbose:
            # print(f'Reward info : _norm_input : {_norm_input}, _norm_obsvel : {_norm_obsvel}, _proj_vetor {_proj_vector}')
            # print(f'Reward info : ctrl_direction_cost : {ctrl_direction_cost}, forward_reward : {forward_reward}, ctrl_cost {ctrl_cost}')
            pass

        terminated = self.terminated
        info = {
            "xy_vel" : xy_velocity,
            "yaw_vel" : yaw_velocity,
            "control_input" : self._controller_input,
            "rewards" : rewards,
            "costs" : costs,
        }

        return observation, step_return, terminated, info

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

        rand_input = np.array([0, 0, 0])

        while np.linalg.norm(rand_input,2) == 0:
            rand_input = np.random.randint([-4, -4, -4],[5, 5, 5]) / 4

        self._controller_input = rand_input

        if self._input_command_verbose:
            print('Reset input cmd to : '+str(rand_input))
        observation = self._get_obs(controller_input=self._controller_input)

        return observation

    # def viewer_setup(self):
    #     assert self.viewer is not None
    #     for key, value in DEFAULT_CAMERA_CONFIG.items():
    #         if isinstance(value, np.ndarray):
    #             getattr(self.viewer.cam, key)[:] = value
    #         else:
    #             setattr(self.viewer.cam, key, value)

    def do_simulation(self, action, n_frames):
        ctrl = action * 0.75 * self.gait_gen.get_next_joints()
        idx = ctrl.nonzero()[0]

        for i in idx:
            self.prior_action[i] = ctrl[i]

        self.sim.data.ctrl[:] = self.prior_action
    
        for _ in range(n_frames):
            self.sim.step()

        self.gait_gen.gait_step()

