from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='joy',
            namespace='horcrux',
            executable='joy_node',
            name='joy_op'
        ),
        Node(
            package='horcrux_state',
            executable='state_node',
            name='horcrux_state',
            remappings=[
                        ('/joy', '/horcrux/joy'),
                        ('/robot_state', '/horcrux/robot_state'),
                        ]
        )
    ])