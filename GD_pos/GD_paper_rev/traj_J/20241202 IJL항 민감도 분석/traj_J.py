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

def J_log(parameters:np.ndarray, parameters_bar:np.ndarray, curve:bool, gamma:float) -> np.ndarray:

    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)
    renderer = mujoco.Renderer(snake, 720, 1280)
    frames = []

    mujoco.mj_forward(snake, data)

    M_name = param2filename(parameters)
    Bar_name = param2filename(parameters_bar)

    gait = serpenoid_gamma.Gait(tuple(parameters), tuple(parameters_bar), gamma)

    if curve:
        q = gait.CurveFunction
    else:
        q = gait.Gk

    expand_q = np.repeat(q, 10, axis=1)

    for i in range(expand_q.shape[1]):
        time_step = time.time()
        index = np.nonzero(expand_q[:, i])
        for idx in index:
            data.ctrl[idx] = expand_q[idx, i]

        mujoco.mj_step(snake, data)
        renderer.update_scene(data)
        pixel = renderer.render()

        frames.append(pixel)

    media.write_video(Bar_name+str(gamma)+'_.mp4',frames, fps=200)
            
    return 0

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


    ctrl_log = np.empty((0,14))
    p_head_log = np.empty((0,2))
    qpos_log = np.empty((0,21))
    head_acc_log = np.empty((0,3))
    head_acc_wo_gravity_log = np.empty((0,3))
    head_gyro_log = np.empty((0,3))
    head_ang_acc_from_gyro = np.empty((0,3))
    head_acc_only_log = np.empty((0,3))
    with mujoco.viewer.launch_passive(snake, data) as viewer:
        input("Press Enter to continue...")
        for i in range(expand_q.shape[1]):
            time_step = time.time()
            index = np.nonzero(expand_q[:, i])
            for idx in index:
                data.ctrl[idx] = expand_q[idx, i]
                ctrl_log = np.vstack((ctrl_log, data.ctrl))

            mujoco.mj_step(snake, data)
            viewer.sync()

            while snake.opt.timestep - (time.time() - time_step) > 0:
                    time.sleep(0)

            step_data = np.hstack((data.body('head').xpos.copy(), get_robot_rot(data), data.ctrl))
            p_head[i] = step_data
            p_head_log = np.vstack((p_head_log, step_data[0:2]))
            qpos_log = np.vstack((qpos_log, data.qpos.copy()))
            head_acc_log = np.vstack((head_acc_log, data.sensordata[-3::]))
            head_gyro_log = np.vstack((head_gyro_log, data.sensordata[-6:-3]))

            temp_acc_from_gyro = np.zeros(3)
            if head_gyro_log.shape[0] == 1:
                pass
            else:
                temp_acc_from_gyro = (data.sensordata[-6:-3] - head_gyro_log[i-1]) / snake.opt.timestep

            head_ang_acc_from_gyro = np.vstack((head_ang_acc_from_gyro, temp_acc_from_gyro))

            # head_quat = Rotation.from_quat([data.body('head').xquat[1], data.body('head').xquat[2], data.body('head').xquat[3], data.body('head').xquat[0]])
            head_quat = Rotation.from_quat([data.qpos.copy()[4], data.qpos.copy()[5], data.qpos.copy()[6], data.qpos.copy()[3]])
            # head_quat = Rotation.from_matrix(data.site('s_head').xmat.copy().reshape(3,3))

            head_rotm = head_quat.as_matrix()

            rotated_g = np.dot(np.array([0, 0, 9.81]), head_rotm)
            g_elimated_acc = data.sensordata[-3::] - rotated_g
            g_elimated_acc = np.dot(g_elimated_acc, head_rotm.T)
            g_ang_elimated_acc = g_elimated_acc - temp_acc_from_gyro

            head_acc_wo_gravity_log = np.vstack((head_acc_wo_gravity_log, g_elimated_acc))
            head_acc_only_log = np.vstack((head_acc_only_log, g_ang_elimated_acc))

    # print(np.mean(head_acc_wo_gravity_log, axis=0))

    ### 예전 방식의 U 계산
    i = 300
    j = -30
    l = -0.05

    p_head_diff = np.diff(p_head[:,0:2],axis=0)
    p_head_diff_l2_norm = np.linalg.norm(p_head_diff,2,axis=1)

    l_traj = np.sum(p_head_diff_l2_norm)
    l_dist = np.linalg.norm(p_head[-1,0:2],2)

    i_term = i * l_dist
    j_term = j * (l_traj + 1)/(l_dist + 1)
    l_term = l * np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    # print(f"l_dist : {l_dist}, j_term : {((l_traj + 1) / (l_dist + 1))}, l_term :{(np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1)))}")
    #######

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

    # if parameters[-2] > 38:
    #     t_orientation = np.abs(t_orientation)  - (np.pi / 2)

    rot = -30 * np.abs(mean_rot[2])
    tf = -60 * np.abs(t_orientation)

    h_acc_norm = np.linalg.norm(head_acc_log, 2, axis=1)
    # print(np.mean(head_acc_log[:,0]))
    # print(np.mean(head_acc_log[:,1]))
    # print(np.mean(head_acc_log[:,2]))
    # print(np.mean(h_acc_norm))

    ### ACC 기반 U 계산
    if parameters_bar[-2] > 38:
        forward_dist = l_dist * np.sin(t_orientation)
        forward_acc = np.mean(head_acc_wo_gravity_log, axis=0)[1]
    else:
        forward_dist = l_dist * np.cos(t_orientation)
        forward_acc = np.mean(head_acc_wo_gravity_log, axis=0)[0]

    ctrl_log = {'ctrl_log':ctrl_log, 'p_head_log':p_head_log, 'qpos_log':qpos_log, 'head_acc_log':head_acc_log, 'head_acc_wo_gravity_log':head_acc_wo_gravity_log, 'head_gyro_log':head_gyro_log, 'head_ang_acc_from_gyro':head_ang_acc_from_gyro, 'head_acc_only_log':head_acc_only_log}
    savemat("./ctrl_log_"+str(gamma)+"_"+M_name+"_"+Bar_name+".mat", ctrl_log)

    # return np.hstack((i_term + j_term + l_term, mean_rot, t_orientation))
    # return i_term + j_term + l_term + rot + tf
    return forward_acc + (1.5 * forward_dist) - (0.2 * np.linalg.norm(mean_rot, 2))

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

def J_traj_acc(parameters:np.ndarray, parameters_bar:np.ndarray, curve:bool, gamma:float) -> np.ndarray:
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


    ctrl_log = np.empty((0,14))
    p_head_log = np.empty((0,2))
    qpos_log = np.empty((0,21))
    head_acc_log = np.empty((0,3))
    head_acc_wo_gravity_log = np.empty((0,3))
    head_gyro_log = np.empty((0,3))
    head_ang_acc_from_gyro = np.empty((0,3))
    head_acc_only_log = np.empty((0,3))

    for i in range(expand_q.shape[1]):
        index = np.nonzero(expand_q[:, i])
        for idx in index:
            data.ctrl[idx] = expand_q[idx, i]
            ctrl_log = np.vstack((ctrl_log, data.ctrl))

        mujoco.mj_step(snake, data)

        step_data = np.hstack((data.body('head').xpos.copy(), get_robot_rot(data), data.ctrl))
        p_head[i] = step_data
        p_head_log = np.vstack((p_head_log, step_data[0:2]))
        qpos_log = np.vstack((qpos_log, data.qpos.copy()))
        head_acc_log = np.vstack((head_acc_log, data.sensordata[-3::]))
        head_gyro_log = np.vstack((head_gyro_log, data.sensordata[-6:-3]))

        temp_acc_from_gyro = np.zeros(3)
        if head_gyro_log.shape[0] == 1:
            pass
        else:
            temp_acc_from_gyro = (data.sensordata[-6:-3] - head_gyro_log[i-1]) / snake.opt.timestep

        head_ang_acc_from_gyro = np.vstack((head_ang_acc_from_gyro, temp_acc_from_gyro))

        # head_quat = Rotation.from_quat([data.body('head').xquat[1], data.body('head').xquat[2], data.body('head').xquat[3], data.body('head').xquat[0]])
        head_quat = Rotation.from_quat([data.qpos.copy()[4], data.qpos.copy()[5], data.qpos.copy()[6], data.qpos.copy()[3]])
        # head_quat = Rotation.from_matrix(data.site('s_head').xmat.copy().reshape(3,3))

        head_rotm = head_quat.as_matrix()

        rotated_g = np.dot(np.array([0, 0, 9.81]), head_rotm)
        g_elimated_acc = data.sensordata[-3::] - rotated_g
        g_elimated_acc = np.dot(g_elimated_acc, head_rotm.T)
        g_ang_elimated_acc = g_elimated_acc - temp_acc_from_gyro

        head_acc_wo_gravity_log = np.vstack((head_acc_wo_gravity_log, g_elimated_acc))
        head_acc_only_log = np.vstack((head_acc_only_log, g_ang_elimated_acc))

    # print(np.mean(head_acc_wo_gravity_log, axis=0))

    ### 예전 방식의 U 계산
    i = 300
    j = -30
    l = -0.05

    p_head_diff = np.diff(p_head[:,0:2],axis=0)
    p_head_diff_l2_norm = np.linalg.norm(p_head_diff,2,axis=1)

    l_traj = np.sum(p_head_diff_l2_norm)
    l_dist = np.linalg.norm(p_head[-1,0:2],2)

    i_term = i * l_dist
    j_term = j * (l_traj + 1)/(l_dist + 1)
    l_term = l * np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    # print(f"l_dist : {l_dist}, j_term : {((l_traj + 1) / (l_dist + 1))}, l_term :{(np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1)))}")
    #######

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

    # if parameters[-2] > 38:
    #     t_orientation = np.abs(t_orientation)  - (np.pi / 2)

    rot = -30 * np.abs(mean_rot[2])
    tf = -60 * np.abs(t_orientation)

    h_acc_norm = np.linalg.norm(head_acc_log, 2, axis=1)
    # print(np.mean(head_acc_log[:,0]))
    # print(np.mean(head_acc_log[:,1]))
    # print(np.mean(head_acc_log[:,2]))
    # print(np.mean(h_acc_norm))

    ### ACC 기반 U 계산
    if parameters_bar[-2] > 38:
        forward_dist = l_dist * np.sin(t_orientation)
        forward_acc = np.mean(head_acc_wo_gravity_log, axis=0)[1]
    else:
        forward_dist = l_dist * np.cos(t_orientation)
        forward_acc = np.mean(head_acc_wo_gravity_log, axis=0)[0]

    ctrl_log = {'ctrl_log':ctrl_log, 'p_head_log':p_head_log, 'qpos_log':qpos_log, 'head_acc_log':head_acc_log, 'head_acc_wo_gravity_log':head_acc_wo_gravity_log, 'head_gyro_log':head_gyro_log, 'head_ang_acc_from_gyro':head_ang_acc_from_gyro, 'head_acc_only_log':head_acc_only_log}
    # savemat("./ctrl_log_"+str(gamma)+"_"+M_name+"_"+Bar_name+".mat", ctrl_log)

    # return np.hstack((i_term + j_term + l_term, mean_rot, t_orientation))
    # return i_term + j_term + l_term + rot + tf
    return forward_acc + (1.5 * forward_dist) - (0.2 * np.linalg.norm(mean_rot, 2))

def J_traj_each(parameters:np.ndarray, parameters_bar:np.ndarray, curve:bool, gamma:float) -> np.ndarray:
    """
    return : [U, avg. yaw]
    """
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

    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
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
    l_term = np.sum(np.sum(np.abs(p_head[:,7:21]),axis=1))

    # Position & Orientation
    ori_head = p_head[:,3:7]
    quat_p_head = Rotation.from_quat(ori_head[:, [1, 2, 3, 0]].copy())
    mean_rot = Rotation.mean(quat_p_head).as_rotvec()

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


        U_map[idx1, idx2, :] = J_traj_each(param_motion, lambda_bar, curve, gamma)

def orderize_linear_amp(param_motion:np.ndarray, curve:bool, isSlit:bool, gamma:float, param_bar_iter:np.ndarray, shd_name:str, shd_shape) -> None:

    for i in param_bar_iter:
        exist_shm = shared_memory.SharedMemory(name=shd_name)
        U_map = np.ndarray(shd_shape, dtype=np.float64, buffer=exist_shm.buf)

        idx1 = i[0] - 1 # psi start 0
        idx2 = i[1] - 1 # nu start 1

        amp_d, amp_l, psi_d, psi_l, nu_d, nu_l, delta = i

        if isSlit:
            lambda_bar = (amp_d, amp_l, psi_d, psi_l, nu_d, nu_l, delta, param_motion[-1])
        else:
            lambda_bar = (amp_d, amp_l, psi_d, psi_l, nu_d, nu_l, delta, param_motion[-1])

        U_map[idx1, idx2, :] = J_traj_each(param_motion, lambda_bar, curve, gamma)

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

    U_map = np.empty((n1,n2,13), dtype=np.float64)
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

    data_dict = {'U_map': data[:,:,0:3], 'Rot_vec':data[:,:,3:6], 'Tf_orientation':data[:,:,6], 'head_acc_wo_g':data[:,:,7:10], 'head_acc':data[:,:,10:13], 'Motion_lambda': motion_param, 'Curve':curve, 'Gamma':gamma}
    # data_dict = {'U_dist' : data[:,:,0],
    #              'U_traj' : data[:,:,1],
    #              'U_ctrl' : data[:,:,2],
    #              'Rot_vec': data[:,:,3:6],
    #              'Tf_orientation': data[:,:,6],
    #              'head_acc': data[:,:,7]
    #     ,'Motion_lambda': motion_param, 
    #     'Curve':curve, 'Gamma':gamma}

    savemat("./U_traj_linear_each_acc_g_"+str(curve)+"_"+str(gamma)+"_"+param2filename(motion_param)+f"_{len(combinations)}"+"_.mat", data_dict)
    
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

def iterator_linear_amp(motion:np.ndarray, curve:bool, gamma:float) -> None:
    motion_param = motion

    amp_d = np.arange(1,75)
    amp_l = np.arange(1,75)

    psi_d = np.array([motion_param[1]])
    psi_l = np.array([motion_param[2]])

    nu_d = np.array([motion_param[3]])
    nu_l = np.array([motion_param[4]])

    delta = np.array([motion_param[-2]])

    isSlit = False
    if motion_param[-3] == motion_param[-4]:
        isSlit = False
        print('Serp, Side or Roll gait...')
    else:
        isSlit = True
        print('Slithering gait...')

    n1 = len(amp_d)
    n2 = len(amp_l)

    U_map = np.empty((n1,n2,8), dtype=np.float64)
    shm = shared_memory.SharedMemory(name="shared_U_map", create=True, size=U_map.nbytes)
    data = np.ndarray(U_map.shape, dtype=U_map.dtype, buffer=shm.buf)

    combinations = list(itertools.product(amp_d, amp_l, psi_d, psi_l, nu_d, nu_l, delta))
    print(f'Number of Combinations : {len(combinations)}')

    ea = len(combinations) // 16
    start_idx = [0, 1 * ea, 2 * ea, 3 * ea, 4 * ea, 5 * ea, 6 * ea, 7 * ea, 8 * ea , 9 * ea, 10 * ea, 11 * ea, 12 * ea, 13 * ea, 14 * ea, 15 * ea] 

    print(f'For 16 processes start indices : {start_idx}')

    pc1 = Process(target= orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[0]:start_idx[1]]),   shm.name, U_map.shape))
    pc2 = Process(target= orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[1]:start_idx[2]]),   shm.name, U_map.shape))
    pc3 = Process(target= orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[2]:start_idx[3]]),   shm.name, U_map.shape))
    pc4 = Process(target= orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[3]:start_idx[4]]),   shm.name, U_map.shape))
    pc5 = Process(target= orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[4]:start_idx[5]]),   shm.name, U_map.shape))
    pc6 = Process(target= orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[5]:start_idx[6]]),   shm.name, U_map.shape))
    pc7 = Process(target= orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[6]:start_idx[7]]),   shm.name, U_map.shape))
    pc8 = Process(target= orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[7]:start_idx[8]]),   shm.name, U_map.shape))
    pc9 = Process(target= orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[8]:start_idx[9]]),   shm.name, U_map.shape))
    pc10 = Process(target=orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[9]:start_idx[10]]),  shm.name, U_map.shape))
    pc11 = Process(target=orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[10]:start_idx[11]]), shm.name, U_map.shape))
    pc12 = Process(target=orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[11]:start_idx[12]]), shm.name, U_map.shape))
    pc13 = Process(target=orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[12]:start_idx[13]]), shm.name, U_map.shape))
    pc14 = Process(target=orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[13]:start_idx[14]]), shm.name, U_map.shape))
    pc15 = Process(target=orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[14]:start_idx[15]]), shm.name, U_map.shape))
    pc16 = Process(target=orderize_linear_amp, args=(np.array(motion_param), curve, isSlit, gamma, list(combinations[start_idx[15]::]),             shm.name, U_map.shape))

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

    data_dict = {'U_map': data[:,:,0:3], 'Rot_vec':data[:,:,3:6], 'Tf_orientation':data[:,:,6], 'head_acc':data[:,:,7],'Motion_lambda': motion_param, 'Curve':curve, 'Gamma':gamma}
    # data_dict = {'U_dist' : data[:,:,0],
    #              'U_traj' : data[:,:,1],
    #              'U_ctrl' : data[:,:,2],
    #              'Rot_vec': data[:,:,3:6],
    #              'Tf_orientation': data[:,:,6],
    #              'head_acc': data[:,:,7]
    #     ,'Motion_lambda': motion_param, 
    #     'Curve':curve, 'Gamma':gamma}

    savemat("./U_amp_"+str(curve)+"_"+str(gamma)+"_"+param2filename(motion_param)+f"_{len(combinations)}"+"_.mat", data_dict)
    
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

def finetuning(param_motion:np.ndarray, gamma:float)->None:
    def scalar_J_traj(param_motion:np.ndarray, param_bar:np.ndarray, curve:bool, gamma:float) -> np.ndarray:
        return J_traj_acc(param_motion, param_bar, curve, gamma)
    
    def J_minimize(x0:np.ndarray):
        lambda_bar = np.hstack((x0, param_motion[-1]))
        result = -1 * scalar_J_traj(param_motion, lambda_bar, False, gamma)
        return result
    # 최적 파라미터 실험
    lower_bound = scalar_J_traj(param_motion, param_motion, True, gamma)

    print(f"Lower Bound : {lower_bound}")
    print(f"Gamma : {gamma}")

    x0 = param_motion[0:-1]
    bound_coeff = [3, 3, 6, 6, 7, 7, 5]
    min_param = np.subtract(x0, bound_coeff)
    max_param = np.add(x0, bound_coeff)
    bounds = ((min_param[0], max_param[0]), (min_param[1], max_param[1]), (min_param[2], max_param[2]), (min_param[3], max_param[3]), (min_param[4], max_param[4]), (min_param[5], max_param[5]), (min_param[6], max_param[6]))

    result = minimize(J_minimize, x0, method='Nelder-Mead', bounds=bounds, options={'disp':True,'maxfev':2400})

    print(result)

def finetuning_each(param_motion:np.ndarray, gamma:float)->None:
    def scalar_J_traj(param_motion:np.ndarray, param_bar:np.ndarray, curve:bool, gamma:float) -> np.ndarray:
        i = 300
        j = -30
        l = -0.05
        rot = -30
        tf = -60

        # i_term, j_term, l_term, rot_term, tf_term = J_traj_each(param_motion, param_bar, curve, gamma)
        each = J_traj_each(param_motion, param_bar, curve, gamma)

        if param_motion[-2] > 38:
            each[-1] = np.abs(each[-1]) - (np.pi / 2)

        return i * each[0] + j * each[1] + l * each[2] + rot * np.abs(each[-2]) + tf * np.abs(each[-1])
    
    def J_minimize(x0:np.ndarray):
        lambda_bar = np.hstack((x0, param_motion[-1]))

        result = -1 * scalar_J_traj(param_motion, lambda_bar, False, gamma)
        return result
    # 최적 파라미터 실험
    lower_bound = scalar_J_traj(param_motion, param_motion, True, gamma)

    print(f"Lower Bound : {lower_bound}")
    print(f"Gamma : {gamma}")

    x0 = param_motion[0:-1]
    bound_coeff = [3, 3, 6, 6, 7, 7, 5]
    min_param = np.subtract(x0, bound_coeff)
    max_param = np.add(x0, bound_coeff)
    bounds = ((min_param[0], max_param[0]), (min_param[1], max_param[1]), (min_param[2], max_param[2]), (min_param[3], max_param[3]), (min_param[4], max_param[4]), (min_param[5], max_param[5]), (min_param[6], max_param[6]))

    result = minimize(J_minimize, x0, method='Nelder-Mead', bounds=bounds, options={'disp':True,'maxfev':5000, 'xatol':5e-1, 'fatol':50})

    print(f'Optimal Parameters : {result.x}')
    print(result)

if __name__ == "__main__":
    snake = mujoco.MjModel.from_xml_path("../resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)

    serpentine = (45, 45, 30, 30, 30, 30, 0, 0.05)
    # serpentine_op = (45, 45, 158, 158, 115, 115, 0, 0.05) #너무 빨라서 취소 이걸로 최적화하면 sidewinding됨
    serpentine_op = (45, 45, 154, 154, 55, 55, 0, 0.05) 
    slithering = (45, 45, 30, 30, 60, 30, 0, 0.05)
    slithering_op = (45, 45, 32, 32, 116, 58, 0, 0.05)
    sidewinding = (45, 45, 30, 30, 30, 30, 45, 0.05)
    sidewinding_op = (45, 45, 159, 159, 85, 85, 45, 0.05)
    rolling = (15, 15, 0, 0, 30, 30, 90, 0.05)
    rolling_op = (15, 15, 169, 169, 119, 119, 90, 0.05)

    # Optimal with acceleration values
    ac_roll_op = (15, 15, 171, 171, 118, 118, 90, 0.05)
    # ac_side_op_bad = (45, 45, 158, 158, 62, 62, 45, 0.05)
    ac_side_op = (45, 45, 26, 26, 59, 59, 45, 0.05)
    ac_slit_op = (45, 45, 32, 32, 117, 117/2, 0, 0.05)
    ac_serp_op = (45, 45, 162, 162, 84, 84, 0, 0.05)

    # GD Scipy Finetuning
    serpcurve_op = (4.508e+01,  4.509e+01,  1.540e+02,  1.600e+02,  5.512e+01,  5.508e+01,  -7.749e-05,  0.05)

    slitcurve_op = (4.526e+01,  4.526e+01,  3.195e+01,  3.318e+01,  1.160e+02,  5.801e+01,  1.173e-05,  0.05) #-325.95
    slit03_op = (4.57874610e+01, 4.47749476e+01, 3.19154641e+01, 3.29436457e+01, 1.16131232e+02, 5.79724657e+01, 2.49956662e-05,  0.05) #
    slit05_op = (4.520e+01,  4.566e+01,  3.346e+01,  3.130e+01,  1.162e+02, 5.721e+01,  4.014e-05,  0.05) #
    slit07_op = (4.538e+01,  4.664e+01,  3.252e+01,  3.115e+01,  1.179e+02, 5.738e+01, -7.195e-07,  0.05) #
    slit09_op = (4.59704920e+01, 4.52503234e+01, 3.23554338e+01, 3.18049948e+01, 1.16461515e+02, 5.74362020e+01, 4.90678713e-05,  0.05) #

    sidecurve_op = (4.639e+01,  4.532e+01,  1.594e+02,  1.593e+02,  8.493e+01,  8.498e+01,  4.522e+01,  0.05) #2455.46
    side03_op = (46.42750657,  45.55030688, 158.67435609, 159.05461942,  85.22372179,  85.10662228,  44.91307382,  0.05) #1809.522
    side05_op = (45.67394843,  44.99912165, 160.03427455, 159.63206874,  85.43994966,  85.37658725,  45.86496331,  0.05) #1714.17
    side07_op = (4.539e+01,  4.539e+01,  1.630e+02,  1.594e+02,  8.578e+01,  8.500e+01,  4.539e+01,  0.05) #1487.80
    side09_op = (4.307e+01,  4.617e+01,  1.616e+02,  1.622e+02,  8.739e+01,  8.705e+01,  4.445e+01,  0.05) #1146.74

    rollcurve_op2 = (1.508e+01,  1.507e+01,  1.692e+02,  1.697e+02,  1.191e+02,  1.187e+02,  9.240e+01, 0.05) #606.61 바운더리 준 값
    roll03_op =(1.495e+01,  1.517e+01,  1.694e+02,  1.688e+02,  1.192e+02,  1.189e+02,  9.247e+01, 0.05) #705.76
    roll05_op =(1.502e+01,  1.506e+01,  1.715e+02,  1.682e+02,  1.189e+02,  1.187e+02,  9.305e+01, 0.05) #784.05
    roll07_op =(14.87815899,  14.90831926, 171.33492883, 174.94054222, 119.32329542,  118.04336397,  88.83467804, 0.05) #807.28
    roll09_op =(15.15487732,  15.23185306, 169.75254068, 167.53307839, 122.03266542, 117.04890007,  91.17241511, 0.05) #485.12

    slit_03_gpg = (4.530e+01,  4.506e+01,  3.205e+01,  3.197e+01,  1.170e+02,  5.852e+01,  9.103e-06,  0.05)
    slit_05_gpg = (4.483e+01,  4.522e+01,  3.197e+01,  3.214e+01,  1.173e+02,  6.145e+01, -9.759e-07,  0.05)
    slit_07_gpg = (4.416e+01,  4.571e+01,  3.282e+01,  3.217e+01,  1.172e+02,  5.905e+01,  4.471e-05,  0.05)
    slit_09_gpg = (4.473e+01,  4.507e+01,  3.335e+01,  3.065e+01,  1.219e+02,  5.956e+01,  1.284e-05,  0.05)

    side_03_gpg = (4.593e+01,  4.590e+01,  2.601e+01,  2.584e+01,  5.874e+01,  5.892e+01,  4.541e+01,  0.05)
    side_05_gpg = (4.612e+01,  4.324e+01,  2.584e+01,  2.643e+01,  5.968e+01,  5.929e+01,  4.618e+01,  0.05)
    side_07_gpg = (4.420e+01,  4.613e+01,  2.623e+01,  2.648e+01,  6.003e+01,  5.965e+01,  4.511e+01,  0.05)
    side_09_gpg = (4.462e+01,  4.419e+01,  2.732e+01,  2.619e+01,  6.053e+01,  5.890e+01,  4.484e+01,  0.05)

    roll_03_gpg = (1.491e+01,  1.508e+01,  1.710e+02,  1.720e+02,  1.186e+02,  1.175e+02,  9.038e+01,  0.05)
    roll_05_gpg = (1.504e+01,  1.505e+01,  1.719e+02,  1.712e+02,  1.177e+02,  1.184e+02,  8.987e+01,  0.05)
    roll_07_gpg = (1.499e+01,  1.496e+01,  1.745e+02,  1.715e+02,  1.183e+02,  1.183e+02,  9.003e+01,  0.05)
    roll_09_gpg = (1.473e+01,  1.524e+01,  1.724e+02,  1.723e+02,  1.194e+02,  1.187e+02,  8.968e+01,  0.05)
    # roll09_op =(1.564e+1,  1.516e+1, 1.736e+2, 1.669e+2, 1.231e+2, 1.134e+2,  9.340e+1, 0.05) #485.12

    # finetuning_each(rolling_op, 0.3)
    # finetuning_each(rolling_op, 0.5)
    # finetuning_each(rolling_op, 0.7071)
    # finetuning_each(rolling_op, 0.9)

    # print(J_view(slithering_op,(4.563e+1, 4.545e+1, 3.255e+1, 3.086e1, 1.180e+2, 5.718e+1, 1.317e-4, 0.05),False,0.7071)[0])


    # print(J_view(ac_slit_op,[4.530e+01,  4.506e+01,  3.205e+01,  3.197e+01,  1.170e+02,   5.852e+01,  9.103e-06, 0.05], False,0.3))
    # print(J_view(ac_slit_op,[4.483e+01,  4.522e+01,  3.197e+01,  3.214e+01,  1.173e+02,  6.145e+01, -9.759e-07, 0.05], False,0.5))
    # print(J_view(ac_slit_op,[4.416e+01,  4.571e+01,  3.282e+01,  3.217e+01,  1.172e+02,   5.905e+01,  4.471e-05, 0.05], False,0.7071))
    # print(J_view(ac_slit_op,[4.473e+01,  4.507e+01,  3.335e+01,  3.065e+01,  1.219e+02,   5.956e+01,  1.284e-05, 0.05], False,0.9))

    # print(J_view(ac_side_op,[4.593e+01,  4.590e+01,  2.601e+01,  2.584e+01,  5.874e+01,  5.892e+01,  4.541e+01, 0.05], False,0.3))
    # print(J_view(ac_side_op,[4.612e+01,  4.324e+01,  2.584e+01,  2.643e+01,  5.968e+01,  5.929e+01,  4.618e+01, 0.05], False,0.5))
    # print(J_view(ac_side_op,[4.420e+01,  4.613e+01,  2.623e+01,  2.648e+01,  6.003e+01,  5.965e+01,  4.511e+01, 0.05], False,0.7071))
    # print(J_view(ac_side_op,[4.462e+01,  4.419e+01,  2.732e+01,  2.619e+01,  6.053e+01,  5.890e+01,  4.484e+01, 0.05], False,0.9))
    
    # print(J_view(ac_roll_op,[1.491e+01,  1.508e+01,  1.710e+02,  1.720e+02,  1.186e+02,   1.175e+02,  9.038e+01, 0.05], False,0.3))
    # print(J_view(ac_roll_op,[1.504e+01,  1.505e+01,  1.719e+02,  1.712e+02,  1.177e+02,   1.184e+02,  8.987e+01, 0.05], False,0.5))
    # print(J_view(ac_roll_op,[1.499e+01,  1.496e+01,  1.745e+02,  1.715e+02,  1.183e+02,  1.183e+02,  9.003e+01, 0.05], False,0.7071))
    # print(J_view(ac_roll_op,[1.473e+01,  1.524e+01,  1.724e+02,  1.723e+02,  1.194e+02,   1.187e+02,  8.968e+01, 0.05], False,0.9))

    # print(J_view(ac_slit_op, ac_slit_op, True, 0.1))
    # print(J_view(ac_side_op, ac_side_op, True, 0.1))
    # print(J_view(ac_roll_op, ac_roll_op, True, 0.1))

    J_log(ac_roll_op, ac_roll_op, True, 0.3)
    J_log(ac_roll_op, roll_03_gpg, False, 0.3)
    J_log(ac_roll_op, roll_05_gpg, False, 0.5)
    J_log(ac_roll_op, roll_07_gpg, False, 0.7)
    J_log(ac_roll_op, roll_09_gpg, False, 0.9)


    # print(J_traj_each(serpentine_op,(45, 45, 20, 20, 108, 108/2, 0, 0.05),True,0.7071))
    exit()

    #### Linear Searching...
    start_iter = time.time()
    # Curves
    iterator_linear(serpentine_op,  True, 0.7071)
    # iterator_linear(slithering_op,  True, 0.7071)
    # iterator_linear(sidewinding_op, True, 0.7071)
    # iterator_linear(rolling_op,     True, 0.7071)

    # Mats
    # iterator_linear(ac_serp_op,     False,  0.3)
    # iterator_linear(ac_slit_op,     False,  0.3)
    # iterator_linear(ac_side_op,     False,  0.3)
    # iterator_linear(ac_roll_op,     False,  0.3)

    # iterator_linear(ac_serp_op,     False,  0.5)
    # iterator_linear(ac_slit_op,     False,  0.5)
    # iterator_linear(ac_side_op,     False,  0.5)
    # iterator_linear(ac_roll_op,     False,  0.5)

    # iterator_linear(ac_serp_op,     False,  0.7071)
    # iterator_linear(ac_slit_op,     False,  0.7071)
    # iterator_linear(ac_side_op,     False,  0.7071)
    # iterator_linear(ac_roll_op,     False,  0.7071)

    # iterator_linear(ac_serp_op,     False,  0.9)
    # iterator_linear(ac_slit_op,     False,  0.9)
    # iterator_linear(ac_side_op,     False,  0.9)
    # iterator_linear(ac_roll_op,     False,  0.9)

    # 20240319 Side만 다시
    # iterator_linear(sidewinding_op, False, 0.3)
    # iterator_linear(sidewinding_op, False, 0.5)
    # iterator_linear(sidewinding_op, False, 0.7071)
    # iterator_linear(sidewinding_op, False, 0.9)

    # iterator_linear(ac_side_op, False, 0.3)
    # iterator_linear(ac_side_op, False, 0.5)
    # iterator_linear(ac_side_op, False, 0.7071)
    # iterator_linear(ac_side_op, False, 0.9)

    # # Fines
    # iterator_fine(serpentine_op, True, 0.3)
    # iterator_fine(slithering_op, True, 0.3)
    # iterator_fine(sidewinding_op,True, 0.3)
    # iterator_fine(rolling_op,       True, 0.3)

    # iterator_fine(serpentine_op, True, 0.5)
    # iterator_fine(slithering_op, True, 0.5)
    # iterator_fine(sidewinding_op,True, 0.5)
    # iterator_fine(rolling_op,       True, 0.5)

    # iterator_fine(serpentine_op, True, 0.7071)
    # iterator_fine(slithering_op, True, 0.7071)
    # iterator_fine(sidewinding_op,True, 0.7071)
    # iterator_fine(rolling_op,       True, 0.7071)

    # iterator_fine(serpentine_op, True, 0.9)
    # iterator_fine(slithering_op, True, 0.9)
    # iterator_fine(sidewinding_op,True, 0.9)
    # iterator_fine(rolling_op,       True, 0.9)

    # # Linear Amplitude
    # iterator_linear_amp(serpentine_op, True, 0.3)
    # iterator_linear_amp(slithering_op, True, 0.3)
    # iterator_linear_amp(sidewinding_op, True, 0.3)
    # iterator_linear_amp(rolling_op, True, 0.3)

    ### Finetuning
    finetuning(ac_slit_op, 0.3)
    finetuning(ac_slit_op, 0.5)
    finetuning(ac_slit_op, 0.7071)
    finetuning(ac_slit_op, 0.9)

    finetuning(ac_side_op, 0.3)
    finetuning(ac_side_op, 0.5)
    finetuning(ac_side_op, 0.7071)
    finetuning(ac_side_op, 0.9)

    finetuning(ac_roll_op, 0.3)
    finetuning(ac_roll_op, 0.5)
    finetuning(ac_roll_op, 0.7071)
    finetuning(ac_roll_op, 0.9)

    end_iter = time.time()
    print(f"Iterating dond... {end_iter-start_iter} seconds elapsed")

