model_xml = \
    """

    <mujoco model="2link-test">

        <compiler inertiafromgeom="true" angle="degree" convexhull="false"/>

        <option timestep="0.01" iterations="50" tolerance="1e-10" solver="Newton" jacobian="dense" cone="pyramidal"/>
        <!-- <option timestep="0.001" iterations="50" tolerance="1e-10" solver="Newton" jacobian="dense" cone="pyramidal"/> -->

        <!-- <size nconmax="5000" njmax="20000" nstack="50000"/> -->
        <size nconmax="500" njmax="2000" nstack="10000"/>

        <visual>
            <map force="0.1" zfar="30"/>
            <rgba haze="0.15 0.25 0.35 1"/>
            <quality shadowsize="2048"/>
            <global offwidth="800" offheight="800"/>
        </visual>

        <asset>
            <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="512"/> 

            <texture name="texplane" type="2d" builtin="checker" rgb1=".2 .3 .4" rgb2=".1 0.15 0.2" width="512" height="512" mark="cross" markrgb=".8 .8 .8"/>  

            <texture name="texgeom" type="cube" builtin="flat" mark="cross" width="127" height="1278" 
                rgb1="0.8 0.6 0.4" rgb2="0.8 0.6 0.4" markrgb="1 1 1" random="0.01"/>  

            <material name="matplane" reflectance="0.3" texture="texplane" texrepeat="1 1" texuniform="true"/>

            <material name="matgeom" texture="texgeom" texuniform="true" rgba="0.8 0.6 .4 1"/>

        </asset>

        <worldbody>

            <geom name="floor" pos="0 0 0" size="0 0 .25" type="plane" material="matplane" condim="3" />

            <light directional="false" diffuse=".2 .2 .2" specular="0 0 0" pos="0 0 5" dir="0 0 -1" castshadow="false"/>

        <!-- Snake -->
            <body name="base" pos="0 0 0">
                <geom type="cylinder" size="0.0325 0.01" rgba="0.1 0.1 0.1 1" mass="0.04"/>
                <geom type="box" size="0.017 0.01425 0.02525" pos="0 0 0.01525" mass="0.1"/>

                <body name="link1" pos="0 0 0.0685">
                    <joint name="joint1" type="hinge" pos="0 0 -0.02925" axis="0 1 0" limited="true" range="-90 90" damping="{damping}" stiffness="0" armature="0.05" />
                    <geom type="cylinder" size="0.0325 0.01" rgba="0.1 0.1 0.1 1" mass="0.04"/>
                    <geom type="box" size="0.01425 0.017 0.02525" pos="0 0 0.01525" mass="0.1"/>
                </body>
            </body>
        </worldbody>

        <actuator>
            {actuator}
        </actuator>
    </mujoco>
    """

p_controller = \
    """
            <position name="servo_1" ctrllimited="true" ctrlrange="-1.5708 1.5708" forcelimited="true" forcerange="-3.7 3.7" gear="1" joint="joint1" kp="3.77"/>
    """

pid_controller = \
    """
            <general ctrlrange='-1 1' gaintype="user" biastype="user" forcerange="-3.7 3.7" gainprm="200 10 10.0 0.1 0.1 0" joint="joint1" name="servo_1"/>
    """