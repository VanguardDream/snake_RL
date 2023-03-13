from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-v3',
         entry_point="snake_v3.envs:SnakeEnv",
         max_episode_steps=620,
          )