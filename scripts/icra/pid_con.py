import datetime
import time
import gait_lambda
import numpy as np
from dynamixel_sdk import *
import matplotlib.pyplot as plt
import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def main():
    start_main = datetime.datetime.now()
    end_main = 0
    t_s = start_main
    timestep = 0
    accum_pos = []

    while(True):
        dt = datetime.datetime.now() - t_s

        if dt.microseconds > 10000:
            timestep = timestep + 1

            if timestep == 500:
                #Move to 60 degree (for dynamixel -> 682)
                packetHandler.write4ByteTxOnly(portHandler, JOINT_ID, ADDR_GOAL_POSITION, 2048 + 682)

            if timestep == 1000:
                #Move to -60 degree
                packetHandler.write4ByteTxOnly(portHandler, JOINT_ID, ADDR_GOAL_POSITION, 2048 - 682)

            if timestep == 1500:
                #Move to 60 degree
                packetHandler.write4ByteTxOnly(portHandler, JOINT_ID, ADDR_GOAL_POSITION, 2048 + 682)

            if timestep == 2000:
                #Move to -60 degree
                packetHandler.write4ByteTxOnly(portHandler, JOINT_ID, ADDR_GOAL_POSITION, 2048 - 682)

            #Log Data Code Below
            # now_pos, results, error = packetHandler.read4ByteTxRx(portHandler,JOINT_ID,ADDR_PRESENT_POSITION)

            # accum_pos.append(now_pos)

            t_s = datetime.datetime.now()

        else:
            if timestep >= 2500:
                end_main = datetime.datetime.now()
                break
            continue

    return accum_pos, end_main - start_main


if __name__ == "__main__":
    # 모터 세팅 프로세스 시작!

    ADDR_TORQUE_ENABLE          = 64
    ADDR_GOAL_POSITION          = 116
    ADDR_PRESENT_POSITION       = 132

    LEN_GOAL_POSITION           = 4

    DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
    DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
    BAUDRATE                    = 3000000 # -> 통신 속도 조절

    PROTOCOL_VERSION            = 2.0

    # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
    # DEVICENAME                  = 'COM4'
    DEVICENAME                  = '/dev/tty.usbserial-FT3FSNN5'

    JOINT_ID = 13


    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()


    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()

    packetHandler.write1ByteTxRx(portHandler, JOINT_ID, ADDR_TORQUE_ENABLE, 1)

    # GroupBW = GroupBulkWrite(portHandler,packetHandler)

#모터 세팅 프로세스 끝!

    print('Ready for moving! press any key to move')
    
    getch()
    packetHandler.write4ByteTxOnly(portHandler, JOINT_ID, ADDR_GOAL_POSITION, 2048)

    data, duration = main()

    # plt.plot(list(range(0,2500)), data,'-*')
    # plt.show()

    print(duration.seconds)

    packetHandler.write1ByteTxRx(portHandler, JOINT_ID, ADDR_TORQUE_ENABLE, 0)

    portHandler.closePort()