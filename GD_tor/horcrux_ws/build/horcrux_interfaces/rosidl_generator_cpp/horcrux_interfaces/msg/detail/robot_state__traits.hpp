// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from horcrux_interfaces:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__TRAITS_HPP_
#define HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "horcrux_interfaces/msg/detail/robot_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'motors'
#include "horcrux_interfaces/msg/detail/motor_states__traits.hpp"
// Member 'joy'
#include "sensor_msgs/msg/detail/joy__traits.hpp"
// Member 'imu'
#include "sensor_msgs/msg/detail/imu__traits.hpp"
// Member 'mag'
#include "sensor_msgs/msg/detail/magnetic_field__traits.hpp"

namespace horcrux_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const RobotState & msg,
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
    out << "motors: ";
    to_flow_style_yaml(msg.motors, out);
    out << ", ";
  }

  // member: joy
  {
    out << "joy: ";
    to_flow_style_yaml(msg.joy, out);
    out << ", ";
  }

  // member: imu
  {
    out << "imu: ";
    to_flow_style_yaml(msg.imu, out);
    out << ", ";
  }

  // member: mag
  {
    out << "mag: ";
    to_flow_style_yaml(msg.mag, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RobotState & msg,
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
    out << "motors:\n";
    to_block_style_yaml(msg.motors, out, indentation + 2);
  }

  // member: joy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "joy:\n";
    to_block_style_yaml(msg.joy, out, indentation + 2);
  }

  // member: imu
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "imu:\n";
    to_block_style_yaml(msg.imu, out, indentation + 2);
  }

  // member: mag
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mag:\n";
    to_block_style_yaml(msg.mag, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RobotState & msg, bool use_flow_style = false)
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
  const horcrux_interfaces::msg::RobotState & msg,
  std::ostream & out, size_t indentation = 0)
{
  horcrux_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use horcrux_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const horcrux_interfaces::msg::RobotState & msg)
{
  return horcrux_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<horcrux_interfaces::msg::RobotState>()
{
  return "horcrux_interfaces::msg::RobotState";
}

template<>
inline const char * name<horcrux_interfaces::msg::RobotState>()
{
  return "horcrux_interfaces/msg/RobotState";
}

template<>
struct has_fixed_size<horcrux_interfaces::msg::RobotState>
  : std::integral_constant<bool, has_fixed_size<horcrux_interfaces::msg::MotorStates>::value && has_fixed_size<sensor_msgs::msg::Imu>::value && has_fixed_size<sensor_msgs::msg::Joy>::value && has_fixed_size<sensor_msgs::msg::MagneticField>::value && has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<horcrux_interfaces::msg::RobotState>
  : std::integral_constant<bool, has_bounded_size<horcrux_interfaces::msg::MotorStates>::value && has_bounded_size<sensor_msgs::msg::Imu>::value && has_bounded_size<sensor_msgs::msg::Joy>::value && has_bounded_size<sensor_msgs::msg::MagneticField>::value && has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<horcrux_interfaces::msg::RobotState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__TRAITS_HPP_
