import rclpy
import time
import numpy as np

from .gait import serpenoid

from rclpy.node import Node
from rclpy.clock import Clock
from rclpy.time import Time

from horcrux_interfaces.msg import EnvState
from horcrux_interfaces.msg import RobotState

class nn_startup(Node):
    def __init__(self, a_type:str = 'continuous'):
        time.sleep(3)
        super().__init__('nn_startup')
        self.get_logger().info(" NN startup node initiation...")
        if a_type.lower() == 'discrete':
            self._ACTION_DISCRETE = True
            self.get_logger().info("\033[32m Set action space to 'DISCRETE'. \033[0m")
        else:
            self._ACTION_DISCRETE = False
            self.get_logger().info("\033[32m Set action space to 'CONTINUOUS'. \033[0m")

        ## Nueral Network Obs Space
        self.__joint_pos = np.empty((14), dtype=np.float32)
        self.__joint_vel = np.empty((14), dtype=np.float32)
        self.__joint_tor = np.empty((14), dtype=np.float32)
        self.__fsr_top = np.empty((14))
        self.__fsr_bot = np.empty((14))
        self.__head_quat = np.empty((4))
        self.__head_angvel = np.empty((3))
        self.__head_linacc = np.empty((3))
        self.__motion_vector = np.empty((14), dtype=np.int8)

        ## For Recurrent NN
        self.__prior_action = np.empty((14))
        self.__action_uptime = self.get_clock().now()

        ## For future use
        self.__joy_axes = np.empty((2))

        ## Nueral Network Act Space
        self.__action = np.empty((14))

        self._pub_state = self.create_publisher(EnvState, 'NN_state', 10)
        pubtime = 1/10
        self.create_timer(pubtime, self._state_pub_cb)

        self.sub_states = self.create_subscription(
            RobotState,
            'robot_state',
            self._state_cb,
            10
        )

        # self.gait = serpenoid.util(30,30,40,40,0) # serpentine
        # self.gait = serpenoid.util(30,30,80,40,0) # slithering
        # self.gait = serpenoid.util(30,30,40,40,45) # sidewinding
        # self.gait = serpenoid.util(0,0,80,80,90) # rolling
        self.gait = serpenoid.util(30,30,40,40,90) # helix
        self.motionMat = self.gait.getMotionMat()
        self.k_max = self.motionMat.shape[1] - 1
        self.k = 0

        self.get_logger().info(f"\033[32m Gait motion matrix is made with shape {self.motionMat.shape} \033[0m")

    def _state_pub_cb(self):
        msg = EnvState()
        msg.header.stamp = self.get_clock().now().to_msg()

        msg.currents = self.__joint_tor
        msg.velocities = self.__joint_vel
        msg.positions = self.__joint_pos

        msg.head_q.w = self.__head_quat[0]
        msg.head_q.x = self.__head_quat[1]
        msg.head_q.y = self.__head_quat[2]
        msg.head_q.z = self.__head_quat[3]

        msg.haed_angular_vel.x = self.__head_angvel[0]
        msg.haed_angular_vel.y = self.__head_angvel[1]
        msg.haed_angular_vel.z = self.__head_angvel[2]

        msg.head_linear_acc.z = self.__head_linacc[0]
        msg.head_linear_acc.y = self.__head_linacc[1]
        msg.head_linear_acc.z = self.__head_linacc[2]

        msg.fsr_top = self.__fsr_top
        msg.fsr_bottom = self.__fsr_bot

        msg.motion_vector = self.__motion_vector

        msg.axes = self.__joy_axes

        msg.motion_vector = self.motionMat[:,self.k]

        self.k += 1
        self.k = self.k % self.k_max

        self._pub_state.publish(msg)
    
    def _state_cb(self, msg:RobotState):
        for idx in range(14):
            self.__joint_tor[idx] = msg.motors.motors[idx].present_current
            self.__joint_vel[idx] = msg.motors.motors[idx].present_velocity
            self.__joint_pos[idx] = msg.motors.motors[idx].present_position

            try:
                self.__fsr_top[idx] = msg.fsr.data[(2*idx)]
                self.__fsr_bot[idx] = msg.fsr.data[(2*idx)+1]
            except Exception as e:
                print(e)
                self.__fsr_top[idx] = [0] * 14
                self.__fsr_bot[idx] = [0] * 14

        # try:
        #     self.__joy_axes[0] = msg.joy.axes[0] # Left X
        #     self.__joy_axes[1] = msg.joy.axes[1] # Left Y
        # except Exception as e:
        #     print(e)

        self.__head_quat[0] = msg.imu.orientation.w
        self.__head_quat[1] = msg.imu.orientation.x
        self.__head_quat[2] = msg.imu.orientation.y
        self.__head_quat[3] = msg.imu.orientation.z

        self.__head_angvel[0] = msg.imu.angular_velocity.x
        self.__head_angvel[1] = msg.imu.angular_velocity.y
        self.__head_angvel[2] = msg.imu.angular_velocity.z

        self.__head_linacc[0] = msg.imu.linear_acceleration.x
        self.__head_linacc[1] = msg.imu.linear_acceleration.y
        self.__head_linacc[2] = msg.imu.linear_acceleration.z
        

def main(args = None):
    rclpy.init(args=args)
    nn_start = nn_startup()
    rclpy.spin(nn_start)

    # Destroy node from here...
    nn_start.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()