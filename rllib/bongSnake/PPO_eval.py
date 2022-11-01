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
                                    "fcnet_hiddens":[512, 256, 128], 
                                    "fcnet_activation": "tanh",
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
algo.load_checkpoint("/home/bong/ray_results/PPO_bongEnv_2022-11-01_02-58-35vczmb1gh/checkpoint_000501/checkpoint-501")

algo.evaluate()