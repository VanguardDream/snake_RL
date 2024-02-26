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

def J_vm(parameters:np.ndarray, parameters_bar:np.ndarray, curve:bool, visual:bool = False, savelog:bool = False) -> np.ndarray:
    _robot_body_names = ["head","link1","link2","link3","link4","link5","link6","link7","link8","link9","link10","link11","link12","link13","tail"]

    def get_robot_com(data)->np.ndarray:
        accum_x = 0
        accum_y = 0
        len_names = len(_robot_body_names)

        for name in _robot_body_names:
            x, y, _ = data.body(name).xpos
            accum_x = accum_x + x
            accum_y = accum_y + y

        return np.array([accum_x / len_names, accum_y / len_names])

    def get_robot_rot(data)->np.ndarray:
        com_roll = 0
        com_pitch = 0
        com_yaw = 0

        robot_quats = np.empty((0,4))
        for name in _robot_body_names:
            robot_quats = np.vstack((robot_quats, data.body(name).xquat.copy()))

        robot_quats = robot_quats[:, [1, 2, 3, 0]]
        robot_rot = Rotation(robot_quats)

        com_roll, com_pitch, com_yaw = robot_rot.mean().as_rotvec(False)

        return np.array([com_roll, com_pitch, com_yaw])

    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)
    mujoco.mj_forward(snake, data)

    M_name = param2filename(parameters)
    Bar_name = param2filename(parameters_bar)

    f_name = "M_" + M_name + "_Bar_" + Bar_name

    gait = serpenoid.Gait(tuple(parameters), tuple(parameters_bar))

    if curve:
        q = gait.CurveFunction
    else:
        q = gait.Gk
    
    expand_q = np.repeat(q, 10, axis=1)

    p_com = np.empty((0,5))
    step_data = np.hstack((get_robot_com(data), get_robot_rot(data)))
    p_com = np.vstack((p_com, step_data))

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

                step_data = np.hstack((get_robot_com(data), get_robot_rot(data)))
                p_com = np.vstack((p_com, step_data))
    
    else: # no visual
        renderer = mujoco.Renderer(snake, 720, 1280)
        frames = []
        time_start_sim = time.time()
        for i in expand_q.transpose():
            index = np.nonzero(i)
            for idx in index:
                data.ctrl[idx] = i[idx]

            mujoco.mj_step(snake, data)

            step_data = np.hstack((get_robot_com(data), get_robot_rot(data)))
            p_com = np.vstack((p_com, step_data))

            if savelog:
                renderer.update_scene(data)
                pixel = renderer.render()

                frames.append(pixel)

        if savelog:
            media.write_video(f_name+'.mp4',frames, fps=200)
    
    if savelog and not(visual):
        sim_data = {"trajectory_"+f_name: p_com}
        savemat("trajectory_"+f_name+'.mat',sim_data)

    d_t = np.diff(p_com,axis=0) / snake.opt.timestep

    return np.mean(d_t, axis=0)

def orderize_linear(param_motion:np.ndarray, curve:bool, param_bar_iter:np.ndarray, shd_name:str, shd_shape, visual:bool, savelog:bool) -> None:

    for i in param_bar_iter:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        U_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        idx1 = i[2] # psi start 0
        idx2 = i[3] - 1 # nu start 1

        amp_d, amp_l, psi, nu, delta = i
        lambda_bar = (amp_d, amp_l, psi, psi, (nu) * (1/2), (nu) * (1/2), delta, param_motion[-1])

        U_map[idx1, idx2, :] = J_vm(param_motion, lambda_bar, curve, visual, savelog)
            

def iterator_linear(motion:np.ndarray, curve:bool, visual:bool = False, savelog:bool = False) -> None:
    # slithering = (45, 45, 30, 30, 60, 30, 0, 0.05)

    motion_param = motion

    amp_d = np.array([motion_param[0]])
    amp_l = np.array([motion_param[1]])

    psi = np.arange(0,181)

    nu = np.arange(1,121)

    # delta = np.array([motion_param[-2]])
    delta = np.array([0])

    n1 = len(psi)
    n2 = len(nu)

    U_map = np.empty((n1,n2,5), dtype=np.float64)
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
    savemat("./velmap_data/U_map_linear_M_"+str(curve)+"_"+param2filename(motion_param)+f"_{len(combinations)}"+"_.mat", data_dict)
    
    shm.close()
    shm.unlink()

    print('done')

if __name__ == "__main__":
    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)

    serpentine = (45, 45, 30, 30, 60, 60, 0, 0.05)
    slithering = (45, 45, 30, 30, 60, 30, 0, 0.05)
    sidewinding = (45, 45, 30, 30, 30, 30, 45, 0.05)
    rolling = (15, 15, 0, 0, 30, 30, 90, 0.05)

    # # Velmap test
    # J_vm(slithering, slithering, False, False)
    # J_vm(serpentine, serpentine, True, False)

    start_iter = time.time()
    iterator_linear(serpentine, False)
    iterator_linear(serpentine, True)
    iterator_linear(slithering, False)
    iterator_linear(slithering, True)
    iterator_linear(sidewinding, False)
    iterator_linear(sidewinding, True)

    end_iter = time.time()
    print(f"Iterating dond... {end_iter-start_iter} seconds elapsed")
