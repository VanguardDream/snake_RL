import serial
import numpy as np
import serpenoid_gamma
import time
from defines import *
from dynamixel_sdk import *
from typing import List, Union

def gait_config(motion:tuple[float, float, float, float, float, float, float, float], curve:tuple[float, float, float, float, float, float, float, float], en:bool, gamma:float)->np.ndarray:
    # Optimal with acceleration values

    gait = serpenoid_gamma.Gait(motion,curve,gamma)
    q = 0

    if en:  
        q = gait.CurveFunction
    else:
        q = gait.Gk

    return q

def comm_config()->List[Union[PortHandler, Protocol2PacketHandler, GroupSyncWrite, GroupSyncRead,GroupSyncRead, GroupSyncRead]]:
    porth = PortHandler(DEVICENAME)
    packh = PacketHandler(PROTOCOL_VERSION)

    gs_pos_write = GroupSyncWrite(porth, packh, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
    
    gs_pos_read = GroupSyncRead(porth, packh, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
    gs_vel_read = GroupSyncRead(porth, packh, ADDR_PRESENT_VELOCITY, LEN_PRESENT_VELOCITY)
    gs_cur_read = GroupSyncRead(porth, packh, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT)

    try:
        porth.openPort()

        if porth.is_open:
            print("\033[32m Serial port opened successfully...\033[0m")
        else:
            print("\033[31m Serial port is not opened...\033[0m")
            exit(0)
    except Exception as e:
        print(e)
        print("\033[31m Serial port open fail...\033[0m")
        exit(0)

    try:
        porth.setBaudRate(BAUDRATE)
    except Exception as e:
        print(e)
        print("\033[31m Setting baudrate fail...\033[0m")
        exit(0)
    else:
        print("\033[32m Buadrate is set...\033[0m")

    return [porth, packh, gs_pos_write, gs_pos_read, gs_vel_read, gs_cur_read]

def motors_reset(port:PortHandler,packet:Protocol2PacketHandler,en:bool)->None:

    for i in range(14):
        packet.write1ByteTxOnly(port,i,ADDR_TORQUE_ENABLE,0)

    time.sleep(0.5)

    for i in range(14):
        packet.write1ByteTxOnly(port,i,ADDR_TORQUE_ENABLE,0)

    time.sleep(0.5)

    if en:
        for i in range(14):
            packet.write1ByteTxOnly(port,i,ADDR_TORQUE_ENABLE,1)

        time.sleep(0.5)

        for i in range(14):
            packet.write1ByteTxOnly(port,i,ADDR_TORQUE_ENABLE,1)

        print("\033[32m Motor enabling done...\033[0m")

        time.sleep(0.5)
        for i in range(14):
            packet.write4ByteTxOnly(port,i,ADDR_GOAL_POSITION,2048)

        print("\033[32m Motor homing done...\033[0m")
    else:
        for i in range(14):
            packet.write1ByteTxOnly(port,i,ADDR_TORQUE_ENABLE,0)

        print("\033[32m Motor torque off...\033[0m")
        
def rad2dynamixel(rad:float)->int:
    deg = np.rad2deg(rad)
    pulse = np.round(deg/0.088)

    return int(2048 + pulse)

if __name__ == "__main__":
    ac_roll_op = (15, 15, 171, 171, 118, 118, 90, 0.05)
    ac_side_op = (45, 45, 24, 24, 62, 62, 45, 0.05)
    ac_slit_op = (45, 45, 32, 32, 117, 117/2, 0, 0.05)
    ac_serp_op = (45, 45, 162, 162, 84, 84, 0, 0.05)

    print('Initiating...')
    q = gait_config(ac_slit_op, ac_slit_op, False, 0.7071)
    print('Gait creating done...')

    poh, pah, pos_writer, pos_reader, vel_reader, cur_reader = comm_config()

    motors_reset(poh,pah,True)

    input("Press any key to move")

    pos_stack = np.empty((0,14))
    vel_stack = np.empty((0,14))
    cur_stack = np.empty((0,14))

    for i in q.T:
        up_t = time.time()
        index = np.nonzero(i)[0]

        for idx in index:
            param_goal_position = [DXL_LOBYTE(DXL_LOWORD(rad2dynamixel(i[idx]))), DXL_HIBYTE(DXL_LOWORD(rad2dynamixel(i[idx]))), DXL_LOBYTE(DXL_HIWORD(rad2dynamixel(i[idx]))), DXL_HIBYTE(DXL_HIWORD(rad2dynamixel(i[idx])))]

            dxl_add_param_result = pos_writer.addParam(idx, param_goal_position)
            if dxl_add_param_result != True:
                print("\033[31m [ID:%03d] Addparam fail(action)...\033[0m" % idx)

        dxl_comm_result = pos_writer.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("\033[31m GBPP_Tx fail with error %s \033[0m" % pah.getTxRxResult(dxl_comm_result))

        ### Sensing add params
        for id in range(14):
            dxl_add_param_result = pos_reader.addParam(id)
            if dxl_add_param_result != True:
                print("\033[31m [ID:%03d] Addparam fail(p pos)...\033[0m" % id)

        for id in range(14):
            dxl_add_param_result = vel_reader.addParam(id)
            if dxl_add_param_result != True:
                print("\033[31m [ID:%03d] Addparam fail(p vel)...\033[0m" % id)

        for id in range(14):
            dxl_add_param_result = cur_reader.addParam(id)
            if dxl_add_param_result != True:
                print("\033[31m [ID:%03d] Addparam fail(p cur)...\033[0m" % id)

        ### Sensing TxRx
        dxl_comm_result = pos_reader.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("\033[31m GBPP_TxRx fail with error %s \033[0m" % pah.getTxRxResult(dxl_comm_result))
        for id in range(14):
            dxl_get_data_result = pos_reader.isAvailable(id,ADDR_PRESENT_POSITION,LEN_PRESENT_POSITION)
            if dxl_get_data_result != True:
                print("\033[31m [ID:%03d] Getdata failed (p pos)... \033[0m" % id)

        dxl_comm_result = vel_reader.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("\033[31m GBPP_TxRx fail with error %s \033[0m" % pah.getTxRxResult(dxl_comm_result))
        for id in range(14):
            dxl_get_data_result = vel_reader.isAvailable(id,ADDR_PRESENT_VELOCITY,LEN_PRESENT_VELOCITY)
            if dxl_get_data_result != True:
                print("\033[31m [ID:%03d] Getdata failed (p vel)... \033[0m" % id)

        dxl_comm_result = cur_reader.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("\033[31m GBPP_TxRx fail with error %s \033[0m" % pah.getTxRxResult(dxl_comm_result))
        for id in range(14):
            dxl_get_data_result = cur_reader.isAvailable(id,ADDR_PRESENT_CURRENT,LEN_PRESENT_CURRENT)
            if dxl_get_data_result != True:
                print("\033[31m [ID:%03d] Getdata failed (p vel)... \033[0m" % id)

        ### Saving data
        pos = np.zeros(14)
        vel = np.zeros(14)
        cur = np.zeros(14)

        for id in range(14):
            # pos[id] = pos_reader.getData(id,ADDR_PRESENT_POSITION,LEN_PRESENT_POSITION)
            # if pos[id] > 0x7fffffff:
                # pos[id] -= 4294967296 
            # vel[id] = vel_reader.getData(id,ADDR_PRESENT_VELOCITY,LEN_PRESENT_VELOCITY)
            # if vel[id] > 0x7fffffff:
            #     vel[id] -= 4294967296 
            cur[id] = cur_reader.getData(id,ADDR_PRESENT_CURRENT,LEN_PRESENT_CURRENT)
            if cur[id] > 0x7fff:
                cur[id] -= 65536

        pos_stack = np.vstack((pos_stack,pos))
        vel_stack = np.vstack((vel_stack,vel))
        cur_stack = np.vstack((cur_stack,cur))

        pos_reader.clearParam()
        vel_reader.clearParam()
        cur_reader.clearParam()
        pos_writer.clearParam()
        # print(time.time() - up_t)
        while time.time() - up_t < 0.05:
            pass

    motors_reset(poh,pah,False)
    poh.closePort()

    
