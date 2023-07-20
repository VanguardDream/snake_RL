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


def main(ia, ia2):
    a = np.radians(ia)
    a2 = np.radians(ia2)

    b = np.radians(0)
    b2 = np.radians(0)

    e_d1 = np.radians(45)
    e_l1 = np.radians(45)

    e_d2 = 4
    e_l2 = 4

    delta = np.radians(0) # for serpenoid
    # delta = np.radians(45) # for sidewinding
    # delta = np.radians(90) # for roll

    print("Setting group communication objects...")
    # Add parameter storage for Dynamixel#1 present position value
    # for idx in range(14):
    #     dxl_addparam_result = gsread_PP.addParam(idx)
    #     if dxl_addparam_result != True:
    #         print("[ID:%03d] groupSyncRead addparam failed" % idx)
    #         quit()

    # for idx in range(14):
    #     dxl_addparam_result = gsread_PV.addParam(idx)
    #     if dxl_addparam_result != True:
    #         print("[ID:%03d] groupSyncRead addparam failed" % idx)
    #         quit()



    for i in range(0,400):
        presentP = np.empty(14)
        presentV = np.empty(14)
        goal = serpenoid(i/10, b, b2,a, a2, e_d1, e_d2, e_l1, e_l2, delta)

        commandQ = time.time()

        goal = np.degrees(goal.copy())
        goalP = np.uint32(2048 + goal.squeeze() * (1 / 0.088))

        for idx in range(14):
            gswrite.addParam(idx, [DXL_LOBYTE(DXL_LOWORD(goalP[idx])), DXL_HIBYTE(DXL_LOWORD(goalP[idx])), DXL_LOBYTE(DXL_HIWORD(goalP[idx])), DXL_HIBYTE(DXL_HIWORD(goalP[idx]))])
                    
        while(True):
            t_period = time.time() - commandQ

            if t_period > 0.1:
                 # Syncwrite goal position
                dxl_comm_result = gswrite.txPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))


                for idx in range(14):
                    dxl_addparam_result = gsread_PP.addParam(idx)
                    if dxl_addparam_result != True:
                        print("[ID:%03d] groupSyncRead addparam failed" % idx)
                        quit()

                # Get present position & velocity value
                dxl_comm_result = gsread_PP.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

                for idx in range(14):
                    dxl_getPdata_result = gsread_PP.isAvailable(idx, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
                    if dxl_getPdata_result != True:
                        print("[ID:%03d] groupSyncRead getdata failed" % idx)
                        quit()

                for idx in range(14):
                    dxl_addparam_result = gsread_PV.addParam(idx)
                    if dxl_addparam_result != True:
                        print("[ID:%03d] groupSyncRead addparam failed" % idx)
                        quit()

                dxl_comm_result = gsread_PV.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))               

                for idx in range(14):
                    dxl_getVdata_result = gsread_PV.isAvailable(idx, ADDR_PRESENT_VELOCITY, LEN_PRESENT_POSITION)
                    if dxl_getVdata_result != True:
                        print("[ID:%03d] groupSyncRead getdata failed" % idx)
                        quit()

                # dxl_comm_result = gsread_PV.txRxPacket()
                # if dxl_comm_result != COMM_SUCCESS:
                #     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))



                presentP[idx] = gsread_PP.getData(idx, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
                presentV[idx] = gsread_PV.getData(idx, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)
                
                break

            print(f"Running... {i / 10} sec.",end="\r")
            
        gswrite.clearParam()
        gsread_PP.clearParam()
        gsread_PV.clearParam()

    print("\nTerminated...")
    

            

                

    
if __name__ == "__main__":
    # 실험용 인풋 파라미터
    ia = 30
    ia2 = 30

    # 모터 세팅 프로세스 시작!

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
    BAUDRATE                    = 3000000 # -> 통신 속도 조절

    PROTOCOL_VERSION            = 2.0

    # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
    DEVICENAME                  = 'COM8'
    # DEVICENAME                    = '/dev/tty.usbserial-FT3M9YHP'


    # Initialize PortHandler instance 
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    
    # Initialize groupBulkWrite Struct
    gswrite = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

    # Initialize Groupsyncwrite instance
    gsread_PP = GroupSyncRead(portHandler, packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
    gsread_PV = GroupSyncRead(portHandler, packetHandler, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)

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
        packetHandler.write1ByteTxRx(portHandler,(i), ADDR_STATUS_RETURN_LEVEL, 1)


    #모터 세팅 프로세스 끝!

    print('Ready for moving! press any key to move')
    getch()

    main(ia, ia2)

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