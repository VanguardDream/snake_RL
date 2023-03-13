from snake_v3.envs.SnakeEnv import SnakeEnv
import gymnasium as gym
import ray

# import rl 알고리즘
from ray.rllib.algorithms.ppo import PPOConfig 
from ray.rllib.algorithms.algorithm_config import AlgorithmConfig

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print


register_env("snake_v3", lambda config: SnakeEnv())

algo = (
    PPOConfig()
    .rollouts(num_rollout_workers=8,)
    .resources(num_gpus=0.85)
    .environment(env="snake_v3")
    .framework('torch')
    .training(gamma=0.9, lr=0.001)
    .build()
)


for i in range(10000):
    result = algo.train()
    # print(pretty_print(result))

    if i % 5 == 0:
        checkpoint_dir = algo.save()
        print(f"Checkpoint saved in directory {checkpoint_dir} \r   ")