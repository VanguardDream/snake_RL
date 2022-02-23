import gym
import argparse
from gym.spaces import Discrete, Box
import numpy as np
import os
import random

import mujoco_py

import ray
from ray import tune
from ray.rllib.agents import ppo
from ray.rllib.env.env_context import EnvContext
from ray.rllib.models import ModelCatalog
from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.models.tf.fcnet import FullyConnectedNetwork
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.models.torch.fcnet import FullyConnectedNetwork as TorchFC
from ray.rllib.utils.framework import try_import_tf, try_import_torch
from ray.rllib.utils.test_utils import check_learning_achieved
from ray.tune.logger import pretty_print

action_space = Box(low=np.array([-800, 0, 100, -800, 0, 1]),high=np.array([800, 3600, 100, 800, 3600, 10]),dtype=int)

# Obs space : k, theta, theta_dot, position(x,y,z), quaternion(r,p,y,w) -> total 36
obs_lim_low = np.array([0,\
            -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi,\
                -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi,\
                    -np.inf,-np.inf,-np.inf,\
                        -1, -1, -1, -1])

obs_lim_high = np.array([np.inf,\
    np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi,\
        np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi,\
            np.inf, np.inf, np.inf,\
                1, 1, 1, 1])

observation_space = Box(low=obs_lim_low, high=obs_lim_high, dtype=np.float32)

print(len(observation_space.sample()))