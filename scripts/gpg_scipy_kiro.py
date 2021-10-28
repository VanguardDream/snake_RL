# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : BRM snake robot main simulation script

import time
import csv

import mujoco_py
import os
import random
import gait_lambda
import math
import numpy as np
from scipy.optimize import minimize

#load model from path
snake = mujoco_py.load_model_from_path("../description/mujoco/snake_dgist.xml")

# mujoco-py
simulator = mujoco_py.MjSim(snake)
# sim_viewer = mujoco_py.MjViewer(simulator)

def J(g,d_a,d_p,d_l,l_a,l_p,l_l,tau):
    gen = gait_lambda.gait(g,d_a,d_p,d_l,l_a,l_p,l_l,tau)

    # Variable for cost(loss) function
    delta_x = 0
    delta_y = 0
    accum_theta = 0 # accumulated joint displacements for all joint.
    x_of_t = np.array([]) # Head link x values of the time t
    y_of_t = np.array([]) # Head link y values of the time t

    # Simulation model info
    # joint_names = simulator.model.joint_names[1:] 
    # For generalized xml code!
    joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']

    for i in range(0,5000):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)

        for idx in spec_motor:
            # Commnad motor here
            if not(len(idx) == 0):
                simulator.data.ctrl[idx] = gen.degtorad(goal[idx])
        
        for name in joint_names:
            accum_theta = accum_theta + abs(simulator.data.get_joint_qpos(name))

        simulator.step()
        # sim_viewer.render()

        # Write step iteration state retrieve code here.
        # s_y = appent(body_xpos('head')[1]) like this.

        x_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[0])
        y_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[1])


    delta_x = simulator.data.get_body_xpos('head')[0]
    delta_y = simulator.data.get_body_xpos('head')[1]

    print(x_of_t)

    simulator.reset()
    #Calculate Cost here

    if not(g == 2):
        J_value = 100 * delta_x - 25 * delta_y - 0.00003 * accum_theta
    else:
        J_value = 100 * abs(delta_y) - 60 * delta_x - 0.00003 * accum_theta

    # print("%f : %f : %f : %f : %d : %lf" %(d_a,d_p,l_a,l_p,tau,J_value))
    return J_value

def getGradient(g = 0, d_a = 130, d_p = 150, l_a = 30, l_p = 150, tau = 1, u = 0.5):
    unit_vector = [1, 1, 1, 1, 1]
    J_k = J(g,d_a,d_p,l_a,l_p,tau)

    if not(g == 0):
        if (J(g, d_a + u, d_p, l_a, l_p, tau) - J_k) > 0:
            unit_vector[0] = u
        else:
            unit_vector[0] = -u

        if (J(g, d_a, d_p + u, l_a, l_p, tau) - J_k) > 0:
            unit_vector[1] = u
        else:
            unit_vector[1] = -u

        if (J(g, d_a, d_p, l_a + u, l_p, tau) - J_k) > 0:
            unit_vector[2] = u
        else:
            unit_vector[2] = -u

        if (J(g, d_a, d_p, l_a, l_p + u, tau) - J_k) > 0:
            unit_vector[3] = u
        else:
            unit_vector[3] = -u

        if (J(g, d_a, d_p, l_a, l_p, tau + 1) - J_k) > 0:
            unit_vector[4] = 1
        else:
            if(tau > 1):
                unit_vector[4] = -1
            else:
                unit_vector[4] = 0
    else:
        if (J(g, d_a + u, d_p, l_a, l_p, tau) - J_k) > 0:
            unit_vector[0] = u
        else:
            unit_vector[0] = -u

        if (J(g, d_a, d_p + u, l_a, l_p, tau) - J_k) > 0:
            unit_vector[1] = u
        else:
            unit_vector[1] = -u

        unit_vector[2] = 0
        unit_vector[3] = 0

        if (J(g, d_a, d_p, l_a, l_p, tau + 1) - J_k) > 0:
            unit_vector[4] = 1
        else:
            if(tau > 1):
                unit_vector[4] = -1
            else:
                unit_vector[4] = 0

    return unit_vector, J_k
        
def optimizeGait(eps = 1, l = 1, local_minima = 0):
    d_amp = random.randint(0, 900) / 10
    d_phase = random.randint(0,3600) / 10
    l_amp = random.randint(0, 900) / 10
    l_phase = random.randint(0,3600) / 10
    tau = random.randint(1,10)

    hist = np.array([d_amp, d_phase, l_amp, l_phase, tau])

    param = [d_amp,d_phase,l_amp,l_phase,tau]
    gradient_vector = []
    j_k = 0

    while True:
        gradient_vector, j_k1 = getGradient(g=1,d_a = param[0], d_p = param[1], l_a = param[2], l_p = param[3], tau = param[4])

        if (j_k1 - j_k) < eps:
            return hist, j_k1

        if j_k1 < local_minima:
            # print("smaller than local minima terminate iteration...")
            return hist, j_k1

        hist = np.vstack([hist, np.array(param)])

        j_k = j_k1

        for i in range(len(param)):
            if i != len(param) - 1:
                param[i] = param[i] + l * gradient_vector[i]
            else:
                param[i] = param[i] + gradient_vector[i]

def optimizeSci(gait = 1, exoptimal = 0,options={'xtol': 0.1, 'ftol' : 0.5, 'disp': True, 'eps': 0.5}):
    d_amp = random.randint(0, 90)
    d_phase = random.randint(0,360)
    d_lambda = random.randint(-10,10)

    l_amp = random.randint(0, 90)
    l_phase = random.randint(0,360)
    l_lambda = random.randint(-10,10)

    tau = random.randint(1,3)

    origin = [d_amp,d_phase,d_lambda,l_amp,l_phase,l_lambda,tau]

    #vertical vector
    xv0 = np.array([d_amp,d_phase,d_lambda,tau])
    xvbound = ((0,90), (0,360), (-10,10), (1,3))

    # Sinuous or Sidewind vector
    x0 = np.array([d_amp,d_phase,d_lambda,l_amp,l_phase,l_lambda,tau])
    xbound = ((0,90), (0,360), (-10,10), (0,90), (0,360), (-10,10), (1,6))

    if gait == 0:
        if exoptimal > J_sci_ver(xv0):
            print('Random vector result is less than ex_optimal value retrying...')
            return origin, -1
        else:
            res = minimize(J_sci_ver, xv0, method='Nelder-Mead', bounds=xvbound,options=options)

    elif gait == 1:
        if exoptimal > J_sci_sin(x0):
            print('Random vector result is less than ex_optimal value retrying...')
            return origin, -1
        else:
            res = minimize(J_sci_sin, x0, method='Nelder-Mead', bounds=xbound,options=options)

    elif gait == 2:
        if exoptimal > J_sci_side(x0):
            print('Random vector result is less than ex_optimal value retrying...')
            return origin, -1
        else:
            res = minimize(J_sci_side, x0, method='Nelder-Mead', bounds=xbound,options=options)

    else:
        return -1

    return origin, res

def J_sci_ver(ndarray):
    gen = gait_lambda.gait(0,ndarray[0],ndarray[1],ndarray[2],0,0,0,int(ndarray[2]))

    # print('Start new gait optimize senario with gait params : [ %f, %f, %f, %f, %d]' %(ndarray[0],ndarray[1],ndarray[2],ndarray[3],ndarray[4]))
    # Variable for cost(loss) function
    # delta_x = 0
    # delta_y = 0
    accum_theta = 0

    x_of_t = np.array([]) # Head link x values of the time t
    y_of_t = np.array([]) # Head link y values of the time t

    # Simulation model info
    # joint_names = simulator.model.joint_names[1:] 
    # For generalized xml code!
    joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']

    for i in range(0,1500):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            # Commnad motor here
            if not(len(idx) == 0):
                simulator.data.ctrl[idx] = gen.degtorad(goal[idx])
        
        # for name in joint_names:
        #     accum_theta = accum_theta + abs(simulator.data.get_joint_qpos(name))

        simulator.step()
        # sim_viewer.render()

        # Write step iteration state retrieve code here.
        # s_y = appent(body_xpos('head')[1]) like this.

        x_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[0])
        y_of_t = np.append(y_of_t, simulator.data.get_body_xpos('head')[1])


    delta_x = simulator.data.get_body_xpos('head')[0]
    delta_y = simulator.data.get_body_xpos('head')[1]

    simulator.reset()
    #Calculate Cost here

    # Vertical or Sinuous Utility function
    J_value = 1500 * delta_x - 60 * abs(delta_y) - 900 * abs(delta_y / delta_x)

    print('End gait optimize senario with gait params : [ %f, %f, %f, %d -> reward : %f]' %(ndarray[0],ndarray[1],ndarray[2],ndarray[3],J_value))
    
    return -1 * J_value

def J_sci_sin(ndarray):
    gen = gait_lambda.gait(1,ndarray[0],ndarray[1],ndarray[2],ndarray[3],ndarray[4],ndarray[5],int(ndarray[6]))

    # print('Start new gait optimize senario with gait params : [ %f, %f, %f, %f, %d]' %(ndarray[0],ndarray[1],ndarray[2],ndarray[3],ndarray[4]))
    # Variable for cost(loss) function
    # delta_x = 0
    # delta_y = 0
    accum_theta = 0
    J_value = 0

    # x_of_t = np.array([]) # Head link x values of the time t
    # y_of_t = np.array([]) # Head link y values of the time t

    # Simulation model info
    # joint_names = simulator.model.joint_names[1:] 
    # For generalized xml code!
    joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']

    for i in range(0,1500):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            simulator.data.ctrl[int(idx)] = gen.degtorad(goal[int(idx)])
        
        # for name in joint_names:
        #     accum_theta = accum_theta + abs(simulator.data.get_joint_qpos(name))

        simulator.step()
        # sim_viewer.render()

        # Write step iteration state retrieve code here.
        # s_y = appent(body_xpos('head')[1]) like this.

        #x_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[0])
        #y_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[1])


    delta_x = simulator.data.get_body_xipos('head')[0]
    delta_y = simulator.data.get_body_xipos('head')[1]

    simulator.reset()
    #Calculate Cost here

    J_value = 1500 * delta_x - 800 * abs(delta_y) - 900 * abs(delta_y / delta_x)

    print('End gait optimize senario with gait params : [ %f, %f, %f, %f, %f, %f, %d -> reward : %f]' %(ndarray[0],ndarray[1],ndarray[2],ndarray[3],ndarray[4],ndarray[5],ndarray[6],J_value))
    
    return -1 * J_value

def J_sci_side(ndarray):
    gen = gait_lambda.gait(2,ndarray[0],ndarray[1],ndarray[2],ndarray[3],ndarray[4],ndarray[5],int(ndarray[6]))

    # print('Start new gait optimize senario with gait params : [ %f, %f, %f, %f, %d]' %(ndarray[0],ndarray[1],ndarray[2],ndarray[3],ndarray[4]))
    # Variable for cost(loss) function
    # delta_x = 0
    # delta_y = 0
    accum_theta = 0
    J_value = 0

    #x_of_t = np.array([]) # Head link x values of the time t
    #y_of_t = np.array([]) # Head link y values of the time t

    # Simulation model info
    # joint_names = simulator.model.joint_names[1:] 
    # For generalized xml code!
    joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']

    for i in range(0,1500):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            simulator.data.ctrl[idx] = gen.degtorad(goal[idx])
        
        # for name in joint_names:
        #     accum_theta = accum_theta + abs(simulator.data.get_joint_qpos(name))
        
        simulator.step()
        # sim_viewer.render()

        # Write step iteration state retrieve code here.
        # s_y = appent(body_xpos('head')[1]) like this.

        #x_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[0])
        #y_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[1])


    delta_x = simulator.data.get_body_xipos('head')[0]
    delta_y = simulator.data.get_body_xipos('head')[1]

    simulator.reset()
    #Calculate Cost here

    J_value = 3500 * abs(delta_y) - 1000 * abs(delta_x / delta_y)

    print('End gait optimize senario with gait params : [ %f, %f, %f, %f, %f, %f, %d -> reward : %f]' %(ndarray[0],ndarray[1],ndarray[2],ndarray[3],ndarray[4],ndarray[5],ndarray[6],J_value))
    
    return -1 * J_value

def main():

    # optimal_reward = 2816;
    global optimal_reward
    optimal_reward = 1600;


    print('Gait optimizing Start...')

    while True:
    # for i in range(200):
        csv_log = open('mark6.csv','a')
        csv_writer = csv.writer(csv_log)

        gait_type = 1
        origin, res = optimizeSci(gait=gait_type,exoptimal=optimal_reward)

        if res != -1:
            temp_result = res.get('fun')

            if (temp_result * -1) < optimal_reward:
                csv_writer.writerow([time.ctime(time.time())] + [gait_type] + ["Origin : "] + origin)
                csv_writer.writerow(['Wrong optimization value'] + [ -1 * temp_result])

            else:
                x_star = res.get('x')
                x_result = x_star.tolist()
                x_result = [round(num, 2) for num in x_result]

                csv_writer.writerow([time.ctime(time.time())] + [gait_type] + ["Origin : "] + origin)
                csv_writer.writerow(x_result + [ -1 * temp_result])

                optimal_reward = -1 * temp_result

        csv_log.close()


        # if temp_result * -1 > optimal_reward:
        #     print('new optimal found! terminate iteration.\n')
        #     print(res)
        #     break
        # else:
        #     print('local found continue iteration...')
        #     continue


if __name__ == "__main__":
    main()