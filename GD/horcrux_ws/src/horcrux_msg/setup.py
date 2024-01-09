from setuptools import find_packages, setup

package_name = 'horcrux_msg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bong',
    maintainer_email='bong@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hello_node = horcrux_msg.hello_node:main',
            'pub = horcrux_msg.pub:main',
            'sub = horcrux_msg.sub:main'
        ],
    },
)
