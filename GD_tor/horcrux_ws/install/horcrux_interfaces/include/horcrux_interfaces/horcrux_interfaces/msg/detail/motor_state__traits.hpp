// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from horcrux_interfaces:msg/MotorState.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__TRAITS_HPP_
#define HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "horcrux_interfaces/msg/detail/motor_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace horcrux_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const MotorState & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: baudrate
  {
    out << "baudrate: ";
    rosidl_generator_traits::value_to_yaml(msg.baudrate, out);
    out << ", ";
  }

  // member: torque
  {
    out << "torque: ";
    rosidl_generator_traits::value_to_yaml(msg.torque, out);
    out << ", ";
  }

  // member: goal_current
  {
    out << "goal_current: ";
    rosidl_generator_traits::value_to_yaml(msg.goal_current, out);
    out << ", ";
  }

  // member: goal_velocity
  {
    out << "goal_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.goal_velocity, out);
    out << ", ";
  }

  // member: goal_position
  {
    out << "goal_position: ";
    rosidl_generator_traits::value_to_yaml(msg.goal_position, out);
    out << ", ";
  }

  // member: present_current
  {
    out << "present_current: ";
    rosidl_generator_traits::value_to_yaml(msg.present_current, out);
    out << ", ";
  }

  // member: present_velocity
  {
    out << "present_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.present_velocity, out);
    out << ", ";
  }

  // member: present_position
  {
    out << "present_position: ";
    rosidl_generator_traits::value_to_yaml(msg.present_position, out);
    out << ", ";
  }

  // member: voltage
  {
    out << "voltage: ";
    rosidl_generator_traits::value_to_yaml(msg.voltage, out);
    out << ", ";
  }

  // member: temperature
  {
    out << "temperature: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotorState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: baudrate
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "baudrate: ";
    rosidl_generator_traits::value_to_yaml(msg.baudrate, out);
    out << "\n";
  }

  // member: torque
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "torque: ";
    rosidl_generator_traits::value_to_yaml(msg.torque, out);
    out << "\n";
  }

  // member: goal_current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_current: ";
    rosidl_generator_traits::value_to_yaml(msg.goal_current, out);
    out << "\n";
  }

  // member: goal_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.goal_velocity, out);
    out << "\n";
  }

  // member: goal_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_position: ";
    rosidl_generator_traits::value_to_yaml(msg.goal_position, out);
    out << "\n";
  }

  // member: present_current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "present_current: ";
    rosidl_generator_traits::value_to_yaml(msg.present_current, out);
    out << "\n";
  }

  // member: present_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "present_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.present_velocity, out);
    out << "\n";
  }

  // member: present_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "present_position: ";
    rosidl_generator_traits::value_to_yaml(msg.present_position, out);
    out << "\n";
  }

  // member: voltage
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "voltage: ";
    rosidl_generator_traits::value_to_yaml(msg.voltage, out);
    out << "\n";
  }

  // member: temperature
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "temperature: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotorState & msg, bool use_flow_style = false)
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
  const horcrux_interfaces::msg::MotorState & msg,
  std::ostream & out, size_t indentation = 0)
{
  horcrux_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use horcrux_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const horcrux_interfaces::msg::MotorState & msg)
{
  return horcrux_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<horcrux_interfaces::msg::MotorState>()
{
  return "horcrux_interfaces::msg::MotorState";
}

template<>
inline const char * name<horcrux_interfaces::msg::MotorState>()
{
  return "horcrux_interfaces/msg/MotorState";
}

template<>
struct has_fixed_size<horcrux_interfaces::msg::MotorState>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<horcrux_interfaces::msg::MotorState>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<horcrux_interfaces::msg::MotorState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__TRAITS_HPP_
