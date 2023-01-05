import mujoco
from mujoco import viewer
import mediapy as media

model = mujoco.MjModel.from_xml_path('./models/snake_circle_alligned.xml')
renderer = mujoco.Renderer(model)
data = mujoco.MjData(model)

ctx = mujoco.GLContext(1280, 720)
ctx.make_current()