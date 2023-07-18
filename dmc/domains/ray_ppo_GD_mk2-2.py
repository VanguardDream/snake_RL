from snake_v8_mk2_2.envs.SnakeEnv import SnakeEnv
import gymnasium as gym

# import rl 알고리즘
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.algorithms.algorithm_config import AlgorithmConfig

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print


register_env("snake_mk2_2_v8", lambda config: SnakeEnv())


algo = (
    PPOConfig()
    .rollouts(num_rollout_workers=10,)
    .resources(num_gpus=0.95)
    .environment(env="snake_mk2_2_v8")
    .framework('torch')
    .training(gamma=0.9, 
              lr=0.0001, 
              clip_param=0.2, 
              kl_coeff=1.0, 
              num_sgd_iter=20, 
              sgd_minibatch_size=16300, 
              train_batch_size=32000, 
              model= {"fcnet_hiddens": [256, 256, 128, 64], 
                      "free_log_std" : True, 
                      }, 
                      )
    .build()
)

for i in range(500):
    result = algo.train()
    # print(pretty_print(result))

    if (i + 1) % 25 == 0:
        checkpoint_dir = algo.save()
        print(f"Checkpoint saved in directory {checkpoint_dir}    \r")