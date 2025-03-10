from snake_v8_CG.envs.SnakeEnv import SnakeEnv
import gymnasium as gym

# import rl 알고리즘
from ray.rllib.algorithms.a2c import A2CConfig

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print


register_env("snake_CG_v8", lambda config: SnakeEnv())

explicit_action_space = gym.spaces.Box(low= -3.0, high= 3.0, shape=(14,))

algo = (
    A2CConfig()
    .rollouts(num_rollout_workers=8,)
    .resources(num_gpus=0.95)
    .environment(env="snake_CG_v8",
                 action_space=explicit_action_space)
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