// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from horcrux_interfaces:msg/MotorStates.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "horcrux_interfaces/msg/detail/motor_states__rosidl_typesupport_introspection_c.h"
#include "horcrux_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "horcrux_interfaces/msg/detail/motor_states__functions.h"
#include "horcrux_interfaces/msg/detail/motor_states__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `motors`
#include "horcrux_interfaces/msg/motor_state.h"
// Member `motors`
#include "horcrux_interfaces/msg/detail/motor_state__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  horcrux_interfaces__msg__MotorStates__init(message_memory);
}

void horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_fini_function(void * message_memory)
{
  horcrux_interfaces__msg__MotorStates__fini(message_memory);
}

size_t horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__size_function__MotorStates__motors(
  const void * untyped_member)
{
  (void)untyped_member;
  return 14;
}

const void * horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__get_const_function__MotorStates__motors(
  const void * untyped_member, size_t index)
{
  const horcrux_interfaces__msg__MotorState * member =
    (const horcrux_interfaces__msg__MotorState *)(untyped_member);
  return &member[index];
}

void * horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__get_function__MotorStates__motors(
  void * untyped_member, size_t index)
{
  horcrux_interfaces__msg__MotorState * member =
    (horcrux_interfaces__msg__MotorState *)(untyped_member);
  return &member[index];
}

void horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__fetch_function__MotorStates__motors(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const horcrux_interfaces__msg__MotorState * item =
    ((const horcrux_interfaces__msg__MotorState *)
    horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__get_const_function__MotorStates__motors(untyped_member, index));
  horcrux_interfaces__msg__MotorState * value =
    (horcrux_interfaces__msg__MotorState *)(untyped_value);
  *value = *item;
}

void horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__assign_function__MotorStates__motors(
  void * untyped_member, size_t index, const void * untyped_value)
{
  horcrux_interfaces__msg__MotorState * item =
    ((horcrux_interfaces__msg__MotorState *)
    horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__get_function__MotorStates__motors(untyped_member, index));
  const horcrux_interfaces__msg__MotorState * value =
    (const horcrux_interfaces__msg__MotorState *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(horcrux_interfaces__msg__MotorStates, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "motors",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    14,  // array size
    false,  // is upper bound
    offsetof(horcrux_interfaces__msg__MotorStates, motors),  // bytes offset in struct
    NULL,  // default value
    horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__size_function__MotorStates__motors,  // size() function pointer
    horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__get_const_function__MotorStates__motors,  // get_const(index) function pointer
    horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__get_function__MotorStates__motors,  // get(index) function pointer
    horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__fetch_function__MotorStates__motors,  // fetch(index, &value) function pointer
    horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__assign_function__MotorStates__motors,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_message_members = {
  "horcrux_interfaces__msg",  // message namespace
  "MotorStates",  // message name
  2,  // number of fields
  sizeof(horcrux_interfaces__msg__MotorStates),
  horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_message_member_array,  // message members
  horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_init_function,  // function to initialize message memory (memory has to be allocated)
  horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_message_type_support_handle = {
  0,
  &horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_message_members,
  get_message_typesupport_handle_function,
  &horcrux_interfaces__msg__MotorStates__get_type_hash,
  &horcrux_interfaces__msg__MotorStates__get_type_description,
  &horcrux_interfaces__msg__MotorStates__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_horcrux_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, horcrux_interfaces, msg, MotorStates)() {
  horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, horcrux_interfaces, msg, MotorState)();
  if (!horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_message_type_support_handle.typesupport_identifier) {
    horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &horcrux_interfaces__msg__MotorStates__rosidl_typesupport_introspection_c__MotorStates_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif