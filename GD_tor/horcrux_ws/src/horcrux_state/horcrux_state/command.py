import rclpy
import numpy as np

from .gait import serpenoid

from rclpy.node import Node
from rclpy.clock import Clock
from rclpy.time import Time

from horcrux_interfaces.msg import EnvAction
from horcrux_interfaces.msg import EnvState
from horcrux_interfaces.msg import RobotState

class horcrux_command(Node):
    def __init__(self, a_type:str = 'continuous'):
        super().__init__('horcrux_command')
        self.get_logger().info(" Command node initiation...")
        if a_type.lower() == 'discrete':
            self._ACTION_DISCRETE = True
            self.get_logger().info("\033[32m Set action space to 'DISCRETE'. \033[0m")
        else:
            self._ACTION_DISCRETE = False
            self.get_logger().info("\033[32m Set action space to 'CONTINUOUS'. \033[0m")

        self.__action = np.empty((14))
        self.__prior_action = np.empty((14))
        self.__action_uptime = self.get_clock().now()

        self.__motion_vector = np.empty((14))
        self.__motor_currents = np.empty((14))
        self.__motor_velocities = np.empty((14))
        self.__motor_positions = np.empty((14))
        self.__head_oreientation = np.empty((4))
        self.__head_angular_vel = np.empty((3))
        self.__head_linear_acc = np.empty((3))
        self.__joy_axes = np.empty((2))

        self._pub_state = self.create_publisher(EnvState, 'NN_state', 10)
        pubtime = 1/10
        self.create_timer(pubtime, self._state_pub_cb)

        self._pub_gait = self.create_publisher(EnvAction, 'NN_action', 10)
        pubtime = 1/10
        self.create_timer(pubtime, self._gait_pub_cb)

        self.sub_action = self.create_subscription(
            EnvAction,
            'NN_action',
            self._action_cb,
            10
        )
        self.sub_states = self.create_subscription(
            RobotState,
            'robot_state',
            self._state_cb,
            10
        )

        self.gait = serpenoid.util(30,30,40,40,0) # serpentine
        # self.gait = serpenoid.util(45,45,10,10,45) # sidewinding
        # self.gait = serpenoid.util(0,0,30,30,90) # rolling
        # self.gait = serpenoid.util(30,30,40,40,90) # helix
        self.motionMat = self.gait.getMotionMat()
        self.k_max = self.motionMat.shape[1] - 1
        self.k = 0

        self.get_logger().info(f"\033[32m Gait motion matrix is made with shape {self.motionMat.shape} \033[0m")

    def _state_pub_cb(self):
        msg = EnvState()
        msg.header.stamp = self.get_clock().now().to_msg()

        msg.currents = self.__motor_currents
        msg.velocities = self.__motor_velocities
        msg.positions = self.__motor_positions

        msg.head_q.w = self.__head_oreientation[0]
        msg.head_q.x = self.__head_oreientation[1]
        msg.head_q.y = self.__head_oreientation[2]
        msg.head_q.z = self.__head_oreientation[3]

        msg.haed_angular_vel.x = self.__head_angular_vel[0]
        msg.haed_angular_vel.y = self.__head_angular_vel[1]
        msg.haed_angular_vel.z = self.__head_angular_vel[2]

        msg.head_linear_acc.z = self.__head_linear_acc[0]
        msg.head_linear_acc.y = self.__head_linear_acc[1]
        msg.head_linear_acc.z = self.__head_linear_acc[2]

        msg.axes = self.__joy_axes

        self._pub_state.publish(msg)

    def _gait_pub_cb(self):
        msg = EnvAction()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.c_action = self.motionMat[:,self.k]
        self.k += 1
        self.k = self.k % self.k_max

        self._pub_gait.publish(msg)

    def _action_cb(self, msg:EnvAction):
        self.__prior_action = self.__action
        if self._ACTION_DISCRETE:
            self.__action = msg.d_action
        else:
            self.__action = msg.c_action

        # print(self.__action_uptime.nanoseconds)
        # if (msg.header.stamp.nanosec - self.__action_uptime.nanoseconds) > 115000000:
        #     print(f'Inference is delayed...')
        
        # self.__action_uptime = msg.header.stamp
    
    def _state_cb(self, msg:RobotState):
        for idx in range(14):
            self.__motor_currents[idx] = msg.motors.motors[idx].present_current
            self.__motor_velocities[idx] = msg.motors.motors[idx].present_velocity
            self.__motor_positions[idx] = msg.motors.motors[idx].present_position

        try:
            self.__joy_axes[0] = msg.joy.axes[0] # Left X
            self.__joy_axes[1] = msg.joy.axes[1] # Left Y
        except Exception as e:
            print(e)

        self.__head_oreientation[0] = msg.imu.orientation.w
        self.__head_oreientation[1] = msg.imu.orientation.x
        self.__head_oreientation[2] = msg.imu.orientation.y
        self.__head_oreientation[3] = msg.imu.orientation.z

        self.__head_angular_vel[0] = msg.imu.angular_velocity.x
        self.__head_angular_vel[1] = msg.imu.angular_velocity.y
        self.__head_angular_vel[2] = msg.imu.angular_velocity.z

        self.__head_linear_acc[0] = msg.imu.linear_acceleration.x
        self.__head_linear_acc[1] = msg.imu.linear_acceleration.y
        self.__head_linear_acc[2] = msg.imu.linear_acceleration.z
        

def main(args = None):
    rclpy.init(args=args)
    joint_cmd = horcrux_command()
    rclpy.spin(joint_cmd)

    # Destroy node from here...
    joint_cmd.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()