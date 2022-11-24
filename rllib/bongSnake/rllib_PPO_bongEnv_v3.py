import ray

# import rl 알고리즘
import ray.rllib.algorithms.ppo as ppo
import datetime

from ray.tune.logger import pretty_print

_short_comment = 'V3 : after 20000 iter'

config = ppo.DEFAULT_CONFIG.copy()
_cp_path = "/home/bong/ray_results/PPO_bongEnv-v3_2022-11-12_11-41-07gt8o20bn/checkpoint_031502/checkpoint-31502"

############# Customize Hyper-Parameters
config["num_gpus"] = 1
config["num_workers"] = 4
config["gamma"] = 0.99
config["framework"] = 'torch'
config["model"] =               {
                                    "fcnet_hiddens":[512, 256, 128], 
                                    "fcnet_activation": "tanh",
                                }
config["evaluation_num_workers"] = 1
config["evaluation_config"] =   {
                                    "render_env": True,
                                }
config["train_batch_size"] = 2048
# print(pretty_print(config))

############# Create PPO Instance & Initiating
ray.init()

algo = ppo.PPO(config, 'bongEnv-v3')
# algo.load_checkpoint(_cp_path)
algo.restore(_cp_path)

f_log = open('./training_log.txt','a')
_date = datetime.datetime.now().strftime('%Y_%m_%d %A %H:%M:%S')
f_log.write(f'Train start at {_date}\n')
f_log.write(_short_comment+'\n')
f_log.close()

############# Training
for i in range(20001):
    result = algo.train()
    print(pretty_print(result))
    print(f'>>>>>>>>>Training...{i} th for loop...')

    if i % 500 == 0:
        cp_i = algo.save()
        f_log = open('./training_log.txt','a')
        f_log.write('\tSaved check point at : \"' + cp_i + f'\" (>> i: {i}) \n')
        f_log.close()
