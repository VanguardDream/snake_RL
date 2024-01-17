// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from horcrux_interfaces:msg/MotorState.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__STRUCT_H_
#define HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Struct defined in msg/MotorState in the package horcrux_interfaces.
/**
  * ROM Area
 */
typedef struct horcrux_interfaces__msg__MotorState
{
  uint16_t id;
  uint32_t baudrate;
  /// RAM Area
  bool torque;
  float goal_current;
  float goal_velocity;
  float goal_position;
  float present_current;
  float present_velocity;
  float present_position;
  float voltage;
  float temperature;
} horcrux_interfaces__msg__MotorState;

// Struct for a sequence of horcrux_interfaces__msg__MotorState.
typedef struct horcrux_interfaces__msg__MotorState__Sequence
{
  horcrux_interfaces__msg__MotorState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} horcrux_interfaces__msg__MotorState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__STRUCT_H_
