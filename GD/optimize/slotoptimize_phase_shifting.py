import scipy
import numpy as np
import mujoco
import mujoco_viewer
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation

## Load Mujoco
import os
import pathlib
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = pathlib.Path(__location__)
__model_location__ = __location__.parent.parent.joinpath("dmc/models/")

xml_full_path = __model_location__.joinpath('snake_circle_contact_fixed_marker.xml')

snake = mujoco.MjModel.from_xml_path(str(xml_full_path))
simdata = mujoco.MjData(snake)
# viewer = mujoco_viewer.MujocoViewer(snake,simdata)

## Global variables
mujoco_xml_time_step = 0.01
gait_sampling_interval = 0.1 # unit : seconds
t_range = np.arange(0, 2 * np.pi, gait_sampling_interval).transpose()
selected_gait_parameters = [[45, 45, 1, 1, 0], #Linear Progression
                            [45, 45, 1, 1, 45], #Sidewinding
                            [0, 0, 1, 1, 90]] #Rolling
curve_function_parameters = -1 + (1+1)*np.random.rand(14,9) #Curve function parameters, it initializes with random numbers
robot_body_names = ["head","link1","link2","link3","link4","link5","link6","link7","link8","link9","link10","link11","link12","link13","tail"]

## Predefined functions
def serpenoid(t, e_d1, e_l1, e_d2, e_l2, delta):
    #Hirose (1993) serpenoid curve implementations
    e_d1 = np.radians(e_d1)
    e_l1 = np.radians(e_l1)
    delta = np.radians(delta)

    f1 = e_d2 * t
    f2 = e_l2 * t

    j_1 = np.sin(e_d1 + f1)
    j_2 = np.sin(e_l1 * 2 + f2 + delta)

    j_3 = np.sin(e_d1 * 3 + f1)
    j_4 = np.sin(e_l1 * 4 + f2 + delta)

    j_5 = np.sin(e_d1 * 5 + f1)
    j_6 = np.sin(e_l1 * 6 + f2 + delta)

    j_7 = np.sin(e_d1 * 7 + f1)
    j_8 = np.sin(e_l1 * 8 + f2 + delta)

    j_9 = np.sin(e_d1 * 9 + f1)
    j_10 = np.sin(e_l1 * 10 + f2 + delta)

    j_11 = np.sin(e_d1 * 11 + f1)
    j_12 = np.sin(e_l1 * 12 + f2 + delta)

    j_13 = np.sin(e_d1 * 13 + f1)
    j_14 = np.sin(e_l1 * 14 + f2 + delta)

    return np.array([j_1, j_2, j_3, j_4, j_5, j_6, j_7, j_8, j_9, j_10, j_11, j_12, j_13, j_14])

def genMotionMat(serp_pos : np.array):
    serp_vel = np.diff(serp_pos.copy()) * (1 / gait_sampling_interval)
    serp_tor = np.diff(serp_vel.copy()) * (1 / gait_sampling_interval)

    motionMat = np.sign(serp_tor)

    return motionMat

def fourierApprox(t, v:np.array): # Fourier vectorized with each function paramters
    # assert np.shape(v)[1] // 2 != 0, "Check dimension of curve function parameters."
    
    v_0 = v[:,0]
    v_s = v[:,1::2]
    v_c = v[:,2::2]

    k_t = np.arange(1, np.shape(v_s)[1] + 1, 1)
    t = np.outer(t, k_t)

    f_s = np.dot(v_s, np.sin(t).transpose())
    f_c = np.dot(v_c, np.cos(t).transpose())

    return np.abs(f_s + f_c + v_0.reshape(14,-1))

def fourierApprox_phase(t, v:np.array): # Fourier vectorized with one function paramters and phase shifting.
    
    v_0 = v[0] # base DC component
    v_s = v[1::2] # Fourier coff for sin
    v_c = v[2::2] # Fourier coff for cos
    k_t = np.arange(1, np.shape(v_s)[0] + 1, 1) # Fourier hamonic

    n = np.arange(1,15, dtype=np.float32) # number of joints

    n[0::2] *= np.radians(gait_param[0]) # Dorsal spatial param
    n[1::2] *= np.radians(gait_param[1]) # lateral spatial param
    n[1::2] += np.radians(gait_param[4]) # Delta

    e_t = t[np.newaxis, np.newaxis, :] * k_t[:, np.newaxis, np.newaxis]
    n_t = n[np.newaxis, :, np.newaxis] + e_t[:, :, :]

    mat_s = np.sin(n_t[:, :, :]) * v_s[:, np.newaxis, np.newaxis] # tensor of sin
    mat_c = np.cos(n_t[:, :, :]) * v_c[:, np.newaxis, np.newaxis] # tensor of cos

    # return np.abs(v_0 + np.sum(mat_s + mat_c, axis=0)) #-> 합해서 절대값 취하기

    tri_func = np.sum(mat_s + mat_c, axis=0).copy()
    return np.array(v_0 + (tri_func - np.min(tri_func)),dtype=np.float32)  #-> 최소값을 DC로 더해서 항상 양수로 만들기

def get_robot_com(data:mujoco.MjData):
    accum_x = 0
    accum_y = 0
    num_bodies = len(robot_body_names)

    for name in robot_body_names:
        x, y, _ = data.body(name).xpos
        accum_x = accum_x + x
        accum_y = accum_y + y

    return np.array([accum_x / num_bodies, accum_y / num_bodies])

def op_param_simulation(v:np.array):
    # pass with 1D param vector.

    op_v = v.reshape(14,-1)
    viewer = mujoco_viewer.MujocoViewer(snake,simdata)
    mujoco.mj_forward(snake,simdata)

    P = fourierApprox(t_range[:-2], op_v)
    u = np.multiply(M, P)
    k = 0

    for _ in range(1830):
        k = k % np.shape(u)[1]

        simdata.ctrl = u[:,k]

        if _ % 10 == 0:
            k = k + 1
        
        simdata.qpos[-2:] = get_robot_com(simdata)
        mujoco.mj_step(snake,simdata)
        viewer.render()

    val = simdata.qpos[-2] - np.abs(simdata.qpos[-1])
    print(val)
    
def op_param_simulation_phase(v:np.array):
    # pass with 1D param vector.
    t = np.arange(0,1.99 * np.pi, 2*np.pi/61).transpose()
    op_v = v

    viewer = mujoco_viewer.MujocoViewer(snake,simdata)
    mujoco.mj_forward(snake,simdata)

    P = fourierApprox_phase(t, op_v).copy()
    u = np.multiply(M, P).copy()
    k = 0
    accum_rotation = 0

    for _ in range(1830):
        simdata.ctrl = u[:,k].copy()
        model_sensordata= simdata.sensordata.copy()

        if _ % 10 == 0:
            k = k + 1
            k = k % np.shape(u)[1]

        # k = k + 1
        # k = k % np.shape(u)[1]
        
        simdata.qpos[-2:] = get_robot_com(simdata).copy()

        # head_R = Rotation.from_quat([model_sensordata[49], model_sensordata[50], model_sensordata[51], model_sensordata[48]])
        # head_rotvec = head_R.as_rotvec(degrees=False).copy()
        # link1_R = Rotation.from_quat([model_sensordata[53], model_sensordata[54], model_sensordata[55], model_sensordata[52]])
        # link2_R = Rotation.from_quat([model_sensordata[57], model_sensordata[58], model_sensordata[59], model_sensordata[56]])
        # link3_R = Rotation.from_quat([model_sensordata[61], model_sensordata[62], model_sensordata[63], model_sensordata[60]])
        # link4_R = Rotation.from_quat([model_sensordata[65], model_sensordata[66], model_sensordata[67], model_sensordata[64]])
        # link5_R = Rotation.from_quat([model_sensordata[69], model_sensordata[70], model_sensordata[71], model_sensordata[68]])
        # link6_R = Rotation.from_quat([model_sensordata[73], model_sensordata[74], model_sensordata[75], model_sensordata[72]])
        # link7_R = Rotation.from_quat([model_sensordata[77], model_sensordata[78], model_sensordata[79], model_sensordata[76]])
        # link8_R = Rotation.from_quat([model_sensordata[81], model_sensordata[82], model_sensordata[83], model_sensordata[80]])
        # link9_R = Rotation.from_quat([model_sensordata[85], model_sensordata[86], model_sensordata[87], model_sensordata[84]])
        # link10_R = Rotation.from_quat([model_sensordata[89], model_sensordata[90], model_sensordata[91], model_sensordata[88]])
        # link11_R = Rotation.from_quat([model_sensordata[93], model_sensordata[94], model_sensordata[95], model_sensordata[92]])
        # link12_R = Rotation.from_quat([model_sensordata[97], model_sensordata[98], model_sensordata[99], model_sensordata[96]])
        # link13_R = Rotation.from_quat([model_sensordata[101], model_sensordata[102], model_sensordata[103], model_sensordata[100]])
        # tail_R = Rotation.from_quat([model_sensordata[101], model_sensordata[102], model_sensordata[103], model_sensordata[100]])

        com_R = Rotation.from_quat([
            [model_sensordata[49], model_sensordata[50], model_sensordata[51], model_sensordata[48]],
            [model_sensordata[53], model_sensordata[54], model_sensordata[55], model_sensordata[52]],
            [model_sensordata[57], model_sensordata[58], model_sensordata[59], model_sensordata[56]],
            [model_sensordata[61], model_sensordata[62], model_sensordata[63], model_sensordata[60]],
            [model_sensordata[65], model_sensordata[66], model_sensordata[67], model_sensordata[64]],
            [model_sensordata[69], model_sensordata[70], model_sensordata[71], model_sensordata[68]],
            [model_sensordata[73], model_sensordata[74], model_sensordata[75], model_sensordata[72]],
            [model_sensordata[77], model_sensordata[78], model_sensordata[79], model_sensordata[76]],
            [model_sensordata[81], model_sensordata[82], model_sensordata[83], model_sensordata[80]],
            [model_sensordata[85], model_sensordata[86], model_sensordata[87], model_sensordata[84]],
            [model_sensordata[89], model_sensordata[90], model_sensordata[91], model_sensordata[88]],
            [model_sensordata[93], model_sensordata[94], model_sensordata[95], model_sensordata[92]],
            [model_sensordata[97], model_sensordata[98], model_sensordata[99], model_sensordata[96]],
            [model_sensordata[101], model_sensordata[102], model_sensordata[103], model_sensordata[100]],
            [model_sensordata[105], model_sensordata[106], model_sensordata[107], model_sensordata[104]]
            ])
        com_rotvec = com_R.mean().as_rotvec(degrees=False).copy()

        accum_rotation = accum_rotation + np.linalg.norm(com_rotvec, 1)

        mujoco.mj_step(snake, simdata)
        viewer.render()

    val = simdata.qpos[-2] - np.abs(simdata.qpos[-1]) - 0.5 * (accum_rotation / 1830)
    # val = simdata.qpos[-2] - np.abs(simdata.qpos[-1])
    print(val)

# Simulation example code
gait_param = selected_gait_parameters[0][:]
M = genMotionMat(serpenoid(t_range, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4])).copy()

loadmat = scipy.io.loadmat("powell_v3_phase_50_result_20230703-105112.mat")
load_value = loadmat['result_value']
load_vector = loadmat['result_vector']

# op_param_simulation_phase(load_vector[2,:])
op_param_simulation_phase(np.array([2.0]))
exit()

# t = np.arange(0,1.9999 * np.pi, 2*np.pi/61).transpose()
# # P = fourierApprox_phase(t, load_vector[2,:])
# P = fourierApprox_phase(t, np.array([0.7]))
# u = np.multiply(M, P)

# fig = plt.pcolor(u)

# fig2, axs = plt.subplots(14)
# axs[0].plot(t, P[0, :])
# axs[1].plot(t, P[1, :])
# axs[2].plot(t, P[2, :])
# axs[3].plot(t, P[3, :])
# axs[4].plot(t, P[4, :])
# axs[5].plot(t, P[5, :])
# axs[6].plot(t, P[6, :])
# axs[7].plot(t, P[7, :])
# axs[8].plot(t, P[8, :])
# axs[9].plot(t, P[9, :])
# axs[10].plot(t, P[10, :])
# axs[11].plot(t, P[11, :])
# axs[12].plot(t, P[12, :])
# axs[13].plot(t, P[13, :])

# plt.show()

# exit()

# Optimize
def J(v0:np.array):
    # print("Initiated with "+str(v0),end='\r')
    v = v0.reshape(14,-1)
    P = fourierApprox(t_range[:-2], v)
    # M = genMotionMat(serpenoid(t_range, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4]))
    u = np.multiply(M, P)
    k = 0

    mujoco.mj_resetData(snake,simdata)

    for _ in range(1830):
        k = k % np.shape(u)[1]

        simdata.ctrl = u[:,k]

        if _ % 10 == 0:
            k = k + 1
        
        simdata.qpos[-2:] = get_robot_com(simdata)
        mujoco.mj_step(snake,simdata)

    val = simdata.qpos[-2] - np.abs(simdata.qpos[-1])

    return -1 * val

def J_phase(v:np.array):
    # print("Initiated with "+str(v0),end='\r')
    t = np.arange(0,1.99 * np.pi, 2*np.pi/61).transpose()
    P = fourierApprox_phase(t, v).copy()
    # M = genMotionMat(serpenoid(t_range, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4]))
    u = np.multiply(M, P).copy()
    k = 0

    mujoco.mj_resetData(snake,simdata)
    mujoco.mj_forward(snake,simdata)

    for _ in range(1830):
        simdata.ctrl = u[:,k].copy()

        if _ % 10 == 0:
            k = k + 1
            k = k % np.shape(u)[1]
        
        simdata.qpos[-2:] = get_robot_com(simdata).copy()
        mujoco.mj_step(snake,simdata)

    val = simdata.qpos[-2] - np.abs(simdata.qpos[-1])

    return -1 * val

def J_phase_orientation(v:np.array):
    # print("Initiated with "+str(v0),end='\r')
    t = np.arange(0,1.99 * np.pi, 2*np.pi/61).transpose()
    P = fourierApprox_phase(t, v).copy()
    # M = genMotionMat(serpenoid(t_range, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4]))
    u = np.multiply(M, P).copy()
    k = 0
    accum_rotation = 0

    mujoco.mj_resetData(snake,simdata)
    mujoco.mj_forward(snake,simdata)

    for _ in range(1830):
        simdata.ctrl = u[:,k].copy()
        model_sensordata = simdata.sensordata.copy()

        if _ % 10 == 0:
            k = k + 1
            k = k % np.shape(u)[1]
        
        simdata.qpos[-2:] = get_robot_com(simdata).copy()

        # head_R = Rotation.from_quat([model_sensordata[49], model_sensordata[50], model_sensordata[51], model_sensordata[48]])
        # head_rotvec = head_R.as_rotvec(degrees=True).copy()

        com_R = Rotation.from_quat([
                    [model_sensordata[49], model_sensordata[50], model_sensordata[51], model_sensordata[48]],
                    [model_sensordata[53], model_sensordata[54], model_sensordata[55], model_sensordata[52]],
                    [model_sensordata[57], model_sensordata[58], model_sensordata[59], model_sensordata[56]],
                    [model_sensordata[61], model_sensordata[62], model_sensordata[63], model_sensordata[60]],
                    [model_sensordata[65], model_sensordata[66], model_sensordata[67], model_sensordata[64]],
                    [model_sensordata[69], model_sensordata[70], model_sensordata[71], model_sensordata[68]],
                    [model_sensordata[73], model_sensordata[74], model_sensordata[75], model_sensordata[72]],
                    [model_sensordata[77], model_sensordata[78], model_sensordata[79], model_sensordata[76]],
                    [model_sensordata[81], model_sensordata[82], model_sensordata[83], model_sensordata[80]],
                    [model_sensordata[85], model_sensordata[86], model_sensordata[87], model_sensordata[84]],
                    [model_sensordata[89], model_sensordata[90], model_sensordata[91], model_sensordata[88]],
                    [model_sensordata[93], model_sensordata[94], model_sensordata[95], model_sensordata[92]],
                    [model_sensordata[97], model_sensordata[98], model_sensordata[99], model_sensordata[96]],
                    [model_sensordata[101], model_sensordata[102], model_sensordata[103], model_sensordata[100]],
                    [model_sensordata[105], model_sensordata[106], model_sensordata[107], model_sensordata[104]]
                    ])
        
        com_rotvec = com_R.mean().as_rotvec(degrees=False).copy()
        accum_rotation = accum_rotation + np.linalg.norm(com_rotvec, 1)

        mujoco.mj_step(snake,simdata)

    val = simdata.qpos[-2] - np.abs(simdata.qpos[-1]) - 0.5 * (accum_rotation / 1830)

    return -1 * val

from scipy.spatial.transform import Rotation
from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.io import savemat
import datetime

t_start = datetime.datetime.now()

# op_method = 'Nelder-Mead'
# op_option = {'adaptive':True}
op_method = 'powell'
op_option = {}

op_iter = 50
op_variables = 1
op_bound = Bounds(lb= [0.0] + ([-0.75] * (op_variables - 1)), ub= [3.0] + ([0.75] * (op_variables - 1)))

v0 = np.random.rand(op_variables)
v0[0] = np.random.random(1)

res_val = np.empty((0,1))
res_vec = np.empty((0,np.size(v0)))
res_initvec = np.empty((0,np.size(v0)))
res_done = np.empty((0,1))

for _ in range(op_iter):

    v0 = -0.75 + (0.75+0.75)*np.random.rand(op_variables)
    v0[0] = 3.0 * np.random.random(1)

    res = minimize(J_phase, v0, method=op_method, bounds=op_bound, options=op_option)

    res_initvec = np.vstack((res_initvec, v0))
    res_val = np.vstack((res_val, res['fun']))
    res_vec = np.vstack((res_vec, res['x']))
    res_done = np.vstack((res_done, res['success']))

    t_done = datetime.datetime.now()
    print(f"Time elapsed : {(t_done - t_start).seconds}")
    t_start = t_done

matdata = {"result_value" : res_val, "result_vector" : res_vec, "result_done" : res_done, "result_init_vector" : res_initvec}
f_name = t_done.strftime(op_method + "_v" +str(op_variables) +"_phase_" + str(op_iter) +"_result_%Y%m%d-%H%M%S.mat")

savemat(f_name,matdata)