from time import sleep
from xmlrpc.client import Boolean
import pygame
import gait as g
import threading
import datetime
import numpy as np
from dynamixel_sdk import *
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


# Define Variables
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_POSITION       = 132

LEN_GOAL_POSITION           = 4

DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
BAUDRATE                    = 3000000 # -> 통신 속도 조절

PROTOCOL_VERSION            = 2.0

# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
# DEVICENAME                  = 'COM1'
# DEVICENAME                    = '/dev/tty.usbserial-FT3M9YHP'
DEVICENAME                    = '/dev/tty.usbmodemFFFFFFFEFFFF1' #OpenCR

portHandler = PortHandler(DEVICENAME)
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

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def tnewline(self, screen):
        textBitmap = self.font.render("", True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 15
        self.y = 15
        self.line_height = 25

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

def tx_thread(idx:int, degree:float)->None:
    # goalP = np.uint32(2048)
    goalP = int(2048 + (degree * (1/0.088)))
    packetHandler.write4ByteTxRx(portHandler, (idx), ADDR_GOAL_POSITION, (goalP))

    # print("idx: {} degree: {}   ".format(idx,goalP),end="\r")

def tx_en_thread(en:int)->None:
    for i in range(14):
        packetHandler.write1ByteTxOnly(portHandler, (i), ADDR_TORQUE_ENABLE, en)

def tx_reset()->None:
    tx_en_thread(0)
    sleep(0.001)
    tx_en_thread(1)

    sleep(0.001)
    for i in range(14):
        packetHandler.write4ByteTxOnly(portHandler, (i), ADDR_GOAL_POSITION, 2048)



done = False
controller = [0, 0, 0, 0, 0, 0, 0] # axis 0 ~ 2 and bt5
bt_flip = False

side_gait = g.gait(2, 37.2, 37.4, -8, 61.9, 61.7, 1, 1)
serp_gait = g.gait(1, 55.7, 57.2, -9.5, 70.5, 76.5, 10, 1)
rot_gait = g.gait(1, 55.7, 57.2, -9.5, 70.5, 76.5, 10, 1)

# tx_th = threading.Thread(target=tx_thread)

def pthread():
    o_t = datetime.datetime.now()
    p_t = o_t
    k = 0
    global bt_flip

    while not done:
        n_t = datetime.datetime.now()
        gait_comm = np.array(controller)
        motor_comand = np.array([])
        en_move = False

        if (n_t - p_t).microseconds > 9000:
            p_t = n_t

            ax_idx = np.argmax(abs(gait_comm[:3]))

            if abs(gait_comm[ax_idx]) > 0.1:
                en_move = True
                if gait_comm[ax_idx] > 0:
                    k = k + 1
                else:
                    k = k - 1

            if en_move:
                if ax_idx == 0:
                    motor_comand = rot_gait.generate(k) * abs(gait_comm[ax_idx])
                    motor_idx = rot_gait.commandIdx(k)
                elif ax_idx == 1:
                    motor_comand = serp_gait.generate(k) * abs(gait_comm[ax_idx])
                    motor_idx = serp_gait.commandIdx(k)
                elif ax_idx == 2:
                    motor_comand = side_gait.generate(k) * abs(gait_comm[ax_idx])
                    motor_idx = side_gait.commandIdx(k)
                else:
                    pass
                    
                if gait_comm[3] == 1:
                    tx_en = threading.Thread(target=tx_en_thread,args=[1])
                    tx_en.run()
                    # tx_en_thread(1)
                    # print("Enabled")

                elif gait_comm[5]  == 1:

                    print("Gait Changed")

                elif gait_comm[4] == 1:
                    tx_en = threading.Thread(target=tx_en_thread,args=[0])
                    tx_en.run()
                    # tx_en_thread(0)
                    # print("Diable")
                elif gait_comm[6] == 1:
                    tx_set = threading.Thread(target=tx_reset)
                    tx_set.run()
                    # tx_reset()
                elif en_move:
                    tx_th = threading.Thread(target=tx_thread, args=(int(motor_idx), float(motor_comand[motor_idx])))
                    tx_th.run()
                    # tx_thread(int(motor_idx),float(motor_comand[motor_idx]))

            # print(motor_idx)
            # print(ax_idx)

            # for _ in range(len(motor_comand) -1):
            #     print(" {:2.2f},".format(float(motor_comand[_])), end="")
            # print(" {:2.2f},".format(float(motor_comand[13])))

pygame.init()

t = threading.Thread(target=pthread)
t.daemon = True

t.start()

screen = pygame.display.set_mode((700, 400))

pygame.display.set_caption("Snake Control")



clock = pygame.time.Clock()

pygame.joystick.init()

textPrint = TextPrint()

p_tick = 0
_up = 0

# -------- Main Program Loop -----------
while not done:

    _event_checker = False
    screen.fill(WHITE)
    textPrint.reset()

    n_tick = pygame.time.get_ticks()

    textPrint.tprint(screen,"Program Timer: {}ms".format(n_tick))
    textPrint.indent()

    # if n_tick - p_tick > 10:
    #     _up = _up + 1
    #     p_tick = n_tick

    # textPrint.tprint(screen, "tick counts: {}, k-value: {}".format(_up, _up%14))

    textPrint.tnewline(screen)

    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.

    joystick_count = pygame.joystick.get_count()

    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            # get_instance_id() is an SDL2 method
            jid = joystick.get_id()
        textPrint.tprint(screen, "Joystick {}".format(jid))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        try:
            guid = joystick.get_guid()
        except AttributeError:
            # get_guid() is an SDL2 method
            pass
        else:
            textPrint.tprint(screen, "GUID: {}".format(guid))


        controller = [round(joystick.get_axis(0),2), round(-joystick.get_axis(1),2), round(joystick.get_axis(3),2), joystick.get_button(0), joystick.get_button(1), joystick.get_button(2), joystick.get_button(3)]
    
    textPrint.tprint(screen,"Controller input: Ax1: {:2.2f}, Ax2: {:2.2f}, Ax3: {:2.2f}, BT: {}".format(controller[0],controller[1],controller[2],controller[3]))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()