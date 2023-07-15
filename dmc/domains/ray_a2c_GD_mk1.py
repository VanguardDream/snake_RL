from snake_v8_mk1.envs.SnakeEnv import SnakeEnv
import gymnasium as gym

# import rl 알고리즘
from ray.rllib.algorithms.a2c import A2CConfig

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print


register_env("snake_mk1_v8", lambda config: SnakeEnv())

algo = (
    A2CConfig()
    .rollouts(num_rollout_workers=8,)
    .resources(num_gpus=0.95)
    .environment(env="snake_mk1_v8")
    .framework('torch')
    .training(gamma=0.9, 
              lr=0.0001, 
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