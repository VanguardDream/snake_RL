#### 학습된 신경망 로드하기
import ray
import ray.rllib.algorithms.ppo as ppo

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

algo = ppo.PPO(config, 'bongEnv')
# algo.load_checkpoint("/home/bong/ray_results/PPO_bongEnv_2022-10-24_18-14-07u23s5wtk/checkpoint_002001/checkpoint-2001")
algo.restore("/home/bong/ray_results/PPO_bongEnv_2022-10-24_18-14-07u23s5wtk/checkpoint_002001/checkpoint-2001")


#### Gym 빌드하기 및 시뮬레이션
import gym
import numpy as np

env = gym.make('bongEnv')
obs = env.reset()

accum_t = [0]
accum_obs = obs

for t in range(1000):
    env.render()
    # action = algo.compute_action(obs)
    action = np.random.randint(0 * np.ones(14), 3 * np.ones(14))
    obs, _, done, _ = env.step(action)
    
    accum_t = np.append(accum_t, (t+1))
    accum_obs = np.vstack((accum_obs, obs))

    # ax1.lines[0].set_data(accum_t, accum_obs[:,0])
    # ax1.lines[1].set_data(accum_t, accum_obs[:,1])
    # ax1.lines[2].set_data(accum_t, accum_obs[:,2])
    # ax1.margins(0.01, 0.01)

    # ax2.lines[0].set_data(accum_t, accum_obs[:,6])
    # ax2.lines[1].set_data(accum_t, accum_obs[:,7])
    # ax2.lines[2].set_data(accum_t, accum_obs[:,8])
    # ax2.margins(0.01, 0.01)

    # ax3.lines[0].set_data(accum_t, accum_obs[:,3])
    # ax3.lines[1].set_data(accum_t, accum_obs[:,4])
    # ax3.lines[2].set_data(accum_t, accum_obs[:,5])
    # ax3.margins(0.01, 0.01)

    # ax4.lines[0].set_data(accum_t, accum_obs[:,9])
    # ax4.lines[1].set_data(accum_t, accum_obs[:,10])
    # ax4.lines[2].set_data(accum_t, accum_obs[:,11])
    # ax4.margins(0.01, 0.01)

    # fig.canvas.draw()
    # fig.canvas.flush_events()

import matplotlib.pyplot as plt
import matplotlib.animation as anim

plt.ion()
fig = plt.figure()
# pos
ax1 = fig.add_subplot(411)
ax1.set_title("CoM Position")
ax1.plot(accum_t, accum_obs[:,0],'r')
ax1.plot(accum_t, accum_obs[:,1],'b')
ax1.plot(accum_t, accum_obs[:,2],'k')
# vel
ax2 = fig.add_subplot(412)
ax2.set_title("CoM Velocity")
ax2.plot(accum_t, accum_obs[:,6],'r')
ax2.plot(accum_t, accum_obs[:,7],'b')
ax2.plot(accum_t, accum_obs[:,8],'k')

# orientation
ax3 = fig.add_subplot(413)
ax3.set_title("CoM Orientation")
ax3.plot(accum_t, accum_obs[:,3],'r')
ax3.plot(accum_t, accum_obs[:,4],'b')
ax3.plot(accum_t, accum_obs[:,5],'k')

# angular vel
ax4 = fig.add_subplot(414)
ax4.set_title("CoM Angular Vel.")
ax4.plot(accum_t, accum_obs[:,9],'r')
ax4.plot(accum_t, accum_obs[:,10],'b')
ax4.plot(accum_t, accum_obs[:,11],'k')

if done:
    print('terminated with fail state')