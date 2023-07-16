from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-cg2-v8',
         entry_point="snake_v8_CG2.envs:SnakeEnv",
          )