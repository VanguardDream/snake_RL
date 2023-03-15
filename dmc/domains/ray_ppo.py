from snake_v3.envs.SnakeEnv import SnakeEnv
import gymnasium as gym
import ray

# import rl 알고리즘
from ray.rllib.algorithms.ppo import PPOConfig, PPO 
from ray.rllib.algorithms.algorithm_config import AlgorithmConfig

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print


register_env("snake_v3", lambda config: SnakeEnv())

algo = (
    PPOConfig()
    .rollouts(num_rollout_workers=8,)
    .resources(num_gpus=0.95)
    .environment(env="snake_v3")
    .framework('torch')
    .training(gamma=0.95, lr=0.0001, model= {"fcnet_hiddens": [16, 16, 16, 8, 4]})
    .build()
)

algo.restore("C:/Users/doore/ray_results/PPO_snake_v3_MLP/checkpoint_001456")

for i in range(4000):
    result = algo.train()
    # print(pretty_print(result))

    if i % 5 == 0:
        checkpoint_dir = algo.save()
        print(f"Checkpoint saved in directory {checkpoint_dir}    \r")