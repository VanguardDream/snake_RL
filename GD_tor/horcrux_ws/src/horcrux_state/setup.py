import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'horcrux_state'
submodules = "horcrux_state/gait"

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'policies'), glob('src/policies/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bong',
    maintainer_email='doorebong@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'state_node = horcrux_state.horcrux_state:main',
            'motors_node = horcrux_state.motor_state:main',
            'command_node = horcrux_state.command:main',
            'nn_state_node = horcrux_state.NN_startup:main',
            'nn_policy_node = horcrux_state.NN_policy:main',
        ],
    },
)
