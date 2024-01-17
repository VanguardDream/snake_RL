// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from horcrux_interfaces:msg/MotorState.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__BUILDER_HPP_
#define HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "horcrux_interfaces/msg/detail/motor_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace horcrux_interfaces
{

namespace msg
{

namespace builder
{

class Init_MotorState_temperature
{
public:
  explicit Init_MotorState_temperature(::horcrux_interfaces::msg::MotorState & msg)
  : msg_(msg)
  {}
  ::horcrux_interfaces::msg::MotorState temperature(::horcrux_interfaces::msg::MotorState::_temperature_type arg)
  {
    msg_.temperature = std::move(arg);
    return std::move(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

class Init_MotorState_voltage
{
public:
  explicit Init_MotorState_voltage(::horcrux_interfaces::msg::MotorState & msg)
  : msg_(msg)
  {}
  Init_MotorState_temperature voltage(::horcrux_interfaces::msg::MotorState::_voltage_type arg)
  {
    msg_.voltage = std::move(arg);
    return Init_MotorState_temperature(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

class Init_MotorState_present_position
{
public:
  explicit Init_MotorState_present_position(::horcrux_interfaces::msg::MotorState & msg)
  : msg_(msg)
  {}
  Init_MotorState_voltage present_position(::horcrux_interfaces::msg::MotorState::_present_position_type arg)
  {
    msg_.present_position = std::move(arg);
    return Init_MotorState_voltage(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

class Init_MotorState_present_velocity
{
public:
  explicit Init_MotorState_present_velocity(::horcrux_interfaces::msg::MotorState & msg)
  : msg_(msg)
  {}
  Init_MotorState_present_position present_velocity(::horcrux_interfaces::msg::MotorState::_present_velocity_type arg)
  {
    msg_.present_velocity = std::move(arg);
    return Init_MotorState_present_position(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

class Init_MotorState_present_current
{
public:
  explicit Init_MotorState_present_current(::horcrux_interfaces::msg::MotorState & msg)
  : msg_(msg)
  {}
  Init_MotorState_present_velocity present_current(::horcrux_interfaces::msg::MotorState::_present_current_type arg)
  {
    msg_.present_current = std::move(arg);
    return Init_MotorState_present_velocity(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

class Init_MotorState_goal_position
{
public:
  explicit Init_MotorState_goal_position(::horcrux_interfaces::msg::MotorState & msg)
  : msg_(msg)
  {}
  Init_MotorState_present_current goal_position(::horcrux_interfaces::msg::MotorState::_goal_position_type arg)
  {
    msg_.goal_position = std::move(arg);
    return Init_MotorState_present_current(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

class Init_MotorState_goal_velocity
{
public:
  explicit Init_MotorState_goal_velocity(::horcrux_interfaces::msg::MotorState & msg)
  : msg_(msg)
  {}
  Init_MotorState_goal_position goal_velocity(::horcrux_interfaces::msg::MotorState::_goal_velocity_type arg)
  {
    msg_.goal_velocity = std::move(arg);
    return Init_MotorState_goal_position(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

class Init_MotorState_goal_current
{
public:
  explicit Init_MotorState_goal_current(::horcrux_interfaces::msg::MotorState & msg)
  : msg_(msg)
  {}
  Init_MotorState_goal_velocity goal_current(::horcrux_interfaces::msg::MotorState::_goal_current_type arg)
  {
    msg_.goal_current = std::move(arg);
    return Init_MotorState_goal_velocity(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

class Init_MotorState_torque
{
public:
  explicit Init_MotorState_torque(::horcrux_interfaces::msg::MotorState & msg)
  : msg_(msg)
  {}
  Init_MotorState_goal_current torque(::horcrux_interfaces::msg::MotorState::_torque_type arg)
  {
    msg_.torque = std::move(arg);
    return Init_MotorState_goal_current(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

class Init_MotorState_baudrate
{
public:
  explicit Init_MotorState_baudrate(::horcrux_interfaces::msg::MotorState & msg)
  : msg_(msg)
  {}
  Init_MotorState_torque baudrate(::horcrux_interfaces::msg::MotorState::_baudrate_type arg)
  {
    msg_.baudrate = std::move(arg);
    return Init_MotorState_torque(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

class Init_MotorState_id
{
public:
  Init_MotorState_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorState_baudrate id(::horcrux_interfaces::msg::MotorState::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_MotorState_baudrate(msg_);
  }

private:
  ::horcrux_interfaces::msg::MotorState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::horcrux_interfaces::msg::MotorState>()
{
  return horcrux_interfaces::msg::builder::Init_MotorState_id();
}

}  // namespace horcrux_interfaces

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__BUILDER_HPP_
