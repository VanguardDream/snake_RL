import gym
from gym import spaces
from gym.utils import seeding
import bongSnake
import numpy as np


if __name__ == '__main__':
    env = bongSnake.bongEnv()

    env.reset()

    for _ in range(10):
        #renders the environment
        #Takes a random action from its action space 
        # aka the number of unique actions an agent can perform
        env.step(env.action_space.sample())
        # print(env.action_space.sample())
        env.reset_model()
    
