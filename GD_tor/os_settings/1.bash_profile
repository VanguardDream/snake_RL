# ROS2 setup
source /opt/ros/iron/setup.zsh

# Colcon (ROS2) workspace source
source /home/bong/project/snake_RL/GD/horcrux_ws/install/local_setup.zsh #This ws is not main just local one

# Colcon build tool settings
source /usr/share/colcon_cd/function/colcon_cd.sh
export _colcon_cd_root=/opt/ros/iron/
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.zsh

# ROS2 Autocompletion (This should be next of ROS & Colcon setting)
eval "$(register-python-argcomplete3 ros2)"
eval "$(register-python-argcomplete3 colcon)"
eval "$(register-python-argcomplete3 colcon_cd)"