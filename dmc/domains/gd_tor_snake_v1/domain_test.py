import gd_tor_snake_v1
import gymnasium as gym
import numpy as np

import os
import pathlib

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = pathlib.Path(__location__)
__model_location__ = __location__.parent.parent.joinpath('models')
__model_path__ = os.path.join(__model_location__,'env_snake_v1.xml')

env = gym.make("gd_tor_snake_v1/plane-v1", model_path = __model_path__, terminate_when_unhealthy = True , ctrl_cost_weight = 0.2)
env.reset()
print(env.observation_space)
print(env.action_space)

for i in range(3003):
    random = np.random.random(14) * 1.5
    obs, rew, terminated, _, info = env.step(random)
    print(rew)
    # print(info['reward_side'])