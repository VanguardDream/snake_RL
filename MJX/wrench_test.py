import jax
import mediapy as media
import mujoco
import mujoco.viewer
from scipy.io import savemat

from mujoco import mjx

import time
import numpy as np
import itertools

from scipy.spatial.transform import Rotation
from multiprocessing import Process, Queue, shared_memory


import mjx_grid_search

snake = mujoco.MjModel.from_xml_path("../dmc/models/snake_circle_contact.xml")
data = mujoco.MjData(snake)
mujoco.mj_forward(snake, data)

t = time.time()
with mujoco.viewer.launch_passive(snake, data) as viewer:
    for i in range(500):
        time_step = time.time()
        data.ctrl= np.ones(14) * 1.5

        mujoco.mj_step(snake, data)
        viewer.sync()

        while snake.opt.timestep - 0.5*(time.time() - time_step) > 0:
            time.sleep(0)