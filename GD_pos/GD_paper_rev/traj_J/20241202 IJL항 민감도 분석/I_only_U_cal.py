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

def J_traj_each(parameters:np.ndarray, parameters_bar:np.ndarray, u_weight:np.ndarray, curve:bool, gamma:float) -> np.ndarray:
    """
    return : [U, avg. yaw]
    """
    w_i = u_weight[0]
    w_j = u_weight[1]
    w_l = u_weight[2]
    
    _robot_body_names = ["head","link1","link2","link3","link4","link5","link6","link7","link8","link9","link10","link11","link12","link13","tail"]

    def get_robot_rot(data)->np.ndarray:
        robot_quats = np.empty((0,4))
        for name in _robot_body_names:
            robot_quats = np.vstack((robot_quats, data.body(name).xquat.copy()))

        robot_quats = robot_quats[:, [1, 2, 3, 0]]
        robot_rot = Rotation(robot_quats)

        # com_roll, com_pitch, com_yaw = robot_rot.mean().as_rotvec(False)
        x, y, z, w = robot_rot.mean().as_quat()

        # return np.array([com_roll, com_pitch, com_yaw])
        return np.array([w, x, y, z])

    snake = mujoco.MjModel.from_xml_path("../resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)
    mujoco.mj_forward(snake, data)

    # M_name = param2filename(parameters)
    # Bar_name = param2filename(parameters_bar)

    # gait = serpenoid.Gait(tuple(parameters), tuple(parameters_bar))
    gait = serpenoid_gamma.Gait(tuple(parameters), tuple(parameters_bar), gamma)

    if curve:
        q = gait.CurveFunction
    else:
        q = gait.Gk

    expand_q = np.repeat(q, 10, axis=1)

    p_head = np.empty((expand_q.shape[1], 24)) # xpos, ypos, quat, ctrl, h_acc
    acc_head = np.empty((expand_q.shape[1], 3)) # For head acceleration
    acc_head_wo_g = np.empty((expand_q.shape[1], 3)) # For head acceleration without gravity

    for i in range(expand_q.shape[1]):
        index = np.nonzero(expand_q[:, i])
        for idx in index:
            data.ctrl[idx] = expand_q[idx, i]

        mujoco.mj_step(snake, data)

        step_data = np.hstack((data.body('head').xpos.copy(), get_robot_rot(data), data.ctrl, data.sensordata[-3::]))
        p_head[i] = step_data

        # Head acceleration without gravity
        tmp_qpos = data.qpos.copy()
        head_quat = Rotation.from_quat([tmp_qpos[4], tmp_qpos[5], tmp_qpos[6], tmp_qpos[3]])
        head_rotm = head_quat.as_matrix()

        rotated_g = np.dot(np.array([0, 0, 9.81]), head_rotm)

        g_elimated_acc = data.sensordata[-3::] - rotated_g
        acc_head[i,:] = g_elimated_acc

        g_elimated_acc = np.dot(g_elimated_acc, head_rotm.T)

        acc_head_wo_g[i,:] = g_elimated_acc


    p_head_diff = np.diff(p_head[:,0:2],axis=0)
    p_head_diff_l2_norm = np.linalg.norm(p_head_diff,2,axis=1)

    l_traj = np.sum(p_head_diff_l2_norm)
    l_dist = np.linalg.norm(p_head[-1,0:2],2)

    i_term = l_dist
    j_term = (l_traj + 1)/(l_dist + 1)
    l_term = np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1)) # -> 원래 코드 인데, 수정하려함.

    # Position & Orientation
    ori_head = p_head[:,3:7]
    quat_p_head = Rotation.from_quat(ori_head[:, [1, 2, 3, 0]].copy())
    mean_rot = Rotation.mean(quat_p_head).as_euler('ZYX',True).copy()
    l_term = np.linalg.norm(mean_rot,2)

    # Terminal orientation
    t_x = p_head[-1,0]
    t_y = p_head[-1,1]

    # Head acceleration each axis
    h_acc_x, h_acc_y, h_acc_z = np.mean(acc_head, axis=0)

    # Head acceleration without gravity
    h_acc_wo_gravity_x,  h_acc_wo_gravity_y,  h_acc_wo_gravity_z = np.mean(acc_head_wo_g, axis=0)
    # print(f"h_acc_wo_gravity_x : {h_acc_wo_gravity_x}, h_acc_wo_gravity_y : {h_acc_wo_gravity_y}, h_acc_wo_gravity_z : {h_acc_wo_gravity_z}")

    t_orientation = 0
    try:
        t_orientation = np.arctan2(t_y, t_x)
    except Exception as e:
        print(e)
        t_orientation = np.nan
    
    return np.hstack((i_term, j_term, l_term, mean_rot, t_orientation, h_acc_wo_gravity_x, h_acc_wo_gravity_y, h_acc_wo_gravity_z, h_acc_x, h_acc_y, h_acc_z))

def for_iter(lambda_m, u_w, shd_name:str, shd_shape):
    lambda_m = [45, 45, 32, 32, 116, 58, 0, 0.05]
    lambda_c = [45, 45, 32, 32, 116, 58, 0, 0.05] # Bar 파라미터가 곡선함수 파라미터임. 따라서 이거를 최적화해야함.
    gamma = 0.7071
    exist_shm = shared_memory.SharedMemory(name=shd_name)
    U_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)
    for i in u_w:
        # [1.5 1 -0.2]
        new_u_w = [(i[0]/10), 1, -0.2]
        def cal_U(lambda_c:np.ndarray):
            result = J_traj_each(lambda_m, lambda_c, new_u_w, False, gamma)

            return -1 * (new_u_w[0] * result[0] + new_u_w[1] * result[1] + new_u_w[2] * result[2])
        result = minimize(cal_U, lambda_m, method='Nelder-Mead')

        if result.success:
            J_value = -1 * result.fun
        else:
            J_value = np.nan

        # result = cal_U(lambda_m) # -> 디버깅용
        # U_map[int(i[0])] = result

        x_fcn = J_traj_each(lambda_m, result.x, new_u_w, False, gamma)

        U_map[int(i[0]),0] = J_value
        U_map[int(i[0]),1] = x_fcn[0]
        U_map[int(i[0]),2] = x_fcn[1]
        U_map[int(i[0]),3] = x_fcn[2]

    return 0

if __name__ == "__main__":
    data_size = 101
    iter_weight = np.arange(0,data_size)
    lambda_m = [45, 45, 32, 32, 116, 58, 0, 0.05]
    lambda_c = [45, 45, 32, 32, 116, 58, 0, 0.05] # Bar 파라미터가 곡선함수 파라미터임. 따라서 이거를 최적화해야함.
    gamma = 0.7071

    # U_map = np.empty(data_size, dtype=np.float64)
    U_map = np.empty((data_size,4), dtype=np.float64)
    shm = shared_memory.SharedMemory(name="shared_U_map", create=True, size=U_map.nbytes)
    data = np.ndarray(U_map.shape, dtype=U_map.dtype, buffer=shm.buf)
    data[:] = 0  # 초기화

    combinations = list(itertools.product(iter_weight))
    print(f'Number of Combinations : {len(combinations)}')

    ea = len(combinations) // 16
    start_idx = [0, 1 * ea, 2 * ea, 3 * ea, 4 * ea, 5 * ea, 6 * ea, 7 * ea, 8 * ea , 9 * ea, 10 * ea, 11 * ea, 12 * ea, 13 * ea, 14 * ea, 15 * ea] 

    print(f'For 16 processes start indices : {start_idx}')

    pc1 =  Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[0]:start_idx[1]]),   shm.name, U_map.shape))
    pc2 =  Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[1]:start_idx[2]]),   shm.name, U_map.shape))
    pc3 =  Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[2]:start_idx[3]]),   shm.name, U_map.shape))
    pc4 =  Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[3]:start_idx[4]]),   shm.name, U_map.shape))
    pc5 =  Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[4]:start_idx[5]]),   shm.name, U_map.shape))
    pc6 =  Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[5]:start_idx[6]]),   shm.name, U_map.shape))
    pc7 =  Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[6]:start_idx[7]]),   shm.name, U_map.shape))
    pc8 =  Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[7]:start_idx[8]]),   shm.name, U_map.shape))
    pc9 =  Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[8]:start_idx[9]]),   shm.name, U_map.shape))
    pc10 = Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[9]:start_idx[10]]),  shm.name, U_map.shape))
    pc11 = Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[10]:start_idx[11]]), shm.name, U_map.shape))
    pc12 = Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[11]:start_idx[12]]), shm.name, U_map.shape))
    pc13 = Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[12]:start_idx[13]]), shm.name, U_map.shape))
    pc14 = Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[13]:start_idx[14]]), shm.name, U_map.shape))
    pc15 = Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[14]:start_idx[15]]), shm.name, U_map.shape))
    pc16 = Process(target= for_iter, args=(lambda_m, list(combinations[start_idx[15]::]),             shm.name, U_map.shape))

    import datetime

    start_time = datetime.datetime.now()

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

    end_time = datetime.datetime.now()
    print(f'Elapsed Time : {end_time - start_time}')

    data_dict = {'U_result': data[:,0], 'I_term':data[:,1], 'J_term':data[:,2], 'L_term':data[:,3]}
    savemat("slithering_I_vary2"+"_.mat", data_dict)

    shm.close()
    shm.unlink()