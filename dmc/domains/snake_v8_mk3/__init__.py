from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-mk3-v8',
         entry_point="snake_v8_mk3.envs:SnakeEnv",
          )