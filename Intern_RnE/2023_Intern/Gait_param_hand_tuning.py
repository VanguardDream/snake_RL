import datetime
import time
import numpy as np
from dynamixel_sdk import *
import os

# from scripts.icra.pid_con import DEVICENAME

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


def serpenoid(t, b, b2, a, a2, e_d1, e_d2, e_l1, e_l2, delta):
    #Hirose (1993) serpenoid curve implementations
    f1 = e_d2 * t
    f2 = e_l2 * t

    j_1 = b + a * np.sin(e_d1 + f1)
    j_2 = b2 + a2 * np.sin(e_l1 * 2 + f2 + delta)

    j_3 = b + a * np.sin(e_d1 * 3 + f1)
    j_4 = b2 + a2 * np.sin(e_l1 * 4 + f2 + delta)

    j_5 = b + a * np.sin(e_d1 * 5 + f1)
    j_6 = b2 + a2 * np.sin(e_l1 * 6 + f2 + delta)

    j_7 = b + a * np.sin(e_d1 * 7 + f1)
    j_8 = b2 + a2 * np.sin(e_l1 * 8 + f2 + delta)

    j_9 = b + a * np.sin(e_d1 * 9 + f1)
    j_10 = b2 + a2 * np.sin(e_l1 * 10 + f2 + delta)

    j_11 = b + a * np.sin(e_d1 * 11 + f1)
    j_12 = b2 + a2 * np.sin(e_l1 * 12 + f2 + delta)

    j_13 = b + a * np.sin(e_d1 * 13 + f1)
    j_14 = b2 + a2 * np.sin(e_l1 * 14 + f2 + delta)

    return np.array([j_1, j_2, j_3, j_4, j_5, j_6, j_7, j_8, j_9, j_10, j_11, j_12, j_13, j_14])

    

def main():
    b = 0
    b2 = 0

    a = 1
    a2 = 1

    e_d1 = np.radians(30)
    e_l1 = np.radians(30)

    e_d2 = 1
    e_l2 = 1

    # delta = np.radians(45) # for sidewinding
    delta = np.radians(90) # for serpenoid

    for i in range(0,1830):

        goal = serpenoid(i/10, b, b2,a, a2, e_d1, e_l1, e_d2, e_l2)

        commandQ = time.time()
        for idx in range(15):
            # Commnad motor here
            
            goalP = int(2048 + (goal[idx] * (1/0.088)))
            #simulator.data.ctrl[idx] = gen.degtorad(goal[idx])

            # GroupBW.addParam((14-(idx+1)),ADDR_GOAL_POSITION,4,goalP)
            while(True):
                t_period = time.time() - commandQ

                if t_period > 0.1:
                    packetHandler.write4ByteTxOnly(portHandler, (idx), ADDR_GOAL_POSITION, goalP)
                    break

    
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
    DEVICENAME                  = 'COM4'
    # DEVICENAME                    = '/dev/tty.usbserial-FT3M9YHP'


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

    for i in range(14):
        packetHandler.write1ByteTxRx(portHandler, (i), ADDR_TORQUE_ENABLE, 1)

    # GroupBW = GroupBulkWrite(portHandler,packetHandler)

#모터 세팅 프로세스 끝!

    print('Ready for moving! press any key to move')
    getch()
    main()

    # print('done!')

    for i in range(14):
        packetHandler.write1ByteTxRx(portHandler, (i), ADDR_TORQUE_ENABLE, 0)

    time.sleep(0.1)

    for i in range(14):
        packetHandler.write1ByteTxRx(portHandler, (i), ADDR_TORQUE_ENABLE, 0)

    time.sleep(0.1)

    for i in range(14):
        packetHandler.write1ByteTxRx(portHandler, (i), ADDR_TORQUE_ENABLE, 0)

    time.sleep(0.1)

    for i in range(14):
        packetHandler.write1ByteTxRx(portHandler, (i), ADDR_TORQUE_ENABLE, 0)

    time.sleep(0.1)

    for i in range(14):
        packetHandler.write1ByteTxRx(portHandler, (i), ADDR_TORQUE_ENABLE, 0)

    portHandler.closePort()