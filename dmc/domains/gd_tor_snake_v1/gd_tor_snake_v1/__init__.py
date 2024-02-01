from gymnasium.envs.registration import register

register(
    id="gd_tor_snake_v1/plane-v1",
    entry_point="gd_tor_snake_v1.envs:PlaneWorld",
    max_episode_steps=3000,
)

register(
    id="gd_tor_snake_v1/plane-control",
    entry_point="gd_tor_snake_v1.envs:PlaneWorld_control",
    max_episode_steps=3000,
)