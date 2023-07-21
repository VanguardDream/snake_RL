from re import X
import os
import sys
import datetime
import mujoco
import numpy as np
import gait as gait_lambda # SVM을 위해서 새롭게 개선된 Gait 객체

sys.path.append('../') # 상위 폴더의 Gait 객체를 불러오기 위해서...

snake = mujoco.MjModel.from_xml_path(str("../../description/mujoco/snake_dgist.xml"))

from threading import Thread
from scipy.io import savemat

def do_sim(ins_idx:int, start:np.ndarray, end:np.ndarray):
    instance_data = mujoco.MjData(snake)
    internal_result = np.empty((41, 72, 41, 72))

    for p1 in range(start[0], end[0]):
        for p2 in range(start[1], end[1]):
            p3_start = datetime.datetime.now()
            for p3 in range(start[2], end[2]):
                # p4_start = datetime.datetime.now()
                for p4 in range(start[3], end[3]):
                    params = np.array([])

                    params = np.array([1, 20 + p1, p2 * 5, -9.1, 20 + p3, p4 * 5, 7.0, 1])
                    gen = gait_lambda.gait(params[0], params[1], params[2], params[3], params[4], params[5], params[6], int(params[7]))
                    g = params[0]

                    # Variable for cost(loss) function
                    delta_x = 0
                    delta_y = 0
                    penalty = 0

                    mujoco.mj_forward(snake, instance_data)

                    for i in range(0,1000):
                        goal = gen.generate(i)

                        spec_motor = np.nonzero(goal)[0]

                        for idx in spec_motor:
                            # Commnad motor here
                            instance_data.ctrl[idx] = gen.degtorad(goal[idx])
                        
                        try:
                            mujoco.mj_step(snake, instance_data)
                        except:
                            print("Doing step occur exception!! add penalty")
                            penalty = -10000
                            break
                                
                    delta_x = instance_data.body('head').xpos[0]
                    delta_y = instance_data.body('head').xpos[1]

                    mujoco.mj_resetData(snake,instance_data)
                    #Calculate Cost here
                    if (g == 2):
                        J_value = 1500 * delta_y - 800 * abs(delta_x) - 900 * abs(delta_x / delta_y) + penalty
                    else:
                        J_value = 1500 * delta_x - 800 * abs(delta_y) - 900 * abs(delta_y / delta_x) + penalty

                    # result_data_mat[p1,p2,p3,p4] = J_value
                    internal_result[p1,p2,p3,p4] = J_value

                # print(str(ins_idx) + " last loop done : " + str(datetime.datetime.now() - p4_start))
            print(str(ins_idx) + " Third loop done : " + str(datetime.datetime.now() - p3_start))

    print("sim done!")
    finished_time = datetime.datetime.now()
    fname = finished_time.strftime(str(ins_idx)+"-grid_result_%Y%m%d-%H%M%S.mat")
    m_dict = {'U' + str(ins_idx) : internal_result}
    savemat(fname, m_dict)


#20230720 논문 재작성 실험을 위해서
# gait_type = 1
# gait_params = [39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1]  #EAAI
# gait_params = [40.7, 191.1, -9.1, 66.5, 160.9, 7.0, 1]  #CG1
# gait_params = [39.8, 189.9, -9.1, 67.1, 160.3, 7.0, 1]  #CG1


# gait_type = 2
# gait_params = [52.76,	319.65,	1.99, 72.07, 262.95, 7.91, 1] # EAAI 263.95? 둘중하나
# gait_params = [52.16,	318.15,	1.99,	72.07,	262.95,	7.91,	1] #EAAI c1
# gait_params = [52.76,	319.65,	1.99,	72.67,	261.75,	7.91,	1] #EAAI c2

# mujoco.mj_forward(snake,snake_data)
# gait_params = np.array([1, 39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1])

if __name__ == "__main__":
    from multiprocessing import Process
    # ((41,73,41,73))

    th0  = Process(target=do_sim, args=( 0, np.array([ 0, 0, 0, 0]), np.array([ 3, 72, 41, 72]), ))
    th1  = Process(target=do_sim, args=( 1, np.array([ 3, 0, 0, 0]), np.array([ 6, 72, 41, 72]), ))
    th2  = Process(target=do_sim, args=( 2, np.array([ 6, 0, 0, 0]), np.array([ 9, 72, 41, 72]), ))
    th3  = Process(target=do_sim, args=( 3, np.array([ 9, 0, 0, 0]), np.array([12, 72, 41, 72]), ))
    th4  = Process(target=do_sim, args=( 4, np.array([12, 0, 0, 0]), np.array([15, 72, 41, 72]), ))
    th5  = Process(target=do_sim, args=( 5, np.array([15, 0, 0, 0]), np.array([18, 72, 41, 72]), ))
    th6  = Process(target=do_sim, args=( 6, np.array([18, 0, 0, 0]), np.array([21, 72, 41, 72]), ))
    th7  = Process(target=do_sim, args=( 7, np.array([21, 0, 0, 0]), np.array([24, 72, 41, 72]), ))
    th8  = Process(target=do_sim, args=( 8, np.array([24, 0, 0, 0]), np.array([27, 72, 41, 72]), ))
    th9  = Process(target=do_sim, args=( 9, np.array([27, 0, 0, 0]), np.array([30, 72, 41, 72]), ))
    th10 = Process(target=do_sim, args=(10, np.array([30, 0, 0, 0]), np.array([33, 72, 41, 72]), ))
    th11 = Process(target=do_sim, args=(11, np.array([33, 0, 0, 0]), np.array([36, 72, 41, 72]), ))
    th12 = Process(target=do_sim, args=(12, np.array([36, 0, 0, 0]), np.array([39, 72, 41, 72]), ))
    th13 = Process(target=do_sim, args=(13, np.array([39, 0, 0, 0]), np.array([41, 72, 41, 72]), ))

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
    th10.start()
    th11.start()
    th12.start()
    th13.start()

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
    th10.join()
    th11.join()
    th12.join()
    th13.join()

    # finished_time = datetime.datetime.now()
    # fname = finished_time.strftime("grid_result_%Y%m%d-%H%M%S.mat")
    # m_dict = {'U' : result_data_mat}
    # savemat(fname, m_dict)
