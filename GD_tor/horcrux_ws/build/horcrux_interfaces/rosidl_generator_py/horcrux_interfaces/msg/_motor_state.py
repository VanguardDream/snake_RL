# generated from rosidl_generator_py/resource/_idl.py.em
# with input from horcrux_interfaces:msg/MotorState.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_MotorState(type):
    """Metaclass of message 'MotorState'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('horcrux_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'horcrux_interfaces.msg.MotorState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__motor_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__motor_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__motor_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__motor_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__motor_state

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MotorState(metaclass=Metaclass_MotorState):
    """Message class 'MotorState'."""

    __slots__ = [
        '_id',
        '_baudrate',
        '_torque',
        '_goal_current',
        '_goal_velocity',
        '_goal_position',
        '_present_current',
        '_present_velocity',
        '_present_position',
        '_voltage',
        '_temperature',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'id': 'uint16',
        'baudrate': 'uint32',
        'torque': 'boolean',
        'goal_current': 'float',
        'goal_velocity': 'float',
        'goal_position': 'float',
        'present_current': 'float',
        'present_velocity': 'float',
        'present_position': 'float',
        'voltage': 'float',
        'temperature': 'float',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.id = kwargs.get('id', int())
        self.baudrate = kwargs.get('baudrate', int())
        self.torque = kwargs.get('torque', bool())
        self.goal_current = kwargs.get('goal_current', float())
        self.goal_velocity = kwargs.get('goal_velocity', float())
        self.goal_position = kwargs.get('goal_position', float())
        self.present_current = kwargs.get('present_current', float())
        self.present_velocity = kwargs.get('present_velocity', float())
        self.present_position = kwargs.get('present_position', float())
        self.voltage = kwargs.get('voltage', float())
        self.temperature = kwargs.get('temperature', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.id != other.id:
            return False
        if self.baudrate != other.baudrate:
            return False
        if self.torque != other.torque:
            return False
        if self.goal_current != other.goal_current:
            return False
        if self.goal_velocity != other.goal_velocity:
            return False
        if self.goal_position != other.goal_position:
            return False
        if self.present_current != other.present_current:
            return False
        if self.present_velocity != other.present_velocity:
            return False
        if self.present_position != other.present_position:
            return False
        if self.voltage != other.voltage:
            return False
        if self.temperature != other.temperature:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property  # noqa: A003
    def id(self):  # noqa: A003
        """Message field 'id'."""
        return self._id

    @id.setter  # noqa: A003
    def id(self, value):  # noqa: A003
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'id' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'id' field must be an unsigned integer in [0, 65535]"
        self._id = value

    @builtins.property
    def baudrate(self):
        """Message field 'baudrate'."""
        return self._baudrate

    @baudrate.setter
    def baudrate(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'baudrate' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'baudrate' field must be an unsigned integer in [0, 4294967295]"
        self._baudrate = value

    @builtins.property
    def torque(self):
        """Message field 'torque'."""
        return self._torque

    @torque.setter
    def torque(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'torque' field must be of type 'bool'"
        self._torque = value

    @builtins.property
    def goal_current(self):
        """Message field 'goal_current'."""
        return self._goal_current

    @goal_current.setter
    def goal_current(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'goal_current' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'goal_current' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._goal_current = value

    @builtins.property
    def goal_velocity(self):
        """Message field 'goal_velocity'."""
        return self._goal_velocity

    @goal_velocity.setter
    def goal_velocity(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'goal_velocity' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'goal_velocity' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._goal_velocity = value

    @builtins.property
    def goal_position(self):
        """Message field 'goal_position'."""
        return self._goal_position

    @goal_position.setter
    def goal_position(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'goal_position' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'goal_position' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._goal_position = value

    @builtins.property
    def present_current(self):
        """Message field 'present_current'."""
        return self._present_current

    @present_current.setter
    def present_current(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'present_current' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'present_current' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._present_current = value

    @builtins.property
    def present_velocity(self):
        """Message field 'present_velocity'."""
        return self._present_velocity

    @present_velocity.setter
    def present_velocity(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'present_velocity' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'present_velocity' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._present_velocity = value

    @builtins.property
    def present_position(self):
        """Message field 'present_position'."""
        return self._present_position

    @present_position.setter
    def present_position(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'present_position' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'present_position' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._present_position = value

    @builtins.property
    def voltage(self):
        """Message field 'voltage'."""
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'voltage' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'voltage' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._voltage = value

    @builtins.property
    def temperature(self):
        """Message field 'temperature'."""
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'temperature' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'temperature' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._temperature = value
