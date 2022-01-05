import mujoco_py
import os
import random
import gait_lambda
import math
import numpy as np

#load model from path
snake = mujoco_py.load_model_from_path("../description/mujoco/snake_dgist.xml")

# mujoco-py
simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

def J(g,d_a,d_p,d_l,l_a,l_p,l_l,tau):
    gen = gait_lambda.gait(g,d_a,d_p,d_l,l_a,l_p,l_l,int(tau))

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

    for i in range(0,1000):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            # Commnad motor here
            simulator.data.ctrl[int(idx)] = gen.degtorad(goal[int(idx)])
        
        for name in joint_names:
            accum_theta = accum_theta + abs(simulator.data.get_joint_qpos(name))

        simulator.step()
        sim_viewer.render()

        # Write step iteration state retrieve code here.
        # s_y = appent(body_xpos('head')[1]) like this.

        x_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[0])
        y_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[1])


    delta_x = simulator.data.get_body_xpos('head')[0]
    delta_y = simulator.data.get_body_xpos('head')[1]

    simulator.reset()
    #Calculate Cost here

    if (g == 2):
        J_value = 3500 * abs(delta_y) - 1000 * abs(delta_x / delta_y)
    else:
        J_value = 1500 * delta_x - 60 * abs(delta_y) - 900 * abs(delta_y / delta_x)

    # print("%f : %f : %f : %f : %d : %lf" %(d_a,d_p,l_a,l_p,tau,J_value))
    return J_value

def main():
    gait_type = 1
    
    gait_params = [39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1]
    reward = J(gait_type, gait_params[0], gait_params[1], gait_params[2], gait_params[3], gait_params[4],gait_params[5],gait_params[6])

    print('Gait\'s reward : %f'  %(reward))

if __name__ == "__main__":
    while True:
        main()