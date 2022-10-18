import ray
import gym

from ray.rllib.algorithms.ppo import PPO

config = { "env":"bongEnv",
            "num_workers": 1,
            "framework":"torch",
            "num_gpus":1,
            "model":{"fcnet_hiddens":[57, 64, 14], "fcnet_activation": "relu",},
            "evaluation_num_workers": 1,
            "evaluation_config": {
            "render_env": True,
            # "controller_input" : (0.99, 0, 0),
            },

        }

env = gym.make('bongEnv')

algo = PPO(config=config)
algo.restore("./tmp/checkpoint_000010")

obs = env.reset()
env.render()
for _ in range(1000):
    action = algo.compute_action(obs)
    obs, reward, b, c = env.step(action)
    print(reward)
