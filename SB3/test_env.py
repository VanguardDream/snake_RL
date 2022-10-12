import bongSnake_v5 
import gym
import numpy as np
import mujoco_py
import os
from gym import spaces
from stable_baselines3 import PPO
from scipy.spatial.transform import Rotation as Rot

version = 'v1'

# rand_ctrl = np.random.randint([-9,-9,-9],[9,9,9])/10
rand_ctrl = (0.0, 0.9 ,0)
# env = bongSnake_v5.bongEnv(controller_input=rand_ctrl)
env = gym.make('bongSnake-v5', controller_input = rand_ctrl)

# model = PPO('MlpPolicy', env).learn(total_timesteps=100)

# load recent checkpoint
if os.path.isfile("model-Torque-PPO"+version +".zip"):
    env.reset()
    model = PPO.load("model-Torque-PPO"+version +".zip", env)

snake = mujoco_py.load_model_from_path("../allnew/torquebasegait/snake_circle.xml")

# mujoco-py
simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

def _get_obs(controller_input:np.ndarray = np.zeros(3), c_action:np.ndarray = np.zeros(14), before_obs:np.ndarray = np.zeros(57)):

    _sensor_data = simulator.data.sensordata
    link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']

    # CoM position -> #3
    position_com = simulator.data.geom_xpos[1::].mean(axis=0)              # 3

    # CoM orientation -> #3
    orientaions_com = np.reshape(_sensor_data[48:],(-1,4)).copy()  
    orientaions_com[:, [0, 1, 2, 3]] = orientaions_com[:, [1, 2, 3, 0]]
    try:
        rot_com = Rot.from_quat(orientaions_com.copy())
        rpy_com = rot_com.mean().as_euler('XYZ')
    except:
        print('zero quat exception occured! is initialized now?')
        orientaion_com = Rot([0,0,0,1])
        rpy_com = Rot.as_euler(orientaion_com,'XYZ')

    # CoM velocity -> #3
    vel_com = (position_com - before_obs[0:3]) / 0.1

    # CoM angular velocity -> #3
    avel_com = (rpy_com - before_obs[4:7]) / 0.1

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

simulator.step()
sim_viewer.render()

action = model.predict(_get_obs(controller_input=rand_ctrl))[0]
simulator.data.ctrl[:] = action

for _ in range(3000):
    simulator.step()
    sim_viewer.render()

    _before_obs = _get_obs(controller_input=rand_ctrl,c_action=action)

    if _ % 10 == 0:
        observation = _get_obs(controller_input=rand_ctrl, c_action=action, before_obs=_before_obs)
        action = model.predict(observation=observation)[0]

        simulator.data.ctrl[:] = action

    xy_position_after = observation[0:3]
    xy_velocity = observation[6:8]
    x_velocity, y_velocity = xy_velocity
    yaw_velocity = observation[11]


    forward_reward = 1.25 * x_velocity
    ctrl_direction_cost = 0.5 * ((rand_ctrl[0] - x_velocity) + (rand_ctrl[1] - yaw_velocity) + (rand_ctrl[2] - y_velocity))
    
    rewards = forward_reward + ctrl_direction_cost


    print(rewards)


