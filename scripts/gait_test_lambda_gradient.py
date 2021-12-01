from re import X
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
    accum_theta = 0

    joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']

    for i in range(0,1000):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            # Commnad motor here
            simulator.data.ctrl[idx] = gen.degtorad(goal[idx])

        for name in joint_names:
            accum_theta = accum_theta + abs(simulator.data.get_joint_qpos(name))
        
        simulator.step()


    delta_x = simulator.data.get_body_xpos('head')[0]
    delta_y = simulator.data.get_body_xpos('head')[1]

    print('accum theta = %d' %(accum_theta))

    simulator.reset()
    #Calculate Cost here

    if (g == 2):
        J_value = 3500 * abs(delta_y) - 1000 * abs(delta_x / delta_y)
    else:
        J_value = 1500 * delta_x - 60 * abs(delta_y) - 900 * abs(delta_y / delta_x)

    # print("%f : %f : %f : %f : %d : %lf" %(d_a,d_p,l_a,l_p,tau,J_value))
    return J_value



def J_t(g, d_a, d_p, d_l, l_a, l_p, l_l, tau):
    gen = gait_lambda.gait(g, d_a, d_p, d_l, l_a, l_p, l_l, int(tau))

    # Variable for cost(loss) function
    delta_x = 0
    delta_y = 0
    
    p_of_7 = np.empty((3,))

    com =np.empty((3,))


    # Simulation model info
    # joint_names = simulator.model.joint_names[1:] 
    # For generalized xml code!
    joint_names = ['joint1','joint2','joint3','joint4','joint5','joint6','joint7','joint8','joint9','joint10','joint11','joint12','joint13','joint14']
    link_names = ['head','body1','body2','body3','body4','body5','body6','body7','body8','body9','body10','body11','body12','body13','tail']

    for i in range(0,3000):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            # Commnad motor here
            simulator.data.ctrl[idx] = gen.degtorad(goal[idx])
        
        simulator.step()

        total = np.array([0,0,0])

        for link in link_names:
            total = np.add(total, simulator.data.get_body_xpos(link))

        total = total /14

        com = np.vstack((com,total))

        # x_of_t = np.append(x_of_t, simulator.data.get_body_xpos('head')[0])
        # y_of_t = np.append(y_of_t, simulator.data.get_body_xpos('head')[1])
        p_of_7 = np.vstack((p_of_7,simulator.data.get_body_xpos('body7')))


    delta_x = simulator.data.get_body_xpos('head')[0]
    delta_y = simulator.data.get_body_xpos('head')[1]

    simulator.reset()
    #Calculate Cost here

    if (g == 2):
        J_value = 3500 * abs(delta_y) - 1000 * abs(delta_x / delta_y)
    else:
        J_value = 1500 * delta_x - 60 * abs(delta_y) - 900 * abs(delta_y / delta_x)

    # print("%f : %f : %f : %f : %d : %lf" %(d_a,d_p,l_a,l_p,tau,J_value))
    return J_value, p_of_7




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

def main2():
    # gait_type = 1
    # gait_params = [55.7, 57.2, -9.5, 70.5, 76.5, 10, 1]
    
    gait_type = 2
    gait_params = [38.2, 43.4, -8, 66, 51.6, 1 ,  3]

    csv_log = open('link_side.csv','w')
    csv_writer = csv.writer(csv_log)

    reward, com = J_t(gait_type, gait_params[0], gait_params[1], gait_params[2], gait_params[3], gait_params[4], gait_params[5], gait_params[6])

    for t in range(0, len(com)):
        csv_writer.writerow(com[t])

    csv_log.close()

def main3():
    gait_type = 1
    # gait_params = [56.0, 57.7, -9.5, 71.0, 76.2, 10, 1]
    #대왕 sin
    gait_params = [55.7, 57.2, -9.5, 70.5, 76.5, 10, 1]
    
    # gait_type = 2
    # # gait_params = [37.2, 37.4, -8, 61.9, 61.7, 1 ,  3]
    # #대왕 side 
    # gait_params = [38.2, 43.4, -8, 66, 51.6, 1 ,  3]


    count = 0

    csv_log = open('sin_dor_a_p_gradient.csv','w')
    csv_writer = csv.writer(csv_log)

    for i0 in range(-5,6): # d_a
        for i1 in range(-5,6): # d_p
            test_params = [gait_params[0] - i0 * 0.1, gait_params[1] - i1 * 0.1, gait_params[2], gait_params[3], gait_params[4], gait_params[5], gait_params[6] ]

            reward = J(gait_type, test_params[0], test_params[1], test_params[2], test_params[3], 
                                        test_params[4],test_params[5],test_params[6])

            csv_writer.writerow(test_params[0:2] + [reward])
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

def main5():
    # gait_type = 1
    # gait_params = [55.7, 57.2, -9.5, 70.5, 76.5, 10, 1] # Optimal
    # gait_params = [55.7, 57.2, -9.5, 70.5, 74.5, 10, 1] # Poor 2minus
    # gait_params = [55.7, 57.2, -9.5, 70.5, 75.5, 10, 1] # Poor 1minus
    # gait_params = [55.7, 57.2, -9.5, 70.5, 77.5, 10, 1] # Poor plus
    # gait_params = [55.7, 57.2, -9.5, 70.5, 78.5, 10, 1] # Poor 2plus
    
    gait_type = 2
    # [37.2, 37.4, -8, 61.9, 61.7, 1 ,  3] # 옵티말

    # gait_params = [38.2, 43.4, -8, 66.0, 51.6, 1 ,  3] 
    # gait_params = [38.2, 43.4, -8, 66.0, 51.6, 1 ,  3] # Poor 원래 옵티말

    gait_params = [38.2, 41.4, -8, 66.0, 51.6, 1 ,  3] # 뉴 옵티말
    # gait_params = [38.2, 39.4, -8, 66.0, 51.6, 1 ,  3] # Poor -
    # gait_params = [38.2, 43.4, -8, 66.0, 51.6, 1 ,  3] # Poor +


    J(gait_type, gait_params[0], gait_params[1], gait_params[2], gait_params[3], 
                                        gait_params[4],gait_params[5],gait_params[6])



if __name__ == "__main__":
        main5()