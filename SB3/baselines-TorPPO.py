from operator import truediv
import os
import gym
import bongSnake_v5
from stable_baselines3 import A2C
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env

version = 'v1'

# Saving Callback func.
class SaveCheckpoint(BaseCallback):
	def __init__(self, save_freq, verbose = 0):
		super(SaveCheckpoint, self).__init__(verbose)
		self.save_freq = save_freq

	def _on_step(self):
		if self.num_timesteps % self.save_freq == 0:
			self.model.save("model-torque-ppo_"+ version +".zip")
			self.training_env.save("model-torque-ppo_"+ version +".pkl")

		return True

env = gym.make('bongSnake-v5')

# load recent checkpoint
if os.path.isfile("model-Torque-PPO"+version +".zip") and os.path.isfile("stats-ppo_v"+ version +".pkl"):
	env = VecNormalize.load("stats-ppo_v"+ version +".pkl", env)
	env.reset()
	model = PPO.load("model-Torque-PPO"+version +".zip", env)
else:
	env = VecNormalize(env)
	model = PPO('MlpPolicy', env, verbose = 1, tensorboard_log = str("./PPO/v"+version), gamma=0.8,)

 # train
model.learn(total_timesteps=500,
    log_interval = 1,
    reset_num_timesteps = False
)

model.save()