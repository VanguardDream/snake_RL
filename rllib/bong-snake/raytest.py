import gym, ray
from ray import tune
from ray.tune.registry import register_env
from ray.rllib.agents import ppo
from ray.rllib.agents import with_common_config
from ray.rllib.agents import pg
from ray.rllib.env.env_context import EnvContext
import bongSnake

ray.init()

register_env("bongsnake", bongSnake.bongEnv)


# Add the following (PG-specific) updates to the (base) `Trainer` config in
# rllib/agents/trainer.py (`COMMON_CONFIG` dict).
DEFAULT_CONFIG = with_common_config({
    # No remote workers by default.
    "num_workers": 0,
    # Learning rate.
    "lr": 0.0004,

    # Experimental: By default, switch off preprocessors for PG.
    "_disable_preprocessor_api": True,

    # PG is the first algo (experimental) to not use the distr. exec API
    # anymore.
    "_disable_execution_plan_api": True,
    "framework":"torch",
})

# trainer = ppo.PPOTrainer(env="bongsnake",config={"framework": "torch"})

# for _ in range(3):
#     print(trainer.train())

# trainer.evaluate()


vg_trainer = pg.PGTrainer(env="bongsnake",config=DEFAULT_CONFIG)

for _ in range(3):
    print(vg_trainer.train())

vg_trainer.evaluate()