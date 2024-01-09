import rclpy
from rclpy.node import Node

from horcrux_interfaces.msg import MotorState


class mini_sub(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            MotorState,                                               # CHANGE
            'motor_state_demo',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self, msg):
            self.get_logger().info('I heard: "%d"' % msg.id)  # CHANGE


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = mini_sub()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()