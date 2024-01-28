import os
import pathlib
import gd_tor_snake_v1
import gymnasium as gym
import mediapy as media

from stable_baselines3 import PPO
from gymnasium.utils.save_video import save_video
from gd_tor_snake_v1.envs.gait import Gait

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = pathlib.Path(__location__)
__model_location__ = __location__.parent.parent.joinpath('models')
__model_path__ = os.path.join(__model_location__,'env_snake_v1.xml')

gait = Gait((30,30,40,40,0))

env = gym.make("gd_tor_snake_v1/plane-v1", 
               model_path = __model_path__, 
               terminate_when_unhealthy = True,
               forward_reward_weight = 7,
               ctrl_cost_weight = 0.2, 
               render_mode = 'rgb_array', 
               render_camera_name = "com", 
               healthy_reward = 0.2,
               use_gait = True,
               gait_params = (30,30,40,40,0)) 

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=30000)

vec_env = model.get_env()
obs = vec_env.reset()


step_starting_index = 0
episode_index = 8
video_prefix = "SB3_PPO_20240128"
frames = []

for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    obs[:, -14:] = gait.getMvec(i)

    pixels = vec_env.render()
    frames.append(pixels)

save_video(frames,"../videos", name_prefix=video_prefix, fps=env.metadata["render_fps"], step_starting_index = step_starting_index, episode_index = episode_index)