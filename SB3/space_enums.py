# © 2022 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Date : 2022-08-04 (YYYYMMDD)
# Version : 2022-08-04
# Description : Bong Snake Env Space Iedexing Enum.

from enum import Enum

class ENUM_ACTION(Enum):
    D_amp   =   0
    D_phase =   1
    D_lam   =   2
    L_amp   =   3
    L_phase =   4
    L_lam   =   5
    tau     =   6
    

class ENUM_OBSERVATION(Enum):
    time_step	    =   0
    stride_ratio	=   1
    D_amp	        =   2
    D_phase	        =   3
    D_lam	        =   4
    L_amp	        =   5
    L_phase	        =   6
    L_lam	        =   7
    tau	            =   8
    acc_x	        =   9
    acc_y	        =   10
    acc_z	        =   11
    gyro_x	        =   12
    gyro_y	        =   13
    gyro_z	        =   14
    pos_joint1	    =   15
    pos_joint2	    =   16
    pos_joint3	    =   17
    pos_joint4	    =   18
    pos_joint5	    =   19
    pos_joint6	    =   20
    pos_joint7	    =   21
    pos_joint8	    =   22
    pos_joint9	    =   23
    pos_joint10	    =   24
    pos_joint11	    =   25
    pos_joint12	    =   26
    pos_joint13	    =   27
    pos_joint14	    =   28
    vel_joint1	    =   29
    vel_joint2	    =   30
    vel_joint3	    =   31
    vel_joint4	    =   32
    vel_joint5	    =   33
    vel_joint6	    =   34
    vel_joint7	    =   35
    vel_joint8	    =   36
    vel_joint9	    =   37
    vel_joint10	    =   38
    vel_joint11	    =   39
    vel_joint12	    =   40
    vel_joint13	    =   41
    vel_joint14	    =   42
    torque_joint1	=   43
    torque_joint2	=   44
    torque_joint3	=   45
    torque_joint4	=   46
    torque_joint5	=   47
    torque_joint6	=   48
    torque_joint7	=   49
    torque_joint8	=   50
    torque_joint9	=   51
    torque_joint10	=   52
    torque_joint11	=   53
    torque_joint12	=   54
    torque_joint13	=   55
    torque_joint14	=   56
    pos_head_x	    =   57
    pos_head_y	    =   58
    pos_head_z	    =   59
    pos_com_x	    =   60
    pos_com_y	    =   61
    pos_com_z	    =   62
    quat_head_w	    =   63
    quat_head_x	    =   64
    quat_head_y	    =   65
    quat_head_z	    =   66
    quat_com_w	    =   67
    quat_com_x	    =   68
    quat_com_y	    =   69
    quat_com_z	    =   70

