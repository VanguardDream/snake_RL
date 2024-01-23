from dynamixel_sdk import *
import serial

from .gait import serpenoid

from horcrux_interfaces.msg import EnvAction
from horcrux_interfaces.msg import MotorStates
from horcrux_interfaces.msg import MotorState

import rclpy
from rclpy.node import Node
from rclpy.clock import Clock
import numpy as np
import struct

# DXL defines
ADDR_TORQUE_ENABLE          = 64
ADDR_STATUS_RETURN_LEVEL    = 68
ADDR_GOAL_CURRENT           = 102
ADDR_GOAL_VELOCITY          = 104 
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_CURRENT        = 126
ADDR_PRESENT_VELOCITY       = 128
ADDR_PRESENT_POSITION       = 132
ADDR_PRESENT_VOLTAGE        = 144
ADDR_PRESENT_TEMPERATURE    = 146

LEN_TORQUE_ENABLE           = 1
LEN_GOAL_CURRENT            = 2
LEN_GOAL_VELOCITY           = 4
LEN_GOAL_POSITION           = 4
LEN_PRESENT_CURRENT         = 2
LEN_PRESENT_VELOCITY        = 4
LEN_PRESENT_POSITION        = 4
LEN_PRESENT_VOLTAGE         = 2
LEN_PRESENT_TEMPERATURE     = 1

DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
BAUDRATE                    = 3000000 # -> 통신 속도 조절
# BAUDRATE                    = 57600 # -> 통신 속도 조절

PROTOCOL_VERSION            = 2.0

# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                    = '/dev/ttyDXL'


class motor_state_node(Node):
    def __init__(self):
        super().__init__('motor_state_node')

        self.dxl_poh = PortHandler(DEVICENAME)
        self.dxl_pah = PacketHandler(PROTOCOL_VERSION)

        self.gswrite = GroupSyncWrite(self.dxl_poh, self.dxl_pah, ADDR_GOAL_CURRENT, LEN_GOAL_CURRENT)

        # self.gbread_TE = GroupBulkRead(self.dxl_poh, self.dxl_pah)
        # self.gbread_GC = GroupBulkRead(self.dxl_poh, self.dxl_pah)
        # self.gbread_GV = GroupBulkRead(self.dxl_poh, self.dxl_pah)
        # self.gbread_GP = GroupBulkRead(self.dxl_poh, self.dxl_pah)
        self.gbread_PC = GroupBulkRead(self.dxl_poh, self.dxl_pah)
        self.gbread_PV = GroupBulkRead(self.dxl_poh, self.dxl_pah)
        self.gbread_PP = GroupBulkRead(self.dxl_poh, self.dxl_pah)
        # self.gbread_PVL = GroupBulkRead(self.dxl_poh, self.dxl_pah)
        self.gbread_PT = GroupBulkRead(self.dxl_poh, self.dxl_pah)

        self.tiktok = 0
        self.pub_time = Clock().now()
        pub_timing = 1/10

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
        
        self.action_sub = self.create_subscription(
            EnvAction,
            'NN_action',
            self.action_sub_cb,
            10
        )

        self.get_logger().info("\033[32m Node initation done...\033[0m")

        self.get_logger().info("\033[32m Send enable command to motors...\033[0m")

        for i in range(14):
            self.dxl_pah.write1ByteTxRx(self.dxl_poh, (i), ADDR_TORQUE_ENABLE, 1)
        for i in range(14):
            self.dxl_pah.write1ByteTxRx(self.dxl_poh, (i), ADDR_TORQUE_ENABLE, 1)

    def pub_cb(self):
        cb_up = Clock().now()

        dxl_data = np.zeros((9,14)) # In order of msg series...
        comm_err_ids = np.zeros((9,14)) # In order of msg series...
        txrx_err = False

        # DXL Group Instance Add params...
        # Torque On/Off
        # for idx in range(14):
        #     dxl_add_param_result = self.gbread_TE.addParam(idx, ADDR_TORQUE_ENABLE, LEN_TORQUE_ENABLE)
        #     if dxl_add_param_result != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] Addparam fail(torque)...\033[0m" % idx)
        #         comm_err_ids[0][idx] = 1
        # Goal Current
        # for idx in range(14):
        #     dxl_add_param_result = self.gbread_GC.addParam(idx, ADDR_GOAL_CURRENT, LEN_GOAL_CURRENT)
        #     if dxl_add_param_result != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] Addparam fail(g vel)...\033[0m" % idx)
        #         comm_err_ids[1][idx] = 1               
        # Goal Velocity
        # for idx in range(14):
        #     dxl_add_param_result = self.gbread_GV.addParam(idx, ADDR_GOAL_VELOCITY, LEN_GOAL_VELOCITY)
        #     if dxl_add_param_result != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] Addparam fail(g vel)...\033[0m" % idx)
        #         comm_err_ids[2][idx] = 1
        # Goal Position
        # for idx in range(14):
        #     dxl_add_param_result = self.gbread_GP.addParam(idx, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
        #     if dxl_add_param_result != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] Addparam fail(g pos)...\033[0m" % idx)
        #         comm_err_ids[3][idx] = 1
        # Present Current
        for idx in range(14):
            dxl_add_param_result = self.gbread_PC.addParam(idx, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT)
            if dxl_add_param_result != True:
                self.get_logger().warn("\033[31m [ID:%03d] Addparam fail(p vel)...\033[0m" % idx)
                comm_err_ids[4][idx] = 1
        # Present Velocity
        for idx in range(14):
            dxl_add_param_result = self.gbread_PV.addParam(idx, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)
            if dxl_add_param_result != True:
                self.get_logger().warn("\033[31m [ID:%03d] Addparam fail(p vel)...\033[0m" % idx)
                comm_err_ids[5][idx] = 1
        # Present Position
        for idx in range(14):
            dxl_add_param_result = self.gbread_PP.addParam(idx, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
            if dxl_add_param_result != True:
                self.get_logger().warn("\033[31m [ID:%03d] Addparam fail(p pos)...\033[0m" % idx)
                comm_err_ids[6][idx] = 1
        # # Present Voltage
        # for idx in range(14):
        #     dxl_add_param_result = self.gbread_PVL.addParam(idx, ADDR_PRESENT_VOLTAGE, LEN_PRESENT_VOLTAGE)
        #     if dxl_add_param_result != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] Addparam fail(p vol)...\033[0m" % idx)
        #         comm_err_ids[7][idx] = 1
        # # Present Temperature
        for idx in range(14):
            dxl_add_param_result = self.gbread_PT.addParam(idx, ADDR_PRESENT_TEMPERATURE, LEN_PRESENT_TEMPERATURE)
            if dxl_add_param_result != True:
                self.get_logger().warn("\033[31m [ID:%03d] Addparam fail(p temp)...\033[0m" % idx)
                comm_err_ids[8][idx] = 1

        # Get data from GB read instance...
        # Torque On/Off
        # dxl_comm_result = self.gbread_TE.txRxPacket()
        # if dxl_comm_result != COMM_SUCCESS:
        #     self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))
        #     txrx_err = True
        # for idx in range(14):
        #     dxl_get_data_result = self.gbread_TE.isAvailable(idx, ADDR_TORQUE_ENABLE, LEN_TORQUE_ENABLE)
        #     if dxl_get_data_result != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] Getdata failed (tor)... \033[0m" % idx)
        # # Goal Current
        # dxl_comm_result = self.gbread_GC.txRxPacket()
        # if dxl_comm_result != COMM_SUCCESS:
        #     self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))
        #     txrx_err = True
        # for idx in range(14):
        #     dxl_get_data_result = self.gbread_GC.isAvailable(idx, ADDR_GOAL_CURRENT, LEN_GOAL_CURRENT)
        #     if dxl_get_data_result != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] Getdata failed (g cur)... \033[0m" % idx)
        # # Goal Velocity
        # dxl_comm_result = self.gbread_GV.txRxPacket()
        # if dxl_comm_result != COMM_SUCCESS:
        #     self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))
        #     txrx_err = True
        # for idx in range(14):
        #     dxl_get_data_result = self.gbread_GV.isAvailable(idx, ADDR_GOAL_VELOCITY, LEN_GOAL_VELOCITY)
        #     if dxl_get_data_result != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] Getdata failed (g vel)... \033[0m" % idx)
        # # Goal Position
        # dxl_comm_result = self.gbread_GP.txRxPacket()
        # if dxl_comm_result != COMM_SUCCESS:
        #     self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))
        #     txrx_err = True
        # for idx in range(14):
        #     dxl_get_data_result = self.gbread_GP.isAvailable(idx, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
        #     if dxl_get_data_result != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] Getdata failed (g pos)... \033[0m" % idx)
        # Present Current
        dxl_comm_result = self.gbread_PC.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))
            txrx_err = True
        for idx in range(14):
            dxl_get_data_result = self.gbread_PC.isAvailable(idx, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT)
            if dxl_get_data_result != True:
                self.get_logger().warn("\033[31m [ID:%03d] Getdata failed (p cur)... \033[0m" % idx)
        # Present Velocity
        dxl_comm_result = self.gbread_PV.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))
            txrx_err = True
        for idx in range(14):
            dxl_get_data_result = self.gbread_PV.isAvailable(idx, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)
            if dxl_get_data_result != True:
                self.get_logger().warn("\033[31m [ID:%03d] Getdata failed (p vel)... \033[0m" % idx)
        # Present Position
        dxl_comm_result = self.gbread_PP.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))
            txrx_err = True
        for idx in range(14):
            dxl_get_data_result = self.gbread_PP.isAvailable(idx, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
            if dxl_get_data_result != True:
                self.get_logger().warn("\033[31m [ID:%03d] Getdata failed (p pos)... \033[0m" % idx)
        # # Present Voltage
        # dxl_comm_result = self.gbread_PVL.txRxPacket()
        # if dxl_comm_result != COMM_SUCCESS:
        #     self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))
        #     txrx_err = True
        # for idx in range(14):
        #     dxl_get_data_result = self.gbread_PVL.isAvailable(idx, ADDR_PRESENT_VOLTAGE, LEN_PRESENT_VOLTAGE)
        #     if dxl_get_data_result != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] Getdata failed (p vol)... \033[0m" % idx)
        # Present Temperature
        dxl_comm_result = self.gbread_PT.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))
            txrx_err = True
        for idx in range(14):
            dxl_get_data_result = self.gbread_PT.isAvailable(idx, ADDR_PRESENT_TEMPERATURE, LEN_PRESENT_TEMPERATURE)
            if dxl_get_data_result != True:
                self.get_logger().warn("\033[31m [ID:%03d] Getdata failed (p temp)... \033[0m" % idx)

        for idx in range(14):
            # dxl_data[0][idx] = self.gbread_TE.getData(idx,ADDR_TORQUE_ENABLE,LEN_TORQUE_ENABLE)
            # dxl_data[1][idx] = self.gbread_GC.getData(idx,ADDR_GOAL_CURRENT,LEN_GOAL_CURRENT)
            # dxl_data[2][idx] = self.gbread_GV.getData(idx,ADDR_GOAL_VELOCITY,LEN_GOAL_VELOCITY)
            # dxl_data[3][idx] = self.gbread_GP.getData(idx,ADDR_GOAL_POSITION,LEN_GOAL_POSITION)
            dxl_data[4][idx] = self.gbread_PC.getData(idx,ADDR_PRESENT_CURRENT,LEN_PRESENT_CURRENT)
            if dxl_data[4][idx] > 0x7fff:
                dxl_data[4][idx] -= 65536
            dxl_data[5][idx] = self.gbread_PV.getData(idx,ADDR_PRESENT_VELOCITY,LEN_PRESENT_VELOCITY)
            if dxl_data[5][idx] > 0x7fffffff:
                dxl_data[5][idx] -= 4294967296 
            dxl_data[6][idx] = self.gbread_PP.getData(idx,ADDR_PRESENT_POSITION,LEN_PRESENT_POSITION)
            if dxl_data[6][idx] > 0x7fffffff:
                dxl_data[6][idx] -= 4294967296 
            # dxl_data[7][idx] = self.gbread_PVL.getData(idx,ADDR_PRESENT_VELOCITY,LEN_PRESENT_VOLTAGE)
            dxl_data[8][idx] = self.gbread_PT.getData(idx,ADDR_PRESENT_TEMPERATURE,LEN_PRESENT_TEMPERATURE)

        # self.gbread_TE.clearParam()
        # self.gbread_GC.clearParam()
        # self.gbread_GV.clearParam()
        # self.gbread_GP.clearParam()
        self.gbread_PC.clearParam()
        self.gbread_PV.clearParam()
        self.gbread_PP.clearParam()
        # self.gbread_PVL.clearParam()
        self.gbread_PT.clearParam()
        

        # for idx in range(14):
        #     dxl_addparam_result_PP = self.gbread_PP.addParam(idx, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        #     if dxl_addparam_result_PP != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] GBRead_PP addparam fail...\033[0m" % idx)
        #         quit()
            
        #     dxl_addparam_result_PV = self.gbread_PV.addParam(idx, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)
        #     if dxl_addparam_result_PV != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] GBRead_PV addparam fail...\033[0m" % idx)
        #         quit()

        # dxl_comm_result = self.gbread_PP.txRxPacket()
        # if dxl_comm_result != COMM_SUCCESS:
        #     self.get_logger().warn("\033[31m GBPP_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))

        # for idx in range(14):
        #     dxl_getPdata_result_PP = self.gbread_PP.isAvailable(idx, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        #     if dxl_getPdata_result_PP != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] groupSyncRead_PP getdata failed \033[0m" % idx)

        #     self.presentP[idx] = self.gbread_PP.getData(idx, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

        # dxl_comm_result = self.gbread_PV.txRxPacket()
        # if dxl_comm_result != COMM_SUCCESS:
        #     self.get_logger().warn("\033[31m GBPV_TxRx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))

        # for idx in range(14):  
        #     dxl_getPdata_result_PV = self.gbread_PV.isAvailable(idx, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)      
        #     if dxl_getPdata_result_PV != True:
        #         self.get_logger().warn("\033[31m [ID:%03d] groupSyncRead_PV getdata failed \033[0m" % idx)

        #     self.presentV[idx] = self.gbread_PV.getData(idx, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)

        # self.gbread_PP.clearParam()
        # self.gbread_PV.clearParam()

        msg = MotorStates()

        for idx in range(14):
            tmp = MotorState()
            # tmp.torque = dxl_data[0][idx]
            # tmp.goal_current = dxl_data[1][idx]
            # tmp.goal_velocity = dxl_data[2][idx]
            # tmp.goal_position = dxl_data[3][idx]
            tmp.present_current = dxl_data[4][idx] * 2.69 # mA
            tmp.present_velocity = dxl_data[5][idx] * 0.229 # RPM
            tmp.present_position = dxl_data[6][idx] * 0.087891 # degree
            # tmp.voltage = dxl_data[7][idx]
            tmp.temperature = dxl_data[8][idx] * 1.0 # Cecius

            msg.motors[idx] = tmp

        dxl_lookup_done = Clock().now()
        self.tiktok = (dxl_lookup_done.nanoseconds - cb_up.nanoseconds)
        if self.tiktok > 85000000:
            self.get_logger().info('DXL motors status comm line is busy... %d' % self.tiktok)
        if self.tiktok > 100000000:
            self.get_logger().info("\033[31m Realtime response fail!!! \033[0m")


        self.pub_time = dxl_lookup_done
        msg.header.stamp = dxl_lookup_done.to_msg()
        self.motors_pub.publish(msg)

    def action_sub_cb(self, msg:EnvAction):
        for idx in range(14):
            # dxl_add_param_result = self.gswrite.addParam(idx, int(100 * msg.c_action[idx]))
            dxl_add_param_result = self.gswrite.addParam(idx, [DXL_LOBYTE(int(50 * msg.c_action[idx])),DXL_HIBYTE(int(50 * msg.c_action[idx]))])
            if dxl_add_param_result != True:
                self.get_logger().warn("\033[31m [ID:%03d] Addparam fail(action)...\033[0m" % idx)

        dxl_comm_result = self.gswrite.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            self.get_logger().warn("\033[31m GBPP_Tx fail with error %s \033[0m" % self.dxl_pah.getTxRxResult(dxl_comm_result))

        self.gswrite.clearParam()
    
    def motor_off(self):
        for i in range(14):
            self.dxl_pah.write1ByteTxRx(self.dxl_poh, (i), ADDR_TORQUE_ENABLE, 0)
        for i in range(14):
            self.dxl_pah.write1ByteTxRx(self.dxl_poh, (i), ADDR_TORQUE_ENABLE, 0)      

    def __del__(self):
        for i in range(14):
            self.dxl_pah.write1ByteTxRx(self.dxl_poh, (i), ADDR_TORQUE_ENABLE, 0)
        for i in range(14):
            self.dxl_pah.write1ByteTxRx(self.dxl_poh, (i), ADDR_TORQUE_ENABLE, 0)
             

def main(args = None):
    rclpy.init(args=args)
    node = motor_state_node()

    rclpy.spin(node)

    node.motor_off()
    node.motor_off()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
