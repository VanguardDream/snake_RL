import gymnasium as gym
import numpy as np

# Gym env
from snake_v4.envs.SnakeEnv import SnakeEnv

# import rl 알고리즘
from ray.rllib.algorithms.mbmpo import MBMPOConfig

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print

class MB_SnakeEnv(SnakeEnv):
    def __init__(self, frame_skip=10, **kwargs) -> None:
        super().__init__(frame_skip, **kwargs)

    def reward(self, obs, action, obs_next):
        if obs.ndim == 2 and action.ndim == 2:
            accel_before = obs[:,14:17].copy()
            accel_after = obs_next[:,14:17].copy()

            axis_acc = accel_after - accel_before

            rew = axis_acc[:,0] - (0.8 * np.abs(axis_acc[:,1])) - (0.1 * np.abs(axis_acc[:,2]))
            rew = np.clip(rew, a_min=-0.8, a_max=0.8, dtype=np.float32)
            return rew
        else:
            accel_before = obs[14:17].copy()
            accel_after = obs_next[14:17].copy()

            axis_acc = accel_after - accel_before

            rew = axis_acc[0] - (0.8 * np.abs(axis_acc[1])) - (0.1 * np.abs(axis_acc[2]))
            rew = np.clip(rew, a_min=-0.8, a_max=0.8, dtype=np.float32)
        
            return rew
    
register_env("snake-v4", lambda config: MB_SnakeEnv())

config = MBMPOConfig()

config = config.training(lr=0.0003, train_batch_size=1024)
config = config.resources(num_gpus=1)
config = config.rollouts(num_rollout_workers=1)
config = config.environment("snake-v4")
config = config.framework('torch')

algo = config.build()

for i in range(6000):
    result = algo.train()
    # print(pretty_print(result))

    if ((i + 1) % 25 == 0):
        checkpoint_dir = algo.save()
        print(f"Checkpoint saved in directory {checkpoint_dir}  \r")