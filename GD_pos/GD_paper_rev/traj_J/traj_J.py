import mujoco
import mujoco.viewer
import mediapy as media
from scipy.io import savemat
from scipy.optimize import minimize

import time
import numpy as np
import itertools
import serpenoid
import serpenoid_gamma

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

def J_view(parameters:np.ndarray, parameters_bar:np.ndarray, curve:bool, gamma:float) -> np.ndarray:
    """
    return : [U, avg. yaw]
    """
    _robot_body_names = ["head","link1","link2","link3","link4","link5","link6","link7","link8","link9","link10","link11","link12","link13","tail"]

    def get_robot_rot(data)->np.ndarray:
        com_roll = 0
        com_pitch = 0
        com_yaw = 0

        robot_quats = np.empty((0,4))
        for name in _robot_body_names:
            robot_quats = np.vstack((robot_quats, data.body(name).xquat.copy()))

        robot_quats = robot_quats[:, [1, 2, 3, 0]]
        robot_rot = Rotation(robot_quats)

        # com_roll, com_pitch, com_yaw = robot_rot.mean().as_rotvec(False)
        x, y, z, w = robot_rot.mean().as_quat()

        # return np.array([com_roll, com_pitch, com_yaw])
        return np.array([w, x, y, z])

    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)
    mujoco.mj_forward(snake, data)

    M_name = param2filename(parameters)
    Bar_name = param2filename(parameters_bar)

    # gait = serpenoid.Gait(tuple(parameters), tuple(parameters_bar))
    gait = serpenoid_gamma.Gait(tuple(parameters), tuple(parameters_bar), gamma)

    if curve:
        q = gait.CurveFunction
    else:
        q = gait.Gk

    expand_q = np.repeat(q, 10, axis=1)

    p_head = np.empty((expand_q.shape[1], 21))


    with mujoco.viewer.launch_passive(snake, data) as viewer:
        for i in range(expand_q.shape[1]):
            time_step = time.time()
            index = np.nonzero(expand_q[:, i])
            for idx in index:
                data.ctrl[idx] = expand_q[idx, i]

            mujoco.mj_step(snake, data)
            viewer.sync()

            while snake.opt.timestep - (time.time() - time_step) > 0:
                    time.sleep(0)

            step_data = np.hstack((data.body('head').xpos.copy(), get_robot_rot(data), data.ctrl))
            p_head[i] = step_data

    i = 300
    j = -30
    l = -0.01

    p_head_diff = np.diff(p_head[:,0:2],axis=0)
    p_head_diff_l2_norm = np.linalg.norm(p_head_diff,2,axis=1)

    l_traj = np.sum(p_head_diff_l2_norm)
    l_dist = np.linalg.norm(p_head[-1,0:2],2)

    i_term = i * l_dist
    j_term = j * (l_traj + 1)/(l_dist + 1)
    l_term = l * np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    # Position & Orientation
    ori_head = p_head[:,3:7]
    quat_p_head = Rotation.from_quat(ori_head[:, [1, 2, 3, 0]].copy())
    mean_rot = Rotation.mean(quat_p_head).as_rotvec()

    # Terminal orientation
    t_x = p_head[-1,0]
    t_y = p_head[-1,1]

    t_orientation = 0
    try:
        t_orientation = np.arctan2(t_y, t_x)
    except Exception as e:
        print(e)
        t_orientation = np.nan
    
    return np.hstack((i_term + j_term + l_term, mean_rot, t_orientation))

def J_traj(parameters:np.ndarray, parameters_bar:np.ndarray, curve:bool, gamma:float) -> np.ndarray:
    """
    return : [U, avg. yaw]
    """
    _robot_body_names = ["head","link1","link2","link3","link4","link5","link6","link7","link8","link9","link10","link11","link12","link13","tail"]

    def get_robot_rot(data)->np.ndarray:
        com_roll = 0
        com_pitch = 0
        com_yaw = 0

        robot_quats = np.empty((0,4))
        for name in _robot_body_names:
            robot_quats = np.vstack((robot_quats, data.body(name).xquat.copy()))

        robot_quats = robot_quats[:, [1, 2, 3, 0]]
        robot_rot = Rotation(robot_quats)

        # com_roll, com_pitch, com_yaw = robot_rot.mean().as_rotvec(False)
        x, y, z, w = robot_rot.mean().as_quat()

        # return np.array([com_roll, com_pitch, com_yaw])
        return np.array([w, x, y, z])

    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)
    mujoco.mj_forward(snake, data)

    M_name = param2filename(parameters)
    Bar_name = param2filename(parameters_bar)

    # gait = serpenoid.Gait(tuple(parameters), tuple(parameters_bar))
    gait = serpenoid_gamma.Gait(tuple(parameters), tuple(parameters_bar), gamma)

    if curve:
        q = gait.CurveFunction
    else:
        q = gait.Gk

    expand_q = np.repeat(q, 10, axis=1)

    p_head = np.empty((expand_q.shape[1], 21))

    for i in range(expand_q.shape[1]):
        index = np.nonzero(expand_q[:, i])
        for idx in index:
            data.ctrl[idx] = expand_q[idx, i]

        mujoco.mj_step(snake, data)

        step_data = np.hstack((data.body('head').xpos.copy(), get_robot_rot(data), data.ctrl))
        p_head[i] = step_data

    i = 300
    j = -30
    l = -0.01

    p_head_diff = np.diff(p_head[:,0:2],axis=0)
    p_head_diff_l2_norm = np.linalg.norm(p_head_diff,2,axis=1)

    l_traj = np.sum(p_head_diff_l2_norm)
    l_dist = np.linalg.norm(p_head[-1,0:2],2)

    i_term = i * l_dist
    j_term = j * (l_traj + 1)/(l_dist + 1)
    l_term = l * np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    # Position & Orientation
    ori_head = p_head[:,3:7]
    quat_p_head = Rotation.from_quat(ori_head[:, [1, 2, 3, 0]].copy())
    mean_rot = Rotation.mean(quat_p_head).as_rotvec()

    # Terminal orientation
    t_x = p_head[-1,0]
    t_y = p_head[-1,1]

    t_orientation = 0
    try:
        t_orientation = np.arctan2(t_y, t_x)
    except Exception as e:
        print(e)
        t_orientation = np.nan
    
    return np.hstack((i_term + j_term + l_term, mean_rot, t_orientation))

def orderize_linear(param_motion:np.ndarray, curve:bool, isSlit:bool, gamma:float, param_bar_iter:np.ndarray, shd_name:str, shd_shape) -> None:

    for i in param_bar_iter:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        U_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        idx1 = i[2] # psi start 0
        idx2 = i[3] - 1 # nu start 1

        amp_d, amp_l, psi, nu, delta = i

        if isSlit:
            lambda_bar = (amp_d, amp_l, psi, psi, (nu), (nu) * (1/2), delta, param_motion[-1])
        else:
            lambda_bar = (amp_d, amp_l, psi, psi, (nu), (nu), delta, param_motion[-1])


        U_map[idx1, idx2, :] = J_traj(param_motion, lambda_bar, curve, gamma)
        
def iterator_linear(motion:np.ndarray, curve:bool, gamma:float) -> None:
    motion_param = motion

    amp_d = np.array([motion_param[0]])
    amp_l = np.array([motion_param[1]])

    psi = np.arange(0,181)

    nu = np.arange(1,121)

    delta = np.array([motion_param[-2]])

    isSlit = False
    if motion_param[-3] == motion_param[-4]:
        isSlit = False
        print('Serp, Side or Roll gait...')
    else:
        isSlit = True
        print('Slithering gait...')

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

    pc1 = Process(target= orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[0]:start_idx[1]]),   shm.name, U_map.shape))
    pc2 = Process(target= orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[1]:start_idx[2]]),   shm.name, U_map.shape))
    pc3 = Process(target= orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[2]:start_idx[3]]),   shm.name, U_map.shape))
    pc4 = Process(target= orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[3]:start_idx[4]]),   shm.name, U_map.shape))
    pc5 = Process(target= orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[4]:start_idx[5]]),   shm.name, U_map.shape))
    pc6 = Process(target= orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[5]:start_idx[6]]),   shm.name, U_map.shape))
    pc7 = Process(target= orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[6]:start_idx[7]]),   shm.name, U_map.shape))
    pc8 = Process(target= orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[7]:start_idx[8]]),   shm.name, U_map.shape))
    pc9 = Process(target= orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[8]:start_idx[9]]),   shm.name, U_map.shape))
    pc10 = Process(target=orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[9]:start_idx[10]]),  shm.name, U_map.shape))
    pc11 = Process(target=orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[10]:start_idx[11]]), shm.name, U_map.shape))
    pc12 = Process(target=orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[11]:start_idx[12]]), shm.name, U_map.shape))
    pc13 = Process(target=orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[12]:start_idx[13]]), shm.name, U_map.shape))
    pc14 = Process(target=orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[13]:start_idx[14]]), shm.name, U_map.shape))
    pc15 = Process(target=orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[14]:start_idx[15]]), shm.name, U_map.shape))
    pc16 = Process(target=orderize_linear, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[15]::]),             shm.name, U_map.shape))

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

    data_dict = {'U_map': data[:,:,0], 'Rot_vec':data[:,:,1:4], 'Tf_orientation':data[:,:,4], 'Motion_lambda': motion_param, 'Curve':curve, 'Gamma':gamma}
    savemat("./U_traj_linear_"+str(curve)+"_"+str(gamma)+"_"+param2filename(motion_param)+f"_{len(combinations)}"+"_.mat", data_dict)
    
    shm.close()
    shm.unlink()

    print('done')

def iterator_fine(motion:np.ndarray, curve:bool, gamma:float) -> None:
    motion_param = motion

    amp_d = np.array([motion_param[0]])
    amp_l = np.array([motion_param[1]])

    psi = np.arange(-90,91)

    nu = np.arange(-60,61)

    delta = np.array([motion_param[-2]])

    isSlit = False
    if motion_param[-3] == motion_param[-4]:
        isSlit = False
        print('Serp, Side or Roll gait...')
    else:
        isSlit = True
        print('Slithering gait...')

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

    pc1 = Process(target= orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[0]:start_idx[1]]),   shm.name, U_map.shape))
    pc2 = Process(target= orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[1]:start_idx[2]]),   shm.name, U_map.shape))
    pc3 = Process(target= orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[2]:start_idx[3]]),   shm.name, U_map.shape))
    pc4 = Process(target= orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[3]:start_idx[4]]),   shm.name, U_map.shape))
    pc5 = Process(target= orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[4]:start_idx[5]]),   shm.name, U_map.shape))
    pc6 = Process(target= orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[5]:start_idx[6]]),   shm.name, U_map.shape))
    pc7 = Process(target= orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[6]:start_idx[7]]),   shm.name, U_map.shape))
    pc8 = Process(target= orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[7]:start_idx[8]]),   shm.name, U_map.shape))
    pc9 = Process(target= orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[8]:start_idx[9]]),   shm.name, U_map.shape))
    pc10 = Process(target=orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[9]:start_idx[10]]),  shm.name, U_map.shape))
    pc11 = Process(target=orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[10]:start_idx[11]]), shm.name, U_map.shape))
    pc12 = Process(target=orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[11]:start_idx[12]]), shm.name, U_map.shape))
    pc13 = Process(target=orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[12]:start_idx[13]]), shm.name, U_map.shape))
    pc14 = Process(target=orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[13]:start_idx[14]]), shm.name, U_map.shape))
    pc15 = Process(target=orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[14]:start_idx[15]]), shm.name, U_map.shape))
    pc16 = Process(target=orderize_fine, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[15]::]),             shm.name, U_map.shape))

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

    data_dict = {'U_map': data[:,:,0], 'Rot_vec':data[:,:,1:4], 'Tf_orientation':data[:,:,4], 'Motion_lambda': motion_param, 'Curve':curve, 'Gamma':gamma}
    savemat("./U_traj_fine_"+str(curve)+"_"+str(gamma)+"_"+param2filename(motion_param)+f"_{len(combinations)}"+"_.mat", data_dict)
    
    shm.close()
    shm.unlink()

    print('done')

def orderize_fine(param_motion:np.ndarray, curve:bool, isSlit:bool, gamma:float, param_bar_iter:np.ndarray, shd_name:str, shd_shape) -> None:

    for i in param_bar_iter:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        U_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        idx1 = i[2] + 90# psi start 0
        idx2 = i[3] + 60 # nu start 1

        amp_d, amp_l, psi, nu, delta = i

        psi = param_motion[2] + psi * (1/30)
        nu = param_motion[4] + nu * (1/6)

        if isSlit:
            lambda_bar = (amp_d, amp_l, psi, psi, (nu), (nu) * (1/2), delta, param_motion[-1])
        else:
            lambda_bar = (amp_d, amp_l, psi, psi, (nu), (nu), delta, param_motion[-1])


        U_map[idx1, idx2, :] = J_traj(param_motion, lambda_bar, curve, gamma)

if __name__ == "__main__":
    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)

    serpentine = (45, 45, 30, 30, 30, 30, 0, 0.05)
    serpentine_op = (45, 45, 158, 158, 115, 115, 0, 0.05)
    slithering = (45, 45, 30, 30, 60, 30, 0, 0.05)
    slithering_op = (45, 45, 32, 32, 116, 58, 0, 0.05)
    sidewinding = (45, 45, 30, 30, 30, 30, 45, 0.05)
    sidewinding_op = (45, 45, 159, 159, 85, 85, 45, 0.05)
    rolling = (15, 15, 0, 0, 30, 30, 90, 0.05)
    rolling_op = (15, 15, 169, 169, 119, 119, 90, 0.05)

    # print(J_view(sidewinding_op, (45, 45, 113, 113, 111, 111, 45, 0.05), False, 0.9)[0])
    # exit()

    #### Linear Searching...
    start_iter = time.time()
    # Curves
    # iterator_linear(serpentine_op, True, 0.7071)
    # iterator_linear(slithering_op, True, 0.7071)
    # iterator_linear(sidewinding_op,True, 0.7071)
    # iterator_linear(rolling,       True, 0.7071)

    # # Mats
    # iterator_linear(serpentine_op, False, 0.3)
    # iterator_linear(slithering_op, False, 0.3)
    # iterator_linear(sidewinding_op,False, 0.3)
    # iterator_linear(rolling_op,       False, 0.3)

    # iterator_linear(serpentine_op, False, 0.5)
    # iterator_linear(slithering_op, False, 0.5)
    # iterator_linear(sidewinding_op,False, 0.5)
    # iterator_linear(rolling_op,       False, 0.5)

    # iterator_linear(serpentine_op, False, 0.7071)
    # iterator_linear(slithering_op, False, 0.7071)
    # iterator_linear(sidewinding_op,False, 0.7071)
    # iterator_linear(rolling_op,       False, 0.7071)

    # iterator_linear(serpentine_op, False, 0.9)
    # iterator_linear(slithering_op, False, 0.9)
    # iterator_linear(sidewinding_op,False, 0.9)
    # iterator_linear(rolling_op,       False, 0.9)

    # Fines
    iterator_fine(serpentine_op, True, 0.3)
    iterator_fine(slithering_op, True, 0.3)
    iterator_fine(sidewinding_op,True, 0.3)
    iterator_fine(rolling_op,       True, 0.3)

    iterator_fine(serpentine_op, True, 0.5)
    iterator_fine(slithering_op, True, 0.5)
    iterator_fine(sidewinding_op,True, 0.5)
    iterator_fine(rolling_op,       True, 0.5)

    iterator_fine(serpentine_op, True, 0.7071)
    iterator_fine(slithering_op, True, 0.7071)
    iterator_fine(sidewinding_op,True, 0.7071)
    iterator_fine(rolling_op,       True, 0.7071)

    iterator_fine(serpentine_op, True, 0.9)
    iterator_fine(slithering_op, True, 0.9)
    iterator_fine(sidewinding_op,True, 0.9)
    iterator_fine(rolling_op,       True, 0.9)

    end_iter = time.time()
    print(f"Iterating dond... {end_iter-start_iter} seconds elapsed")

