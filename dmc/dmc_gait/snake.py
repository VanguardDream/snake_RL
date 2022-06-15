# 2022 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : DM control snake domain

""" Bong snake Domain for DM control """

import collections

from dm_control import mujoco
from dm_control.mujoco.wrapper import mjbindings
from dm_control.rl import control
from dm_control.suite import base
from dm_control.suite import common
from dm_control.utils import containers
from dm_control.utils import rewards
from dm_control.utils import xml_tools
from lxml import etree
import numpy as np
from scipy import ndimage

enums = mjbindings.enums
mjlib = mjbindings.mjlib

SUITE = containers.TaggedTasks()

def make_model():
    """ This function returns XML """
    
    xml_string = common.read_model('snake.xml')

    parser = etree.XMLParser(remove_blank_text=True)
    mjcf = etree.XML(xml_string, parser)

    #나중에 지형 변경 코드 추가 가능할 듯

    return etree.tostring(mjcf, pretty_print=True)

class Physics(mujoco.Physics):
    """Physics simulation with additional features for the Cartpole domain."""

    def cart_position(self):
        """Returns the position of the cart."""
        return self.named.data.qpos['slider'][0]

    def angular_vel(self):
        """Returns the angular velocity of the pole."""
        return self.data.qvel[1:]

    def pole_angle_cosine(self):
        """Returns the cosine of the pole angle."""
        return self.named.data.xmat[2:, 'zz']

    def bounded_position(self):
        """Returns the state, with pole angle split into sin/cos."""
        return np.hstack((self.cart_position(),
                            self.named.data.xmat[2:, ['zz', 'xz']].ravel()))