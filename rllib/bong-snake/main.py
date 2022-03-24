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
        done = False

        # action = (39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1)
        action = env.action_space.sample()

        while not done:
            _, reward, done, _ = env.step(action)
            
            if done:
                env.reset()
                print(done)
                break
        
            print(reward)

        env.reset()
    
