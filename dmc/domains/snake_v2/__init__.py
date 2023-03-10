from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-v2',
         entry_point="snake_v2.envs:SnakeEnv",
         max_episode_steps=620,
          )