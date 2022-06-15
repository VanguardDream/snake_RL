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

_DEFAULT_TIME_LIMIT = 20
_CONTROL_TIMESTEP = .01

def make_model():
    """ This function returns XML """
    
    xml_string = common.read_model('snake.xml')

    parser = etree.XMLParser(remove_blank_text=True)
    mjcf = etree.XML(xml_string, parser)

    #나중에 지형 변경 코드 추가 가능할 듯

    return etree.tostring(mjcf, pretty_print=True)

<<<<<<< HEAD
@SUITE.add()
def crawl(time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None):
    """Returns the crawl task."""
    xml_string = make_model()
    physics = Physics.from_xml_string(xml_string, common.ASSETS)
    task = Move(desired_speed=_WALK_SPEED, random=random)
    environment_kwargs = environment_kwargs or {}
    return control.Environment(physics, task, time_limit=time_limit,
                                control_timestep=_CONTROL_TIMESTEP,
                                **environment_kwargs)

class Physics(mujoco.Physics):
    """Physics simulation with additional features for the Quadruped domain."""

    def _reload_from_data(self, data):
        super()._reload_from_data(data)
        # Clear cached sensor names when the physics is reloaded.
        self._sensor_types_to_names = {}
        self._hinge_names = []

    def _get_sensor_names(self, *sensor_types):
        try:
            sensor_names = self._sensor_types_to_names[sensor_types]
        except KeyError:
            [sensor_ids] = np.where(np.in1d(self.model.sensor_type, sensor_types))
            sensor_names = [self.model.id2name(s_id, 'sensor') for s_id in sensor_ids]
            self._sensor_types_to_names[sensor_types] = sensor_names
        return sensor_names


class Move(base.Task):
    """A quadruped task solved by moving forward at a designated speed."""

    def __init__(self, desired_speed, random=None):
        """Initializes an instance of `Move`.
        Args:
            desired_speed: A float. If this value is zero, reward is given simply
            for standing upright. Otherwise this specifies the horizontal velocity
            at which the velocity-dependent reward component is maximized.
            random: Optional, either a `numpy.random.RandomState` instance, an
            integer seed for creating a new `RandomState`, or None to select a seed
            automatically (default).
        """
        self._desired_speed = desired_speed
        super().__init__(random=random)

    def initialize_episode(self, physics):  
        """Sets the state of the environment at the start of each episode.
        Args:
            physics: An instance of `Physics`.
        """
        # Initial configuration.
        orientation = self.random.randn(4)
        orientation /= np.linalg.norm(orientation)
        _find_non_contacting_height(physics, orientation)
        super().initialize_episode(physics)

    def get_observation(self, physics):
        """Returns an observation to the agent."""
        return _common_observations(physics)

    def get_reward(self, physics):
        """Returns a reward to the agent."""

        # Move reward term.
        move_reward = rewards.tolerance(
            physics.torso_velocity()[0],
            bounds=(self._desired_speed, float('inf')),
            margin=self._desired_speed,
            value_at_margin=0.5,
            sigmoid='linear')

        return _upright_reward(physics) * move_reward
=======
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
>>>>>>> 6ca823b2315c10bfdef089385cf38f39b1db15b0
