import gd_tor_snake_v1
import gymnasium as gym
import numpy as np

import os
import pathlib
import time
import mediapy as media
import ray

from gymnasium.utils.save_video import save_video
from gd_tor_snake_v1.envs.plane_v1 import PlaneWorld
from ray import tune

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = pathlib.Path(__location__)
__model_location__ = __location__.parent.parent.joinpath('models')
__model_path__ = os.path.join(__model_location__,'env_snake_v1.xml')

from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.logger import pretty_print
from ray.tune.registry import register_env

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

ray.init()
register_env("snake_env", lambda env_config: PlaneWorld(env_config))

config = (  # 1. Configure the algorithm,
    PPOConfig()
    .environment("snake_env")
    .rollouts(num_rollout_workers=2)
    .framework("torch")
    .training(model={"fcnet_hiddens": [64, 64]})
    .evaluation(evaluation_num_workers=1)
)

algo = config.build()  # 2. build the algorithm,


# #camera names : com, ceiling, head_mount
# # (30,30,40,40,0) # serpentine
# # (45,45,10,10,45) # sidewinding
# # (0,0,30,30,90) # rolling
# # (30,30,40,40,90) # helix
# env = gym.make("gd_tor_snake_v1/plane-v1", 
#                model_path = __model_path__, 
#                terminate_when_unhealthy = True, 
#                ctrl_cost_weight = 0.2, 
#                render_mode = 'rgb_array', 
#                render_camera_name = "com", 
#                use_gait = False,
#                gait_params = (30,30,40,40,0)) 
# _ = env.reset()

# step_starting_index = 0
# episode_index = 8
# video_prefix = "PPO_20240126"
# frames = []

# for i in range(1000):
#     # random = np.random.random(14) * 1.5
#     random = np.ones(14) * 0.3

#     obs, rew, terminated, _, info = env.step(random)

#     pixels = env.render()

#     frames.append(pixels)

# env.reset()

# save_video(frames,"../videos", name_prefix=video_prefix, fps=env.metadata["render_fps"], step_starting_index = step_starting_index, episode_index = episode_index)

# env.close()
        