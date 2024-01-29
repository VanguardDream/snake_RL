import os
import pathlib
import gd_tor_snake_v1
import gymnasium as gym
import mediapy as media

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from gymnasium.utils.save_video import save_video
from gd_tor_snake_v1.envs.gait import Gait

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = pathlib.Path(__location__)
__model_location__ = __location__.parent.parent.joinpath('models')
__model_path__ = os.path.join(__model_location__,'env_snake_v1.xml')

env_config = {
                "terminate_when_unhealthy":True,
                "forward_reward_weight": 2,
                "side_cost_weight": 1.1,
                "ctrl_cost_weight": 0.1,
                "render_mode": 'rgb_array',
                "render_camera_name": "com",
                "healthy_reward": 0.2,
                "use_gait": False,
                "gait_params": (30,30,40,40,0),
            }


gait = Gait((30,30,40,40,0))

env = gym.make("gd_tor_snake_v1/plane-v1", 
               model_path = __model_path__, 
               terminate_when_unhealthy = True,
               forward_reward_weight = 2,
               side_cost_weight = 1.1,
               ctrl_cost_weight = 0.1, 
               render_mode = 'rgb_array', 
               render_camera_name = "head_mount", 
               healthy_reward = 0.2,
               use_gait = False,
               gait_params = (30,30,40,40,0)) 

step_starting_index = 0
episode_index = 8
policy_dir = "../policies"
os.makedirs(policy_dir, exist_ok=True)
tensorboard_logdir = "../tensorboard"
os.makedirs(tensorboard_logdir, exist_ok=True)

import datetime
__now_str = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
video_prefix = "SB3_PPO_" + __now_str
log_prefix = "/SB3_PPO_" + __now_str

# Learning
# vec_env = make_vec_env("gd_tor_snake_v1/plane-v1", n_envs=10, env_kwargs=env_config)
# model = PPO("MlpPolicy", vec_env, gamma=0.9, tensorboard_log= tensorboard_logdir + log_prefix, verbose=1)
# model.learn(total_timesteps=2000000)

# model.save(f"{policy_dir+'/PPO/'+__now_str}")

# Loading
model = PPO.load(policy_dir+'/PPO/'+'20240129_14-30-22')
obs, info = env.reset()

# frames = []
# for i in range(1000):
#     action, _states = model.predict(obs, deterministic=True)
#     obs, reward, done, _, info = env.step(action)
#     obs[-14:] = gait.getMvec(i)

#     pixels = env.render()
#     frames.append(pixels)

# save_video(frames,"../videos", name_prefix=video_prefix, fps=env.metadata["render_fps"], step_starting_index = step_starting_index, episode_index = episode_index)