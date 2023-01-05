import mujoco
from mujoco import viewer
import mediapy as media

import numpy as np

model = mujoco.MjModel.from_xml_path('./models/snake_circle_alligned.xml')
renderer = mujoco.Renderer(model)
data = mujoco.MjData(model)

ctrl = np.array([1]*14)
data.ctrl = ctrl

viewer.launch(model,data)

# print("can access over here?")