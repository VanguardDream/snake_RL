// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from horcrux_interfaces:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_
#define HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_

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
#include "horcrux_interfaces/msg/detail/motor_states__struct.hpp"
// Member 'joy'
#include "sensor_msgs/msg/detail/joy__struct.hpp"
// Member 'imu'
#include "sensor_msgs/msg/detail/imu__struct.hpp"
// Member 'mag'
#include "sensor_msgs/msg/detail/magnetic_field__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__horcrux_interfaces__msg__RobotState __attribute__((deprecated))
#else
# define DEPRECATED__horcrux_interfaces__msg__RobotState __declspec(deprecated)
#endif

namespace horcrux_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RobotState_
{
  using Type = RobotState_<ContainerAllocator>;

  explicit RobotState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    motors(_init),
    joy(_init),
    imu(_init),
    mag(_init)
  {
    (void)_init;
  }

  explicit RobotState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    motors(_alloc, _init),
    joy(_alloc, _init),
    imu(_alloc, _init),
    mag(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _motors_type =
    horcrux_interfaces::msg::MotorStates_<ContainerAllocator>;
  _motors_type motors;
  using _joy_type =
    sensor_msgs::msg::Joy_<ContainerAllocator>;
  _joy_type joy;
  using _imu_type =
    sensor_msgs::msg::Imu_<ContainerAllocator>;
  _imu_type imu;
  using _mag_type =
    sensor_msgs::msg::MagneticField_<ContainerAllocator>;
  _mag_type mag;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__motors(
    const horcrux_interfaces::msg::MotorStates_<ContainerAllocator> & _arg)
  {
    this->motors = _arg;
    return *this;
  }
  Type & set__joy(
    const sensor_msgs::msg::Joy_<ContainerAllocator> & _arg)
  {
    this->joy = _arg;
    return *this;
  }
  Type & set__imu(
    const sensor_msgs::msg::Imu_<ContainerAllocator> & _arg)
  {
    this->imu = _arg;
    return *this;
  }
  Type & set__mag(
    const sensor_msgs::msg::MagneticField_<ContainerAllocator> & _arg)
  {
    this->mag = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    horcrux_interfaces::msg::RobotState_<ContainerAllocator> *;
  using ConstRawPtr =
    const horcrux_interfaces::msg::RobotState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<horcrux_interfaces::msg::RobotState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<horcrux_interfaces::msg::RobotState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      horcrux_interfaces::msg::RobotState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<horcrux_interfaces::msg::RobotState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      horcrux_interfaces::msg::RobotState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<horcrux_interfaces::msg::RobotState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<horcrux_interfaces::msg::RobotState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<horcrux_interfaces::msg::RobotState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__horcrux_interfaces__msg__RobotState
    std::shared_ptr<horcrux_interfaces::msg::RobotState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__horcrux_interfaces__msg__RobotState
    std::shared_ptr<horcrux_interfaces::msg::RobotState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RobotState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->motors != other.motors) {
      return false;
    }
    if (this->joy != other.joy) {
      return false;
    }
    if (this->imu != other.imu) {
      return false;
    }
    if (this->mag != other.mag) {
      return false;
    }
    return true;
  }
  bool operator!=(const RobotState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RobotState_

// alias to use template instance with default allocator
using RobotState =
  horcrux_interfaces::msg::RobotState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace horcrux_interfaces

#endif  // HORCRUX_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_
