// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from horcrux_interfaces:msg/MotorStates.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__STRUCT_HPP_
#define HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'motors'
#include "horcrux_interfaces/msg/detail/motor_state__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__horcrux_interfaces__msg__MotorStates __attribute__((deprecated))
#else
# define DEPRECATED__horcrux_interfaces__msg__MotorStates __declspec(deprecated)
#endif

namespace horcrux_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotorStates_
{
  using Type = MotorStates_<ContainerAllocator>;

  explicit MotorStates_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->motors.fill(horcrux_interfaces::msg::MotorState_<ContainerAllocator>{_init});
    }
  }

  explicit MotorStates_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    motors(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->motors.fill(horcrux_interfaces::msg::MotorState_<ContainerAllocator>{_alloc, _init});
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _motors_type =
    std::array<horcrux_interfaces::msg::MotorState_<ContainerAllocator>, 14>;
  _motors_type motors;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__motors(
    const std::array<horcrux_interfaces::msg::MotorState_<ContainerAllocator>, 14> & _arg)
  {
    this->motors = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    horcrux_interfaces::msg::MotorStates_<ContainerAllocator> *;
  using ConstRawPtr =
    const horcrux_interfaces::msg::MotorStates_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<horcrux_interfaces::msg::MotorStates_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<horcrux_interfaces::msg::MotorStates_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      horcrux_interfaces::msg::MotorStates_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<horcrux_interfaces::msg::MotorStates_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      horcrux_interfaces::msg::MotorStates_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<horcrux_interfaces::msg::MotorStates_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<horcrux_interfaces::msg::MotorStates_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<horcrux_interfaces::msg::MotorStates_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__horcrux_interfaces__msg__MotorStates
    std::shared_ptr<horcrux_interfaces::msg::MotorStates_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__horcrux_interfaces__msg__MotorStates
    std::shared_ptr<horcrux_interfaces::msg::MotorStates_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorStates_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->motors != other.motors) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorStates_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorStates_

// alias to use template instance with default allocator
using MotorStates =
  horcrux_interfaces::msg::MotorStates_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace horcrux_interfaces

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__MOTOR_STATES__STRUCT_HPP_
