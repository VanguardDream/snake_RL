# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : BRM snake robot main simulation script

import mujoco_py
import os
import random
import gait
import math
import numpy as np

#load model from path
snake = mujoco_py.load_model_from_path("../description/mujoco/snake_allign.xml")

# mujoco-py
simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

def J(g,d_a,d_p,l_a,l_p,tau):
    gen = gait.gait(g,d_a,d_p,l_a,l_p,tau)

    # Variable for cost(loss) function
    delta_x = 0
    delta_y = 0
    accum_theta = 0

    # Simulation model info
    # joint_names = simulator.model.joint_names[1:] 
    # For generalized xml code!
    joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14','joint15']

    for i in range(0,5001):
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


    delta_x = simulator.data.get_body_xpos('head')[0]
    delta_y = simulator.data.get_body_xpos('head')[1]

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

def main():
    print('Gait optimizing Start...')

    local_minima = 0
    while True:
        hist, j_k = optimizeGait(local_minima=local_minima)

        if j_k > local_minima:
            local_minima = j_k

        print('local finding done...')
        print(hist,end='')
        print(" : reward = %lf" %(j_k))


if __name__ == "__main__":
    main()
