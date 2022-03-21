import imp
import gym, ray
from gym import envs
from ray import tune
from ray.tune.registry import register_env
from ray.rllib.agents import ppo
from ray.rllib.agents import with_common_config
from ray.rllib.agents import pg
from ray.rllib.env.env_context import EnvContext
import bongSnake

import os
import shutil
chkpt_root = "tmp/exa"
shutil.rmtree(chkpt_root, ignore_errors=True, onerror=None)
ray_results = "{}/ray_results/".format(os.getenv("HOME"))
shutil.rmtree(ray_results, ignore_errors=True, onerror=None)

ray.init(ignore_reinit_error=True)

select_env = "bongsnake"
register_env(select_env, lambda config: gym.make('Ant-v3'))

config = ppo.DEFAULT_CONFIG.copy()
config["log_level"] = "WARN"

agent = ppo.PPOTrainer(config, env=select_env)

status = "{:2d} reward {:6.2f}/{:6.2f}/{:6.2f} len {:4.2f} saved {}"
n_iter = 5
for n in range(n_iter):
    result = agent.train()
    chkpt_file = agent.save(chkpt_root)
    print(status.format(
            n + 1,
            result["episode_reward_min"],
            result["episode_reward_mean"],
            result["episode_reward_max"],
            result["episode_len_mean"],
            chkpt_file
            ))