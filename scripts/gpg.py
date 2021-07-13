# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : BRM snake robot main simulation script

import mujoco_py
import os
import random
import gait
import numpy as np

#load model from path
snake = mujoco_py.load_model_from_path("../description/mujoco/snake_allign.xml")

# mujoco-py
simulator = mujoco_py.MjSim(snake)
sim_viewer = mujoco_py.MjViewer(simulator)

def J(g,d_a,d_p,l_a,l_p,tau):
    gen = gait.gait(g,d_a,d_p,l_a,l_p,tau)

    # Variable for cost(loss) function
    delta_x = 0
    delta_y = 0
    accum_theta = 0

    # Simulation model info
    joint_names = simulator.model.joint_names[1:] 

    for i in range(0,1000):
        g = gen.generate(i)

        spec_motor = np.nonzero(g)

        for idx in spec_motor:
            # Commnad motor here
            if not(len(idx) == 0):
                simulator.data.ctrl[idx] = gen.degtorad(g[idx])
        
        for name in joint_names:
            accum_theta = accum_theta + abs(simulator.data.get_joint_qpos(name))

        simulator.step()
        sim_viewer.render()

    simulator.reset()

    #Calculate Cost here
    return 10 * delta_x - 5 * delta_y - 0.0003 * accum_theta



def main():
    for i in range(5):
        print(J(0,30,150,30,150,4))


if __name__ == "__main__":
    main()
