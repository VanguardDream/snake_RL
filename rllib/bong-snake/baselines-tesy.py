import os
from bongSnake import bongEnv
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import VecNormalize
from stable_baselines3.common.env_util import make_vec_env

# # Learning

# env = make_vec_env(bongEnv, n_envs=6)

# model = A2C('MlpPolicy', env, verbose=1, tensorboard_log="./tb_bongEnv/")

# model.learn(total_timesteps = 100000, tb_log_name="1st batch")
# model.learn(total_timesteps = 100000, tb_log_name="2nd batch")
# model.learn(total_timesteps = 100000, tb_log_name="3th batch")
# model.learn(total_timesteps = 100000, tb_log_name="4th batch")
# model.learn(total_timesteps = 100000, tb_log_name="5th batch")

# model.save("BongEnv_A2C")


## Loading & Evaluating

model = A2C.load("BongEnv_A2C")

eval_env = bongEnv(render_option=True)

obs = eval_env.reset()

for i in range(1000):
    action, _state = model.predict(obs, deterministic=True)
    print(action)
    obs, reward, done, info = eval_env.step(action)
    if done:
      obs = eval_env.reset()
