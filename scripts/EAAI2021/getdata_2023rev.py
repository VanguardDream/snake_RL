from re import X
import mujoco_py
import os
import random
import sys
import datetime

from threading import Thread
from scipy.io import savemat

sys.path.append('../') # 상위 폴더의 Gait 객체를 불러오기 위해서...
# import gait_lambda # 이전 Gait 객체
import gait as gait_lambda # SVM을 위해서 새롭게 개선된 Gait 객체

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

def main2(): #xy 경로 생성
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
    # gait_type = 1
    # gait_params = [39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1] #EAAI Serp

    gait_type = 2
    gait_params = [52.76,319.65,1.99,72.07,262.95,7.91,1] #EAAI side 2nd try
    
    count = 0

    csv_log = open('side_grid_11_3_3.csv','w')
    csv_writer = csv.writer(csv_log)

    for i0 in range(-5,6): # d_a
        for i1 in range(-5,6): # d_p
            for i2 in range (-5,6):
                for i3 in range(-5,6):
                    test_params = [gait_params[0] + i0 * 0.3, gait_params[1] + i1 * 0.3, gait_params[2], gait_params[3] + i2 * 0.3, gait_params[4] + i3 * 0.3, gait_params[5], gait_params[6] ]

                    reward = J(gait_type, round(test_params[0],2), round(test_params[1],2), test_params[2], round(test_params[3],2), 
                                                round(test_params[4],2),test_params[5],test_params[6])

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

def main5():
    #20230720 논문 재작성 실험을 위해서
    # gait_type = 1
    # gait_params = [39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1]  #EAAI
    # gait_params = [40.7, 191.1, -9.1, 66.5, 160.9, 7.0, 1]  #CG1
    # gait_params = [39.8, 189.9, -9.1, 67.1, 160.3, 7.0, 1]  #CG1

    
    # gait_type = 2
    # gait_params = [52.76,	319.65,	1.99, 72.07, 262.95, 7.91, 1] # EAAI 263.95? 둘중하나
    # gait_params = [52.16,	318.15,	1.99,	72.07,	262.95,	7.91,	1] #EAAI c1
    # gait_params = [52.76,	319.65,	1.99,	72.67,	261.75,	7.91,	1] #EAAI c2

    num_sims = 10
    obj_sims = []
    # gait_params = np.array([1, 39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1])

    result_data_mat = np.empty((41,73,41,73))

    for idx in range(num_sims):
        obj_sims.append(mujoco_py.MjSim(snake))

    def do_sim(sim :mujoco_py.MjSim, start:np.ndarray, end:np.ndarray):

        internal_result = np.empty((41,73,41,73))

        for p1 in range(start[0], end[0]):
            for p2 in range(start[1], end[1]):
                for p3 in range(start[2], end[2]):
                    p4_start = datetime.datetime.now()
                    for p4 in range(start[3], end[3]):
                        params = np.array([])

                        params = np.array([1, 20 + p1, p2 * 5, -9.1, 20 + p3, p4 * 5, 7.0, 1])
                        gen = gait_lambda.gait(params[0], params[1], params[2], params[3], params[4], params[5], params[6], int(params[7]))
                        g = params[0]

                        # Variable for cost(loss) function
                        delta_x = 0
                        delta_y = 0
                        penalty = 0

                        for i in range(0,1000):
                            goal = gen.generate(i)

                            spec_motor = np.nonzero(goal)[0]

                            for idx in spec_motor:
                                # Commnad motor here
                                sim.data.ctrl[idx] = gen.degtorad(goal[idx])
                            
                            try:
                                sim.step()
                            except:
                                print("Doing step occur exception!! add penalty")
                                penalty = -10000
                                break


                        delta_x = sim.data.get_body_xpos('head')[0]
                        delta_y = sim.data.get_body_xpos('head')[1]

                        sim.reset()
                        #Calculate Cost here
                        if (g == 2):
                            J_value = 1500 * delta_y - 800 * abs(delta_x) - 900 * abs(delta_x / delta_y) + penalty
                        else:
                            J_value = 1500 * delta_x - 800 * abs(delta_y) - 900 * abs(delta_y / delta_x) + penalty

                        # result_data_mat[p1,p2,p3,p4] = J_value
                        internal_result[p1,p2,p3,p4] = J_value

                    print(str(sim)+" last loop done : " + str(datetime.datetime.now()-p4_start))

        print(str(sim) + " done!")
        finished_time = datetime.datetime.now()
        fname = finished_time.strftime(str(sim)+"grid_result_%Y%m%d-%H%M%S.mat")
        m_dict = {'U' : internal_result}
        savemat(fname, m_dict)


    # do_sim(obj_sims[0],[0,0,0,0], [2,2,2,2], num_done, result_data_mat)
    # ((41,73,41,73))

    th0 = Thread(target=do_sim, args=(obj_sims[0], [3, 72, 0, 0], [4, 73, 41, 73]))
    th1 = Thread(target=do_sim, args=(obj_sims[1], [7, 72, 0, 0], [8, 73, 41, 73]))
    th2 = Thread(target=do_sim, args=(obj_sims[2], [11, 72, 0, 0], [12, 73, 41, 73]))
    th3 = Thread(target=do_sim, args=(obj_sims[3], [15, 72, 0, 0], [16, 73, 41, 73]))
    th4 = Thread(target=do_sim, args=(obj_sims[4], [19, 72, 0, 0], [20, 73, 41, 73]))
    th5 = Thread(target=do_sim, args=(obj_sims[5], [23, 72, 0, 0], [24, 73, 41, 73]))
    th6 = Thread(target=do_sim, args=(obj_sims[6], [27, 72, 0, 0], [28, 73, 41, 73]))
    th7 = Thread(target=do_sim, args=(obj_sims[7], [31, 72, 0, 0], [32, 73, 41, 73]))
    th8 = Thread(target=do_sim, args=(obj_sims[8], [35, 72, 0, 0], [36, 73, 41, 73]))
    th9 = Thread(target=do_sim, args=(obj_sims[9], [40, 72, 0, 0], [41, 73, 41, 73]))

    # th0 = Thread(target=do_sim, args=(obj_sims[0], [0,0,0,0], [4,7,4,7]))
    # th1 = Thread(target=do_sim, args=(obj_sims[1], [4,7,4,7], [8,14,8,14]))
    # th2 = Thread(target=do_sim, args=(obj_sims[2], [8,14,8,14], [12,21,12,21]))
    # th3 = Thread(target=do_sim, args=(obj_sims[3], [12,21,12,21], [16,28,16,28]))
    # th4 = Thread(target=do_sim, args=(obj_sims[4], [16,28,16,28], [20,35,20,35]))
    # th5 = Thread(target=do_sim, args=(obj_sims[5], [20,35,20,35], [24,42,24,42]))
    # th6 = Thread(target=do_sim, args=(obj_sims[6], [24,42,24,42], [28,49,28,49]))
    # th7 = Thread(target=do_sim, args=(obj_sims[7], [28,49,28,49], [32,56,32,56]))
    # th8 = Thread(target=do_sim, args=(obj_sims[8], [32,56,32,56], [36,63,36,63]))
    # th9 = Thread(target=do_sim, args=(obj_sims[9], [36,63,36,63], [41,73,41,73]))

    th0.start()
    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th5.start()
    th6.start()
    th7.start()
    th8.start()
    th9.start()

    th0.join()
    th1.join()
    th2.join()
    th3.join()
    th4.join()
    th5.join()
    th6.join()
    th7.join()
    th8.join()
    th9.join()

    # finished_time = datetime.datetime.now()
    # fname = finished_time.strftime("grid_result_%Y%m%d-%H%M%S.mat")
    # m_dict = {'U' : result_data_mat}
    # savemat(fname, m_dict)




if __name__ == "__main__":
        import time

        print('Sim start...')
        t_start = time.time()
        main5()
        print(time.time-t_start)