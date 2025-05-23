# from snake_v5.envs.SnakeEnv import SnakeEnv
# from snake_v8.envs.SnakeEnv import SnakeEnv
# from snake_v8_mk1.envs.SnakeEnv import SnakeEnv
from snake_v8_mk2_2.envs.SnakeEnv import SnakeEnv
# from snake_v8_CG.envs.SnakeEnv import SnakeEnv
# from snake_v8_CG2.envs.SnakeEnv import SnakeEnv
import gymnasium as gym
import numpy as np

# import rl 알고리즘
import ray
from ray import tune
from ray.rllib.algorithms import Algorithm
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.algorithms.algorithm_config import AlgorithmConfig
from ray.rllib.policy.policy import Policy
from ray.rllib.models import ModelCatalog
from ray.rllib.models.modelv2 import ModelV2
from ray.rllib.models.preprocessors import get_preprocessor
from ray.rllib.models.torch.recurrent_net import RecurrentNetwork as TorchRNN

from ray.tune.registry import register_env
from ray.tune.logger import pretty_print


# register_env("snake_v5", lambda config: SnakeEnv())
env = gym.make('snake/SnakeEnv-mk2-2-v8', render_mode="human")
# env = gym.make('snake/SnakeEnv-cg2-v8', render_mode="human")
# register_env("snake_CG_v8", lambda config: SnakeEnv())
# register_env("snake_CG_v8", lambda config: SnakeEnv())

# algo = (
#     PPOConfig()
#     .rollouts(num_rollout_workers=10,)
#     .resources(num_gpus=0.95)
#     .environment(env="snake_mk1_v8")
#     .framework('torch')
#     .evaluation()
#     .training(gamma=0.995, lr=0.0001, clip_param=0.2, kl_coeff=1.0, num_sgd_iter=20, sgd_minibatch_size=16384, train_batch_size=160000, model= {"fcnet_hiddens": [128, 128, 64, 64, 32], "free_log_std" : True }, )
#     .build()
# )

# algo.restore('C:\Users\Bong\ray_results\PPO_snake_mk1_v8_2023-07-13_19-45-351ev0yhrq\checkpoint_000500')

pol = Policy.from_checkpoint("C:\\Users\\Bong\\ray_results\\PPO_snake_mk2_2_v8_2023-07-19_21-47-593am6il07\\checkpoint_000450")

_state = pol['default_policy'].get_initial_state()
_prev_action = np.zeros(14,)
_reward = 0
_obs, _ = env.reset()
_accum_reward = 0

for epi in range(100):


    for i in range(61*10):
        _act, _state, _ = pol['default_policy'].compute_single_action(obs=_obs.copy(), state=_state.copy(), prev_action=_prev_action.copy(), explore=False)
        # _act, _state, _ = pol['default_policy'].compute_single_action(obs=_obs.copy(),explore=True)
        # _act = np.clip(_act, a_min=-3.0, a_max=3.0)
        # _act = np.clip(_act, a_min=0.0, a_max=3.0)
        _prev_action = _act.copy()
        # print(_act)
        _obs, _reward, _done, _, _dict = env.step(_act)
        _accum_reward = _accum_reward + _reward

        if _done:
            break

        # print(str(_accum_reward)+"  \r",end='')
        # print(f"{_dict['head_rotation']}")
        # print(_dict['forward_reward'])

    _state = pol['default_policy'].get_initial_state()
    _prev_action = np.zeros(14,)
    _obs, _ = env.reset()
    print(_accum_reward)
    _accum_reward = 0
    print("episode done...")
env.close()