import snake
import numpy as np
import gymnasium as gym
from dm_control import viewer

env = gym.make('snake/SnakeEnv-v1',render_mode="human")
action = gym.spaces.Box(low= -3.0, high= 3.0, shape=(14,))

t = 0
env.reset()
while t < 1000:
    env.step(action.sample())
    env.render()
    t = t + 1

# env.close()