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
    time_step	    = 0
    stride_ratio	= 1
    gait_type	    = 2
    D_amp	        = 3
    D_phase	        = 4
    D_lam	        = 5
    L_amp	        = 6
    L_phase	        = 7
    L_lam	        = 8
    tau	            = 9
    acc_x	        = 10
    acc_y	        = 11
    acc_z	        = 12
    gyro_x	        = 13
    gyro_y	        = 14
    gyro_z	        = 15
    pos_joint1	    = 16
    pos_joint2	    = 17
    pos_joint3	    = 18
    pos_joint4	    = 19
    pos_joint5	    = 20
    pos_joint6	    = 21
    pos_joint7	    = 22
    pos_joint8	    = 23
    pos_joint9	    = 24
    pos_joint10	    = 25
    pos_joint11	    = 26
    pos_joint12	    = 27
    pos_joint13	    = 28
    pos_joint14	    = 29
    vel_joint1	    = 30
    vel_joint2	    = 31
    vel_joint3	    = 32
    vel_joint4	    = 33
    vel_joint5	    = 34
    vel_joint6	    = 35
    vel_joint7	    = 36
    vel_joint8	    = 37
    vel_joint9	    = 38
    vel_joint10	    = 39
    vel_joint11	    = 40
    vel_joint12	    = 41
    vel_joint13	    = 42
    vel_joint14	    = 43
    torque_joint1	= 44
    torque_joint2	= 45
    torque_joint3	= 46
    torque_joint4	= 47
    torque_joint5	= 48
    torque_joint6	= 49
    torque_joint7	= 50
    torque_joint8	= 51
    torque_joint9	= 52
    torque_joint10	= 53
    torque_joint11	= 54
    torque_joint12	= 55
    torque_joint13	= 56
    torque_joint14	= 57
    pos_head_x	    = 58
    pos_head_y	    = 59
    pos_head_z	    = 60
    pos_com_x	    = 61
    pos_com_y	    = 62
    pos_com_z	    = 63
    quat_head_w	    = 64
    quat_head_x	    = 65
    quat_head_y	    = 66
    quat_head_z	    = 67
    quat_com_w	    = 68
    quat_com_x	    = 69
    quat_com_y	    = 70
    quat_com_z	    = 71

