from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-v6',
         entry_point="snake_v6.envs:SnakeEnv",
          )