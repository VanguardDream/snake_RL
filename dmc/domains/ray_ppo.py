from snake.envs.SnakeEnv import SnakeEnv
import gymnasium as gym
import ray

# import rl 알고리즘
from ray.rllib.algorithms.ppo import PPOConfig 
from ray.rllib.algorithms.algorithm_config import AlgorithmConfig

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print


register_env("snake", lambda config: SnakeEnv())

algo = (
    PPOConfig()
    .rollouts(num_rollout_workers=4,)
    .resources(num_gpus=1)
    .environment(env="snake")
    .framework('torch')
    .training(gamma=0.9, lr=0.001)
    .build()
)

algo.from_checkpoint("C:/Users/doore/ray_results/PPO_snake_18obs/checkpoint_001731/")

for i in range(10000):
    result = algo.train()
    # print(pretty_print(result))

    if i % 5 == 0:
        # checkpoint_dir = algo.save()
        algo.export_policy_checkpoint()
        # print(f"Checkpoint saved in directory {checkpoint_dir}")