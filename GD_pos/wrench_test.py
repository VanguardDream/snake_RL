
# import mediapy as media
import mujoco
import mujoco.viewer
from scipy.io import savemat

# from mujoco import mjx

import time
import numpy as np
import itertools

from scipy.spatial.transform import Rotation
from multiprocessing import Process, Queue, shared_memory


import mjx_grid_search

snake = mujoco.MjModel.from_xml_path("../dmc/models/env_snake_v1.xml")
data = mujoco.MjData(snake)
mujoco.mj_forward(snake, data)

t = time.time()
with mujoco.viewer.launch_passive(snake, data) as viewer:
    for i in range(100):
        time_step = time.time()
        data.ctrl= np.zeros(14) + np.array(([3]+[0]*13))

        mujoco.mj_step(snake, data)
        viewer.sync()

        while snake.opt.timestep - 0.5*(time.time() - time_step) > 0:
            time.sleep(0)

robot_quats = np.empty((0,4))
for name in ["head","link1","link2","link3","link4","link5","link6","link7","link8","link9","link10","link11","link12","link13","tail"]:
    # np.append(robot_quats, data.body(name).xquat, axis= 1)
    robot_quats = np.vstack((robot_quats, data.body(name).xquat))

robot_quats = robot_quats[:, [1, 2, 3, 0]]

robot_rot = Rotation(robot_quats)

print(robot_rot.mean().as_rotvec(True))