import serpenoid

import mujoco
import mujoco.viewer
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


if __name__ == "__main__":
    snake = mujoco.MjModel.from_xml_path("./resources/env_snake_v1_contact_servo.xml")
    data = mujoco.MjData(snake)
    sim_start()
