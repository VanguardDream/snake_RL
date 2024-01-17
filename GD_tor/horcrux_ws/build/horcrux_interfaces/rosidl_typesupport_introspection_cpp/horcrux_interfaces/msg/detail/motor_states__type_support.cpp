// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from horcrux_interfaces:msg/MotorStates.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "horcrux_interfaces/msg/detail/motor_states__functions.h"
#include "horcrux_interfaces/msg/detail/motor_states__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace horcrux_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void MotorStates_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) horcrux_interfaces::msg::MotorStates(_init);
}

void MotorStates_fini_function(void * message_memory)
{
  auto typed_message = static_cast<horcrux_interfaces::msg::MotorStates *>(message_memory);
  typed_message->~MotorStates();
}

size_t size_function__MotorStates__motors(const void * untyped_member)
{
  (void)untyped_member;
  return 14;
}

const void * get_const_function__MotorStates__motors(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<horcrux_interfaces::msg::MotorState, 14> *>(untyped_member);
  return &member[index];
}

void * get_function__MotorStates__motors(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<horcrux_interfaces::msg::MotorState, 14> *>(untyped_member);
  return &member[index];
}

void fetch_function__MotorStates__motors(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const horcrux_interfaces::msg::MotorState *>(
    get_const_function__MotorStates__motors(untyped_member, index));
  auto & value = *reinterpret_cast<horcrux_interfaces::msg::MotorState *>(untyped_value);
  value = item;
}

void assign_function__MotorStates__motors(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<horcrux_interfaces::msg::MotorState *>(
    get_function__MotorStates__motors(untyped_member, index));
  const auto & value = *reinterpret_cast<const horcrux_interfaces::msg::MotorState *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember MotorStates_message_member_array[2] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(horcrux_interfaces::msg::MotorStates, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "motors",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<horcrux_interfaces::msg::MotorState>(),  // members of sub message
    true,  // is array
    14,  // array size
    false,  // is upper bound
    offsetof(horcrux_interfaces::msg::MotorStates, motors),  // bytes offset in struct
    nullptr,  // default value
    size_function__MotorStates__motors,  // size() function pointer
    get_const_function__MotorStates__motors,  // get_const(index) function pointer
    get_function__MotorStates__motors,  // get(index) function pointer
    fetch_function__MotorStates__motors,  // fetch(index, &value) function pointer
    assign_function__MotorStates__motors,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers MotorStates_message_members = {
  "horcrux_interfaces::msg",  // message namespace
  "MotorStates",  // message name
  2,  // number of fields
  sizeof(horcrux_interfaces::msg::MotorStates),
  MotorStates_message_member_array,  // message members
  MotorStates_init_function,  // function to initialize message memory (memory has to be allocated)
  MotorStates_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t MotorStates_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &MotorStates_message_members,
  get_message_typesupport_handle_function,
  &horcrux_interfaces__msg__MotorStates__get_type_hash,
  &horcrux_interfaces__msg__MotorStates__get_type_description,
  &horcrux_interfaces__msg__MotorStates__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace horcrux_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<horcrux_interfaces::msg::MotorStates>()
{
  return &::horcrux_interfaces::msg::rosidl_typesupport_introspection_cpp::MotorStates_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, horcrux_interfaces, msg, MotorStates)() {
  return &::horcrux_interfaces::msg::rosidl_typesupport_introspection_cpp::MotorStates_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
