import ray

# import rl 알고리즘
import ray.rllib.algorithms.a2c as a2c

from ray.tune.logger import pretty_print

config = a2c.A2C_DEFAULT_CONFIG.copy()

############# Customize Hyper-Parameters
config["num_gpus"] = 1
config["num_workers"] = 4
config["gamma"] = 0.9
config["framework"] = 'torch'
# config["model"] =               {
#                                     "fcnet_hiddens":[512, 256, 128], 
#                                     "fcnet_activation": "tanh",
#                                 }
config["evaluation_num_workers"] = 1
config["evaluation_config"] =   {
                                    "render_env": True,
                                }
config["train_batch_size"] = 512
# print(pretty_print(config))

############# Create PPO Instance & Initiating
ray.init()

algo = a2c.A2C(config, 'bongEnv')
algo.load_checkpoint("/home/bong/ray_results/A2C_bongEnv_2022-11-07_10-41-21jocess0_/checkpoint_003001/checkpoint-3001")

algo.evaluate()