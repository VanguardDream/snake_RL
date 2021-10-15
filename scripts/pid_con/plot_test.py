import mujoco_py
import matplotlib

def main():
    #import model xml
    model = mujoco_py.load_model_from_path("../description/mujoco/2link_dynamixel_test.xml")

    sim = mujoco_py.MjSim(model)

def sim_config():
    