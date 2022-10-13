from ray.rllib.algorithms.ppo import PPO
from ray.rllib.algorithms.sac import SAC

import gym

config = { "env":"bongEnv",
            "num_workers": 4,
            "framework":"torch",
            "model":{"fcnet_hiddens":[57, 64, 14], "fcnet_activation": "relu",},
            "evaluation_num_workers": 1,
            "evaluation_config": {
            "render_env": True,
            },

        }

algo = PPO(config=config)

for _ in range(5):
    # print(algo.train())
    algo.train()

algo.evaluate()
