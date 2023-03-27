import gymnasium as gym

# Gym env
from snake_v6.envs.SnakeEnv import SnakeEnv

# import rl 알고리즘
from ray.rllib.algorithms.ppo import PPOConfig 
# from ray.rllib.algorithms.algorithm_config import AlgorithmConfig
from ray.rllib.models import ModelCatalog
from ray.rllib.models.modelv2 import ModelV2
from ray.rllib.models.preprocessors import get_preprocessor
# from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.models.torch.recurrent_net import RecurrentNetwork as TorchRNN
# from ray.rllib.models.tf.recurrent_net import RecurrentNetwork

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print


register_env("snake-v6", lambda config: SnakeEnv())

algo = (
    PPOConfig()
    .rollouts(num_rollout_workers=16,)
    .resources(num_gpus=1)
    .environment(env="snake-v6")
    .framework('torch')
    .training(gamma=0.9, 
              lr=0.0001,
              sgd_minibatch_size=8192,
              train_batch_size=160000,
              model= {
        "fcnet_hiddens": [256, 512, 256, 128, 64], 
        "use_lstm" : True,  
        "max_seq_len": 310,
        "lstm_use_prev_action": True,
        "lstm_cell_size": 256, 
        "_time_major": True,
    })
    .evaluation(evaluation_interval=25)
    .build()
)

for i in range(1000):
    result = algo.train()
    # print(pretty_print(result))

    if ((i + 1) % 25 == 0):
        checkpoint_dir = algo.save()
        print(f"Checkpoint saved in directory {checkpoint_dir}  \r")