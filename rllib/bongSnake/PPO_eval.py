from dataclasses import dataclass
import ray

# import rl 알고리즘
import ray.rllib.algorithms.ppo as ppo

from ray.tune.logger import pretty_print

config = ppo.DEFAULT_CONFIG.copy()

############# Customize Hyper-Parameters
config["env_config"] =          {
                                    "print_input_command" : True,
                                }
config["num_gpus"] = 1
config["num_workers"] = 0
config["gamma"] = 0.9
config["framework"] = 'torch'
config["model"] =               {
                                    "fcnet_hiddens":[128, 64], 
                                    "fcnet_activation": "relu",
                                }
config["evaluation_num_workers"] = 1
config["evaluation_config"] =   {
                                    "render_env": True,                                
                                }
config["evaluation_duration"] = 30
# print(pretty_print(config))

############# Create PPO Instance & Initiating
ray.init()

algo = ppo.PPO(config, 'bongEnv')
algo.load_checkpoint("/home/bong/ray_results/PPO_bongEnv_2022-10-20_14-49-57md2dl9dg/checkpoint_001501/checkpoint-1501")

algo.evaluate()