import sys
import datetime
import mujoco
import mujoco_viewer
import numpy as np
import gait_lambda

sys.path.append('../') # 상위 폴더의 Gait 객체를 불러오기 위해서...

snake = mujoco.MjModel.from_xml_path(str("../../description/mujoco/snake_dgist_friction_chgd.xml"))

from threading import Thread
from scipy.io import savemat

def J(g, d_a, d_p, d_l, l_a, l_p, l_l, tau):
    instance_data = mujoco.MjData(snake)
    viewer = mujoco_viewer.MujocoViewer(snake, instance_data)

    gen = gait_lambda.gait(g, d_a, d_p, d_l, l_a, l_p, l_l, int(tau))

    # Variable for cost(loss) function
    delta_x = 0
    delta_y = 0

    mujoco.mj_forward(snake, instance_data)
    for i in range(0,1000):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            # Commnad motor here

            instance_data.ctrl[idx] = gen.degtorad(goal[idx])
        
        mujoco.mj_step(snake,instance_data)
        viewer.render()


        delta_x = instance_data.body('head').xpos[0]
        delta_y = instance_data.body('head').xpos[1]

    mujoco.mj_resetData(snake,instance_data)
    #Calculate Cost here

    if (g == 2):
        J_value = 1500 * delta_y - 800 * abs(delta_x) - 900 * abs(delta_x / delta_y)
    else:
        J_value = 1500 * delta_x - 800 * abs(delta_y) - 900 * abs(delta_y / delta_x)

    return [delta_x, delta_y, J_value]


if __name__ == "__main__":

    [x, y, result] = J(1, 39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1)
    
    print(x)
    print(y)
    print(result)