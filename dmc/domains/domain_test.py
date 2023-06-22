import snake_v8
import time as te
import numpy as np
import gymnasium as gym
from dm_control import viewer

# env = gym.make('snake/SnakeEnv-v1', render_mode="human")
env = gym.make('snake/SnakeEnv-v8', render_mode="human")
# env = gym.make('snake/SnakeEnv-v3')
action = gym.spaces.Box(low= -3.0, high= 3.0, shape=(14,))

t = 0
env.reset()
for testing in range(1):
    for time in range(1000):
        _obs, _reward, done, _, _dict = env.step(0.8* np.ones((14,)))
        _act = env.action_space.sample()
        # _obs, _reward, done, _, _dict = env.step(np.array([1]+[0]*13))
        print(f"{_dict['head_rotation']}")
        # print(np.argmax(_dict['head_torque']))
        # print(f"forward : {_dict['forward_reward']} head torque : {_dict['head_torque_cost']} terminated : {_dict['terminated_reward']}")

        # print(str(_dict["head_rotation"])+"  \r",end='')
    env.reset()