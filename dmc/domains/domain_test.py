import snake
import numpy as np
import gymnasium as gym
from dm_control import viewer

# env = gym.make('snake/SnakeEnv-v1', render_mode="human")
env = gym.make('snake/SnakeEnv-v1')
action = gym.spaces.Box(low= -3.0, high= 3.0, shape=(14,))

t = 0
env.reset()
for testing in range(5):
    for time in range(10):
        # env.step(action.sample())
        env.step(np.zeros((14,)))
        # env.render()
    env.reset()
    print('resetting!')

env.close()