from setuptools import find_packages
from setuptools import setup

setup(
    name='horcrux_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('horcrux_interfaces', 'horcrux_interfaces.*')),
)
