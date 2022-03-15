import gym
import numpy as np
import bongSnake
from gym.spaces import *

if __name__ == '__main__':
    env = bongSnake.bongEnv()

    env.reset()

    for _ in range(1000):
        #renders the environment
        # env.render()
        #Takes a random action from its action space 
        # aka the number of unique actions an agent can perform
        env.step(env.action_space.sample())
    
