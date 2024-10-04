from gymnasium.envs.registration import register

register(
    id="horcrux_terrain_v1/plane-v1",
    entry_point="horcrux_terrain_v1.envs:PlaneWorld",
    max_episode_steps=3000,
)
register(
    id="horcrux_terrain_v1/plane-cg",
    entry_point="horcrux_terrain_v1.envs:PlaneCGWorld",
    max_episode_steps=3000,
)

register(
    id="horcrux_terrain_v1/sand-v1",
    entry_point="horcrux_terrain_v1.envs:SandWorld",
    max_episode_steps=3000,
)

register(
    id="horcrux_terrain_v1/grass-v1",
    entry_point="horcrux_terrain_v1.envs:GrassWorld",
    max_episode_steps=3000,
)



# 각 지형 별로 각각 환경 등록하도록...
# register(
#     id="gd_tor_snake_v1/plane-control",
#     entry_point="gd_tor_snake_v1.envs:PlaneWorld_control",
#     max_episode_steps=3000,
# )