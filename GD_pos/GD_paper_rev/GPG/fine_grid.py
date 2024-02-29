import serpenoid

import mujoco
import mujoco.viewer
import mediapy as media
from scipy.io import savemat
from scipy.optimize import minimize

import time
import numpy as np
import itertools
import serpenoid

from scipy.spatial.transform import Rotation
from multiprocessing import Process, Queue, shared_memory

def param2filename(params:np.ndarray)->str:
    f_name = str(params)
    f_name = f_name.replace('(','')
    f_name = f_name.replace(')','')
    f_name = f_name.replace(',','')
    f_name = f_name.replace(' ','x')
    f_name = f_name.replace('[','')
    f_name = f_name.replace(']','')
    f_name = f_name.replace('.','_')

    return f_name

def J(parameters:np.ndarray, parameters_bar:np.ndarray, visual:bool = False, savelog:bool = False) -> np.ndarray:
    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)
    mujoco.mj_forward(snake, data)

    M_name = param2filename(parameters)
    Bar_name = param2filename(parameters_bar)

    f_name = "M_" + M_name + "_Bar_" + Bar_name

    gait = serpenoid.Gait(tuple(parameters), tuple(parameters_bar))

    q = gait.Gk
    
    expand_q = np.repeat(q, 10, axis=1)

    p_head = np.empty((0,21))
    step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[28:32].copy(), np.zeros(14)))
    p_head = np.vstack((p_head, step_data))

    if visual:
        with mujoco.viewer.launch_passive(snake, data) as viewer:
            for i in expand_q.transpose():
                time_step = time.time()
                index = np.nonzero(i)
                for idx in index:
                    data.ctrl[idx] = i[idx]
                
                mujoco.mj_step(snake, data)
                viewer.sync()

                while snake.opt.timestep - (time.time() - time_step) > 0:
                    time.sleep(0)

                step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[28:32].copy(), data.ctrl))
                p_head = np.vstack((p_head, step_data))
    
    else: # no visual
        renderer = mujoco.Renderer(snake, 720, 1280)
        frames = []
        time_start_sim = time.time()
        for i in expand_q.transpose():
            index = np.nonzero(i)
            for idx in index:
                data.ctrl[idx] = i[idx]

            mujoco.mj_step(snake, data)

            step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[28:32].copy(), data.ctrl))
            p_head = np.vstack((p_head, step_data))

            if savelog:
                renderer.update_scene(data)
                pixel = renderer.render()

                frames.append(pixel)

        if savelog:
            media.write_video(f_name+'.mp4',frames, fps=200)
    
    if savelog and not(visual):
        sim_data = {"trajectory_"+f_name: p_head}
        savemat("trajectory_"+f_name+'.mat',sim_data)

    i = 1500
    j = -800
    l = -900
    m = 0.0001

    i_term = 0
    j_term = 0
    l_term = 0
    m_term = 0

    if abs(parameters_bar[6]) < 30:  #forward way...
        i_term = i * p_head[-1,0]
        j_term = j * np.abs(p_head[-1,1])
        l_term = l * np.abs(p_head[-1,1]) / (np.abs(p_head[-1,0]) + 0.01)
        m_term = m * np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    else:
        i_term = i * p_head[-1,1]
        j_term = j * np.abs(p_head[-1,0])
        l_term = l * np.abs(p_head[-1,0]) / (np.abs(p_head[-1,1]) + 0.01)
        m_term = m * np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    return i_term + j_term + l_term + m_term

def J_curve(parameters:np.ndarray, parameters_bar:np.ndarray, visual:bool = False, savelog:bool = False) -> np.ndarray:
    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)
    mujoco.mj_forward(snake, data)

    M_name = param2filename(parameters)
    Bar_name = param2filename(parameters_bar)

    f_name = "M_" + M_name + "_Bar_" + Bar_name

    gait = serpenoid.Gait(tuple(parameters), tuple(parameters_bar))

    q = gait.CurveFunction
    
    expand_q = np.repeat(q, 10, axis=1)

    p_head = np.empty((0,21))
    step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[28:32].copy(), np.zeros(14)))
    p_head = np.vstack((p_head, step_data))

    if visual:
        with mujoco.viewer.launch_passive(snake, data) as viewer:
            for i in expand_q.transpose():
                time_step = time.time()
                index = np.nonzero(i)
                for idx in index:
                    data.ctrl[idx] = i[idx]
                
                mujoco.mj_step(snake, data)
                viewer.sync()

                while snake.opt.timestep - (time.time() - time_step) > 0:
                    time.sleep(0)

                step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[28:32].copy(), data.ctrl))
                p_head = np.vstack((p_head, step_data))
    
    else: # no visual
        renderer = mujoco.Renderer(snake, 720, 1280)
        frames = []
        time_start_sim = time.time()
        for i in expand_q.transpose():
            index = np.nonzero(i)
            for idx in index:
                data.ctrl[idx] = i[idx]

            mujoco.mj_step(snake, data)

            step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[28:32].copy(), data.ctrl))
            p_head = np.vstack((p_head, step_data))

            if savelog:
                renderer.update_scene(data)
                pixel = renderer.render()

                frames.append(pixel)

        if savelog:
            media.write_video(f_name+'.mp4',frames, fps=200)
    
    if savelog and not(visual):
        sim_data = {"trajectory_"+f_name: p_head}
        savemat("trajectory_"+f_name+'.mat',sim_data)

    i = 1500
    j = -800
    l = -900
    m = 0.0001

    i_term = 0
    j_term = 0
    l_term = 0
    m_term = 0

    if abs(parameters_bar[6]) < 30:  #forward way...
        i_term = i * p_head[-1,0]
        j_term = j * np.abs(p_head[-1,1])
        l_term = l * np.abs(p_head[-1,1]) / (np.abs(p_head[-1,0]) + 0.01)
        m_term = m * np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    else:
        i_term = i * p_head[-1,1]
        j_term = j * np.abs(p_head[-1,0])
        l_term = l * np.abs(p_head[-1,0]) / (np.abs(p_head[-1,1]) + 0.01)
        m_term = m * np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    return i_term + j_term + l_term + m_term

def orderize_linear_fine(param_motion:np.ndarray, curve:bool, param_bar_iter:np.ndarray, shd_name:str, shd_shape, visual:bool, savelog:bool) -> None:

    for i in param_bar_iter:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        U_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        idx1 = i[2] + 90 # psi fine start -90
        idx2 = i[3] + 90 # nu fine start -90

        op_amp_d = param_motion[0]
        op_amp_l = param_motion[1]
        op_psi_d = param_motion[2]
        op_psi_l = param_motion[3]
        op_nu_d = param_motion[4]
        op_nu_l = param_motion[5]

        amp_d, amp_l, psi, nu, delta = i
        lambda_bar = (amp_d, amp_l, op_psi_d + (1/18) * psi, op_psi_l + (1/18) * psi, op_nu_d + (2/135) * nu, op_nu_l + (1/135) * nu, delta, param_motion[-1])

        if curve:
            U_map[idx1, idx2, :] = J_curve(param_motion, lambda_bar, visual, savelog)
        else:
            U_map[idx1, idx2, :] = J(param_motion, lambda_bar, visual, savelog)

def iterator_linear_fine(motion:np.ndarray, curve:bool, visual:bool = False, savelog:bool = False) -> None:
    # slithering = (45, 45, 30, 30, 60, 30, 0, 0.05)

    motion_param = motion

    amp_d = np.array([motion_param[0]])
    amp_l = np.array([motion_param[1]])

    psi = np.arange(-90,91)

    nu = np.arange(-90,91)

    delta = np.array([motion_param[-2]])
    # delta = np.array([motion_param[-2]])

    n1 = len(psi)
    n2 = len(nu)

    U_map = np.empty((n1,n2,1), dtype=np.float64)
    shm = shared_memory.SharedMemory(name="shared_U_map", create=True, size=U_map.nbytes)
    data = np.ndarray(U_map.shape, dtype=U_map.dtype, buffer=shm.buf)

    combinations = list(itertools.product(amp_d, amp_l, psi, nu, delta))
    print(f'Number of Combinations : {len(combinations)}')

    ea = len(combinations) // 16
    start_idx = [0, 1 * ea, 2 * ea, 3 * ea, 4 * ea, 5 * ea, 6 * ea, 7 * ea, 8 * ea , 9 * ea, 10 * ea, 11 * ea, 12 * ea, 13 * ea, 14 * ea, 15 * ea] 

    print(f'For 16 processes start indices : {start_idx}')

    pc1 = Process(target= orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[0]:start_idx[1]]),   shm.name, U_map.shape, visual, savelog))
    pc2 = Process(target= orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[1]:start_idx[2]]),   shm.name, U_map.shape, visual, savelog))
    pc3 = Process(target= orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[2]:start_idx[3]]),   shm.name, U_map.shape, visual, savelog))
    pc4 = Process(target= orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[3]:start_idx[4]]),   shm.name, U_map.shape, visual, savelog))
    pc5 = Process(target= orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[4]:start_idx[5]]),   shm.name, U_map.shape, visual, savelog))
    pc6 = Process(target= orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[5]:start_idx[6]]),   shm.name, U_map.shape, visual, savelog))
    pc7 = Process(target= orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[6]:start_idx[7]]),   shm.name, U_map.shape, visual, savelog))
    pc8 = Process(target= orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[7]:start_idx[8]]),   shm.name, U_map.shape, visual, savelog))
    pc9 = Process(target= orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[8]:start_idx[9]]),   shm.name, U_map.shape, visual, savelog))
    pc10 = Process(target=orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[9]:start_idx[10]]),  shm.name, U_map.shape, visual, savelog))
    pc11 = Process(target=orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[10]:start_idx[11]]), shm.name, U_map.shape, visual, savelog))
    pc12 = Process(target=orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[11]:start_idx[12]]), shm.name, U_map.shape, visual, savelog))
    pc13 = Process(target=orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[12]:start_idx[13]]), shm.name, U_map.shape, visual, savelog))
    pc14 = Process(target=orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[13]:start_idx[14]]), shm.name, U_map.shape, visual, savelog))
    pc15 = Process(target=orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[14]:start_idx[15]]), shm.name, U_map.shape, visual, savelog))
    pc16 = Process(target=orderize_linear_fine, args=(np.array(motion_param), curve, list(combinations[start_idx[15]::]),             shm.name, U_map.shape, visual, savelog))

    pc1.start()
    pc2.start()
    pc3.start()
    pc4.start()
    pc5.start()
    pc6.start()
    pc7.start()
    pc8.start()
    pc9.start()
    pc10.start()
    pc11.start()
    pc12.start()
    pc13.start()
    pc14.start()
    pc15.start()
    pc16.start()

    pc1.join()
    pc2.join()
    pc3.join()
    pc4.join()
    pc5.join()
    pc6.join()
    pc7.join()
    pc8.join()
    pc9.join()
    pc10.join()
    pc11.join()
    pc12.join()
    pc13.join()
    pc14.join()
    pc15.join()
    pc16.join()

    data_dict = {'U_map': data, 'Motion_lambda': motion_param}
    savemat("./U_map_fine_"+str(curve)+"_"+param2filename(motion_param)+f"_{len(combinations)}"+"_.mat", data_dict)
    
    shm.close()
    shm.unlink()

    print('done')

if __name__ == "__main__":
    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)

    serpentine = (45, 45, 30, 30, 30, 30, 0, 0.05)
    serpentine_op = (45, 45, 19, 19, 59, 59, 0, 0.05)
    slithering = (45, 45, 30, 30, 60, 30, 0, 0.05)
    slithering_op = (45, 45, 15, 15, 56.5, 28.25, 0, 0.05)
    sidewinding = (45, 45, 30, 30, 30, 30, 45, 0.05)
    sidewinding_op = (45, 45, 27, 27, 53, 53, 45, 0.05)
    rolling = (15, 15, 0, 0, 30, 30, 90, 0.05)

    # #### Linear Searching...
    start_iter = time.time()
    # iterator_linear_fine(serpentine_op,True)
    # iterator_linear_fine(serpentine_op,False)
    iterator_linear_fine(slithering_op,True)
    iterator_linear_fine(slithering_op,False)
    # iterator_linear_fine(sidewinding_op,True)
    # iterator_linear_fine(sidewinding_op,False)

    end_iter = time.time()
    print(f"Iterating dond... {end_iter-start_iter} seconds elapsed")

