import ray

from ray.rllib.algorithms.ppo import PPO
from ray.rllib.algorithms.sac import SAC
from ray.tune.logger import pretty_print

PPO.get_default_config()

import gym

version = 'v20221017'

config = { "env":"bongEnv",
            "num_workers": 10,
            "framework":"torch",
            "num_gpus":1,
            "model":{"fcnet_hiddens":[57, 64, 14], "fcnet_activation": "relu",},
            "evaluation_num_workers": 1,
            "evaluation_config": {
            "render_env": True,
            # "controller_input" : (0.99, 0, 0),
            },

        }

algo = PPO(config=config)
# algo.restore("./tmp/checkpoint_000005")

for _ in range(10):
    # print(algo.train())
    step_train_result = algo.train()

    if _ % 1 == 0:
        print(pretty_print(step_train_result))
        print(f'Outter Loop Iteration : {_}')
cp_path = algo.save('./tmp/')
print(f"Check point saved!, Path : \"{cp_path}\"")

algo.evaluate()
