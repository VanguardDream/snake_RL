# -*- coding:utf-8 -*-

import serial
import struct
# import rospy

import rclpy
from rclpy.node import Node
from rclpy.clock import Clock

import math
import platform
import serial.tools.list_ports
from std_msgs.msg import Int32MultiArray

def find_ttyUSB():
    print('Default port is /dev/ttyACM0, If use multiple serial devices, Please use launch after modify in the file imu corresponding serial port')
    posts = [port.device for port in serial.tools.list_ports.comports() if 'ACM' in port.device]
    print('Current connection {} Total devices {} ea. : {}'.format('USB', len(posts), posts))


class skin_fsr_node(Node):
    def __init__(self):
        super().__init__('skin_fsr_node', enable_rosout=True)
        self.timer_period = 1/30
        self.msg_timer = self.create_timer(self.timer_period, self.timer_cb)

        self.fsr_msg = Int32MultiArray()

        try:
            self.leonardo_fsr = serial.Serial(port="/dev/ttyFSR", baudrate=115200, timeout=0.5)

            if self.leonardo_fsr.is_open:
                self.get_logger().info("\033[32m Serial port opened successfully...\033[0m")
            else:
                self.leonardo_fsr.open()
                self.get_logger().info("\033[32m Serial port opened successfully...\033[0m")

        except Exception as e:
            print(e)
            self.get_logger().warn("\033[32m Serial port open fail...\033[0m")
            exit(0)
        else:
            self.pub_fsr_ = self.create_publisher(Int32MultiArray, "skin_fsr", 10)

        self.get_logger().info("\033[32m Node initation done...\033[0m")

    def timer_cb(self):
        try:
            buff_count = self.leonardo_fsr.in_waiting
        except Exception as e:
            print("exception:" + str(e))
            print("FSR Loss of connection, poor contact, or broken wire")
            exit(0)
        else:
            if buff_count > 0:
                serial_data = self.leonardo_fsr.readline().decode('utf-8').strip()
                serial_data = serial_data[0:-1]
                # self.get_logger().info(f'{serial_data}')
                try:
                    int_data = list(map(int, serial_data.split(',')))
                except Exception as e:
                    self.get_logger().warn(f"\033[31m FSR parse failed... load all 0 array : {e} \033[0m")
                    int_data = [0]*28

                if len(int_data) == 28:  # 데이터가 12개일 경우에만 publish
                    self.fsr_msg.data = int_data
                    self.pub_fsr_.publish(self.fsr_msg)
                    # self.get_logger().info(f'Publishing: {self.fsr_msg.data}')

    def __del__(self):
        self.get_logger().info("Node destroyer called...")
        self.destroy_timer(self.msg_timer)
        self.leonardo_fsr.close()
        self.get_logger().info("Node has been terminated sucessfully...")

def main(args = None):
    find_ttyUSB()
    rclpy.init(args=args)
    fsr_node = skin_fsr_node()
    rclpy.spin(fsr_node)

    fsr_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

