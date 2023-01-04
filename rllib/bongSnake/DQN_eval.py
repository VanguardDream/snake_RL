import ray

# import rl 알고리즘
import ray.rllib.algorithms.dqn as dqn

config = dqn.DEFAULT_CONFIG.copy()

############# Customize Hyper-Parameters
config["num_gpus"] = 1
config["num_workers"] = 1
config["gamma"] = 0.9
config["framework"] = 'tf'
# config["model"] =               {
#                                     "fcnet_hiddens":[512, 256, 128], 
#                                     "fcnet_activation": "tanh",
#                                 }
config["evaluation_num_workers"] = 1
config["evaluation_config"] =   {
                                    "render_env": True,
                                }
config["train_batch_size"] = 1024

############# Create PPO Instance & Initiating
ray.init()

algo = dqn.DQN(config, 'bongEnv-v3')
algo.restore("/home/bong/ray_results/DQN_bongEnv-v3_2022-11-27_06-41-40l4bvjj8n/checkpoint_022503")

algo.evaluate()