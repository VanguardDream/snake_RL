import snake_v3
import numpy as np
import gymnasium as gym
from dm_control import viewer

# env = gym.make('snake/SnakeEnv-v1', render_mode="human")
env = gym.make('snake/SnakeEnv-v3', render_mode="human")
# env = gym.make('snake/SnakeEnv-v3')
action = gym.spaces.Box(low= -3.0, high= 3.0, shape=(14,))

t = 0
env.reset()
for testing in range(3):
    for time in range(183):
        _obs, _reward, done, _, _ = env.step(np.ones((14,)))
    env.reset()

env.close()