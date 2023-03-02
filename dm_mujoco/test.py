import mujoco
from mujoco import viewer
import mediapy as media

import numpy as np

def gait_control(model : mujoco.MjModel, data : mujoco.MjData):
    ctrl = np.random.rand(14) * 3 - 1.5
    data.ctrl = ctrl

def load_callback(m=None, d=None):
  global model, data
  mujoco.set_mjcb_control(None)

  m = model
  d = data

  if m is not None:
    mujoco.set_mjcb_control(lambda m, d: gait_control(m, d))

  return m, d

if __name__ == "__main__":
  model = mujoco.MjModel.from_xml_path('./models/snake_circle_alligned.xml')
  renderer = mujoco.Renderer(model)
  data = mujoco.MjData(model)

  viewer.launch(loader=load_callback)
