import sys, os
# import matlab.engine
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

gait = snake_gait(gait_type=2)

def gait_control(model : mujoco.MjModel, data : mujoco.MjData):
    u = gait.get_selected_joints() * (np.random.random((1,1)) - 0.5) * 6
    u = u.squeeze()
    idx = int(np.nonzero(u)[0])
    gait.gait_step()

    data.ctrl[idx] = u[idx]


def load_cb(model : mujoco.MjModel = None , data : mujoco.MjData = None ):
    mujoco.set_mjcb_control(None)

    filename = ".\\description\\snake_circle.xml"
    path = filename

    model = mujoco.MjModel.from_xml_path(path)
    data = mujoco.MjData(model)

    if model is not None:
        mujoco.set_mjcb_control(lambda model, data: gait_control(model, data))

    return model, data

viewer.launch(loader=load_cb)