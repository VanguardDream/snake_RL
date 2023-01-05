from time import sleep
from xmlrpc.client import Boolean
import ray
import ray.rllib.algorithms.ppo as ppo
from scipy.spatial.transform import Rotation as Rot

import threading

import gym
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as anim


config = ppo.DEFAULT_CONFIG.copy()

## Customize Hyper-Parameters
config["env_config"] =          {
                                    # "print_input_command" : True,
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

algo = ppo.PPO(config, 'bongEnv-v3')
# algo.load_checkpoint("/home/bong/ray_results/PPO_bongEnv_2022-11-02_19-47-44m40rff21/checkpoint_003001/checkpoint-3001")
algo.restore("/home/bong/ray_results/PPO_bongEnv-v3_2022-11-09_18-25-10h_idntni/checkpoint_005501/checkpoint-5501")

def simulation(done, sim_data, lock_done, lock_data):
    #### Gym 빌드하기 및 시뮬레이션
    env = gym.make('bongEnv-v3')
    obs = env.reset()

    accum_obs = np.append(0, obs)

    for t in range(10):
        env.render()
        action = algo.compute_single_action(obs) -2
        # action = np.random.randint(-2,3)

        with lock_done:
            obs, _, done, _ = env.step(action)
        
        # accum_t = np.append(accum_t, (t+1))
        # accum_obs = np.vstack((accum_obs, obs))
        with lock_data:
            data = np.append(t+1, obs)
            accum_obs = np.vstack((accum_obs, data))

        
    sim_data = accum_obs.copy()

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

def rt_plotting(sim_data: np.ndarray):

    plt.ion()
    fig = plt.figure()
    # pos
    ax1 = fig.add_subplot(511)
    ax1.set_title("CoM Position")
    ax1.plot(accum_t, accum_obs[:,0],'r')
    ax1.plot(accum_t, accum_obs[:,1],'b')
    ax1.plot(accum_t, accum_obs[:,2],'k')

    # Head orientation
    ax2 = fig.add_subplot(513)
    ax2.set_title("Head Orientation")

    head_quat = accum_obs[:,3:7].copy()
    head_quat[:, [0, 1, 2, 3]] = head_quat[:, [1, 2, 3, 0]]

    accum_head = Rot(head_quat)
    head_eul = accum_head.as_euler('ZYX')

    ax2.plot(accum_t, head_eul[:,0],'r')
    ax2.plot(accum_t, head_eul[:,1],'b')
    ax2.plot(accum_t, head_eul[:,2],'k')

    # # orientation
    # ax3 = fig.add_subplot(515)
    # ax3.set_title("CoM Orientation")

    # com_quat = accum_obs[:,-4::].copy()

    # accum_com = Rot(com_quat)
    # com_eul = accum_com.as_euler('ZYX')

    # ax3.plot(accum_t, com_eul[:,0],'r')
    # ax3.plot(accum_t, com_eul[:,1],'b')
    # ax3.plot(accum_t, com_eul[:,2],'k')

def main():
    global done, sim_data

    done = False
    lock_done = threading.Lock()

    sim_data = np.array([])
    lock_data = threading.Lock()

    th_simulation = threading.Thread(target=simulation, args=(done, sim_data, lock_done, lock_data,))
    th_simulation.start()

    sleep(20)

    print(done)
    print(sim_data)

if __name__ == "__main__":
    main()