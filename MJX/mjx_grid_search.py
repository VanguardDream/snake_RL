import jax
import mediapy as media
import mujoco
import mujoco.viewer
from scipy.io import savemat

from mujoco import mjx

import time
import numpy as np
import itertools

from multiprocessing import Process, Queue

m_serp = np.eye(14)

m_side = np.array([[0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                    [0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,0,0,0,0,0,0,1,0]],dtype='int')

m_ones = np.ones((14,14))

t = np.arange(0,14,0.01)
# amp_dor = 80
# amp_lat = 80
# omega_dor = 4
# omega_lat = 4
# nu_dor = 1
# nu_lat = 1
# phi = 0

def make_ref_input(t, amp_dor, amp_lat, omega_dor, omega_lat, nu_dor, nu_lat, phi) -> np.ndarray:
    link_n = np.arange(1,15,1)
    amp_n = np.tile([amp_dor, amp_lat], 7)
    omega_n = np.tile([omega_dor, omega_lat], 7)
    nu_n = np.tile([nu_dor, nu_lat], 7)
    phi_n = np.tile([0, phi], 7)

    temporal = np.outer(t, omega_n)

    u_input = np.sin(temporal + nu_n * link_n) * amp_n + phi_n

    return u_input.copy()

def make_gait_input(u_input:np.ndarray, gait_mat:np.ndarray) -> np.ndarray:
    actual_input = np.zeros((u_input.shape[0] + 1, u_input.shape[1]))

    for i in range(actual_input.shape[0]-1):
        actual_input[i+1,:] = actual_input[i,:]
        non_zero_idx = np.squeeze(np.nonzero(gait_mat[i % gait_mat.shape[0],:]))
        actual_input[i+1,non_zero_idx] = u_input[i, non_zero_idx]

    return actual_input.copy()

def randomize_parameter() -> np.ndarray:

    a_d = np.random.randint(1,15) / 10 # Radian
    a_l = np.random.randint(1,15) / 10 # Radian
    o_d = np.random.randint(1,17) / 8 * np.pi # Radian
    o_l = np.random.randint(1,17) / 8 * np.pi # Radian
    n_d = np.random.randint(1,17) / 8 * np.pi # Radian
    n_l = np.random.randint(1,17) / 8 * np.pi # Radian
    # p = np.random.randint(1,17) / 8 * np.pi
    p = 0 # Radian

    return np.array([a_d, a_l, o_d, o_l, n_d, n_l, p])

def sim_start() -> None:
    global data, snake
    data = mujoco.MjData(snake)

    random_parameter = randomize_parameter()
    print(random_parameter)
    q = make_gait_input(make_ref_input(t, random_parameter[0], random_parameter[1], random_parameter[2], random_parameter[3], random_parameter[4], random_parameter[5], random_parameter[6]), m_serp)
    # q = make_gait_input(make_ref_input(t, amp_dor, amp_lat, omega_dor, omega_lat, nu_dor, nu_lat, phi), m_side)

    with mujoco.viewer.launch_passive(snake, data) as viewer:
        # time_start_sim = time.time()
        # for t in range(1401):
        #     time_step = time.time()
        #     slot = t // 10
        #     data.ctrl= q[slot,:]

        #     mujoco.mj_step(snake, data)

        #     viewer.sync()

        #     while snake.opt.timestep - (time.time() - time_step) > 0:
        #         time.sleep(0)
        #         pass

        time_start_sim = time.time()
        for i in q:
            time_step = time.time()
            data.ctrl= i

            mujoco.mj_step(snake, data)

            viewer.sync()

            while snake.opt.timestep - (time.time() - time_step) > 0:
                time.sleep(0)
                pass

    print(time.time() - time_start_sim)

def param2filename(params:np.ndarray)->str:
    f_name = str(params)
    f_name = f_name.replace(' ','x')
    f_name = f_name.replace('[','')
    f_name = f_name.replace(']','')
    f_name = f_name.replace('.','_')

    return f_name

def J(t, parameters:np.ndarray, g:str = 'serp', visual:bool = False, savelog:bool = False) -> np.ndarray:
    snake = mujoco.MjModel.from_xml_path("../dmc/models/snake_circle_contact.xml")
    data = mujoco.MjData(snake)
    mujoco.mj_forward(snake, data)

    f_name = param2filename(parameters)
    m = []
    if g == "serp":
        m = m_serp
    elif g == "side":
        m = m_side
    elif g == "ones":
        m = m_ones

    q = make_gait_input(make_ref_input(t, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6]), m)
    
    if savelog:
        p_head = np.empty((0,7))
        step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[48:52].copy()))
        p_head = np.vstack((p_head, step_data))

    if visual:
        with mujoco.viewer.launch_passive(snake, data) as viewer:
            time_start_sim = time.time()
            for i in q:
                time_step = time.time()
                data.ctrl= i

                mujoco.mj_step(snake, data)

                if savelog:
                    step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[48:52].copy()))
                    p_head = np.vstack((p_head, step_data))

                viewer.sync()

                while snake.opt.timestep - (time.time() - time_step) > 0:
                    time.sleep(0)
    else:
        renderer = mujoco.Renderer(snake)
        frames = []
        time_start_sim = time.time()
        for i in q:
            data.ctrl= i

            mujoco.mj_step(snake, data)

            if savelog:
                step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[48:52].copy()))
                p_head = np.vstack((p_head, step_data))

                renderer.update_scene(data)
                pixel = renderer.render()

                frames.append(pixel)

        if savelog:
            media.write_video(f_name+g+'.mp4',frames, fps=100)
    
    print(time.time() - time_start_sim)

    if savelog:
        data = {g+"trajectory_"+f_name: p_head}
        savemat(g+f_name+'.mat',data)

    return data.body('head').xpos.copy()

def orderize_J(param_min:np.ndarray, param_max:np.ndarray, g:str = 'serp', visual:bool = False, savelog:bool = False)->np.ndarray:
    #min param -> [0, 0, 0, 0, 0, 0, 0]
    #max param -> [14, 14, 16, 16, 16, 16, 0]

    a_d = np.arange(1,15)[param_min[0]:param_max[0]] # Radian
    a_l = np.arange(1,15)[param_min[1]:param_max[1]] # Radian
    o_d = np.arange(1,17)[param_min[2]:param_max[2]] # Radian
    o_l = np.arange(1,17)[param_min[3]:param_max[3]] # Radian
    n_d = np.arange(1,17)[param_min[4]:param_max[4]] # Radian
    n_l = np.arange(1,17)[param_min[5]:param_max[5]] # Radian
    # p = np.random.randint(1,17) / 8 * np.pi
    p = [0] # Radian

    combinations = list(itertools.product(a_d, a_l, o_d, o_l, n_d, n_l, p))
    param_coeff = [10, 10, 8 * np.pi, 8 * np.pi, 8 * np.pi, 8 * np.pi, 10]

    combinations = np.round(np.divide(combinations, param_coeff), 1)

    print(f'Number of Combinations : {len(combinations)}')

    ea = len(combinations) // 6

    start_idx = [0, 1 * ea, 2 * ea, 3 * ea, 4 * ea, 5 * ea] 

    print(f'For 6 processes start indices : {start_idx}')

    def iter_J(param, g:str, visual:bool, savelog:bool):
        for i in range(iter):
            print(J(t, i, g, visual, savelog))

    pc1 = Process(target=iter_J, args=(combinations[start_idx[0]:start_idx[1]], g, visual, savelog))
    pc2 = Process(target=iter_J, args=(combinations[start_idx[1]:start_idx[2]], g, visual, savelog))
    pc3 = Process(target=iter_J, args=(combinations[start_idx[2]:start_idx[3]], g, visual, savelog))
    pc4 = Process(target=iter_J, args=(combinations[start_idx[3]:start_idx[4]], g, visual, savelog))
    pc5 = Process(target=iter_J, args=(combinations[start_idx[4]:start_idx[5]], g, visual, savelog))
    pc6 = Process(target=iter_J, args=(combinations[start_idx[5]::], g, visual, savelog))

    pc1.start()
    pc2.start()
    pc3.start()
    pc4.start()
    pc5.start()
    pc6.start()
    pc1.join()
    pc2.join()
    pc3.join()
    pc4.join()
    pc5.join()
    pc6.join()


### Main script
if __name__ == "__main__":
    params = np.array([1.3, 0.6, 5.50, 0.79, 5.90, 6.30, 0])
    params = np.round(params, 1)

    orderize_J([7, 7, 0, 0, 0, 0, 0], [8, 8, 2, 2, 2, 2, 0])
    # pc1 = Process(target=J, args=())
    # J(t, params, 'side', False, True)

    pass


