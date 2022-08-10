import os
import gym
import numpy as np
import bongSnake_v3
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env

version = "0810"
testing = False

# Saving Callback func.
class SaveCheckpoint(BaseCallback):
	def __init__(self, save_freq, verbose = 0):
		super(SaveCheckpoint, self).__init__(verbose)
		self.save_freq = save_freq

	def _on_step(self):
		if self.num_timesteps % self.save_freq == 0:
			self.model.save("model-ppo_v"+ version +".zip")
			self.training_env.save("stats-ppo_v"+ version +".pkl")

		return True

if __name__ == '__main__':

  if not testing:
    # inits
    env = gym.make('bongSnake-v3', render_option = True)
    # env = Monitor(env)

    env = DummyVecEnv([lambda: Monitor(env)])
    model = None

    # load recent checkpoint
    if os.path.isfile("model-ppo_v"+ version +".zip") and os.path.isfile("stats-ppo_v"+ version +".pkl"):
      env = VecNormalize.load("stats-ppo_v"+ version +".pkl", env)
      env.reset()
      model = PPO.load("model-ppo_v"+ version +".zip", env)
    else:
      env = VecNormalize(env)
      model = PPO('MlpPolicy', env, verbose = 1, tensorboard_log = str("./PPO/v"+version), gamma=0.8,)

    # replay buffer
    if os.path.isfile("replay_buffer-ppo_v"+ version +".pkl"):
      model.load_replay_buffer("replay_buffer-ppo_v"+ version +".pkl")

    # train
    model.learn(50000000,
      callback = SaveCheckpoint(1000),
      log_interval = 1,
      reset_num_timesteps = False
    )

    env.close()

  # Loading & Evaluating
  if testing:

    # eval_env = gym.make('bongSnake-v3', render_option = True)
    # eval_env = DummyVecEnv([lambda: Monitor(eval_env)])

    eval_env = bongSnake_v3.bongEnv_v3(render_option=True)
    model = PPO.load("model-ppo_v"+ version +".zip",eval_env)


    eval_env.reset_model()
    obs, reward, done, info = eval_env.step(np.array([6, 4, 3, 6, 4, 3, 4]))
    for i in range(1000000):
        action, _state = model.predict(obs)
        obs, reward, done, info = eval_env.step(action)
        if done:
          obs = eval_env.reset_model()