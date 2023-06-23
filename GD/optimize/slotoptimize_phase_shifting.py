import scipy
import numpy as np
import mujoco
import mujoco_viewer
import matplotlib.pyplot as plt

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

    return np.abs(v_0 + np.sum(mat_s + mat_c, axis=0))

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

    P = fourierApprox_phase(t, op_v)
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

# Simulation example code
gait_param = selected_gait_parameters[0][:]
M = genMotionMat(serpenoid(t_range, gait_param[0], gait_param[1], gait_param[2], gait_param[3], gait_param[4]))

# loadmat = scipy.io.loadmat("powell_phase_1_result_20230623-002016.mat")
# load_value = loadmat['result_value']
# load_vector = loadmat['result_vector']

# load_vector = np.array([[2.71,	0.25,	-0.10,	-0.12,	-0.71]])

# # op_param_simulation_phase(load_vector[0,:])
# op_param_simulation_phase(np.array([2.71,	0.25,	-0.10,	-0.12,	-0.71]))

# exit()

load_vector = np.array([[2.71,	0.25,	-0.10,	-0.12,	-0.71]])
t = np.arange(0,1.99 * np.pi, 2*np.pi/61).transpose()
P = fourierApprox_phase(t, load_vector[0,:])
u = np.multiply(M, P)

fig = plt.pcolor(u)

fig2, axs = plt.subplots(14)
axs[0].plot(t, P[0, :])
axs[1].plot(t, P[1, :])
axs[2].plot(t, P[2, :])
axs[3].plot(t, P[3, :])
axs[4].plot(t, P[4, :])
axs[5].plot(t, P[5, :])
axs[6].plot(t, P[6, :])
axs[7].plot(t, P[7, :])
axs[8].plot(t, P[8, :])
axs[9].plot(t, P[9, :])
axs[10].plot(t, P[10, :])
axs[11].plot(t, P[11, :])
axs[12].plot(t, P[12, :])
axs[13].plot(t, P[13, :])

plt.show()
exit()

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
    P = fourierApprox_phase(t, v)
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

from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.io import savemat
import datetime

t_start = datetime.datetime.now()

op_method = 'powell'
op_iter = 2
op_variables = 5
op_bound = Bounds(lb=[-2.7] * op_variables, ub=[2.7] * op_variables)

v0 = -1 + (1+1)*np.random.rand(op_variables)
res_val = np.empty((0,1))
res_vec = np.empty((0,np.size(v0)))
res_done = np.empty((0,1))

for _ in range(op_iter):

    v0 = -1 + (1+1)*np.random.rand(op_variables)

    res = minimize(J_phase, v0, method=op_method, bounds=op_bound)

    res_val = np.vstack((res_val, res['fun']))
    res_vec = np.vstack((res_vec, res['x']))
    res_done = np.vstack((res_done, res['success']))

    t_done = datetime.datetime.now()
    print(f"Time elapsed : {(t_done - t_start).seconds}")
    t_start = t_done

matdata = {"result_value" : res_val, "result_vector" : res_vec, "result_done" : res_done}
f_name = t_done.strftime(op_method + "_v" +str(op_variables) +"_phase_" + str(op_iter) +"_result_%Y%m%d-%H%M%S.mat")

savemat(f_name,matdata)