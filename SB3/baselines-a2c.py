from operator import truediv
import os
import gym
import bongSnake_v3
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env

version = "v3"

# ## Saving Callback func.
# class SaveCheckpoint(BaseCallback):
# 	def __init__(self, save_freq, verbose = 0):
# 		super(SaveCheckpoint, self).__init__(verbose)
# 		self.save_freq = save_freq

# 	def _on_step(self):
# 		if self.num_timesteps % self.save_freq == 0:
# 			self.model.save("model_"+version+".zip")
# 			self.training_env.save("stats_"+version+".pkl")

# 		return True

# if __name__ == '__main__':

# 	# inits
# 	env = gym.make('bongSnake-v3', render_option = True)
# 	# env = Monitor(env)

# 	env = DummyVecEnv([lambda: Monitor(env)])
# 	model = None

# 	# load recent checkpoint
# 	if os.path.isfile("model_"+version+".zip") and os.path.isfile("stats_"+version+".pkl"):
# 		env = VecNormalize.load("stats_"+version+".pkl", env)
# 		env.reset()
# 		model = A2C.load("model_"+version+".zip", env)
# 	else:
# 		env = VecNormalize(env)
# 		model = A2C('MlpPolicy', env, verbose = 1, tensorboard_log = "./A2C_"+version+"/", learning_rate=0.1, gamma= 0.8)

# 	# replay buffer
# 	if os.path.isfile("replay_buffer_"+version+".pkl"):
# 		model.load_replay_buffer("replay_buffer_"+version+".pkl")

# 	# train
# 	model.learn(500000,
# 		callback = SaveCheckpoint(5000),
# 		log_interval = 10,
# 		reset_num_timesteps = False
# 	)

# 	env.close()


# Loading & Evaluating

model = A2C.load("model_"+version+".zip")

eval_env = bongSnake_v3.bongEnv_v3(render_option=True)

obs = eval_env.reset()
for i in range(10000):
    action, _state = model.predict(obs, deterministic=True)
    print(action)
    obs, reward, done, info = eval_env.step(action)
    if done:
      obs = eval_env.reset()