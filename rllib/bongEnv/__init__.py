from gym.envs.bongEnv.gait import snake_gait
from gym.envs.bongEnv.bongSnake import bongEnv
from gym.envs.bongEnv.bongSnake_v2 import bongEnv_v2

# register(
#     id="bongEnv",
#     entry_point="gym.envs.bongEnv.bonsSnake:bongEnv",
#     max_episode_steps=1000,
# )

register(
    id="bongEnv-v2",
    entry_point="gym.envs.bongEnv.bongSnake_v2:bongEnv_v2",
    max_episode_steps=1000,
)
