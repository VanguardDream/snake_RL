from bongSnake import bongEnv
from testAnt import AntEnv

from ray.rllib.agents.ppo import PPOTrainer

trainer = PPOTrainer(
    config={
        "env": AntEnv
    })

