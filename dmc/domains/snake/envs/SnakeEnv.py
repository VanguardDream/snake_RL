__author__ = ["Bongsub Song"]

import numpy as np
import os
import pathlib

from gymnasium import spaces
from gymnasium import utils
from gymnasium.envs.mujoco import MujocoEnv

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = pathlib.Path(__location__)
__model_location__ = __location__.parent.parent.parent.joinpath('models')

class SnakeEnv(MujocoEnv, utils.EzPickle):

    def __init__(self, frame_skip = 10) -> None:

        # Action Space
        self.action_space = spaces.Box(low= -3.0, high= 3.0, shape=(14,))

        # Observation Space
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(48,)
        )


        MujocoEnv.__init__(self, os.path.join(__model_location__,'snake_circle_alligned.xml'), frame_skip, observation_space= self.observation_space, )