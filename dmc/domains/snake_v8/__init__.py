from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-v8',
         entry_point="snake_v8.envs:SnakeEnv",
          )