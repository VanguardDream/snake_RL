import mujoco_py
import os
import random
import gait_kiro
import math
import numpy as np

#load model from path
snake = mujoco_py.load_model_from_path("../description/mujoco/snake_kiro.xml")

# mujoco-py
simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

def J(g,d_a,d_p,l_a,l_p,tau):
    gen = gait_kiro.gait(g,d_a,d_p,l_a,l_p,tau)

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

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            # Commnad motor here
            simulator.data.ctrl[idx] = gen.degtorad(goal[idx])
        
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

    if not(g == 2):
        J_value = 100 * delta_x - 25 * delta_y - 0.00003 * accum_theta
    else:
        J_value = 100 * abs(delta_y) - 60 * delta_x - 0.00003 * accum_theta

    # print("%f : %f : %f : %f : %d : %lf" %(d_a,d_p,l_a,l_p,tau,J_value))
    return J_value

def main():
    gait_type = 1
    gait_params = [ 88.318680, 149.475858, 70.091854, 119.160065, 1]

    reward = J(gait_type, gait_params[0], gait_params[1], gait_params[2], gait_params[3], gait_params[4])

    print('Gait\'s reward : %f'  %(reward))

if __name__ == "__main__":
    while True:
        main()