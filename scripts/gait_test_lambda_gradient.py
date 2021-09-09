import mujoco_py
import os
import random
import gait_lambda
import math
import numpy as np
import csv

#load model from path
snake = mujoco_py.load_model_from_path("../description/mujoco/snake_kiro.xml")

# mujoco-py
simulator = mujoco_py.MjSim(snake)
# sim_viewer = mujoco_py.MjViewer(simulator)

def J(g, d_a, d_p, d_l, l_a, l_p, l_l, tau):
    gen = gait_lambda.gait(g, d_a, d_p, d_l, l_a, l_p, l_l, int(tau))

    # Variable for cost(loss) function
    delta_x = 0
    delta_y = 0

    for i in range(0,1000):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            # Commnad motor here
            simulator.data.ctrl[idx] = gen.degtorad(goal[idx])
        
        simulator.step()


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
    gait_params = [56.0, 57.7, -9.5, 71.0, 76.2, 10, 1]
    
    # gait_type = 2
    # gait_params = [37.2, 37.4, -8, 61.9, 61.7, 1 ,  3]

    count = 0

    csv_log = open('gradient_sin_10E4.csv','a')
    csv_writer = csv.writer(csv_log)

    for i0 in range(-5,6): # d_a
        for i1 in range(-5,6): # d_p
            for i3 in range(-5,6): # l_a
                for i4 in range(-5,6): # l_p
                    # for i6 in range(-10,11):
                    test_params = [gait_params[0] - i0, gait_params[1] - i1 * 2, gait_params[2], 
                                    gait_params[3] - i3, gait_params[4] - i4 * 2, gait_params[5], gait_params[6] ]

                    reward = J(gait_type, test_params[0], test_params[1], test_params[2], test_params[3], 
                                                test_params[4],test_params[5],test_params[6])

                    csv_writer.writerow(test_params + [reward])
                    print('Iteration : (%d) reward : %f'  %(count,reward))
                    count = count + 1


            
    

    # gait_params = [36.8,    296.2,  -8, 61.3,   318.8,  1,  3] -> Side
    # gait_params = [58.3,    344.4,  -9.4,   72.1,   193,    10.6,   1] -> Sin



if __name__ == "__main__":
        main()