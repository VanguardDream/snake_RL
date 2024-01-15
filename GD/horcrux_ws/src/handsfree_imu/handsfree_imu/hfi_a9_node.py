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
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
from tf_transformations import quaternion_from_euler
from tf_transformations import euler_from_quaternion

def find_ttyUSB():
    print('imu Default port is /dev/ttyUSB0, If use multiple serial devices, Please use launch after modify in the file imu corresponding serial port')
    posts = [port.device for port in serial.tools.list_ports.comports() if 'USB' in port.device]
    print('Current connection {} Total devices {} ea. : {}'.format('USB', len(posts), posts))


# crc 校验
def checkSum(list_data, check_data):
    data = bytearray(list_data)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return hex(((crc & 0xff) << 8) + (crc >> 8)) == hex(check_data[0] << 8 | check_data[1])

key = 0
flag = 0
buff = {}
angularVelocity = [0, 0, 0]
acceleration = [0, 0, 0]
magnetometer = [0, 0, 0]
angle_degree = [0, 0, 0]
pub_flag = [True, True]
data_right_count = 0

class imu_hfi_a9_node(Node):
    def __init__(self):
        super().__init__('imu_hfi_a9_node', enable_rosout=True)
        self.timer_period = 1/300
        self.msg_timer = self.create_timer(self.timer_period, self.timer_cb)

        self.gra_normalization = True

        self.imu_msg = Imu()
        self.mag_msg = MagneticField()

        try:
            self.hf_imu = serial.Serial(port="/dev/ttyIMU_head", baudrate=921600, timeout=0.5)

            if self.hf_imu.is_open:
                self.get_logger().info("\033[32m Serial port opened successfully...\033[0m")
            else:
                self.hf_imu.open()
                self.get_logger().info("\033[32m Serial port opened successfully...\033[0m")

        except Exception as e:
            print(e)
            self.get_logger().warn("\033[32m Serial port open fail...\033[0m")
            exit(0)
        else:
            self.pub_imu_ = self.create_publisher(Imu, "imu", 10)
            self.pub_mag_ = self.create_publisher(MagneticField, "mag", 10)

        self.get_logger().info("\033[32m Node initation done...\033[0m")

    def timer_cb(self):
        try:
            buff_count = self.hf_imu.in_waiting
        except Exception as e:
            print("exception:" + str(e))
            print("imu Loss of connection, poor contact, or broken wire")
            exit(0)
        else:
            if buff_count > 0:
                buff_data = self.hf_imu.read(buff_count)
                for i in range(0, buff_count):
                    self.handleSerialData(buff_data[i])

    def handleSerialData(self, raw_data):
        global buff, key, angle_degree, magnetometer, acceleration, angularVelocity, pub_flag, data_right_count

        if data_right_count > 200000:
            print("The device transmitted data error, exit")
            exit(0)

        buff[key] = raw_data

        key += 1
        if buff[0] != 0xaa:
            data_right_count += 1
            key = 0
            return
        if key < 3:
            return
        if buff[1] != 0x55:
            key = 0
            return
        if key < buff[2] + 5:  # 根据数据长度位的判断, 来获取对应长度数据
            return

        else:
            data_right_count = 0
            data_buff = list(buff.values())  # 获取字典所以 value

            if buff[2] == 0x2c and pub_flag[0]:
                if checkSum(data_buff[2:47], data_buff[47:49]):
                    data = self.hex_to_ieee(data_buff[7:47])
                    angularVelocity = data[1:4]
                    acceleration = data[4:7]
                    magnetometer = data[7:10]
                else:
                    print('Calibration failure')
                pub_flag[0] = False
            elif buff[2] == 0x14 and pub_flag[1]:
                if checkSum(data_buff[2:23], data_buff[23:25]):
                    data = self.hex_to_ieee(data_buff[7:23])
                    angle_degree = data[1:4]
                else:
                    print('Calibration failure')
                pub_flag[1] = False
            else:
                print("This data processing class does not provide to do this " + str(buff[2]) + " (Kinds of)")
                print("or data errors")
                buff = {}
                key = 0

            buff = {}
            key = 0
            #if pub_flag[0] == True or pub_flag[1] == True:
            #    return
            pub_flag[0] = pub_flag[1] = True
            stamp = Clock().now().to_msg()

            self.imu_msg.header.stamp = stamp
            self.imu_msg.header.frame_id = "base_link"

            self.mag_msg.header.stamp = stamp
            self.mag_msg.header.frame_id = "base_link"

            angle_radian = [angle_degree[i] * math.pi / 180 for i in range(3)]
            qua = quaternion_from_euler(angle_radian[0], -angle_radian[1], -angle_radian[2])

            self.imu_msg.orientation.x = float(qua[0])
            self.imu_msg.orientation.y = float(qua[1])
            self.imu_msg.orientation.z = float(qua[2])
            self.imu_msg.orientation.w = float(qua[3])

            self.imu_msg.angular_velocity.x = float(angularVelocity[0])
            self.imu_msg.angular_velocity.y = float(angularVelocity[1])
            self.imu_msg.angular_velocity.z = float(angularVelocity[2])
            
            acc_k = math.sqrt(acceleration[0] ** 2 + acceleration[1] ** 2 + acceleration[2] ** 2)
            if acc_k == 0:
                acc_k = 1
            
            if self.gra_normalization:
                self.imu_msg.linear_acceleration.x = acceleration[0] * -9.8 / acc_k
                self.imu_msg.linear_acceleration.y = acceleration[1] * -9.8 / acc_k
                self.imu_msg.linear_acceleration.z = acceleration[2] * -9.8 / acc_k
            else:
                self.imu_msg.linear_acceleration.x = acceleration[0] * -9.8
                self.imu_msg.linear_acceleration.y = acceleration[1] * -9.8
                self.imu_msg.linear_acceleration.z = acceleration[2] * -9.8

            self.mag_msg.magnetic_field.x = float(magnetometer[0])
            self.mag_msg.magnetic_field.y = float(magnetometer[1])
            self.mag_msg.magnetic_field.z = float(magnetometer[2])

            self.pub_imu_.publish(self.imu_msg)
            self.pub_mag_.publish(self.mag_msg)

    def hex_to_ieee(self, raw_data):
        ieee_data = []
        raw_data.reverse()
        for i in range(0, len(raw_data), 4):
            data2str =hex(raw_data[i] | 0xff00)[4:6] + hex(raw_data[i + 1] | 0xff00)[4:6] + hex(raw_data[i + 2] | 0xff00)[4:6] + hex(raw_data[i + 3] | 0xff00)[4:6]

            ieee_data.append(struct.unpack('>f', bytes.fromhex(data2str))[0])

        ieee_data.reverse()
        return ieee_data

    def __del__(self):
        self.get_logger().info("Node destroyer called...")
        self.destroy_timer(self.msg_timer)
        self.destroy_publisher(self.pub_imu_)
        self.destroy_publisher(self.pub_mag_)
        self.hf_imu.close()
        self.get_logger().info("Node has been terminated sucessfully...")

def main(args = None):
    find_ttyUSB()
    rclpy.init(args=args)
    imu_node = imu_hfi_a9_node()
    rclpy.spin(imu_node)

    imu_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

