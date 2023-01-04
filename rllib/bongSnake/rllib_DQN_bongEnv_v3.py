import ray

# import rl 알고리즘
import ray.rllib.algorithms.dqn as dqn
import datetime

from ray.tune.logger import pretty_print

_short_comment = 'V3: Restore data at 17002'

config = dqn.DEFAULT_CONFIG.copy()
_cp_path = "/home/bong/ray_results/DQN_bongEnv-v3_2022-11-24_21-28-20pazj6_lr/checkpoint_017002"

############# Customize Hyper-Parameters
config["num_gpus"] = 1
config["num_workers"] = 8
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
# print(pretty_print(config))

############# Create PPO Instance & Initiating
algo = dqn.DQN(config, 'bongEnv-v3')
algo.restore(_cp_path)

f_log = open('./training_log.txt','a')
_date = datetime.datetime.now().strftime('%Y_%m_%d %A %H:%M:%S')
f_log.write(f'Train start at {_date}\n')
f_log.write(_short_comment+'\n')
f_log.close()

############# Training
for i in range(10001):
    result = algo.train()
    print(pretty_print(result))
    print(f'>>>>>>>>>Training...{i} th for loop...')

    if i % 500 == 0:
        cp_i = algo.save()
        f_log = open('./training_log.txt','a')
        f_log.write('\tSaved check point at : \"' + cp_i + f'\" (>> i: {i}) \n')
        f_log.close()
