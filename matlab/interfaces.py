import sys, os
import matlab.engine
import numpy as np
import mujoco
from mujoco import viewer
import mediapy as media
import matplotlib.pyplot as plt

class snake_gait:
    def __init__(self, gait_type: int = 1, start_k: int = 0):
        self.k = start_k

        if gait_type == 0: #Vertical
            self.M = np.array([[1,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0],
                                [0,1,0,0,0,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,1,0,0,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,1,0,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,0,1,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,0,0,1,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,1],
                                [0,0,0,0,0,0,0]],dtype='int')

        elif gait_type == 1: #Serpentine
            self.M = np.eye(14)

        elif gait_type == 2: #Sidewinding
            self.M = np.array([[0,1,0,0,0,0,0,0,0,0,0,0,0,0],
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

        else:
            self.M = np.ones((14,1))

        self.M_cols = self.M.shape[1]

        self.k = self.k % self.M_cols

    def get_selected_joints(self) -> np.ndarray:
        return self.M[:,self.k]

    def gait_step(self):
        self.k = (self.k + 1) % self.M_cols

def getpath(file:str, path:str):
    return path + file

def simstart():
    filename = ".\\description\\snake_circle_alligned.xml"
    # dirpath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\description\\"

    path = filename

    model = mujoco.MjModel.from_xml_path(path)
    data = mujoco.MjData(model)

    mujoco.mj_forward(model, data)

    SIM_DURATION = 10 # (seconds)
    TIMESTEPS = np.power(10, np.linspace(-2, -4, 5))

    # prepare plotting axes
    _, ax = plt.subplots(1, 1)

    for dt in TIMESTEPS:
        # set timestep, print
        model.opt.timestep = dt

        # allocate
        n_steps = int(SIM_DURATION / model.opt.timestep)
        sim_time = np.zeros(n_steps)
        energy = np.zeros(n_steps)

        # initialize
        mujoco.mj_resetData(model, data)
        data.qvel[0] = 9 # root joint velocity

        # simulate
        print('{} steps at dt = {:2.2g}ms'.format(n_steps, 1000*dt))
        for i in range(n_steps):
            mujoco.mj_step(model, data)
            sim_time[i] = data.time
            energy[i] = data.energy[0] + data.energy[1]

        # plot
        ax.plot(sim_time, energy, label='timestep = {:2.2g}ms'.format(1000*dt))

    # finalize plot
    ax.set_title('energy')
    ax.set_ylabel('Joule')
    ax.set_xlabel('second')
    ax.legend(frameon=True)
    plt.tight_layout()

    # viewer.launch(model)

simstart()