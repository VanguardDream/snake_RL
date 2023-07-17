# Gym env
from snake_v8.envs.SnakeEnv import SnakeEnv

# import rl 알고리즘
from ray.rllib.algorithms.dqn import DQNConfig 
from ray import tune
from ray.tune.registry import register_env

register_env("snake-v8", lambda config: SnakeEnv())

algo = (
    DQNConfig()
    .rollouts(num_rollout_workers=16,)
    .resources(num_gpus=1)
    .environment(env="snake-v8")
    .framework('torch')
    .training(gamma=0.9, 
              lr=0.0001,
              train_batch_size=320000,
              n_step=10,
              hiddens = [250, 150, 100, 50],
              )
    .evaluation(evaluation_interval=10)
    .build()
)

for i in range(1000):
    result = algo.train()
    # print(pretty_print(result))

    if ((i + 1) % 25 == 0):
        checkpoint_dir = algo.save()
        print(f"Checkpoint saved in directory {checkpoint_dir}  \r")