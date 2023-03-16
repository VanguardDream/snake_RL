import snake_v5
import numpy as np
import gymnasium as gym
from dm_control import viewer

# env = gym.make('snake/SnakeEnv-v1', render_mode="human")
env = gym.make('snake/SnakeEnv-v5', render_mode="human")
# env = gym.make('snake/SnakeEnv-v3')
action = gym.spaces.Box(low= -3.0, high= 3.0, shape=(14,))

t = 0
env.reset()
for testing in range(3):
    for time in range(183):
        _obs, _reward, done, _, _dict = env.step(1* np.ones((14,)))
        # print(np.argmax(_dict['head_torque']))
    env.reset()

env.close()