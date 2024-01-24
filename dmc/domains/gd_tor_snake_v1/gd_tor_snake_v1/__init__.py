from gymnasium.envs.registration import register

register(
    id="gd_tor/plane-v1",
    entry_point="gd_tor_snake_v1.envs:PlaneWorld",
)