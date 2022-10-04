from curses.ascii import ctrl
from operator import truediv
import os
from statistics import mode
import gym
import numpy as np
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



for _ in range(500):
	rand_ctrl = np.random.randint([-9,-9,-9],[9,9,9])/10
	env = gym.make('bongSnake-v5', controller_input = rand_ctrl)

	# load recent checkpoint
	if os.path.isfile("model-Torque-PPO"+version +".zip"):
		env.reset()
		model = PPO.load("model-Torque-PPO"+version +".zip", env)
	else:
		model = PPO('MlpPolicy', env, verbose = 1, tensorboard_log = str("./TorquePPO/"+version), gamma=0.8,)

	# train
	model.learn(total_timesteps=10000,
		log_interval = 1,
		reset_num_timesteps = False
	)

	model.save("model-Torque-PPO"+version +".zip")
	print(f'saved! iteration : {_}, ctrl : {rand_ctrl}')