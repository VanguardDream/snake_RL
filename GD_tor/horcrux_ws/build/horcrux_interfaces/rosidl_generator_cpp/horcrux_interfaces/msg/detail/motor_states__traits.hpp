// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from horcrux_interfaces:msg/MotorStates.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__TRAITS_HPP_
#define HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "horcrux_interfaces/msg/detail/motor_states__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'motors'
#include "horcrux_interfaces/msg/detail/motor_state__traits.hpp"

namespace horcrux_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const MotorStates & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: motors
  {
    if (msg.motors.size() == 0) {
      out << "motors: []";
    } else {
      out << "motors: [";
      size_t pending_items = msg.motors.size();
      for (auto item : msg.motors) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotorStates & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: motors
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.motors.size() == 0) {
      out << "motors: []\n";
    } else {
      out << "motors:\n";
      for (auto item : msg.motors) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotorStates & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace horcrux_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use horcrux_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const horcrux_interfaces::msg::MotorStates & msg,
  std::ostream & out, size_t indentation = 0)
{
  horcrux_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use horcrux_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const horcrux_interfaces::msg::MotorStates & msg)
{
  return horcrux_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<horcrux_interfaces::msg::MotorStates>()
{
  return "horcrux_interfaces::msg::MotorStates";
}

template<>
inline const char * name<horcrux_interfaces::msg::MotorStates>()
{
  return "horcrux_interfaces/msg/MotorStates";
}

template<>
struct has_fixed_size<horcrux_interfaces::msg::MotorStates>
  : std::integral_constant<bool, has_fixed_size<horcrux_interfaces::msg::MotorState>::value && has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<horcrux_interfaces::msg::MotorStates>
  : std::integral_constant<bool, has_bounded_size<horcrux_interfaces::msg::MotorState>::value && has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<horcrux_interfaces::msg::MotorStates>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__TRAITS_HPP_
