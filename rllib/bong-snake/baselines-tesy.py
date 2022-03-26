import os
import gym
from bongSnake import bongEnv
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env


## Saving Callback func.
class SaveCheckpoint(BaseCallback):
	def __init__(self, save_freq, verbose = 0):
		super(SaveCheckpoint, self).__init__(verbose)
		self.save_freq = save_freq

	def _on_step(self):
		if self.num_timesteps % self.save_freq == 0:
			self.model.save("AutoSavedmodel.zip")
			self.training_env.save("stats.pkl")

		return True

# Learning
# env = make_vec_env('bongEnv-v0', n_envs=6)
# env = DummyVecEnv( [lambda: Monitor(bongEnv(),info_keywords=("reward_forward", "reward_ctrl", "reward_contact", "reward_survive", "x_position", "y_position", "distance_from_origin", "x_velocity", "y_velocity", "forward_reward"))] )

env = gym.make('bongEnv-v0')
env = Monitor(env)

model = A2C('MlpPolicy', env, verbose=1, tensorboard_log="./A2C_bongEnv/")


model.learn(total_timesteps = 100000, tb_log_name="1st batch")
# model.learn(total_timesteps = 100000, tb_log_name="2nd batch")
# model.learn(total_timesteps = 100000, tb_log_name="3th batch")
# model.learn(total_timesteps = 100000, tb_log_name="4th batch")
# model.learn(total_timesteps = 100000, tb_log_name="5th batch")

model.save("BongEnv_A2C")


# ## Loading & Evaluating

# model = A2C.load("BongEnv_A2C")

# eval_env = bongEnv(render_option=True)

# obs = eval_env.reset()
# for i in range(1000):
#     action, _state = model.predict(obs, deterministic=True)
#     print(action)
#     obs, reward, done, info = eval_env.step(action)
#     if done:
#       obs = eval_env.reset()
