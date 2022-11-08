#### 학습된 신경망 로드하기
import ray
import ray.rllib.algorithms.ppo as ppo
from scipy.spatial.transform import Rotation as Rot

config = ppo.DEFAULT_CONFIG.copy()

## Customize Hyper-Parameters
config["env_config"] =          {
                                    "print_input_command" : True,
                                }
config["num_gpus"] = 1
config["num_workers"] = 0
config["gamma"] = 0.9
config["framework"] = 'torch'
config["model"] =               {
                                    "fcnet_hiddens":[512, 256, 128], 
                                    "fcnet_activation": "tanh",
                                }
config["evaluation_num_workers"] = 1
config["evaluation_config"] =   {
                                    "render_env": False,                                
                                }
config["evaluation_duration"] = 30

algo = ppo.PPO(config, 'bongEnv-v2')
# algo.load_checkpoint("/home/bong/ray_results/PPO_bongEnv_2022-11-02_19-47-44m40rff21/checkpoint_003001/checkpoint-3001")
algo.restore("/home/bong/ray_results/PPO_bongEnv-v2_2022-11-08_19-56-344h43i1i0/checkpoint_000501/checkpoint-501")


#### Gym 빌드하기 및 시뮬레이션
import gym
import numpy as np

env = gym.make('bongEnv-v2')
obs = env.reset()

print(obs)
accum_t = [0]
accum_obs = obs

for t in range(1000):
    env.render()
    action = algo.compute_action(obs) -2
    # action = np.random.randint(-2,3)
    obs, _, done, _ = env.step(action)

    print(action)
    
#     accum_t = np.append(accum_t, (t+1))
#     accum_obs = np.vstack((accum_obs, obs))

#     # ax1.lines[0].set_data(accum_t, accum_obs[:,0])
#     # ax1.lines[1].set_data(accum_t, accum_obs[:,1])
#     # ax1.lines[2].set_data(accum_t, accum_obs[:,2])
#     # ax1.margins(0.01, 0.01)

#     # ax2.lines[0].set_data(accum_t, accum_obs[:,6])
#     # ax2.lines[1].set_data(accum_t, accum_obs[:,7])
#     # ax2.lines[2].set_data(accum_t, accum_obs[:,8])
#     # ax2.margins(0.01, 0.01)

#     # ax3.lines[0].set_data(accum_t, accum_obs[:,3])
#     # ax3.lines[1].set_data(accum_t, accum_obs[:,4])
#     # ax3.lines[2].set_data(accum_t, accum_obs[:,5])
#     # ax3.margins(0.01, 0.01)

#     # ax4.lines[0].set_data(accum_t, accum_obs[:,9])
#     # ax4.lines[1].set_data(accum_t, accum_obs[:,10])
#     # ax4.lines[2].set_data(accum_t, accum_obs[:,11])
#     # ax4.margins(0.01, 0.01)

#     # fig.canvas.draw()
#     # fig.canvas.flush_events()

# import matplotlib.pyplot as plt
# import matplotlib.animation as anim

# plt.ion()
# fig = plt.figure()
# # pos
# ax1 = fig.add_subplot(511)
# ax1.set_title("CoM Position")
# ax1.plot(accum_t, accum_obs[:,0],'r')
# ax1.plot(accum_t, accum_obs[:,1],'b')
# ax1.plot(accum_t, accum_obs[:,2],'k')

# # Head orientation
# ax2 = fig.add_subplot(513)
# ax2.set_title("Head Orientation")

# head_quat = accum_obs[:,3:7].copy()
# head_quat[:, [0, 1, 2, 3]] = head_quat[:, [1, 2, 3, 0]]

# accum_head = Rot(head_quat)
# head_eul = accum_head.as_euler('ZYX')

# ax2.plot(accum_t, head_eul[:,0],'r')
# ax2.plot(accum_t, head_eul[:,1],'b')
# ax2.plot(accum_t, head_eul[:,2],'k')

# # # orientation
# # ax3 = fig.add_subplot(515)
# # ax3.set_title("CoM Orientation")

# # com_quat = accum_obs[:,-4::].copy()

# # accum_com = Rot(com_quat)
# # com_eul = accum_com.as_euler('ZYX')

# # ax3.plot(accum_t, com_eul[:,0],'r')
# # ax3.plot(accum_t, com_eul[:,1],'b')
# # ax3.plot(accum_t, com_eul[:,2],'k')

# if done:
#     print('terminated with fail state')