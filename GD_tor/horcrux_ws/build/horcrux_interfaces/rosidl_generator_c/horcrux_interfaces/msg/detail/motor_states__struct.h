// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from horcrux_interfaces:msg/MotorStates.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__STRUCT_H_
#define HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__STRUCT_H_

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
#include "horcrux_interfaces/msg/detail/motor_state__struct.h"

/// Struct defined in msg/MotorStates in the package horcrux_interfaces.
/**
  * Header
 */
typedef struct horcrux_interfaces__msg__MotorStates
{
  std_msgs__msg__Header header;
  /// Motor States
  horcrux_interfaces__msg__MotorState motors[14];
} horcrux_interfaces__msg__MotorStates;

// Struct for a sequence of horcrux_interfaces__msg__MotorStates.
typedef struct horcrux_interfaces__msg__MotorStates__Sequence
{
  horcrux_interfaces__msg__MotorStates * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} horcrux_interfaces__msg__MotorStates__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__STRUCT_H_
