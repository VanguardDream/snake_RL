import mujoco_py
import os
import random
import gait_lambda
import math
import numpy as np
import matplotlib.pyplot as plt

#load model from path
# snake = mujoco_py.load_model_from_path("../description/mujoco/snake_dgistV3.xml")
# snake = mujoco_py.load_model_from_path("../allnew/svm/snake.xml") # Circular frame
snake = mujoco_py.load_model_from_path("../description/mujoco/snake_circle.xml") # Triangular frame

# mujoco-py
simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

def J(g, d_a, d_p, d_l, l_a, l_p, l_l, tau):
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

    for i in range(0,10000):
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

        x_of_t = np.append(x_of_t, simulator.data.get_body_xpos('link6')[0])
        y_of_t = np.append(y_of_t, simulator.data.get_body_xpos('link6')[1])


    delta_x = simulator.data.get_body_xpos('head')[0]
    delta_y = simulator.data.get_body_xpos('head')[1]

    simulator.reset()
    #Calculate Cost here

    if (g == 2):
        J_value = 1500 * delta_y - 800 * abs(delta_x) - 900 * abs(delta_x / delta_y)

    else:
        J_value = 1500 * delta_x - 800 * abs(delta_y) - 900 * abs(delta_y / delta_x) - 0.0001 * accum_theta

    print(accum_theta)

    # print("%f : %f : %f : %f : %d : %lf" %(d_a,d_p,l_a,l_p,tau,J_value))
    return J_value, x_of_t, y_of_t

def main():
    gait_type = 1
    # gait_params = [39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1] # -> new serpenoid param
    # gait_params = [40.7, 191.1, -9.1, 66.5, 160.9, 7.0, 1] #EAAI serp c1 group
    # gait_params = [39.8, 189.9, -9.1, 67.1, 160.3, 7.0, 1] #EAAI serp c2 group
    # gait_params = [40.7, 188.7, -9.1, 66.5, 159.7, 7.0, 15] #EAAI 중 값은 낮지만 엄청 잘가는 파라미터
    gait_params = [25,   190,   -1,    55,   109,    -8,     10]

    # gait_params = [39.8, 189.9, -9.1, 67.3, 160.9, 7.0, 10] # grid search중 튀는 값

    # gait_type = 2
    # gait_params = [52.76,	319.65,	1.99,	72.07,	262.95,	7.91,	1] #EAAI Op
    # gait_params = [52.16,	318.15,	1.99,	72.07,	262.95,	7.91,	1] #EAAI c1
    # gait_params = [52.76,	319.65,	1.99,	72.67,	261.75,	7.91,	1]
    
    # gait_params = [87.13,40.16,2.02,13.87,267.47,-1.02,1] #EAAI side op

    # gait_params = [55.7, 57.2, -9.5, 70.5, 76.5, 10, 10]
    # gait_params = [38.2, 41.4, -8, 66.0, 51.6, 1 ,  3] # -> icra2022 sidewind gait
    # gait_params = [87, 	40.16,	2.02,	13.87,	267.47,	-1.02,	1] # For now best? sidewind
    

    # gait_params = [55.7, 70.5,	-9.5,	57.2,	75.5,	10,	1]
    # gait_params = [55.7, 57.2, -9.5, 70.5, 76.5, 10, 1] #-> optimal serpenoid
    # gait_params = [61.03, 10.9, 2.8, 15.71, 26.21, 1.05, 1]
    
    

    reward, x_t, y_t = J(gait_type, gait_params[0], gait_params[1], gait_params[2], gait_params[3], gait_params[4], gait_params[5], gait_params[6])

    print('Gait\'s reward : %f'  %(reward))

    # plt.plot(x_t,y_t)
    # plt.xlim([-0.7, 1.5])
    # plt.ylim([-0.6,0.4])
    # plt.show()

if __name__ == "__main__":
    # while True:
    for _ in range(3):
        main()