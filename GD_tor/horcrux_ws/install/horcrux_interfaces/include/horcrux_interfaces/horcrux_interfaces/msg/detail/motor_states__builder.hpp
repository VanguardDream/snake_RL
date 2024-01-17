// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from horcrux_interfaces:msg/MotorStates.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__BUILDER_HPP_
#define HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "horcrux_interfaces/msg/detail/motor_states__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace horcrux_interfaces
{

namespace msg
{

namespace builder
{

class Init_MotorStates_motors
{
public:
  explicit Init_MotorStates_motors(::horcrux_interfaces::msg::MotorStates & msg)
  : msg_(msg)
  {}
  ::horcrux_interfaces::msg::MotorStates motors(::horcrux_interfaces::msg::MotorStates::_motors_type arg)
  {
    msg_.motors = std::move(arg);
    return std::move(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorStates msg_;
};

class Init_MotorStates_header
{
public:
  Init_MotorStates_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorStates_motors header(::horcrux_interfaces::msg::MotorStates::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_MotorStates_motors(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorStates msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::horcrux_interfaces::msg::MotorStates>()
{
  return horcrux_interfaces::msg::builder::Init_MotorStates_header();
}

}  // namespace horcrux_interfaces

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__BUILDER_HPP_
