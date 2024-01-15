from dynamixel_sdk import *
import serial
from horcrux_interfaces.msg import MotorStates
from horcrux_interfaces.msg import MotorState
import rclpy
from rclpy.node import Node
from rclpy.clock import Clock
import numpy as np

# DXL defines
ADDR_TORQUE_ENABLE          = 64
ADDR_STATUS_RETURN_LEVEL    = 68
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_VELOCITY       = 128
ADDR_PRESENT_POSITION       = 132

LEN_GOAL_POSITION           = 4
LEN_PRESENT_POSITION        = 4
LEN_PRESENT_VELOCITY        = 4

DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
BAUDRATE                    = 1000000 # -> 통신 속도 조절
# BAUDRATE                    = 57600 # -> 통신 속도 조절

PROTOCOL_VERSION            = 2.0

# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                    = '/dev/ttyDXL'


class motor_state_node(Node):
    def __init__(self):
        super().__init__('motor_state_node')

        self.dxl_poh = PortHandler(DEVICENAME)
        self.dxl_pah = PacketHandler(PROTOCOL_VERSION)

        self.presentP = np.empty(14)
        self.presentV = np.empty(14)

        self.gswrite = GroupSyncWrite(self.dxl_poh, self.dxl_pah, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
        self.gbread_PP = GroupBulkRead(self.dxl_poh, self.dxl_pah)
        self.gbread_PV = GroupBulkRead(self.dxl_poh, self.dxl_pah)
        
        self.pub_time = Clock().now()
        pub_timing = 1

        try:
            self.dxl_poh.openPort()

            if self.dxl_poh.is_open:
                self.get_logger().info("\033[32m Serial port opened successfully...\033[0m")
            else:
                self.get_logger().info("\033[31m Serial port is not opened...\033[0m")
                exit(0)
        except Exception as e:
            print(e)
            self.get_logger().warn("\033[31m Serial port open fail...\033[0m")
            exit(0)

        try:
            self.dxl_poh.setBaudRate(BAUDRATE)
        except Exception as e:
            print(e)
            self.get_logger().warn("\033[31m Setting baudrate fail...\033[0m")
            exit(0)
        else:
            self.pub_timer = self.create_timer(pub_timing, self.pub_cb)
            self.motors_pub = self.create_publisher(MotorStates, 'motor_states', 10)

        self.get_logger().info("\033[32m Node initation done...\033[0m")


    def pub_cb(self):
        cb_up = Clock().now()

        for idx in range(14):
            dxl_addparam_result_PP = self.gbread_PP.addParam(idx, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
            if dxl_addparam_result_PP != True:
                self.get_logger().warn("\033[31m [ID:%03d] GBRead_PP addparam fail...\033[0m" % idx)
                quit()
            
            dxl_addparam_result_PV = self.gbread_PV.addParam(idx, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)
            if dxl_addparam_result_PV != True:
                self.get_logger().warn("\033[31m [ID:%03d] GBRead_PV addparam fail...\033[0m" % idx)
                quit()

        dxl_comm_result = self.gbread_PP.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))

        for idx in range(14):
            dxl_getPdata_result_PP = self.gbread_PP.isAvailable(idx, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
            if dxl_getPdata_result_PP != True:
                self.get_logger().warn("\033[31m [ID:%03d] groupSyncRead_PP getdata failed \033[0m" % idx)

            self.presentP[idx] = self.gbread_PP.getData(idx, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

        dxl_comm_result = self.gbread_PV.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().warn("\033[31m GBPV_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))

        for idx in range(14):  
            dxl_getPdata_result_PV = self.gbread_PV.isAvailable(idx, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)      
            if dxl_getPdata_result_PV != True:
                self.get_logger().warn("\033[31m [ID:%03d] groupSyncRead_PV getdata failed \033[0m" % idx)

            self.presentV[idx] = self.gbread_PV.getData(idx, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)

        self.gbread_PP.clearParam()
        self.gbread_PV.clearParam()

        dxl_lookup_done = Clock().now()
        print(dxl_lookup_done.nanoseconds - cb_up.nanoseconds)

        self.pub_time = dxl_lookup_done

        # msg = MotorStates()

        # for idx in range(14):
        #     tmp = MotorState()
        #     tmp.present_position = self.presentP[idx]
        #     tmp.present_velocity = self.presentV[idx]

        #     msg.motors[idx] = tmp

        # msg.header.stamp = dxl_lookup_done.to_msg()

        # self.motors_pub.publish(msg)


def main(args = None):
    rclpy.init(args=args)
    node = motor_state_node()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
