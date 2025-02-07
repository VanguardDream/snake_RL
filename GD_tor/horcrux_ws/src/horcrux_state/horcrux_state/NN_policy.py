import rclpy
from rclpy.node import Node
from rclpy.clock import Clock

import rclpy.time

import os

import time

import numpy as np

# import ray
from ray.rllib.algorithms.algorithm import Algorithm
from ray.rllib.algorithms.ppo import PPOConfig

from ament_index_python.packages import get_package_share_directory

from horcrux_interfaces.msg import EnvState
from horcrux_interfaces.msg import EnvAction

from std_msgs.msg import Float32

import gymnasium as gym
import horcrux_terrain_v1
from horcrux_terrain_v1.envs import PlaneWorld
from ray.tune.registry import register_env

class nn_policy(Node):
    def __init__(self):
        super().__init__('nn_policy')

        time.sleep(5)

        self.__prior_state = None
        self.__prior_action = None
        self.get_logger().info("\033[32m Loading PPO Policy... \033[0m")

        # 패키지의 경로를 동적으로 가져옴
        package_name = 'horcrux_state'  # 패키지 이름을 여기에 입력하세요.
        package_share_directory = get_package_share_directory(package_name)

        # 상대 경로로 체크포인트 파일 경로 설정
        checkpoint_path = os.path.join(package_share_directory, 'policies')
        # print(checkpoint_path)
        self.get_logger().info(f"Policy checkpoint path: {checkpoint_path}")

        # Env 등록
        register_env("plane-v1", lambda config: PlaneWorld())
        
        # New 알고리즘 생성
        # PPO Config
        new_algo_config = PPOConfig()
        # Activate new API stack. -> 구려서 안씀.
        new_algo_config.api_stack(
            enable_rl_module_and_learner=False,
            enable_env_runner_and_connector_v2=False,
        )
        new_algo_config.framework("torch")
        new_algo_config.environment("plane-v1")
        new_algo_config.resources(num_gpus=0)
        new_algo_config.training(
            gamma=0.9, 
            lr=0.001, 

            model={ "fcnet_hiddens": [512, 512, 512, 512, 512],
                    },
        )

        self.__algo = new_algo_config.build()

        try:
            self.__algo.get_policy().from_checkpoint(checkpoint_path+"/linear")
            self.get_logger().info("\033[32m Policy loaded successfully. \033[0m")

        except Exception as e:
            self.get_logger().error(f"\033[31m Failed to load policy: {e} \033[0m")
            self.__algo = None

        self.__sub_obs = self.create_subscription(
            EnvState,
            'NN_state',
            self._obs_cb,
            10
        )

        self.__pub_action = self.create_publisher(EnvAction, 'NN_action', 10)
        self.__pub_inf_time = self.create_publisher(Float32, 'NN_inf_time', 10)

    def _obs_cb(self, msg):
        if self.__algo is not None:
            obs = np.empty(94, dtype=np.float32)

            obs[0:14] = msg.positions
            obs[14:28] = msg.velocities
            obs[28:42] = msg.currents
            obs[42:56] = msg.fsr_top
            obs[56:70] = msg.fsr_bottom
            obs[70] = msg.head_q.w
            obs[71] = msg.head_q.x
            obs[72] = msg.head_q.y
            obs[73] = msg.head_q.z
            obs[74] = msg.haed_angular_vel.x
            obs[75] = msg.haed_angular_vel.y
            obs[76] = msg.haed_angular_vel.z
            obs[77] = msg.head_linear_acc.x
            obs[78] = msg.head_linear_acc.y
            obs[79] = msg.head_linear_acc.z
            obs[80:94] = msg.motion_vector

            t_up = Clock().now()
            torque_vector = self.__algo.compute_action(obs)
            action = np.array(msg.motion_vector) * torque_vector
            # action = np.array(obs[80:94]) * 0.1
            t_done = Clock().now()

            self.__prior_state = obs
            self.__prior_action = action

            self.get_logger().debug(f"Action: {action}")
            self.get_logger().debug(f"Action computation time: {(t_done - t_up).nanoseconds/1e6} ms")

            self.__pub_inf_time.publish(Float32(data=(t_done - t_up).nanoseconds/1e6))

            pub_msg = EnvAction()
            pub_msg.c_action = action

            self.__pub_action.publish(pub_msg)
        else:
            self.get_logger().error("\033[31m Policy is not loaded. \033[0m")


def main(args=None):
    rclpy.init(args=args)

    node = nn_policy()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()