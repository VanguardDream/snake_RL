import rclpy
from rclpy.node import Node

#msgs
from horcrux_interfaces.msg import RobotState
from sensor_msgs.msg import Joy

class joy_sub(Node):
    def __init__(self):
        super().__init__('joy_sub')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_cb,
            10            
        )
        self.subscription
        self.publisher_ = self.create_publisher(RobotState, 'robot_state', 10)
        timer_period = 1/20
        self.create_timer(timer_period, self.timer_cb)
        self.joy_data = Joy()

    def joy_cb(self, msg:Joy):
        self.joy_data = msg

    def timer_cb(self):
        msg = RobotState()
        msg.joy = self.joy_data
        self.publisher_.publish(msg)

class state_pub(Node):
    def __init__(self):
        super().__init__('state_pub')
        self.publisher_ = self.create_publisher(RobotState, 'robot_state', 10)
        timer_period = 1/20
        self.create_timer(timer_period, self.timer_cb)
    
    def timer_cb(self):
        msg = RobotState()

        self.publisher_.publish(msg)

def main(args = None):
    rclpy.init(args=args)

    joy_subscriber = joy_sub()

    rclpy.spin(joy_subscriber)

    # Destroy node from here...
    joy_subscriber.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()