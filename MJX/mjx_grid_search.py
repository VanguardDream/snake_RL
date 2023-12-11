import jax
import mediapy as media
import mujoco
import mujoco.viewer
from scipy.io import savemat

from mujoco import mjx

import time
import numpy as np

m_serp = np.eye(14)

m_side = np.array([[0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                    [0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,0,0,0,0,0,0,1,0]],dtype='int')

t = np.arange(0,14,0.01)
# amp_dor = 80
# amp_lat = 80
# omega_dor = 4
# omega_lat = 4
# nu_dor = 1
# nu_lat = 1
# phi = 0

#load model from path
snake = mujoco.MjModel.from_xml_path("../description/mujoco/snake_dgist.xml")
data = mujoco.MjData(snake)

def make_ref_input(t, amp_dor, amp_lat, omega_dor, omega_lat, nu_dor, nu_lat, phi) -> np.ndarray:
    link_n = np.arange(1,15,1)
    amp_n = np.tile([amp_dor, amp_lat], 7)
    omega_n = np.tile([omega_dor, omega_lat], 7)
    nu_n = np.tile([nu_dor, nu_lat], 7)
    phi_n = np.tile([0, phi], 7)

    temporal = np.outer(t, omega_n)

    u_input = np.sin(temporal + nu_n * link_n) * amp_n + phi_n

    return u_input.copy()

def make_gait_input(u_input:np.ndarray, gait_mat:np.ndarray) -> np.ndarray:
    actual_input = np.zeros((u_input.shape[0] + 1, u_input.shape[1]))

    for i in range(actual_input.shape[0]-1):
        actual_input[i+1,:] = actual_input[i,:]
        non_zero_idx = np.squeeze(np.nonzero(gait_mat[i % gait_mat.shape[0],:]))
        actual_input[i+1,non_zero_idx] = u_input[i, non_zero_idx]

    return actual_input.copy()

def randomize_parameter() -> np.ndarray:

    a_d = np.random.randint(1,15) / 10 # Radian
    a_l = np.random.randint(1,15) / 10 # Radian
    o_d = np.random.randint(1,17) / 8 * np.pi # Radian
    o_l = np.random.randint(1,17) / 8 * np.pi # Radian
    n_d = np.random.randint(1,17) / 8 * np.pi # Radian
    n_l = np.random.randint(1,17) / 8 * np.pi # Radian
    # p = np.random.randint(1,17) / 8 * np.pi
    p = 0 # Radian

    return np.array([a_d, a_l, o_d, o_l, n_d, n_l, p])

def sim_start() -> None:
    global data, snake
    data = mujoco.MjData(snake)

    random_parameter = randomize_parameter()
    print(random_parameter)
    q = make_gait_input(make_ref_input(t, random_parameter[0], random_parameter[1], random_parameter[2], random_parameter[3], random_parameter[4], random_parameter[5], random_parameter[6]), m_serp)
    # q = make_gait_input(make_ref_input(t, amp_dor, amp_lat, omega_dor, omega_lat, nu_dor, nu_lat, phi), m_side)

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
        for i in q:
            time_step = time.time()
            data.ctrl= i

            mujoco.mj_step(snake, data)

            viewer.sync()

            while snake.opt.timestep - (time.time() - time_step) > 0:
                time.sleep(0)
                pass

    print(time.time() - time_start_sim)

def J(t, parameters:np.ndarray, m:np.ndarray, visual = False) -> float:
    global snake, data
    data = mujoco.MjData(snake)
    mujoco.mj_forward(snake, data)

    q = make_gait_input(make_ref_input(t, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6]), m)

    if visual:
        with mujoco.viewer.launch_passive(snake, data) as viewer:
            time_start_sim = time.time()
            for i in q:
                time_step = time.time()
                data.ctrl= i

                mujoco.mj_step(snake, data)

                viewer.sync()

                while snake.opt.timestep - (time.time() - time_step) > 0:
                    time.sleep(0)
    else:
        renderer = mujoco.Renderer(snake)
        frames = []
        time_start_sim = time.time()
        for i in q:
            data.ctrl= i

            mujoco.mj_step(snake, data)
            renderer.update_scene(data)
            pixel = renderer.render()

            frames.append(pixel)

    print(time.time() - time_start_sim)

    media.write_video('1.mp4',frames, fps=100)

    return 0

### Main script
params = np.array([1.3, 0.6, 5.50, 0.79, 5.90, 6.30, 0])

J(t, params, m_serp, False)

# J(t, params, m_side, True)


