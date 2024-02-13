import os
import pathlib
import gd_tor_snake_v1
import gymnasium as gym
import mediapy as media
import torch as th

from sb3_contrib import RecurrentPPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from gymnasium.utils.save_video import save_video


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = pathlib.Path(__location__)
__model_location__ = __location__.parent.parent.joinpath('models')
__model_path__ = os.path.join(__model_location__,'env_snake_v1.xml')
__contact_model_path__ = os.path.join(__model_location__,'env_snake_v1_contact.xml')

env_config = {
                "model_path": __contact_model_path__,
                "terminate_when_unhealthy":True,
                "side_cost_weight": 10,
                "healthy_reward" : 1.0,
                "render_mode": 'rgb_array',
                "render_camera_name": "com",
                "use_gait": True,
                "gait_params": (30,30,15,15,0),
            }

policy_kwargs = dict(net_arch=dict(pi=[128, 128], vf=[128, 128]))

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

if __name__ == '__main__':

    # Env Creating
    vec_env = make_vec_env("gd_tor_snake_v1/plane-v1", n_envs=32, vec_env_cls=SubprocVecEnv, vec_env_kwargs=dict(start_method='spawn'), env_kwargs=env_config)

    # 20240204 Optuna hyper-params
    model = RecurrentPPO(
        "MlpLstmPolicy", 
        vec_env, 
        batch_size=32768, 
        n_steps=32768, 
        gamma=0.9, 
        learning_rate=0.001, 
        ent_coef=4.1605292e-05, 
        clip_range=0.4, 
        n_epochs=5, 
        gae_lambda=0.9, 
        max_grad_norm=5, 
        vf_coef=0.143442327, 
        use_sde=True,
        sde_sample_freq=8,
        tensorboard_log = tensorboard_logdir + "/" + log_prefix, 
        verbose=1, 
        policy_kwargs= policy_kwargs,
        )

    # Loading
    model = RecurrentPPO.load(policy_dir+'/RPPO/'+'20240207_17-50-46.zip',env=vec_env) # For learning 삭제하지 않고 계속 아래로 이어갈 것!!
    # model = PPO.load(policy_dir+'/PPO/'+'20240201_01-22-36.zip',env=env) # For evaluating

    # Check point CB
    from stable_baselines3.common.callbacks import CheckpointCallback
    cp_callback = CheckpointCallback(
        save_freq=500000,
        save_path= policy_dir+'/RPPO/'+__now_str+'/',
        save_replay_buffer= True,
        save_vecnormalize= True,
    )

    model.learn(total_timesteps=100000000,callback=cp_callback, progress_bar=True)
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