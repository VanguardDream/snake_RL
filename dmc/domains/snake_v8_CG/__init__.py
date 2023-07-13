from gymnasium.envs.registration import register

register(id = 'snake/SnakeEnv-cg-v8',
         entry_point="snake_v8_CG.envs:SnakeEnv",
          )