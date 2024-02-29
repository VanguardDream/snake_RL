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

def randomize_parameter_rad() -> np.ndarray:

    amp_d = np.random.randint(1,15) / 10 # Radian
    amp_l = np.random.randint(1,15) / 10 # Radian
    psi_d = np.random.randint(0,17) / 16 * np.pi # Radian
    psi_l = np.random.randint(0,17) / 16 * np.pi # Radian
    nu_d = np.random.randint(1,61) / 10  # Radian
    nu_l = np.random.randint(1,61) / 10  # Radian
    delta = np.random.randint(0,17) / 16 * np.pi

    return np.array([amp_d, amp_l, psi_d, psi_l, nu_d, nu_l, delta])

def randomize_parameter_deg() -> np.ndarray:

    amp_d = np.random.randint(1,17) * 5 # Degree
    amp_l = np.random.randint(1,17) * 5 # Degree
    psi_d = np.random.randint(0,19) * 10 # Degree
    psi_l = np.random.randint(0,19) * 10 # Degree
    nu_d = np.random.randint(1,61) / 10  # Degree
    nu_l = np.random.randint(1,61) / 10  # Degree
    delta = np.random.randint(0,19) * 10 # Degree

    return np.array([amp_d, amp_l, psi_d, psi_l, nu_d, nu_l, delta])

def sim_start() -> None:
    global data, snake
    data = mujoco.MjData(snake)

    l_bar = randomize_parameter_deg()

    # gait = serpenoid.Gait((45, 45, 30, 30, 60, 30, 0, 0.05), (l_bar[0], l_bar[1], l_bar[2], l_bar[3], l_bar[4], l_bar[5], l_bar[6], 0.05))
    gait = serpenoid.Gait((45, 45, 45, 45, 120, 120, 0, 0.05), (45, 45, 45, 45, 120, 120, 0, 0.05))

    q = gait.Gk
    print(q.shape)

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
        step = 0
        for k in range(8000):
            time_step = time.time()
            if k % 10 == 0 and k != 0:
                step += 1

            # Motion Matrix
            index = np.nonzero(gait.Gk[:,step])

            for idx in index:
                data.ctrl[idx] = gait.Gk[idx,step]

            # # Serpenoid
            # data.ctrl = gait.CurveFunction[:,step]

            mujoco.mj_step(snake, data)

            viewer.sync()

        # for i in q.transpose():
        #     time_step = time.time()
        #     index = np.nonzero(i)

        #     for idx in index:
        #         data.ctrl[idx] = i[idx]

        #     mujoco.mj_step(snake, data)

        #     viewer.sync()

            while snake.opt.timestep - (time.time() - time_step) > 0:
                time.sleep(0)

    print(time.time() - time_start_sim)

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

def orderize(param_motion:np.ndarray, basis:np.ndarray, param_bar_iter:np.ndarray, param_coef:np.ndarray, shd_name:str, shd_shape, visual:bool, savelog:bool) -> None:
    param_coeff = param_coef

    for i in param_bar_iter:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        U_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        # idx = i - (basis + np.array([0, 0, 1, 1, 0, 0, 1]))
        idx = np.array(i) - (np.array(basis) + np.array([1,1,0,0,1,1,0]))
        i = np.multiply(i, param_coeff)
        lambda_bar = np.hstack((i, param_motion[-1]))

        U_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :] = J(param_motion, lambda_bar, visual, savelog)

def orderize_curve(param_motion:np.ndarray, basis:np.ndarray, param_bar_iter:np.ndarray, param_coef:np.ndarray, shd_name:str, shd_shape, visual:bool, savelog:bool) -> None:
    param_coeff = param_coef

    for i in param_bar_iter:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        U_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        # idx = i - (basis + np.array([0, 0, 1, 1, 0, 0, 1]))
        idx = np.array(i) - (np.array(basis) + np.array([1,1,0,0,1,1,0]))
        i = np.multiply(i, param_coeff)
        lambda_bar = np.hstack((i, param_motion[-1]))

        U_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :] = J_curve(param_motion, lambda_bar, visual, savelog)

def orderize_linear(param_motion:np.ndarray, curve:bool, param_bar_iter:np.ndarray, shd_name:str, shd_shape, visual:bool, savelog:bool) -> None:

    for i in param_bar_iter:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        U_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        idx1 = i[2] # psi start 0
        idx2 = i[3] - 1 # nu start 1

        amp_d, amp_l, psi, nu, delta = i
        lambda_bar = (amp_d, amp_l, psi, psi, (nu) * (1/2), (nu) * (1/2), delta, param_motion[-1])

        if curve:
            U_map[idx1, idx2, :] = J_curve(param_motion, lambda_bar, visual, savelog)
        else:
            U_map[idx1, idx2, :] = J(param_motion, lambda_bar, visual, savelog)

def orderize_linear_fine(param_motion:np.ndarray, curve:bool, param_bar_iter:np.ndarray, shd_name:str, shd_shape, visual:bool, savelog:bool) -> None:

    for i in param_bar_iter:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        U_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        idx1 = i[2] # psi fine start -90
        idx2 = i[3] - 1 # nu fine start -90

        amp_d, amp_l, psi, nu, delta = i
        lambda_bar = (amp_d, amp_l, psi, psi, (nu) * (1/2), (nu) * (1/2), delta, param_motion[-1])

        if curve:
            U_map[idx1, idx2, :] = J_curve(param_motion, lambda_bar, visual, savelog)
        else:
            U_map[idx1, idx2, :] = J(param_motion, lambda_bar, visual, savelog)
            

def J_minize(param:tuple[float, float, float, float, float]):
    amp_d = param[0]
    amp_l = param[1]
    psi = param[2]
    nu = param[3]
    delta = param[4]

    parameters = (amp_d, amp_l, psi, psi, 2 * nu, nu, delta, 0.05)
    parameters_bar = parameters

    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)
    mujoco.mj_forward(snake, data)

    gait = serpenoid.Gait(tuple(parameters), tuple(parameters_bar))

    # q = gait.CurveFunction
    q = gait.Gk
    
    expand_q = np.repeat(q, 10, axis=1)

    p_head = np.empty((0,21))
    step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[28:32].copy(), np.zeros(14)))
    p_head = np.vstack((p_head, step_data))

    for i in expand_q.transpose():
        index = np.nonzero(i)
        for idx in index:
            data.ctrl[idx] = i[idx]

        mujoco.mj_step(snake, data)

        step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[28:32].copy(), data.ctrl))
        p_head = np.vstack((p_head, step_data))


    i = 1500
    j = -800
    l = -900
    m = 0.0001

    i_term = 0
    j_term = 0
    l_term = 0
    m_term = 0

    if abs(parameters[6]) < 30:  #forward way...
        i_term = i * p_head[-1,0]
        j_term = j * np.abs(p_head[-1,1])
        l_term = l * np.abs(p_head[-1,1]/p_head[-1,0])
        m_term = m * np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    else:
        i_term = i * p_head[-1,1]
        j_term = j * np.abs(p_head[-1,0])
        l_term = l * np.abs(p_head[-1,0]/p_head[-1,1])
        m_term = m * np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    return -1 * (i_term + j_term + l_term + m_term)

def iterator(param_m:np.ndarray, param_min:np.ndarray, param_max:np.ndarray, param_coeff:np.ndarray, visual:bool = False, savelog:bool = False) -> None:
    motion_param = param_m
    basis = param_min

    p_coeff = param_coeff

    amp_d = np.arange(1,17)[param_min[0]:param_max[0]]
    amp_l = np.arange(1,17)[param_min[1]:param_max[1]]
    psi_d = np.arange(0,181)[param_min[2]:param_max[2]]
    psi_l = np.arange(0,181)[param_min[3]:param_max[3]]
    # psi_d = np.arange(0,19)[param_min[2]:param_max[2]]
    # psi_l = np.arange(0,19)[param_min[3]:param_max[3]]
    nu_d = np.arange(1,121)[param_min[4]:param_max[4]]
    nu_l = np.arange(1,121)[param_min[5]:param_max[5]]
    # nu_d = np.arange(1,7)[param_min[4]:param_max[4]]
    # nu_l = np.arange(1,7)[param_min[5]:param_max[5]]
    delta = np.arange(0,19)[param_min[6]:param_max[6]]

    print(f'base param : {np.array([amp_d[0], amp_l[0], psi_d[0], psi_l[0], nu_d[0], nu_l[0], delta[0]]) *param_coeff}')

    n1 = len(amp_d)
    n2 = len(amp_l)
    n3 = len(psi_d)
    n4 = len(psi_l)
    n5 = len(nu_d)
    n6 = len(nu_l)
    n7 = len(delta)

    U_map = np.empty((n1,n2,n3,n4,n5,n6,n7,1), dtype=np.float64)
    shm = shared_memory.SharedMemory(name="shared_U_map", create=True, size=U_map.nbytes)
    data = np.ndarray(U_map.shape, dtype=U_map.dtype, buffer=shm.buf)

    combinations = list(itertools.product(amp_d, amp_l, psi_d, psi_l, nu_d, nu_l, delta))
    print(f'Number of Combinations : {len(combinations)}')

    ea = len(combinations) // 16
    start_idx = [0, 1 * ea, 2 * ea, 3 * ea, 4 * ea, 5 * ea, 6 * ea, 7 * ea, 8 * ea , 9 * ea, 10 * ea, 11 * ea, 12 * ea, 13 * ea, 14 * ea, 15 * ea] 

    print(f'For 16 processes start indices : {start_idx}')

    pc1 = Process(target=orderize,  args=(np.array(motion_param), basis, list(combinations[start_idx[0]:start_idx[1]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc2 = Process(target=orderize,  args=(np.array(motion_param), basis, list(combinations[start_idx[1]:start_idx[2]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc3 = Process(target=orderize,  args=(np.array(motion_param), basis, list(combinations[start_idx[2]:start_idx[3]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc4 = Process(target=orderize,  args=(np.array(motion_param), basis, list(combinations[start_idx[3]:start_idx[4]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc5 = Process(target=orderize,  args=(np.array(motion_param), basis, list(combinations[start_idx[4]:start_idx[5]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc6 = Process(target=orderize,  args=(np.array(motion_param), basis, list(combinations[start_idx[5]:start_idx[6]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc7 = Process(target=orderize,  args=(np.array(motion_param), basis, list(combinations[start_idx[6]:start_idx[7]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc8 = Process(target=orderize,  args=(np.array(motion_param), basis, list(combinations[start_idx[7]:start_idx[8]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc9 = Process(target=orderize,  args=(np.array(motion_param), basis, list(combinations[start_idx[8]:start_idx[9]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc10 = Process(target=orderize, args=(np.array(motion_param), basis, list(combinations[start_idx[9]:start_idx[10]]),  p_coeff, shm.name, U_map.shape, visual, savelog))
    pc11 = Process(target=orderize, args=(np.array(motion_param), basis, list(combinations[start_idx[10]:start_idx[11]]), p_coeff, shm.name, U_map.shape, visual, savelog))
    pc12 = Process(target=orderize, args=(np.array(motion_param), basis, list(combinations[start_idx[11]:start_idx[12]]), p_coeff, shm.name, U_map.shape, visual, savelog))
    pc13 = Process(target=orderize, args=(np.array(motion_param), basis, list(combinations[start_idx[12]:start_idx[13]]), p_coeff, shm.name, U_map.shape, visual, savelog))
    pc14 = Process(target=orderize, args=(np.array(motion_param), basis, list(combinations[start_idx[13]:start_idx[14]]), p_coeff, shm.name, U_map.shape, visual, savelog))
    pc15 = Process(target=orderize, args=(np.array(motion_param), basis, list(combinations[start_idx[14]:start_idx[15]]), p_coeff, shm.name, U_map.shape, visual, savelog))
    pc16 = Process(target=orderize, args=(np.array(motion_param), basis, list(combinations[start_idx[15]::]),             p_coeff, shm.name, U_map.shape, visual, savelog))

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

    data_dict = {'U_map': data, 'min': param_min, 'Motion_lambda': param_m, 'max': param_max, 'param_coefficient': param_coeff}
    savemat("./data/U_map_M_"+param2filename(param_m)+'_min_'+param2filename(param_min)+f"_{len(combinations)}"+"_.mat", data_dict)

    shm.close()
    shm.unlink()

    print('done')

def iterator_curve(param_m:np.ndarray, param_min:np.ndarray, param_max:np.ndarray, param_coeff:np.ndarray, visual:bool = False, savelog:bool = False) -> None:
    motion_param = param_m
    basis = param_min

    p_coeff = param_coeff

    amp_d = np.arange(1,17)[param_min[0]:param_max[0]]
    amp_l = np.arange(1,17)[param_min[1]:param_max[1]]
    psi_d = np.arange(0,181)[param_min[2]:param_max[2]]
    psi_l = np.arange(0,181)[param_min[3]:param_max[3]]
    # psi_d = np.arange(0,19)[param_min[2]:param_max[2]]
    # psi_l = np.arange(0,19)[param_min[3]:param_max[3]]
    nu_d = np.arange(1,121)[param_min[4]:param_max[4]]
    nu_l = np.arange(1,121)[param_min[5]:param_max[5]]
    # nu_d = np.arange(1,7)[param_min[4]:param_max[4]]
    # nu_l = np.arange(1,7)[param_min[5]:param_max[5]]
    delta = np.arange(0,19)[param_min[6]:param_max[6]]

    print(f'base param : {np.array([amp_d[0], amp_l[0], psi_d[0], psi_l[0], nu_d[0], nu_l[0], delta[0]]) *param_coeff}')

    n1 = len(amp_d)
    n2 = len(amp_l)
    n3 = len(psi_d)
    n4 = len(psi_l)
    n5 = len(nu_d)
    n6 = len(nu_l)
    n7 = len(delta)

    U_map = np.empty((n1,n2,n3,n4,n5,n6,n7,1), dtype=np.float64)
    shm = shared_memory.SharedMemory(name="shared_U_map", create=True, size=U_map.nbytes)
    data = np.ndarray(U_map.shape, dtype=U_map.dtype, buffer=shm.buf)

    combinations = list(itertools.product(amp_d, amp_l, psi_d, psi_l, nu_d, nu_l, delta))
    print(f'Number of Combinations : {len(combinations)}')

    ea = len(combinations) // 16
    start_idx = [0, 1 * ea, 2 * ea, 3 * ea, 4 * ea, 5 * ea, 6 * ea, 7 * ea, 8 * ea , 9 * ea, 10 * ea, 11 * ea, 12 * ea, 13 * ea, 14 * ea, 15 * ea] 

    print(f'For 16 processes start indices : {start_idx}')

    pc1 = Process(target=orderize_curve,  args=(np.array(motion_param), basis, list(combinations[start_idx[0]:start_idx[1]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc2 = Process(target=orderize_curve,  args=(np.array(motion_param), basis, list(combinations[start_idx[1]:start_idx[2]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc3 = Process(target=orderize_curve,  args=(np.array(motion_param), basis, list(combinations[start_idx[2]:start_idx[3]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc4 = Process(target=orderize_curve,  args=(np.array(motion_param), basis, list(combinations[start_idx[3]:start_idx[4]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc5 = Process(target=orderize_curve,  args=(np.array(motion_param), basis, list(combinations[start_idx[4]:start_idx[5]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc6 = Process(target=orderize_curve,  args=(np.array(motion_param), basis, list(combinations[start_idx[5]:start_idx[6]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc7 = Process(target=orderize_curve,  args=(np.array(motion_param), basis, list(combinations[start_idx[6]:start_idx[7]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc8 = Process(target=orderize_curve,  args=(np.array(motion_param), basis, list(combinations[start_idx[7]:start_idx[8]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc9 = Process(target=orderize_curve,  args=(np.array(motion_param), basis, list(combinations[start_idx[8]:start_idx[9]]),   p_coeff, shm.name, U_map.shape, visual, savelog))
    pc10 = Process(target=orderize_curve, args=(np.array(motion_param), basis, list(combinations[start_idx[9]:start_idx[10]]),  p_coeff, shm.name, U_map.shape, visual, savelog))
    pc11 = Process(target=orderize_curve, args=(np.array(motion_param), basis, list(combinations[start_idx[10]:start_idx[11]]), p_coeff, shm.name, U_map.shape, visual, savelog))
    pc12 = Process(target=orderize_curve, args=(np.array(motion_param), basis, list(combinations[start_idx[11]:start_idx[12]]), p_coeff, shm.name, U_map.shape, visual, savelog))
    pc13 = Process(target=orderize_curve, args=(np.array(motion_param), basis, list(combinations[start_idx[12]:start_idx[13]]), p_coeff, shm.name, U_map.shape, visual, savelog))
    pc14 = Process(target=orderize_curve, args=(np.array(motion_param), basis, list(combinations[start_idx[13]:start_idx[14]]), p_coeff, shm.name, U_map.shape, visual, savelog))
    pc15 = Process(target=orderize_curve, args=(np.array(motion_param), basis, list(combinations[start_idx[14]:start_idx[15]]), p_coeff, shm.name, U_map.shape, visual, savelog))
    pc16 = Process(target=orderize_curve, args=(np.array(motion_param), basis, list(combinations[start_idx[15]::]),             p_coeff, shm.name, U_map.shape, visual, savelog))

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

    data_dict = {'U_map': data, 'min': param_min, 'Motion_lambda': param_m, 'max': param_max, 'param_coefficient': param_coeff}
    savemat("./data/U_map_Curve_M_"+param2filename(param_m)+'_min_'+param2filename(param_min)+f"_{len(combinations)}"+"_.mat", data_dict)

    shm.close()
    shm.unlink()

    print('done')

def iterator_linear(motion:np.ndarray, curve:bool, visual:bool = False, savelog:bool = False) -> None:
    # slithering = (45, 45, 30, 30, 60, 30, 0, 0.05)

    motion_param = motion

    amp_d = np.array([motion_param[0]])
    amp_l = np.array([motion_param[1]])

    psi = np.arange(0,181)

    nu = np.arange(1,121)

    delta = np.array([0])
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

    pc1 = Process(target= orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[0]:start_idx[1]]),   shm.name, U_map.shape, visual, savelog))
    pc2 = Process(target= orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[1]:start_idx[2]]),   shm.name, U_map.shape, visual, savelog))
    pc3 = Process(target= orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[2]:start_idx[3]]),   shm.name, U_map.shape, visual, savelog))
    pc4 = Process(target= orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[3]:start_idx[4]]),   shm.name, U_map.shape, visual, savelog))
    pc5 = Process(target= orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[4]:start_idx[5]]),   shm.name, U_map.shape, visual, savelog))
    pc6 = Process(target= orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[5]:start_idx[6]]),   shm.name, U_map.shape, visual, savelog))
    pc7 = Process(target= orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[6]:start_idx[7]]),   shm.name, U_map.shape, visual, savelog))
    pc8 = Process(target= orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[7]:start_idx[8]]),   shm.name, U_map.shape, visual, savelog))
    pc9 = Process(target= orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[8]:start_idx[9]]),   shm.name, U_map.shape, visual, savelog))
    pc10 = Process(target=orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[9]:start_idx[10]]),  shm.name, U_map.shape, visual, savelog))
    pc11 = Process(target=orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[10]:start_idx[11]]), shm.name, U_map.shape, visual, savelog))
    pc12 = Process(target=orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[11]:start_idx[12]]), shm.name, U_map.shape, visual, savelog))
    pc13 = Process(target=orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[12]:start_idx[13]]), shm.name, U_map.shape, visual, savelog))
    pc14 = Process(target=orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[13]:start_idx[14]]), shm.name, U_map.shape, visual, savelog))
    pc15 = Process(target=orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[14]:start_idx[15]]), shm.name, U_map.shape, visual, savelog))
    pc16 = Process(target=orderize_linear, args=(np.array(motion_param), curve, list(combinations[start_idx[15]::]),             shm.name, U_map.shape, visual, savelog))

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
    savemat("./opti_step/U_map_linear_serp_compare_"+str(curve)+"_"+param2filename(motion_param)+f"_{len(combinations)}"+"_.mat", data_dict)
    
    shm.close()
    shm.unlink()

    print('done')

def iterator_linear_fine(motion:np.ndarray, curve:bool, visual:bool = False, savelog:bool = False) -> None:
    # slithering = (45, 45, 30, 30, 60, 30, 0, 0.05)

    motion_param = motion

    amp_d = np.array([motion_param[0]])
    amp_l = np.array([motion_param[1]])

    psi = np.arange(-90,91)

    nu = np.arange(-90,91)

    delta = np.array([0])
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
    savemat("./opti_step/U_map_linear_serp_compare_"+str(curve)+"_"+param2filename(motion_param)+f"_{len(combinations)}"+"_.mat", data_dict)
    
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

    print(J_curve(serpentine_op, serpentine_op, True, False))
    exit()

    # #### Grid searching
    # start_iter = time.time()
    # # iterator(slithering, (9,9,0,0,1,1,0), (10,10,19,19,7,7,19), (5, 5, 10, 10, 10, 10, 5))
    # # iterator(slithering, (8,8,0,0,1,1,0), (9,9,3,3,3,3,3), (5, 5, 10, 10, 10, 10, 5))
    # iterator(sidewinding, (8,8,0,0,2,2,10), (9,9,181,181,3,3,11), (5, 5, 1, 1, 10, 10, 5))
    # end_iter = time.time()

    # print(f"Iterating dond... {end_iter-start_iter} seconds elapsed")

    # start_iter = time.time()
    # # iterator(slithering, (9,9,0,0,1,1,0), (10,10,19,19,7,7,19), (5, 5, 10, 10, 10, 10, 5))
    # # iterator(slithering, (8,8,0,0,1,1,0), (9,9,3,3,3,3,3), (5, 5, 10, 10, 10, 10, 5))
    # iterator_curve(sidewinding, (8,8,0,0,2,2,10), (9,9,181,181,3,3,11), (5, 5, 1, 1, 10, 10, 5))
    # end_iter = time.time()

    # print(f"Iterating dond... {end_iter-start_iter} seconds elapsed")

    # #### Linear Searching...
    # start_iter = time.time()
    # # iterator_linear(serpentine_op, False)
    # iterator_linear(sidewinding_op,False)
    # # iterator_linear(slithering_op,False)

    # iterator(rolling, (2,2,0,0,0,0,10), (3,3,1,1,121,121,11), (5, 5, 1, 1, 0.5, 0.5, 5))
    # # iterator_curve(rolling, (2,2,0,0,0,0,10), (3,3,1,1,121,121,11), (5, 5, 1, 1, 0.5, 0.5, 5))

    # end_iter = time.time()
    # print(f"Iterating dond... {end_iter-start_iter} seconds elapsed")

    # #### Minimizing...
    # start_iter = time.time()
    # xv0 = np.array([45,45,30,30,0])
    # xvbound = ((0,90), (0,90), (0,180), (10,60), (-25,25))
    # options={'xatol': 3, 'fatol' : 10, 'disp': True}
    # res = minimize(J_minize, xv0, method='Nelder-Mead', bounds=xvbound, options=options)
    # end_iter = time.time()
    # print(f"Iterating dond... {end_iter-start_iter} seconds elapsed")
    # print(res)

    ### Evaluating
    # U = J_curve((4.590e+01,  4.587e+01,  3.174e+01,  3.174e+01,  2 * 2.723e+01,  2.723e+01,  2.381e-04, 0.05), (4.590e+01,  4.587e+01,  3.174e+01,  3.174e+01,  2 * 2.723e+01,  2.723e+01,  2.381e-04, 0.05), False, False)
    # print(U)
    # U = J((4.590e+01,  4.587e+01,  3.174e+01,  3.174e+01,  2 * 2.723e+01,  2.723e+01,  2.381e-04, 0.05), (4.590e+01,  4.587e+01,  3.174e+01,  3.174e+01,  2 * 2.723e+01,  2.723e+01,  2.381e-04, 0.05), False, False)
    # U = J(slithering, (45,  45,  28,  44,  30,  60,  0, 0.05), False, False)
    # print(U)
    # U = J(slithering, slithering, False, False)
    # print(U)
    # U = J_curve(slithering, slithering, False, False)
    # print(U)

    # U = J((4.687e+01,  4.318e+01,  3.209e+01,  3.209e+01,  3.387e+01 * 2,  3.387e+01, -4.326e-04, 0.05), (4.687e+01,  4.318e+01,  3.209e+01,  3.209e+01,  3.387e+01 * 2,  3.387e+01, -4.326e-04, 0.05), True, False)