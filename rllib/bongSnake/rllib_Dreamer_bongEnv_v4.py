import ray

# import rl 알고리즘
import ray.rllib.algorithms.dreamer as dreamer
import datetime

from ray.tune.logger import pretty_print

_short_comment = 'V4 : Model based algorithm applied (Dreamer)'

config = dreamer.DEFAULT_CONFIG.copy()
# _cp_path = "/home/bong/ray_results/PPO_bongEnv-v3_2022-11-10_19-34-41klb9ik01/checkpoint_020001/checkpoint-20001"

############# Customize Hyper-Parameters
config["gamma"] = 0.9
config["framework"] = 'torch'

############# Create PPO Instance & Initiating
ray.init()

algo = dreamer.Dreamer(config, 'bongEnv-v4')
# algo.restore(_cp_path)

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
