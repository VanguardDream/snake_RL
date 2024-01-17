// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from horcrux_interfaces:msg/MotorState.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__STRUCT_HPP_
#define HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__horcrux_interfaces__msg__MotorState __attribute__((deprecated))
#else
# define DEPRECATED__horcrux_interfaces__msg__MotorState __declspec(deprecated)
#endif

namespace horcrux_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotorState_
{
  using Type = MotorState_<ContainerAllocator>;

  explicit MotorState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0;
      this->baudrate = 0ul;
      this->torque = false;
      this->goal_current = 0.0f;
      this->goal_velocity = 0.0f;
      this->goal_position = 0.0f;
      this->present_current = 0.0f;
      this->present_velocity = 0.0f;
      this->present_position = 0.0f;
      this->voltage = 0.0f;
      this->temperature = 0.0f;
    }
  }

  explicit MotorState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0;
      this->baudrate = 0ul;
      this->torque = false;
      this->goal_current = 0.0f;
      this->goal_velocity = 0.0f;
      this->goal_position = 0.0f;
      this->present_current = 0.0f;
      this->present_velocity = 0.0f;
      this->present_position = 0.0f;
      this->voltage = 0.0f;
      this->temperature = 0.0f;
    }
  }

  // field types and members
  using _id_type =
    uint16_t;
  _id_type id;
  using _baudrate_type =
    uint32_t;
  _baudrate_type baudrate;
  using _torque_type =
    bool;
  _torque_type torque;
  using _goal_current_type =
    float;
  _goal_current_type goal_current;
  using _goal_velocity_type =
    float;
  _goal_velocity_type goal_velocity;
  using _goal_position_type =
    float;
  _goal_position_type goal_position;
  using _present_current_type =
    float;
  _present_current_type present_current;
  using _present_velocity_type =
    float;
  _present_velocity_type present_velocity;
  using _present_position_type =
    float;
  _present_position_type present_position;
  using _voltage_type =
    float;
  _voltage_type voltage;
  using _temperature_type =
    float;
  _temperature_type temperature;

  // setters for named parameter idiom
  Type & set__id(
    const uint16_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__baudrate(
    const uint32_t & _arg)
  {
    this->baudrate = _arg;
    return *this;
  }
  Type & set__torque(
    const bool & _arg)
  {
    this->torque = _arg;
    return *this;
  }
  Type & set__goal_current(
    const float & _arg)
  {
    this->goal_current = _arg;
    return *this;
  }
  Type & set__goal_velocity(
    const float & _arg)
  {
    this->goal_velocity = _arg;
    return *this;
  }
  Type & set__goal_position(
    const float & _arg)
  {
    this->goal_position = _arg;
    return *this;
  }
  Type & set__present_current(
    const float & _arg)
  {
    this->present_current = _arg;
    return *this;
  }
  Type & set__present_velocity(
    const float & _arg)
  {
    this->present_velocity = _arg;
    return *this;
  }
  Type & set__present_position(
    const float & _arg)
  {
    this->present_position = _arg;
    return *this;
  }
  Type & set__voltage(
    const float & _arg)
  {
    this->voltage = _arg;
    return *this;
  }
  Type & set__temperature(
    const float & _arg)
  {
    this->temperature = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    horcrux_interfaces::msg::MotorState_<ContainerAllocator> *;
  using ConstRawPtr =
    const horcrux_interfaces::msg::MotorState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<horcrux_interfaces::msg::MotorState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<horcrux_interfaces::msg::MotorState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      horcrux_interfaces::msg::MotorState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<horcrux_interfaces::msg::MotorState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      horcrux_interfaces::msg::MotorState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<horcrux_interfaces::msg::MotorState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<horcrux_interfaces::msg::MotorState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<horcrux_interfaces::msg::MotorState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__horcrux_interfaces__msg__MotorState
    std::shared_ptr<horcrux_interfaces::msg::MotorState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__horcrux_interfaces__msg__MotorState
    std::shared_ptr<horcrux_interfaces::msg::MotorState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorState_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    if (this->baudrate != other.baudrate) {
      return false;
    }
    if (this->torque != other.torque) {
      return false;
    }
    if (this->goal_current != other.goal_current) {
      return false;
    }
    if (this->goal_velocity != other.goal_velocity) {
      return false;
    }
    if (this->goal_position != other.goal_position) {
      return false;
    }
    if (this->present_current != other.present_current) {
      return false;
    }
    if (this->present_velocity != other.present_velocity) {
      return false;
    }
    if (this->present_position != other.present_position) {
      return false;
    }
    if (this->voltage != other.voltage) {
      return false;
    }
    if (this->temperature != other.temperature) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorState_

// alias to use template instance with default allocator
using MotorState =
  horcrux_interfaces::msg::MotorState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace horcrux_interfaces

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATE__STRUCT_HPP_
