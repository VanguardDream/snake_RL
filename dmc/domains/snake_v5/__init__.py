from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-v5',
         entry_point="snake_v5.envs:SnakeEnv",
         max_episode_steps=620,
          )