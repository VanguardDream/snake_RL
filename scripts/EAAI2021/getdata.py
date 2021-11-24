from re import X
import mujoco_py
import os
import random
import sys

sys.path.append('../')

import gait_lambda
import math
import numpy as np
import csv

#load model from path
snake = mujoco_py.load_model_from_path("../../description/mujoco/snake_dgist.xml")

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
        J_value = 1500 * delta_y - 800 * abs(delta_x) - 900 * abs(delta_x / delta_y)
    else:
        J_value = 1500 * delta_x - 800 * abs(delta_y) - 900 * abs(delta_y / delta_x)

    return J_value



def J_t(g, d_a, d_p, d_l, l_a, l_p, l_l, tau):
    gen = gait_lambda.gait(g, d_a, d_p, d_l, l_a, l_p, l_l, int(tau))

    # Variable for cost(loss) function
    delta_x = 0
    delta_y = 0
    
    p_of_6 = np.empty((3,))

    com =np.empty((3,))


    # Simulation model info
    # joint_names = simulator.model.joint_names[1:] 
    # For generalized xml code!
    joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
    link_names = ['head','link1','link2','link3','link4','link5','link6','link7','link8','link9','link10','link11','link12','link13','tail']

    for i in range(0,1000):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            # Commnad motor here
            simulator.data.ctrl[idx] = gen.degtorad(goal[idx])
        
        simulator.step()

        total = np.array([0,0,0])


        # # 무게 중심의 좌표를 찍고 싶으면...
        # for link in link_names:
        #     total = np.add(total, simulator.data.get_body_xpos(link))

        # total = total /14

        # 한 링크의 좌료를 찍고 싶으면...
        total = np.add(total, simulator.data.get_body_xpos('link6')) #우리 지정한 중간 link는 6이라 가정...


        com = np.vstack((com,total))

        # x_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[0])
        # y_of_t = np.append(y_of_t, simulator.data.get_body_xpos('head')[1])
        p_of_6 = np.vstack((p_of_6,simulator.data.get_body_xpos('link6')))


    delta_x = simulator.data.get_body_xpos('head')[0]
    delta_y = simulator.data.get_body_xpos('head')[1]

    simulator.reset()
    #Calculate Cost here

    if (g == 2):
        J_value = 1500 * delta_y - 800 * abs(delta_x) - 900 * abs(delta_x / delta_y)
    else:
        J_value = 1500 * delta_x - 800 * abs(delta_y) - 900 * abs(delta_y / delta_x)

    # print("%f : %f : %f : %f : %d : %lf" %(d_a,d_p,l_a,l_p,tau,J_value))
    return J_value, p_of_6




def main():
    # gait_type = 1
    # gait_params = [56.0, 57.7, -9.5, 71.0, 76.2, 10, 1]
    
    # gait_type = 2
    # gait_params = [37.2, 37.4, -8, 61.9, 61.7, 1 ,  3]

    #EAAI

    gait_type = 2
    gait_params = [52.76,	319.65,	1.99,	72.07,	262.95,	7.91,	1] #EAAI Op

    count = 0

    csv_log = open('gradient_side_.csv','a')
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

def main2():
    # gait_type = 1
    # gait_params = [39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1] #EAAI Serp
    # gait_params = [40.7, 191.1, -9.1, 66.5, 160.9, 7.0, 1] #EAAI serp c1 group
    # gait_params = [39.8, 189.9, -9.1, 67.1, 160.3, 7.0, 1] #EAAI serp c2 group
    
    gait_type = 2
    # gait_params = [87, 	40.16,	2.02,	13.87,	267.47,	-1.02,	1] #EAAI side 1st try

    # gait_params = [52.76,	319.65,	1.99,	72.07,	262.95,	7.91,	1] #EAAI side 2nd try op
    # gait_params = [52.16,	318.15,	1.99,	72.07,	262.95,	7.91,	1] #EAAI side c1
    gait_params = [52.76,	319.65,	1.99,	72.67,	261.75,	7.91,	1] #EAAI side c2

    csv_log = open('side_xy_trajactory_c2.csv','w')
    csv_writer = csv.writer(csv_log)

    reward, com = J_t(gait_type, gait_params[0], gait_params[1], gait_params[2], gait_params[3], gait_params[4], gait_params[5], gait_params[6])

    for t in range(0, len(com)):
        csv_writer.writerow(com[t])

    csv_log.close()

def main3(): # Grid search code all params
    gait_type = 1
    gait_params = [39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1] #EAAI Serp
    
    count = 0

    csv_log = open('serp_gridsearch.csv','w')
    csv_writer = csv.writer(csv_log)

    for i0 in range(-8,9): # d_a
        for i1 in range(-8,9): # d_p
            for i2 in range (-8,9):
                for i3 in range(-8,9):
                    test_params = [gait_params[0] + i0 * 0.4, gait_params[1] + i1 * 0.4, gait_params[2], gait_params[3] + i2 * 0.4, gait_params[4] + i3 * 0.4, gait_params[5], gait_params[6] ]

                    reward = J(gait_type, test_params[0], test_params[1], test_params[2], test_params[3], 
                                                test_params[4],test_params[5],test_params[6])

                    csv_writer.writerow(test_params[0:6] + [reward])
                    print('Iteration : (%d) reward : %f'  %(count,reward))
                    count = count + 1

def main4():
    gait_type = 1
    # gait_params = [56.0, 57.7, -9.5, 71.0, 76.2, 10, 1]
    #대왕 sin
    gait_params = [55.7, 57.2, -9.5, 70.5, 76.5, 10, 1]

    # gait_type = 2
    # # gait_params = [37.2, 37.4, -8, 61.9, 61.7, 1 ,  3]
    # #대왕 side 
    # gait_params = [38.2, 43.4, -8, 66, 51.6, 1 ,  3]


    count = 0

    csv_log = open('sin_lat_a_p_gradient.csv','w')
    csv_writer = csv.writer(csv_log)

    for i0 in range(-5,6): # d_a
        for i1 in range(-5,6): # d_p
            test_params = [gait_params[0], gait_params[1], gait_params[2], gait_params[3] - i0 * 0.1, gait_params[4] - i1 * 0.1, gait_params[5], gait_params[6] ]

            reward = J(gait_type, test_params[0], test_params[1], test_params[2], test_params[3], 
                                        test_params[4],test_params[5],test_params[6])

            csv_writer.writerow(test_params[3:5] + [reward])
            print('Iteration : (%d) reward : %f'  %(count,reward))
            count = count + 1

if __name__ == "__main__":
        main()