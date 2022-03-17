import gym, ray
from ray import tune
from ray.tune.registry import register_env
from ray.rllib.agents import ppo
from ray.rllib.env.env_context import EnvContext
import bongSnake

ray.init()

register_env("bongsnake", bongSnake.bongEnv)

# trainer = ppo.PPOTrainer(env="bongsnake",config={"framework": "torch"})

tune.run(ppo.PPOTrainer, stop= {"timesteps_total": 200}, config={"env": "bongsnake","framwork" : "torch"})