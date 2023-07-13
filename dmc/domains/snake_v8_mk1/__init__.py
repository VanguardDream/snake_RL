from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-mk1-v8',
         entry_point="snake_v8_mk1.envs:SnakeEnv",
          )