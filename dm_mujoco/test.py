import mujoco
from mujoco import viewer
import mediapy as media

model = mujoco.MjModel.from_xml_path('./models/snake_circle_alligned.xml')
renderer = mujoco.Renderer(model)
data = mujoco.MjData(model)

mujoco.mj_forward(model, data)
renderer.update_scene(data)
media.show_image(renderer.render())