import gym
from gym import spaces
from gym.utils import seeding
import bongSnake
import numpy as np


if __name__ == '__main__':
    env = bongSnake.bongEnv(render_option=True)

    env.reset()

    for _ in range(10):
        #renders the environment
        #Takes a random action from its action space 
        # aka the number of unique actions an agent can perform
        _, reward, done, _ = env.step((env.action_space.sample()))
        if done:
            env.reset_model()
            continue
        
        print(reward)

        # print(env.action_space.sample())
        env.reset_model()
    
