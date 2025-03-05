from gymnasium.envs.registration import register

register(
    id="horcrux_terrain_v2/plane-v1",
    entry_point="horcrux_terrain_v2.envs:PlaneWorld",
    max_episode_steps=6000,
)
register(
    id="horcrux_terrain_v2/plane-v2",
    entry_point="horcrux_terrain_v2.envs:PlaneJoyWorld",
    max_episode_steps=6000,
)