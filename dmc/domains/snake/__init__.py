from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-v1',
         entry_point="snake.envs:SnakeEnv",
          )