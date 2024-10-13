import rclpy
from rclpy.node import Node
from rclpy.clock import Clock

import rclpy.time

import os

import numpy as np

# import ray
from ray.rllib.algorithms.algorithm import Algorithm
# from ray.rllib.algorithms import ppo
from ament_index_python.packages import get_package_share_directory

from horcrux_interfaces.msg import EnvState
from horcrux_interfaces.msg import EnvAction

class nn_policy(Node):
    def __init__(self):
        super().__init__('nn_policy')

        self.__prior_state = None
        self.__prior_action = None
        self.get_logger().info("\033[32m Loading PPO Policy... \033[0m")

        # 패키지의 경로를 동적으로 가져옴
        package_name = 'horcrux_state'  # 패키지 이름을 여기에 입력하세요.
        package_share_directory = get_package_share_directory(package_name)

        # 상대 경로로 체크포인트 파일 경로 설정
        checkpoint_path = os.path.join(package_share_directory, 'policy')
        self.get_logger().info(f"Policy checkpoint path: {checkpoint_path}")

        try:
            self.__algo = Algorithm.from_checkpoint(checkpoint_path)
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

    def _obs_cb(self, msg):
        if self.__algo is not None:
            obs = np.empty(94, dtype=np.float32)

            obs[0:14] = msg.joint_pos
            obs[14:28] = msg.joint_vel
            obs[28:42] = msg.joint_tor
            obs[42:56] = msg.fsr_top
            obs[56:70] = msg.fsr_bot
            obs[70:74] = msg.head_quat
            obs[74:77] = msg.head_angvel
            obs[77:80] = msg.head_linacc
            obs[80:94] = msg.motion_vector

            t_up = Clock().now()
            action = self.__algo.compute_action(obs)
            t_done = Clock().now()

            self.__prior_state = obs
            self.__prior_action = action

            self.get_logger().debug(f"Action: {action}")
            self.get_logger().debug(f"Action computation time: {(t_done - t_up).nanoseconds/1e6} ms")

            pub_msg = EnvAction()
            pub_msg.c_action = np.array(msg.motion_vector) * action

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