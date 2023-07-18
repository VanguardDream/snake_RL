from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-mk2-2-v8',
         entry_point="snake_v8_mk2_2.envs:SnakeEnv",
          )