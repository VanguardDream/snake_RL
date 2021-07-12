import mujoco_py

#load model from path
snake = mujoco_py.load_model_from_path("../description/mujoco/snake.xml")

sim = mujoco_py.MjSim(snake)
sim_view = mujoco_py.MjViewer(sim)

joint_names = sim.model.joint_names[1:]

sim_state = sim.get_state()