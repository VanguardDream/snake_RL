import mujoco_py

#load model from path
snake = mujoco_py.load_model_from_path("../description/mujoco/snake_dgistV2.xml")

sim = mujoco_py.MjSim(snake)
# sim_view = mujoco_py.MjViewer(sim)

joint_names = sim.model.joint_names[1:]

sim_state = sim.get_state()

# for k in range(1000):
#     if k % 1000 > 500:
#         sim.data.ctrl[1] = -1
#     else:
#         sim.data.ctrl[1] = 1

#     if k % 100 == 0:
#         print(sim.data.get_body_xquat('head'))

#     sim.step()
#     sim_view.render()
    
