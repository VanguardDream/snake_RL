import imp
import bongSnake_v5 
import gym
import numpy as np
import mujoco_py
import os

from gym import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env
from scipy.spatial.transform import Rotation as Rot


version = 'v1'

# rand_ctrl = np.random.randint([-9,-9,-9],[9,9,9])/10
rand_ctrl = (0.99, 0.0 ,0.0)

# env = make_vec_env("bongSnake-v5", n_envs = 4, env_kwargs={'controller_input':rand_ctrl})
env = gym.make("bongSnake-v5",controller_input=rand_ctrl)

# # load recent checkpoint
if os.path.isfile("vec_ppo_bongSnake.zip"):
    env.reset()
    model = PPO.load("vec_ppo_bongSnake",)
else:
    print(f'Making new PPO policy')
    model = PPO('MlpPolicy', env, verbose = 1, tensorboard_log = str("./Tor_Vec_PPO/"+version))


model.learn(total_timesteps=500000)

model.save("vec_ppo_bongSnake")

# del model

# model = PPO.load("vec_ppo_bongSnake")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()