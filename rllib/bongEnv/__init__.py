from gym.envs.registration import register
"""
위에 다른 레지스터가 있을 것
"""
register(
    id="bongEnv",
    entry_point="gym.envs.bongEnv:bongEnv",
    max_episode_steps=500,
)
