from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-v4',
         entry_point="snake_v4.envs:SnakeEnv",
         max_episode_steps=620,
          )