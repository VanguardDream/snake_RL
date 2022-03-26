import os
import gym
import bongSnake
from stable_baselines3 import A2C, PPO
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
			self.model.save("model-ppo.zip")
			self.training_env.save("stats-ppo.pkl")

		return True

if __name__ == '__main__':

	# inits
	env = gym.make('bongEnv-v0')
	# env = Monitor(env)

	env = DummyVecEnv([lambda: Monitor(env)])
	model = None

	# load recent checkpoint
	if os.path.isfile("model-ppo.zip") and os.path.isfile("stats-ppo.pkl"):
		env = VecNormalize.load("stats-ppo.pkl", env)
		env.reset()
		model = PPO.load("model-ppo.zip", env)
	else:
		env = VecNormalize(env)
		model = PPO('MlpPolicy', env, verbose = 1, tensorboard_log = "./PPO/")

	# replay buffer
	if os.path.isfile("replay_buffer-ppo.pkl"):
		model.load_replay_buffer("replay_buffer-ppo.pkl")

	# train
	model.learn(500000,
		callback = SaveCheckpoint(10000),
		log_interval = 1,
		reset_num_timesteps = False
	)

	env.close()


# # Loading & Evaluating

# model = PPO.load("model-ppo")

# eval_env = bongSnake.bongEnv(render_option=True)

# obs = eval_env.reset()
# for i in range(1000):
#     action, _state = model.predict(obs, deterministic=True)
#     print(action)
#     obs, reward, done, info = eval_env.step(action)
#     if done:
#       obs = eval_env.reset()