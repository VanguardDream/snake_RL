import rclpy
from rclpy.node import Node

from horcrux_interfaces.msg import MotorState

class mini_pub(Node):
    def __init__(self):
        super().__init__('mini_pub')
        self.publishers_ = self.create_publisher(MotorState, 'motor_state_demo', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_cb)
        self.i = 0

    def timer_cb(self):
        msg = MotorState()
        msg.id = self.i
        self.publishers_.publish(msg)
        self.i = self.i + 1
        pass

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = mini_pub()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()