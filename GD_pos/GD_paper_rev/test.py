import serpenoid

import mujoco
import mujoco.viewer
import mediapy as media
from scipy.io import savemat

import time
import numpy as np
import itertools
import serpenoid

from scipy.spatial.transform import Rotation
from multiprocessing import Process, Queue, shared_memory

def randomize_parameter_rad() -> np.ndarray:

    amp_d = np.random.randint(1,15) / 10 # Radian
    amp_l = np.random.randint(1,15) / 10 # Radian
    psi_d = np.random.randint(0,17) / 16 * np.pi # Radian
    psi_l = np.random.randint(0,17) / 16 * np.pi # Radian
    nu_d = np.random.randint(1,61) / 10  # Radian
    nu_l = np.random.randint(1,61) / 10  # Radian
    delta = np.random.randint(0,17) / 16 * np.pi

    return np.array([amp_d, amp_l, psi_d, psi_l, nu_d, nu_l, delta])

def randomize_parameter_deg() -> np.ndarray:

    amp_d = np.random.randint(1,17) * 5 # Degree
    amp_l = np.random.randint(1,17) * 5 # Degree
    psi_d = np.random.randint(0,19) * 10 # Degree
    psi_l = np.random.randint(0,19) * 10 # Degree
    nu_d = np.random.randint(1,61) / 10  # Degree
    nu_l = np.random.randint(1,61) / 10  # Degree
    delta = np.random.randint(0,19) * 10 # Degree

    return np.array([amp_d, amp_l, psi_d, psi_l, nu_d, nu_l, delta])

def sim_start() -> None:
    global data, snake
    data = mujoco.MjData(snake)

    l_bar = randomize_parameter_deg()

    # gait = serpenoid.Gait((45, 45, 30, 30, 60, 30, 0, 0.05), (l_bar[0], l_bar[1], l_bar[2], l_bar[3], l_bar[4], l_bar[5], l_bar[6], 0.05))
    gait = serpenoid.Gait((45, 45, 45, 45, 120, 120, 0, 0.05), (45, 45, 45, 45, 120, 120, 0, 0.05))

    q = gait.Gk
    print(q.shape)

    with mujoco.viewer.launch_passive(snake, data) as viewer:
        # time_start_sim = time.time()
        # for t in range(1401):
        #     time_step = time.time()
        #     slot = t // 10
        #     data.ctrl= q[slot,:]

        #     mujoco.mj_step(snake, data)

        #     viewer.sync()

        #     while snake.opt.timestep - (time.time() - time_step) > 0:
        #         time.sleep(0)
        #         pass

        time_start_sim = time.time()
        step = 0
        for k in range(8000):
            time_step = time.time()
            if k % 10 == 0 and k != 0:
                step += 1

            # Motion Matrix
            index = np.nonzero(gait.Gk[:,step])

            for idx in index:
                data.ctrl[idx] = gait.Gk[idx,step]

            # # Serpenoid
            # data.ctrl = gait.CurveFunction[:,step]

            mujoco.mj_step(snake, data)

            viewer.sync()

        # for i in q.transpose():
        #     time_step = time.time()
        #     index = np.nonzero(i)

        #     for idx in index:
        #         data.ctrl[idx] = i[idx]

        #     mujoco.mj_step(snake, data)

        #     viewer.sync()

            while snake.opt.timestep - (time.time() - time_step) > 0:
                time.sleep(0)

    print(time.time() - time_start_sim)

def param2filename(params:np.ndarray)->str:
    f_name = str(params)
    f_name = f_name.replace(',','')
    f_name = f_name.replace(' ','x')
    f_name = f_name.replace('[','')
    f_name = f_name.replace(']','')
    f_name = f_name.replace('.','_')

    return f_name

def J(parameters:np.ndarray, parameters_bar:np.ndarray, visual:bool = False, savelog:bool = False) -> np.ndarray:
    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)
    mujoco.mj_forward(snake, data)

    f_name = param2filename(parameters)

    gait = serpenoid.Gait(tuple(parameters), tuple(parameters_bar))

    q = gait.Gk
    
    p_head = np.empty((0,7))
    step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[28:32].copy()))
    p_head = np.vstack((p_head, step_data))

    t_start = time.time()
    if visual:
        with mujoco.viewer.launch_passive(snake, data) as viewer:
            for i in q.transpose():
                index = np.nonzero(i)
                for idx in index:
                    data.ctrl[idx] = i[idx]
                
                for _ in range(9):
                    time_step = time.time()
                    mujoco.mj_step(snake, data)
                    viewer.sync()

                    while snake.opt.timestep - (time.time() - time_step) > 0:
                        time.sleep(0)

                step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[28:32].copy()))
                p_head = np.vstack((p_head, step_data))

        t_end = time.time()

        print(t_end - t_start)
    
    else: # no visual
        renderer = mujoco.Renderer(snake)
        frames = []
        time_start_sim = time.time()
        for i in q:
            data.ctrl= i

            mujoco.mj_step(snake, data)

            step_data = np.hstack((data.body('head').xpos.copy(), data.sensordata[48:52].copy()))
            p_head = np.vstack((p_head, step_data))

            if savelog:
                renderer.update_scene(data)
                pixel = renderer.render()

                frames.append(pixel)

        if savelog:
            media.write_video(f_name+g+'.mp4',frames, fps=100)
    
    if savelog and not(visual):
        sim_data = {g+"_trajectory_"+f_name: p_head}
        savemat("trajectory_"+g+f_name+'.mat',sim_data)

if __name__ == "__main__":
    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)

    J((45, 45, 45, 45, 120, 120, 0, 0.05),(45, 45, 45, 45, 120, 120, 0, 0.05),True,False)
    # gait = serpenoid.Gait((45, 45, 45, 45, 120, 120, 0, 0.05), (45, 45, 45, 45, 120, 120, 0, 0.05))
    # sim_start()
