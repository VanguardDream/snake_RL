from dataclasses import dataclass
import ray

# import rl 알고리즘
import ray.rllib.algorithms.ppo as ppo
import datetime

from ray.tune.logger import pretty_print

config = ppo.DEFAULT_CONFIG.copy()
_short_comment = 'Direc cost, crrl cost removed, forward reward increased'

############# Customize Hyper-Parameters
config["num_gpus"] = 1
config["num_workers"] = 10
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
# print(pretty_print(config))

############# Create PPO Instance & Initiating
ray.init()

algo = ppo.PPO(config, 'bongEnv')

f_log = open('./training_log.txt','a')
_date = datetime.datetime.now().strftime('%Y_%m_%d %A %H:%M:%S')
f_log.write(f'Train start at {_date}\n')
f_log.write(_short_comment+'\n')
f_log.close()

############# Training
for i in range(2000):
    result = algo.train()
    print(pretty_print(result))
    print(f'>>>>>>>>>Training...{i} th for loop...')

    if i % 500 == 0:
        cp_i = algo.save()
        f_log = open('./training_log.txt','a')
        f_log.write('\tSaved check point at : \"' + cp_i + f'\" (>> i: {i}) \n')
        f_log.close()
