# DXL defines
ADDR_TORQUE_ENABLE          = 64
ADDR_STATUS_RETURN_LEVEL    = 68
ADDR_GOAL_CURRENT           = 102
ADDR_GOAL_VELOCITY          = 104 
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_CURRENT        = 126
ADDR_PRESENT_VELOCITY       = 128
ADDR_PRESENT_POSITION       = 132
ADDR_PRESENT_VOLTAGE        = 144
ADDR_PRESENT_TEMPERATURE    = 146

LEN_TORQUE_ENABLE           = 1
LEN_GOAL_CURRENT            = 2
LEN_GOAL_VELOCITY           = 4
LEN_GOAL_POSITION           = 4
LEN_PRESENT_CURRENT         = 2
LEN_PRESENT_VELOCITY        = 4
LEN_PRESENT_POSITION        = 4
LEN_PRESENT_VOLTAGE         = 2
LEN_PRESENT_TEMPERATURE     = 1

DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
BAUDRATE                    = 3000000 # -> 통신 속도 조절
# BAUDRATE                    = 57600 # -> 통신 속도 조절

PROTOCOL_VERSION            = 2.0

# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
# DEVICENAME                    = '/dev/ttyDXL'
DEVICENAME                    = '/dev/ttyUSB0'
# DEVICENAME                    = '/dev/tty.usbserial-FT7WBAA4'
# DEVICENAME                    = '/dev/tty.usbserial-FT3M9YHP'

VALUE_STATUS_RETURN_NO_RETURN = 0
VALUE_STATUS_RETURN_ONLY_READ = 1
VALUE_STATUS_RETURN_ALL = 2
