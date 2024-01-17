// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from horcrux_interfaces:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_
#define HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "horcrux_interfaces/msg/detail/robot_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace horcrux_interfaces
{

namespace msg
{

namespace builder
{

class Init_RobotState_mag
{
public:
  explicit Init_RobotState_mag(::horcrux_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  ::horcrux_interfaces::msg::RobotState mag(::horcrux_interfaces::msg::RobotState::_mag_type arg)
  {
    msg_.mag = std::move(arg);
    return std::move(msg_);
  }

private:
  ::horcrux_interfaces::msg::RobotState msg_;
};

class Init_RobotState_imu
{
public:
  explicit Init_RobotState_imu(::horcrux_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_mag imu(::horcrux_interfaces::msg::RobotState::_imu_type arg)
  {
    msg_.imu = std::move(arg);
    return Init_RobotState_mag(msg_);
  }

private:
  ::horcrux_interfaces::msg::RobotState msg_;
};

class Init_RobotState_joy
{
public:
  explicit Init_RobotState_joy(::horcrux_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_imu joy(::horcrux_interfaces::msg::RobotState::_joy_type arg)
  {
    msg_.joy = std::move(arg);
    return Init_RobotState_imu(msg_);
  }

private:
  ::horcrux_interfaces::msg::RobotState msg_;
};

class Init_RobotState_motors
{
public:
  explicit Init_RobotState_motors(::horcrux_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_joy motors(::horcrux_interfaces::msg::RobotState::_motors_type arg)
  {
    msg_.motors = std::move(arg);
    return Init_RobotState_joy(msg_);
  }

private:
  ::horcrux_interfaces::msg::RobotState msg_;
};

class Init_RobotState_header
{
public:
  Init_RobotState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotState_motors header(::horcrux_interfaces::msg::RobotState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_RobotState_motors(msg_);
  }

private:
  ::horcrux_interfaces::msg::RobotState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::horcrux_interfaces::msg::RobotState>()
{
  return horcrux_interfaces::msg::builder::Init_RobotState_header();
}

}  // namespace horcrux_interfaces

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_
