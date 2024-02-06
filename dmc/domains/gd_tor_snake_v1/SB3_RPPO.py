import os
import pathlib
import gd_tor_snake_v1
import gymnasium as gym
import mediapy as media
import torch as th

from sb3_contrib import RecurrentPPO
from stable_baselines3.common.env_util import make_vec_env
from gymnasium.utils.save_video import save_video
from gd_tor_snake_v1.envs.gait import Gait

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = pathlib.Path(__location__)
__model_location__ = __location__.parent.parent.joinpath('models')
__model_path__ = os.path.join(__model_location__,'env_snake_v1.xml')
__contact_model_path__ = os.path.join(__model_location__,'env_snake_v1_contact.xml')

env_config = {
                "model_path": __contact_model_path__,
                "terminate_when_unhealthy":True,
                "side_cost_weight": 1,
                "render_mode": 'rgb_array',
                "render_camera_name": "com",
                "use_gait": False,
                "gait_params": (30,30,15,15,0),
            }

policy_kwargs = dict(net_arch=dict(pi=[256, 256, 64], vf=[256, 256]))

step_starting_index = 0
episode_index = 8
policy_dir = "../policies"
os.makedirs(policy_dir, exist_ok=True)
tensorboard_logdir = "../tensorboard"
os.makedirs(tensorboard_logdir, exist_ok=True)

import datetime
__now_str = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
video_prefix = "SB3_RPPO_" + __now_str
log_prefix = "SB3_RPPO_" + __now_str

# # # Learning
vec_env = make_vec_env("gd_tor_snake_v1/plane-v1", n_envs=60, env_kwargs=env_config)
# vec_env_control = make_vec_env("gd_tor_snake_v1/plane-control", n_envs=60, env_kwargs=env_config)

# 20240204 Optuna hyper-params
model = RecurrentPPO(
    "MlpLstmPolicy", 
    vec_env, 
    batch_size=128, 
    n_steps=32, 
    gamma=0.995, 
    learning_rate=8.838841e-05, 
    clip_range=0.2, 
    n_epochs=5, 
    gae_lambda=0.9, 
    max_grad_norm=0.9, 
    vf_coef=0.667859, 
    use_sde=True,
    sde_sample_freq=16,
    tensorboard_log = tensorboard_logdir + "/" + log_prefix, 
    verbose=1, 
    policy_kwargs= policy_kwargs)

# Loading
# model = PPO.load(policy_dir+'/PPO/'+'20240130_21-12-04.zip',env=vec_env) # For learning 삭제하지 않고 계속 아래로 이어갈 것!!
# model = PPO.load(policy_dir+'/PPO/'+'20240201_01-22-36.zip',env=env) # For evaluating

# Check point CB
from stable_baselines3.common.callbacks import CheckpointCallback
cp_callback = CheckpointCallback(
    save_freq=10000,
    save_path= policy_dir+'/RPPO/'+__now_str+'/',
    save_replay_buffer= True,
    save_vecnormalize= True,
)

model.learn(total_timesteps=20000000,callback=cp_callback, progress_bar=True)
model.save(f"{policy_dir+'/RPPO/'+__now_str}")


# frames = []
# obs, info = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs, deterministic=True)
#     obs, reward, done, _, info = env.step(action)
#     # obs[-14:] = gait.getMvec(i)

#     pixels = env.render()
#     frames.append(pixels)

# save_video(frames,"../videos", name_prefix=video_prefix, fps=env.metadata["render_fps"], step_starting_index = step_starting_index, episode_index = episode_index)