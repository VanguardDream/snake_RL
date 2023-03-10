import snake
import snake_v2
import numpy as np
import gymnasium as gym
from dm_control import viewer

# env = gym.make('snake/SnakeEnv-v1', render_mode="human")
env = gym.make('snake/SnakeEnv-v2', render_mode="human")
action = gym.spaces.Box(low= -3.0, high= 3.0, shape=(14,))

t = 0
env.reset()
for testing in range(12):
    for time in range(100):
        env.step(action.sample())
    env.reset()
    print('reseting!')

env.close()