# import jax
# import mediapy as media
import mujoco
import mujoco.viewer
from scipy.io import savemat

import time
import numpy as np
import itertools
import serpenoid

from scipy.spatial.transform import Rotation
from multiprocessing import Process, Queue, shared_memory

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

    u_input = np.sin(temporal + nu_n * link_n + phi_n) * amp_n 

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
    f_name = f_name.replace(',','')
    f_name = f_name.replace(' ','x')
    f_name = f_name.replace('[','')
    f_name = f_name.replace(']','')
    f_name = f_name.replace('.','_')

    return f_name

def J(t, parameters:np.ndarray, g:str = 'serp', visual:bool = False, savelog:bool = False) -> np.ndarray:
    snake = mujoco.MjModel.from_xml_path("../dmc/models/snake_circle_contact_servo.xml")
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

            step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[48:52].copy()))
            p_head = np.vstack((p_head, step_data))

            if savelog:
                renderer.update_scene(data)
                pixel = renderer.render()

                frames.append(pixel)

        if savelog:
            media.write_video(f_name+g+'.mp4',frames, fps=100)
    
    if savelog and not(visual):
        sim_data = {g+"_trajectory_"+f_name: p_head}
        savemat("trajectory_"+g+f_name+'.mat',sim_data)


    # Scalar J
    J_value = 0

    if (g == 'side'):
        J_value = 1500 * p_head[-1,1] - 800 * abs(p_head[-1,1]) - 900 * abs(p_head[-1,0] / p_head[-1,1])
    else:
        J_value = 1500 * p_head[-1,0] - 800 * abs(p_head[-1,0]) - 900 * abs(p_head[-1,1] / p_head[-1,0])

    return J_value

    # Position & Orientation
    ori_head = p_head[:,3::]

    quat_p_head = Rotation.from_quat(ori_head[:, [1, 2, 3, 0]].copy())
    
    # return np.hstack((np.mean(p_head[:,0:3], axis=0), Rotation.mean(quat_p_head).as_quat()[3], Rotation.mean(quat_p_head).as_quat()[0], Rotation.mean(quat_p_head).as_quat()[1], Rotation.mean(quat_p_head).as_quat()[2]))

def J_velocity(t, parameters:np.ndarray, g:str = 'serp', visual:bool = False, savelog:bool = False) -> np.ndarray:
    snake = mujoco.MjModel.from_xml_path("../dmc/models/snake_circle_contact_servo.xml")
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

            step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[48:52].copy()))
            p_head = np.vstack((p_head, step_data))

            if savelog:
                renderer.update_scene(data)
                pixel = renderer.render()

                frames.append(pixel)

        if savelog:
            media.write_video(f_name+g+'.mp4',frames, fps=100)
    
    if savelog:
        sim_data = {g+"_trajectory_"+f_name: p_head, "joint_input":q}
        savemat("trajectory_"+g+f_name+'.mat',sim_data)


    # Position & Orientation
    ori_head = p_head[:,3::]
    quat_p_head = Rotation.from_quat(ori_head[:, [1, 2, 3, 0]].copy())
    
    J_result = np.hstack((np.mean(p_head[:,0:3], axis=0), Rotation.mean(quat_p_head).as_quat()[3], Rotation.mean(quat_p_head).as_quat()[0], Rotation.mean(quat_p_head).as_quat()[1], Rotation.mean(quat_p_head).as_quat()[2]))

    J_value = 0

    # Return scalar data -> X-Y 위치 기반의 U 값
    if (g == 'side'):
        J_value = np.abs(J_result[1]) - np.abs(J_result[0])
    else:
        # J_value = J_result[0] - np.abs(J_result[1])
        J_value = np.abs(J_result[1]) - np.abs(J_result[0]) #20240104 ones 게이트 비교를 위해서 기존 Side와 똑같이

    return J_value

    # Return raw p data
    # return np.hstack((np.mean(p_head[:,0:3], axis=0), Rotation.mean(quat_p_head).as_quat()[3], Rotation.mean(quat_p_head).as_quat()[0], Rotation.mean(quat_p_head).as_quat()[1], Rotation.mean(quat_p_head).as_quat()[2]))

def J_force_mean(t, parameters:np.ndarray, g:str = 'serp', visual:bool = False, savelog:bool = False) -> np.ndarray:
    snake = mujoco.MjModel.from_xml_path("../dmc/models/snake_circle_contact_servo.xml")
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

            step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[48:52].copy()))
            p_head = np.vstack((p_head, step_data))

            if savelog:
                renderer.update_scene(data)
                pixel = renderer.render()

                frames.append(pixel)

        if savelog:
            media.write_video(f_name+g+'.mp4',frames, fps=100)
    
    if savelog and not(visual):
        sim_data = {g+"_trajectory_"+f_name: p_head}
        savemat("trajectory_"+g+f_name+'.mat',sim_data)


    # Scalar J
    J_value = 0

    if (g == 'side'):
        J_value = 1500 * p_head[-1,1] - 800 * abs(p_head[-1,1]) - 900 * abs(p_head[-1,0] / p_head[-1,1])
    else:
        J_value = 1500 * p_head[-1,0] - 800 * abs(p_head[-1,0]) - 900 * abs(p_head[-1,1] / p_head[-1,0])

    return J_value

    # Position & Orientation
    ori_head = p_head[:,3::]

    quat_p_head = Rotation.from_quat(ori_head[:, [1, 2, 3, 0]].copy())
    
    # return np.hstack((np.mean(p_head[:,0:3], axis=0), Rotation.mean(quat_p_head).as_quat()[3], Rotation.mean(quat_p_head).as_quat()[0], Rotation.mean(quat_p_head).as_quat()[1], Rotation.mean(quat_p_head).as_quat()[2]))

def iter_J(basis:np.ndarray, param, g:str, shd_name:str, shd_shape, visual:bool, savelog:bool) -> None:
    param_coeff = [10, 10, 0.8 * np.pi, 0.8 * np.pi, 8 * np.pi, 8 * np.pi, 10]

    for i in param:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        d_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        idx = i - (basis + np.array([1, 1, 1, 1, 1, 1, 0]))
        combinations = np.round(np.divide(i, param_coeff), 2)

        d_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :] = J(t, combinations, g, visual, savelog)

        # print(d_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :])
        # print(J(t, combinations, g, visual, savelog))

        exist_shm.close()

def iter_scalar_J(basis:np.ndarray, param, g:str, shd_name:str, shd_shape, visual:bool, savelog:bool) -> None:
    param_coeff = [10, 10, 0.8 * np.pi, 0.8 * np.pi, 180 / np.pi, 180 / np.pi, 10]

    for i in param:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        d_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        idx = i - (basis + np.array([1, 1, 1, 1, 1, 1, 0]))
        combinations = np.round(np.divide(i, param_coeff), 2)

        d_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :] = J(t, combinations, g, visual, savelog)

        # print(d_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :])
        # print(J(t, combinations, g, visual, savelog))

        exist_shm.close()

def iter_velocity_J(basis:np.ndarray, param, g:str, shd_name:str, shd_shape, visual:bool, savelog:bool) -> None:
    param_coeff = [10, 10, 0.8 * np.pi, 0.8 * np.pi, 180 / np.pi, 180 / np.pi, 180 / np.pi]

    for i in param:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        d_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        idx = i - (basis + np.array([1, 1, 1, 1, 1, 1, 1]))
        combinations = np.round(np.divide(i, param_coeff), 2)

        d_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :] = J_velocity(t, combinations, g, visual, savelog)

        # print(d_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :])
        # print(J(t, combinations, g, visual, savelog))

        exist_shm.close()

def orderize_J(param_min:np.ndarray, param_max:np.ndarray, g:str = 'serp', visual:bool = False, savelog:bool = False)->np.ndarray:
    #min param -> [0, 0, 0, 0, 0, 0, 0]
    #max param -> [14, 14, 16, 16, 16, 16, 0]

    basis = param_min

    a_d = np.arange(1,15)[param_min[0]:param_max[0]] # Radian
    a_l = np.arange(1,15)[param_min[1]:param_max[1]] # Radian
    o_d = np.arange(1,17)[param_min[2]:param_max[2]] # Radian
    o_l = np.arange(1,17)[param_min[3]:param_max[3]] # Radian
    n_d = np.arange(1,17)[param_min[4]:param_max[4]] # Radian
    n_l = np.arange(1,17)[param_min[5]:param_max[5]] # Radian
    # p = np.random.randint(1,17) / 8 * np.pi
    p = [0] # Radian

    n1 = len(a_d)
    n2 = len(a_l)
    n3 = len(o_d)
    n4 = len(o_l)
    n5 = len(n_d)
    n6 = len(n_l)
    n7 = len(p)

    vel_map = np.empty((n1,n2,n3,n4,n5,n6,n7,7), dtype=np.float64)
    shm = shared_memory.SharedMemory(name="shared_vel_map", create=True, size=vel_map.nbytes)
    data_map = np.ndarray(vel_map.shape, dtype=vel_map.dtype, buffer=shm.buf)

    combinations = list(itertools.product(a_d, a_l, o_d, o_l, n_d, n_l, p))

    print(f'Number of Combinations : {len(combinations)}')

    ea = len(combinations) // 12

    start_idx = [0, 1 * ea, 2 * ea, 3 * ea, 4 * ea, 5 * ea, 6 * ea, 7 * ea, 8 * ea , 9 * ea, 10 * ea, 11 * ea] 

    print(f'For 12 processes start indices : {start_idx}')

    pc1 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[0]:start_idx[1]]), g, shm.name, vel_map.shape, visual, savelog))
    pc2 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[1]:start_idx[2]]), g, shm.name, vel_map.shape, visual, savelog))
    pc3 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[2]:start_idx[3]]), g, shm.name, vel_map.shape, visual, savelog))
    pc4 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[3]:start_idx[4]]), g, shm.name, vel_map.shape, visual, savelog))
    pc5 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[4]:start_idx[5]]), g, shm.name, vel_map.shape, visual, savelog))
    pc6 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[5]:start_idx[6]]), g, shm.name, vel_map.shape, visual, savelog))
    pc7 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[6]:start_idx[7]]), g, shm.name, vel_map.shape, visual, savelog))
    pc8 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[7]:start_idx[8]]), g, shm.name, vel_map.shape, visual, savelog))
    pc9 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[8]:start_idx[9]]), g, shm.name, vel_map.shape, visual, savelog))
    pc10 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[9]:start_idx[10]]), g, shm.name, vel_map.shape, visual, savelog))
    pc11 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[10]:start_idx[11]]), g, shm.name, vel_map.shape, visual, savelog))
    pc12 = Process(target=iter_J, args=(np.array(basis), list(combinations[start_idx[11]::]), g, shm.name, vel_map.shape, visual, savelog))


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

    # for i in combinations:
    #     idx = i - (basis + np.array([1,1,1,1,1,1,0]))
    #     print(data_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :])

    data_dict = {g+'_map': data_map, g+'_basis' : basis}
    savemat("vel_map_"+g+'_b_'+param2filename(basis)+f"_{len(combinations)}"+"_.mat", data_dict)
    
    shm.close()
    shm.unlink()

    print('done')

def orderize_scalar_J(param_min:np.ndarray, param_max:np.ndarray, g:str = 'serp', visual:bool = False, savelog:bool = False)->np.ndarray:
    #this for paper grid searching...
    #min param -> [0, 0, 0, 0, 0, 0, 0]
    #max param -> [14, 14, 16, 16, 16, 16, 0]

    basis = param_min

    a_d = np.arange(1,15)[param_min[0]:param_max[0]] # Radian
    a_l = np.arange(1,15)[param_min[1]:param_max[1]] # Radian
    o_d = np.arange(1,17)[param_min[2]:param_max[2]] # Radian
    o_l = np.arange(1,17)[param_min[3]:param_max[3]] # Radian
    n_d = np.arange(1,361)[param_min[4]:param_max[4]] # Degree
    n_l = np.arange(1,361)[param_min[5]:param_max[5]] # Degree
    # p = np.random.randint(1,17) / 8 * np.pi
    p = [0] # Radian

    n1 = len(a_d)
    n2 = len(a_l)
    n3 = len(o_d)
    n4 = len(o_l)
    n5 = len(n_d)
    n6 = len(n_l)
    n7 = len(p)

    vel_map = np.empty((n1,n2,n3,n4,n5,n6,n7,7), dtype=np.float64)
    shm = shared_memory.SharedMemory(name="shared_vel_map", create=True, size=vel_map.nbytes)
    data_map = np.ndarray(vel_map.shape, dtype=vel_map.dtype, buffer=shm.buf)

    combinations = list(itertools.product(a_d, a_l, o_d, o_l, n_d, n_l, p))

    print(f'Number of Combinations : {len(combinations)}')

    ea = len(combinations) // 12

    start_idx = [0, 1 * ea, 2 * ea, 3 * ea, 4 * ea, 5 * ea, 6 * ea, 7 * ea, 8 * ea , 9 * ea, 10 * ea, 11 * ea] 

    print(f'For 12 processes start indices : {start_idx}')

    pc1 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[0]:start_idx[1]]), g, shm.name, vel_map.shape, visual, savelog))
    pc2 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[1]:start_idx[2]]), g, shm.name, vel_map.shape, visual, savelog))
    pc3 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[2]:start_idx[3]]), g, shm.name, vel_map.shape, visual, savelog))
    pc4 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[3]:start_idx[4]]), g, shm.name, vel_map.shape, visual, savelog))
    pc5 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[4]:start_idx[5]]), g, shm.name, vel_map.shape, visual, savelog))
    pc6 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[5]:start_idx[6]]), g, shm.name, vel_map.shape, visual, savelog))
    pc7 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[6]:start_idx[7]]), g, shm.name, vel_map.shape, visual, savelog))
    pc8 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[7]:start_idx[8]]), g, shm.name, vel_map.shape, visual, savelog))
    pc9 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[8]:start_idx[9]]), g, shm.name, vel_map.shape, visual, savelog))
    pc10 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[9]:start_idx[10]]), g, shm.name, vel_map.shape, visual, savelog))
    pc11 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[10]:start_idx[11]]), g, shm.name, vel_map.shape, visual, savelog))
    pc12 = Process(target=iter_scalar_J, args=(np.array(basis), list(combinations[start_idx[11]::]), g, shm.name, vel_map.shape, visual, savelog))


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

    # for i in combinations:
    #     idx = i - (basis + np.array([1,1,1,1,1,1,0]))
    #     print(data_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :])

    data_dict = {g+'_grid': data_map, g+'_basis' : basis}
    savemat("grid_map_"+g+'_b_'+param2filename(basis)+f"_{len(combinations)}"+"_.mat", data_dict)
    
    shm.close()
    shm.unlink()

    print('done')

def orderize_velocity_J(param_min:np.ndarray, param_max:np.ndarray, g:str = 'serp', visual:bool = False, savelog:bool = False)->np.ndarray:
    #this for paper grid searching...
    #min param -> [0, 0, 0, 0, 0, 0, 0]
    #max param -> [14, 14, 16, 16, 16, 16, 0]

    basis = param_min

    a_d = np.arange(1,15)[param_min[0]:param_max[0]] # Radian
    a_l = np.arange(1,15)[param_min[1]:param_max[1]] # Radian
    o_d = np.arange(1,17)[param_min[2]:param_max[2]] # Radian
    o_l = np.arange(1,17)[param_min[3]:param_max[3]] # Radian
    n_d = np.arange(1,361)[param_min[4]:param_max[4]] # Degree
    n_l = np.arange(1,361)[param_min[5]:param_max[5]] # Degree
    # p = np.random.randint(1,17) / 8 * np.pi
    p = np.arange(0,360)[param_min[6]:param_max[6]] # Radian

    n1 = len(a_d)
    n2 = len(a_l)
    n3 = len(o_d)
    n4 = len(o_l)
    n5 = len(n_d)
    n6 = len(n_l)
    n7 = len(p)

    vel_map = np.empty((n1,n2,n3,n4,n5,n6,n7,7), dtype=np.float64)
    shm = shared_memory.SharedMemory(name="shared_vel_map", create=True, size=vel_map.nbytes)
    data_map = np.ndarray(vel_map.shape, dtype=vel_map.dtype, buffer=shm.buf)

    combinations = list(itertools.product(a_d, a_l, o_d, o_l, n_d, n_l, p))

    print(f'Number of Combinations : {len(combinations)}')

    ea = len(combinations) // 12

    start_idx = [0, 1 * ea, 2 * ea, 3 * ea, 4 * ea, 5 * ea, 6 * ea, 7 * ea, 8 * ea , 9 * ea, 10 * ea, 11 * ea] 

    print(f'For 12 processes start indices : {start_idx}')

    pc1 = Process(target= iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[0]:start_idx[1]]), g, shm.name, vel_map.shape, visual, savelog))
    pc2 = Process(target= iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[1]:start_idx[2]]), g, shm.name, vel_map.shape, visual, savelog))
    pc3 = Process(target= iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[2]:start_idx[3]]), g, shm.name, vel_map.shape, visual, savelog))
    pc4 = Process(target= iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[3]:start_idx[4]]), g, shm.name, vel_map.shape, visual, savelog))
    pc5 = Process(target= iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[4]:start_idx[5]]), g, shm.name, vel_map.shape, visual, savelog))
    pc6 = Process(target= iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[5]:start_idx[6]]), g, shm.name, vel_map.shape, visual, savelog))
    pc7 = Process(target= iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[6]:start_idx[7]]), g, shm.name, vel_map.shape, visual, savelog))
    pc8 = Process(target= iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[7]:start_idx[8]]), g, shm.name, vel_map.shape, visual, savelog))
    pc9 = Process(target= iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[8]:start_idx[9]]), g, shm.name, vel_map.shape, visual, savelog))
    pc10 = Process(target=iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[9]:start_idx[10]]), g, shm.name, vel_map.shape, visual, savelog))
    pc11 = Process(target=iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[10]:start_idx[11]]), g, shm.name, vel_map.shape, visual, savelog))
    pc12 = Process(target=iter_velocity_J, args=(np.array(basis), list(combinations[start_idx[11]::]), g, shm.name, vel_map.shape, visual, savelog))

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

    # for i in combinations:
    #     idx = i - (basis + np.array([1,1,1,1,1,1,0]))
    #     print(data_map[idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], :])

    data_dict = {g+'_grid': data_map, g+'_basis' : basis}
    savemat("velocity_grid_map_"+g+'_b_'+param2filename(basis)+f"_{len(combinations)}"+"_.mat", data_dict)
    
    shm.close()
    shm.unlink()

    print('done')

def base2Param(base:list, param:list) -> np.ndarray:
    base = np.array(base)
    param = np.array(param)
    idx = np.array([1, 1, 1, 1, 1, 1, 0])

    param_coeff = [10, 10, 0.8 * np.pi, 0.8 * np.pi, 8 * np.pi, 8 * np.pi, 10]

    input_p = np.round(np.divide((base + param +  idx), param_coeff), 2)

    return input_p

def base2Param_scalar(base:list, param:list) -> np.ndarray:
    base = np.array(base)
    param = np.array(param)
    idx = np.array([1, 1, 1, 1, 1, 1, 0])

    param_coeff = [10, 10, 0.8 * np.pi, 0.8 * np.pi, 180 / np.pi, 180 / np.pi, 180 / np.pi]

    input_p = np.round(np.divide((base + param +  idx), param_coeff), 2)

    return input_p


### Main script
if __name__ == "__main__":
    grid_start_time = time.time()

    # # Sim once
    # bais = [7, 11, 14, 7, 0, 0, 0] # Serp
    # # bais = [8, 12, 14, 7, 0, 0, 0] # Side
    
    # # param = [0, 0, 0, 0, 233, 18, 180] # Serp OP
    # # param = [0, 0, 0, 0, 220, 198, 0] # Side OP
    # param = [0, 0, 0, 0, 233, 197, 90] # Side Phi90 OP



    # # sim_data = J(t, base2Param(bais, param), 'serp', False, False)
    # sim_data = J_velocity(t, base2Param_scalar(bais, param), 'side', True, False)
    # print(sim_data)

    # # Grid Search
    # orderize_J([7, 7, 14, 7, 0, 0, 0], [8, 8, 15, 8, 16, 16, 1],g='serp')
    # orderize_J([7, 7, 14, 7, 0, 0, 0], [8, 8, 15, 8, 16, 16, 1],g='side')
    # orderize_J([7, 7, 14, 7, 0, 0, 0], [8, 8, 15, 8, 16, 16, 1],g='ones')

    # # Grid Search
    # orderize_J([7, 7, 7, 7, 0, 0, 0], [8, 8, 16, 16, 16, 16, 1],g='serp')
    # orderize_J([7, 7, 7, 7, 0, 0, 0], [8, 8, 16, 16, 16, 16, 1],g='side')
    # orderize_J([7, 7, 7, 7, 0, 0, 0], [8, 8, 16, 16, 16, 16, 1],g='ones')

    # Paper Grid Search
    # orderize_velocity_J([7, 11, 14, 7, 0, 0, 0], [8, 12, 15, 8, 360, 360, 1],g='serp')
    # orderize_velocity_J([7, 11, 14, 7, 0, 0, 0], [8, 12, 15, 8, 360, 360, 1],g='side')
    # orderize_velocity_J([7, 11, 14, 7, 0, 0, 0], [8, 12, 15, 8, 360, 360, 1],g='ones')

    # orderize_velocity_J([8, 12, 14, 7, 0, 0, 0], [9, 13, 15, 8, 360, 360, 1],g='side')
    # orderize_velocity_J([8, 12, 14, 7, 0, 0, 0], [9, 13, 15, 8, 360, 360, 1],g='serp')
    # orderize_velocity_J([8, 12, 14, 7, 0, 0, 0], [9, 13, 15, 8, 360, 360, 1],g='ones')

    orderize_velocity_J([7, 11, 14, 7, 0, 0, 90], [8, 12, 15, 8, 360, 360, 91],g='ones')
    orderize_velocity_J([8, 12, 14, 7, 0, 0, 90], [9, 13, 15, 8, 360, 360, 91],g='ones')

    # # Optimal param and Phi differ grid searching
    # orderize_velocity_J([7, 11, 14, 7, 233, 18, 0], [8, 12, 15, 8, 234, 19, 360],g='serp')
    # orderize_velocity_J([7, 11, 14, 7, 233, 18, 0], [8, 12, 15, 8, 234, 19, 360],g='side')
    # orderize_velocity_J([7, 11, 14, 7, 233, 18, 0], [8, 12, 15, 8, 234, 19, 360],g='ones')

    # orderize_velocity_J([8, 12, 14, 7, 220, 198, 0], [9, 13, 15, 8, 221, 199, 360],g='side')
    # orderize_velocity_J([8, 12, 14, 7, 220, 198, 0], [9, 13, 15, 8, 221, 199, 360],g='serp')
    # orderize_velocity_J([8, 12, 14, 7, 220, 198, 0], [9, 13, 15, 8, 221, 199, 360],g='ones')





    print(f'Simdone... {time.time() - grid_start_time}')

    # vel_map = np.empty((15,15,17,17,17), dtype=object)
    # vel_map[0,0,0,0,0] = np.array([0, 0, 0])
    # data_dict = {'map': vel_map}
    # savemat("testing.mat", data_dict, noneObject=[0])


