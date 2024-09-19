from setuptools import setup, find_packages

setup(
    name="horcrux_terrain_v1",
    version="0.0.1",
    install_requires=["gymnasium>=0.29.0", "pygame>=2.1.0", "mujoco>=3"],
    packages=find_packages(exclude=('logs',))
)