import os
from bongSnake import bongEnv
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import VecNormalize
from stable_baselines3.common.env_util import make_vec_env

env = make_vec_env(bongEnv,n_envs=10)

model = A2C('MlpPolicy', env, verbose=1)

model.learn(total_timesteps = 100000)

model.save("BongEnv_A2C")

# model = A2C.load("BongEnv_A2C")

# obs = env.reset()

# while True:
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     print(rewards)

# # # Don't forget to save the VecNormalize statistics when saving the agent
# # log_dir = "/tmp/"
# # model.save(log_dir + "A2C_bongSnake")

# # stats_path = os.path.join(log_dir, "vec_normalize.pkl")
# # env.save(stats_path)

# eval_env = bongEnv(render_option=True)

# eval_env.reset()

# for i in range(1000):
#     action, _state = model.predict(obs, deterministic=True)
#     print(action)
#     obs, reward, done, info = eval_env.step(action)
#     if done:
#       obs = eval_env.reset()
