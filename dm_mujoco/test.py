import mujoco
from mujoco import viewer
import mediapy as media

import numpy as np

def gait_control(model : mujoco.MjModel, data : mujoco.MjData):
    ctrl = np.random.rand(14) * 3 - 1.5
    data.ctrl = ctrl

    print(data.time)

def load_callback(m=None, d=None):
  # Clear the control callback before loading a new model
  # or a Python exception is raised
  mujoco.set_mjcb_control(None)

  m = mujoco.MjModel.from_xml_path('./models/snake_circle_alligned.xml')
  d = mujoco.MjData(m)

  if m is not None:
    mujoco.set_mjcb_control(lambda m, d: gait_control(m, d))

  return m, d

model = mujoco.MjModel.from_xml_path('./models/snake_circle_alligned.xml')
renderer = mujoco.Renderer(model)
data = mujoco.MjData(model)


viewer.launch(loader=load_callback)
