from snake_v5.envs.SnakeEnv import SnakeEnv
import gymnasium as gym
import ray

# import rl 알고리즘
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.algorithms.algorithm_config import AlgorithmConfig

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print


register_env("snake_v5_Att", lambda config: SnakeEnv())

algo = (
    PPOConfig()
    .rollouts(num_rollout_workers=10,)
    .resources(num_gpus=0)
    .environment(env="snake_v5_Att")
    .training(gamma=0.995, 
              lr=0.0001, 
              clip_param=0.2, 
              num_sgd_iter=10, 
            #   sgd_minibatch_size=16384, 
              sgd_minibatch_size=512, 
              train_batch_size=3200, 
              model= {
                        "fcnet_hiddens": [512, 512, 256, 256, 64], 
                        "use_attention": True,
                        "max_seq_len": 10,
                        "attention_num_transformer_units": 1,
                        "attention_dim": 32,
                        "attention_memory_inference": 10,
                        "attention_memory_training": 10,
                        "attention_num_heads": 1,
                        "attention_head_dim": 32,
                        "attention_position_wise_mlp_dim": 32,
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