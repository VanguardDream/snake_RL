from snake_v5.envs.SnakeEnv import SnakeEnv
import gymnasium as gym

# import rl 알고리즘
import ray
from ray.rllib.algorithms import Algorithm
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.algorithms.algorithm_config import AlgorithmConfig

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print


register_env("snake_v5", lambda config: SnakeEnv())

algo = (
    PPOConfig()
    .rollouts(num_rollout_workers=10,)
    .resources(num_gpus=0.95)
    .environment(env="snake_v5")
    .framework('torch')
    .evaluation()
    .training(gamma=0.995, lr=0.0001, clip_param=0.2, kl_coeff=1.0, num_sgd_iter=20, sgd_minibatch_size=16384, train_batch_size=160000, model= {"fcnet_hiddens": [128, 128, 64, 64, 32], "free_log_std" : True }, )
    .build()
)

algo.restore('C:/Users/doore/ray_results/PPO_snake_v5_2023-03-16_21-07-0237rbvpin/checkpoint_000476')