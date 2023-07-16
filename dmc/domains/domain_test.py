# import snake_v8_CG
# import snake_v8_mk1
import snake_v8_mk2
# import snake_v8_mk3
import time as te
import numpy as np
import gymnasium as gym
from dm_control import viewer

float_formatter = "{:.5f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})

# env = gym.make('snake/SnakeEnv-v1', render_mode="human")
env = gym.make('snake/SnakeEnv-mk2-v8', render_mode="human")
# env = gym.make('snake/SnakeEnv-cg-v8', render_mode="human")
# env = gym.make('snake/SnakeEnv-v3')
action = gym.spaces.Box(low= -3.0, high= 3.0, shape=(14,))

r = 0
env.reset()
for testing in range(10):
    for time in range(1500):
        # _act = env.action_space.sample()
        _obs, _reward, done, _, _dict = env.step(-0.5 * np.ones((14,)))
        # _obs, _reward, done, _, _dict = env.step(_act)
        r = r + _reward
        if done:
            print(f"terminated : {r}")
            break

        
        # _obs, _reward, done, _, _dict = env.step(np.array([1]+[0]*13))
        # print(f"{_dict['com_angular_velocity']}",end="   ")
        # print(f"{_dict['com_rotation']}")
        # print(np.argmax(_dict['head_torque']))
        # print(f"forward : {_dict['forward_reward']} head torque : {_dict['head_torque_cost']} terminated : {_dict['terminated_reward']}")
    print(f"Done {r}")
    r = 0
        # print(str(_dict["head_rotation"])+"  \r",end='')
    env.reset()