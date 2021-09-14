
import datetime
import time
import gait_lambda
import numpy as np
from dynamixel_sdk import *



def J(g, d_a, d_p, d_l, l_a, l_p, l_l, tau):
    gen = gait_lambda.gait(g, d_a, d_p, d_l, l_a, l_p, l_l, int(tau))

    # Variable for cost(loss) function
    delta_x = 0
    delta_y = 0

    for i in range(0,100):
        goal = gen.generate(i)

        spec_motor = np.nonzero(goal)[0]

        for idx in spec_motor:
            # Commnad motor here
            
            goalP = int(2048 + (goal[idx] * (1/0.088)))
            #simulator.data.ctrl[idx] = gen.degtorad(goal[idx])

            # packetHandler.write4ByteTxOnly(portHandler, (idx+1), ADDR_GOAL_POSITION, goalP)

            print(idx,end=':')
            print(goalP)


            time.sleep(0.01)

        # print('slot end!')
        


def main():
    gait_type = 1
    gait_params = [56.0, 57.7, -9.5, 71.0, 76.2, 10, 1]
    
    # gait_type = 2
    # gait_params = [37.2, 37.4, -8, 61.9, 61.7, 1 ,  3]

    count = 0

    J(gait_type, gait_params[0], gait_params[1], gait_params[2], gait_params[3], gait_params[4],gait_params[5],gait_params[6])

def motorSetting():
    pass


if __name__ == "__main__":

# 모터 세팅 프로세스 시작!

    ADDR_TORQUE_ENABLE          = 64
    ADDR_GOAL_POSITION          = 116
    ADDR_PRESENT_POSITION       = 132
    DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
    DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
    BAUDRATE                    = 57600 # -> 통신 속도 조절

    PROTOCOL_VERSION            = 2.0

    # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
    # DEVICENAME                  = '/dev/ttyUSB0'


    # portHandler = PortHandler(DEVICENAME)
    # packetHandler = PacketHandler(PROTOCOL_VERSION)

    # portHandler.openPort()
    # portHandler.setBaudRate(BAUDRATE)

#모터 세팅 프로세스 끝!
    main()
    print('done!')
