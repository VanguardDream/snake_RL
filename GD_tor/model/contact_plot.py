import numpy as np
import mujoco
import mujoco.viewer
import mediapy as media

import time
import serpenoid
import serpenoid_gamma


def varying_xml(val:list):
    txt_xml = f"""
    <mujoco model="contact testing">
        <option timestep="0.005"/>
        <size memory="1000M"/>

        <asset>
            <texture type="skybox" builtin="gradient" width="512" height="512" rgb1=".4 .6 .8" rgb2="0 0 0"/>
            <texture name="texgeom" type="cube" builtin="flat" mark="cross" width="128" height="128"
                    rgb1="0.6 0.6 0.6" rgb2="0.6 0.6 0.6" markrgb="1 1 1"/>
            <texture name="texplane" type="2d" builtin="checker" rgb1=".4 .4 .4" rgb2=".6 .6 .6"
                    width="512" height="512"/>
            <material name="MatPlane" reflectance="0.0" texture="texplane" texrepeat="1 1" texuniform="true"
                    rgba=".7 .7 .7 1"/>
            <material name="capsule" texture="texgeom" texuniform="true" rgba=".4 .9 .6 1" />
            <material name="ellipsoid" texture="texgeom" texuniform="true" rgba=".4 .6 .9 1" />
            <material name="box" texture="texgeom" texuniform="true" rgba=".4 .9 .9 1" />
            <material name="cylinder" texture="texgeom" texuniform="true" rgba=".8 .6 .8 1" />
            <material name="sphere" texture="texgeom" texuniform="true" rgba=".9 .1 .1 1" />

            <mesh name="link_collision" file="./assets/link_collision_mesh.STL"/>
        </asset>

        <default>
            <default class="collision-mesh">
                <geom type="mesh" mesh="link_collision" mass="0.165" condim="4" rgba="0.5 0.5 0.5 1.0" priority="1" friction="0.7 0.015 0.001" euler="90 90 0"/>
            </default>
        </default>

        <visual>
            <map force="0.1" zfar="30"/>
            <rgba haze="0.15 0.25 0.35 1"/>
            <quality shadowsize="4096"/>
            <global offwidth="1280" offheight="1280"/>
        </visual>

    <worldbody>
        <!-- solimp default : "0.9 0.95 0.001 0.5 2" // solref default : "0.02 1" -->
        <geom name="floor" type="plane" size="3 3 .5" priority="2" friction="0.55 0.015 0.001" solimp="{val[0]} {val[1]} {val[2]} {val[3]} {val[4]}" solref="{val[5]} {val[6]}" material="MatPlane"/>

        <body name="debris" pos="0 0 0.43655" euler="0 0 0"> 
            <freejoint name="root"/>
            <site name="s_link1_top" type="box" size="0.021 0.038 0.014" pos="0.016 0 0.018" rgba="0.8 0.1 0.2 0.1"/>
            <site name="s_link1_bot" type="box" size="0.021 0.038 0.014" pos="0.016 0 -0.018" rgba="0.8 0.1 0.2 0.1"/>
            <geom class="collision-mesh"/> 
        </body>
    </worldbody>

    <sensor>
        <touch name="top_link1" site="s_link1_top"/>
        <touch name="bot_link1" site="s_link1_bot"/>
    </sensor>

    </mujoco>
    """

    print(txt_xml)
    return txt_xml

# Defaut values imp : 0.9 0.95 0.001 0.5 2, ref : 0.02 1
con_values = [0.1, 0.95, 0.001, 0.5, 2, 0.02, 1]

varying_xml(con_values)


# debris = mujoco.MjModel.from_xml_path("./contact_testing.xml")
# data = mujoco.MjData(debris)
# renderer = mujoco.Renderer(debris, 720, 1280)

# t_step = debris.opt.timestep
# stepspersecond = int(1/t_step)

# frames = []
# contact_force = []
# debris_pos = []

# mujoco.mj_resetData(debris, data)

# mujoco.mj_forward(debris, data)

# for i in range(4*stepspersecond):
#     mujoco.mj_step(debris, data)
#     renderer.update_scene(data)
#     pixel = renderer.render()

#     frames.append(pixel)
#     contact_force.append(data.sensordata[1])
#     debris_pos.append(data.body("debris").xpos[2])
#     # print(data.body("debris").xpos[2])

# # media.show_video(frames, fps=stepspersecond)

# import matplotlib.pyplot as plt

# plt.plot(contact_force[0:50])

# plt.plot(debris_pos[0:50])