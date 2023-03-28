from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-v7',
         entry_point="snake_v7.envs:SnakeEnv",
          )