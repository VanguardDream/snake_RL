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