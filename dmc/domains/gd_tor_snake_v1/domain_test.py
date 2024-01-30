import gd_tor_snake_v1
import gymnasium as gym
import numpy as np

import os
import pathlib
import time
import mediapy as media

from gymnasium.utils.save_video import save_video

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = pathlib.Path(__location__)
__model_location__ = __location__.parent.parent.joinpath('models')
__model_path__ = os.path.join(__model_location__,'env_snake_v1.xml')

#camera names : com, ceiling, head_mount
# (30,30,40,40,0) # serpentine
# (45,45,10,10,45) # sidewinding
# (0,0,30,30,90) # rolling
# (30,30,40,40,90) # helix
env = gym.make("gd_tor_snake_v1/plane-v1", 
               terminate_when_unhealthy = True, 
               render_mode = 'human', 
               render_camera_name = "head_mount", 
               use_gait = True,
               gait_params = (0,0,30,30,90),) 
_ = env.reset()

step_starting_index = 0
episode_index = 8
video_prefix = "PPO_20240126-0.28.1"
frames = []

for i in range(3000):
    # random = np.random.random(14) * 1.5
    random = np.ones(14) * 0.3

    obs, rew, terminated, _, info = env.step(random)
    if terminated:
        env.reset()

    if i % 300 == 0:
        env.reset()

    # print(info)
    # print(np.round((info['reward_forward'] + info['reward_side']),6))
    print(np.round(info['reward_forward'],6), end='    ')
    print(np.round(info['reward_side'],6), end='    ')
    print(np.round(info['reward_unhealthy'],6), end='    ')
    print(np.round(info['reward_healthy'],6))

    pixels = env.render()

    frames.append(pixels)

env.reset()

# save_video(frames,"../videos", name_prefix=video_prefix, fps=env.metadata["render_fps"], step_starting_index = step_starting_index, episode_index = episode_index)

env.close()
        