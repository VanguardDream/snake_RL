import ray
from ray import tune
# import rl 알고리즘
import ray.rllib.algorithms.ppo as ppo
import ray.rllib.algorithms.algorithm_config

from ray.tune.logger import pretty_print

config = ppo.DEFAULT_CONFIG.copy()
# _cp_path = "/home/bong/ray_results/PPO_bongEnv_2022-10-28_23-31-31gbhv2yef/checkpoint_003001/checkpoint-3001"

############# Customize Hyper-Parameters
config["num_gpus"] = 1
config["num_workers"] = 4
config["gamma"] = 0.9
config["framework"] = 'torch'
config["model"] =               {
                                    "fcnet_hiddens":[512, 256, 128], 
                                    "fcnet_activation": "tanh",
                                }
config["evaluation_num_workers"] = 1
config["evaluation_config"] =   {
                                    "render_env": True,
                                }
config["train_batch_size"] = 1000

# print(pretty_print(config))

tune.run("PPO", config=config)


