// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from horcrux_interfaces:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_H_
#define HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'motors'
#include "horcrux_interfaces/msg/detail/motor_states__struct.h"
// Member 'joy'
#include "sensor_msgs/msg/detail/joy__struct.h"
// Member 'imu'
#include "sensor_msgs/msg/detail/imu__struct.h"
// Member 'mag'
#include "sensor_msgs/msg/detail/magnetic_field__struct.h"

/// Struct defined in msg/RobotState in the package horcrux_interfaces.
/**
  * Header
 */
typedef struct horcrux_interfaces__msg__RobotState
{
  std_msgs__msg__Header header;
  /// Motor State
  horcrux_interfaces__msg__MotorStates motors;
  /// Sensor State
  sensor_msgs__msg__Joy joy;
  sensor_msgs__msg__Imu imu;
  sensor_msgs__msg__MagneticField mag;
} horcrux_interfaces__msg__RobotState;

// Struct for a sequence of horcrux_interfaces__msg__RobotState.
typedef struct horcrux_interfaces__msg__RobotState__Sequence
{
  horcrux_interfaces__msg__RobotState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} horcrux_interfaces__msg__RobotState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_H_
