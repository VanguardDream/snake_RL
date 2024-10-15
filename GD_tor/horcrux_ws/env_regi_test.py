import rclpy
from rclpy.node import Node
from rclpy.clock import Clock

import rclpy.time

import os

import time

import numpy as np

# import ray
from ray.rllib.algorithms.algorithm import Algorithm
# from ray.rllib.algorithms import ppo
from ament_index_python.packages import get_package_share_directory

from horcrux_interfaces.msg import EnvState
from horcrux_interfaces.msg import EnvAction

import gymnasium as gym
import horcrux_terrain_v1
from horcrux_terrain_v1.envs import PlaneWorld
from ray.tune.registry import register_env

register_env("plane-v1", lambda config: PlaneWorld(config))

# 패키지의 경로를 동적으로 가져옴
package_name = 'horcrux_state'  # 패키지 이름을 여기에 입력하세요.
package_share_directory = get_package_share_directory(package_name)

# 상대 경로로 체크포인트 파일 경로 설정
checkpoint_path = os.path.join(package_share_directory, 'policies')

# algo = Algorithm.from_checkpoint(checkpoint_path+"/LP")