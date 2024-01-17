from launch import LaunchDescription
from launch_ros.actions import Node, RosTimer

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='joy',
            executable='joy_node',
            namespace='horcrux',
            name='joy_op'
        ),
        Node(
            package='handsfree_imu',
            executable='hfi_a9_node',
            namespace='horcrux',
            name='head_imu'
        ),
        Node(
            package='horcrux_state',
            executable='motors_node',
            namespace='horcrux',
            name='dxl_comm'
        ),
        Node(
            package='horcrux_state',
            executable='state_node',
            namespace='horcrux',
            name='horcrux_state'
            # remappings=[
            #             ('/joy', '/horcrux/joy'),
            #             ('/robot_state', '/horcrux/robot_state'),
            #             ]
        )
    ])