import rclpy
from rclpy.node import Node

#msgs
from horcrux_interfaces.msg import RobotState
from horcrux_interfaces.msg import MotorStates
from sensor_msgs.msg import Joy, Imu, MagneticField

class joy_sub(Node):
    def __init__(self):
        super().__init__('joy_sub')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_cb,
            10            
        )
        self.sub_imu = self.create_subscription(
            Imu,
            'imu',
            self.imu_cb,
            1
        )
        self.sub_mag = self.create_subscription(
            MagneticField,
            'mag',
            self.mag_cb,
            1
        )
        self.sub_motors = self.create_subscription(
            MotorStates,
            'motor_states',
            self.motors_cb,
            1
        )

        self.publisher_ = self.create_publisher(RobotState, 'robot_state', 10)
        timer_period = 1/20
        self.create_timer(timer_period, self.timer_cb)
        self.joy_data = Joy()
        self.imu_data = Imu()
        self.mag_data = MagneticField()
        self.motors_data = MotorStates()

    def joy_cb(self, msg:Joy):
        self.joy_data = msg

    def imu_cb(self, msg:Imu):
        self.imu_data = msg

    def mag_cb(self, msg:MagneticField):
        self.mag_data = msg

    def motors_cb(self, msg:MotorStates):
        self.motors_data = msg

    def timer_cb(self):
        msg = RobotState()
        msg.joy = self.joy_data
        msg.imu = self.imu_data
        msg.mag = self.mag_data
        msg.motors = self.motors_data

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