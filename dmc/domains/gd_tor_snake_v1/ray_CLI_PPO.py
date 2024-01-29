from gd_tor_snake_v1.envs import PlaneWorld
import gymnasium as gym
import numpy as np

# import rl 알고리즘
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.algorithms.algorithm_config import AlgorithmConfig

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print

from gymnasium.spaces import Box

register_env("GD_TOR_v1", lambda config: PlaneWorld())

obs_space = Box(
                low=-np.inf, high= np.inf, shape=(52,), dtype=np.float64
)

act_space =  Box(
                low=0, high=1.5, shape=(14,), dtype=np.float64
)


algo = (
    PPOConfig()
    .rollouts(num_rollout_workers=10,)
    .resources(num_gpus=0.95)
    .environment(env="GD_TOR_v1",observation_space=obs_space,action_space=act_space)
    .framework('torch')
    .training(gamma=0.9, 
              lr=0.01, 
              clip_param=0.2, 
              kl_coeff=1.0, 
              num_sgd_iter=20, 
              sgd_minibatch_size=1600, 
              train_batch_size=32000, 
              model= {"fcnet_hiddens": [256, 256, 128, 64], 
                      "free_log_std" : True, 
                      }, 
                      )
    .evaluation(evaluation_num_workers=1)
    .build()
)

for i in range(500):
    result = algo.train()
    # print(pretty_print(result))

    if (i + 1) % 25 == 0:
        checkpoint_dir = algo.save()
        print(f"Checkpoint saved in directory {checkpoint_dir}    \r")