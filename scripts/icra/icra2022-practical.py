import datetime
import time
import gait_lambda
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


def J(g, d_a, d_p, d_l, l_a, l_p, l_l, tau):
    gen = gait_lambda.gait(g, d_a, d_p, d_l, l_a, l_p, l_l, int(tau))

    # Variable for cost(loss) function
    delta_x = 0
    delta_y = 0

    for i in range(0,1000):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        # commandQ = datetime.datetime.now()
        commandQ = time.time()
        for idx in spec_motor:
            # Commnad motor here
            
            goalP = int(2048 + (goal[idx] * (1/0.088)))
            #simulator.data.ctrl[idx] = gen.degtorad(goal[idx])

            # GroupBW.addParam((14-(idx+1)),ADDR_GOAL_POSITION,4,goalP)
            while(True):
                t_period = time.time() - commandQ

                if t_period > 0.01 :
                    packetHandler.write4ByteTxOnly(portHandler, (idx), ADDR_GOAL_POSITION, goalP)
                    break



        


def main():

    # gait_type = 1
    # Optimal
    # gait_params = [39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1]  #EAAI



    # gait_params = [55.7, 57.2, -9.5, 70.5, 76.5, 10, 1] 
    
    # gait_params = [55.7, 57.2, -9.5, 70.5, 74.5, 10, 1] # Poor minus
    # gait_params = [55.7, 57.2, -9.5, 70.5, 78.5, 10, 1] # Poor plus
    
    gait_type = 2
    # gait_params = [52.76,	319.65,	1.99,	72.07,	263.95,	7.91,	1] # EAAI

    # gait_params = [52.76,	319.65,	1.99,	72.07,	262.95,	7.91,	1] #EAAI Op
    gait_params = [52.16,	318.15,	1.99,	72.07,	262.95,	7.91,	1] #EAAI c1
    # gait_params = [52.76,	319.65,	1.99,	72.67,	261.75,	7.91,	1] #EAAI c2


    # [37.2, 37.4, -8, 61.9, 61.7, 1 ,  3] # op

    # gait_params = [38.2, 43.4, -8, 66.0, 51.6, 1 ,  3] 
    # gait_params = [38.2, 43.4, -8, 66.0, 51.6, 1 ,  3] # Poor original op

    # gait_params = [38.2, 41.4, -8, 66.0, 51.6, 1 ,  3] # new optimal
    # gait_params = [38.2, 39.4, -8, 66.0, 51.6, 1 ,  3] # Poor -
    # gait_params = [38.2, 43.4, -8, 66.0, 51.6, 1 ,  3] # Poor +

    




    count = 0

    J(gait_type, gait_params[0], gait_params[1], gait_params[2], gait_params[3], gait_params[4],gait_params[5],gait_params[6])

def motorSetting():
    pass


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
    DEVICENAME                    = '/dev/tty.usbserial-FT3M9YHP'


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