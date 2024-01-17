// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from horcrux_interfaces:msg/RobotState.idl
// generated code does not contain a copyright notice
#include "horcrux_interfaces/msg/detail/robot_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `motors`
#include "horcrux_interfaces/msg/detail/motor_states__functions.h"
// Member `joy`
#include "sensor_msgs/msg/detail/joy__functions.h"
// Member `imu`
#include "sensor_msgs/msg/detail/imu__functions.h"
// Member `mag`
#include "sensor_msgs/msg/detail/magnetic_field__functions.h"

bool
horcrux_interfaces__msg__RobotState__init(horcrux_interfaces__msg__RobotState * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    horcrux_interfaces__msg__RobotState__fini(msg);
    return false;
  }
  // motors
  if (!horcrux_interfaces__msg__MotorStates__init(&msg->motors)) {
    horcrux_interfaces__msg__RobotState__fini(msg);
    return false;
  }
  // joy
  if (!sensor_msgs__msg__Joy__init(&msg->joy)) {
    horcrux_interfaces__msg__RobotState__fini(msg);
    return false;
  }
  // imu
  if (!sensor_msgs__msg__Imu__init(&msg->imu)) {
    horcrux_interfaces__msg__RobotState__fini(msg);
    return false;
  }
  // mag
  if (!sensor_msgs__msg__MagneticField__init(&msg->mag)) {
    horcrux_interfaces__msg__RobotState__fini(msg);
    return false;
  }
  return true;
}

void
horcrux_interfaces__msg__RobotState__fini(horcrux_interfaces__msg__RobotState * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // motors
  horcrux_interfaces__msg__MotorStates__fini(&msg->motors);
  // joy
  sensor_msgs__msg__Joy__fini(&msg->joy);
  // imu
  sensor_msgs__msg__Imu__fini(&msg->imu);
  // mag
  sensor_msgs__msg__MagneticField__fini(&msg->mag);
}

bool
horcrux_interfaces__msg__RobotState__are_equal(const horcrux_interfaces__msg__RobotState * lhs, const horcrux_interfaces__msg__RobotState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // motors
  if (!horcrux_interfaces__msg__MotorStates__are_equal(
      &(lhs->motors), &(rhs->motors)))
  {
    return false;
  }
  // joy
  if (!sensor_msgs__msg__Joy__are_equal(
      &(lhs->joy), &(rhs->joy)))
  {
    return false;
  }
  // imu
  if (!sensor_msgs__msg__Imu__are_equal(
      &(lhs->imu), &(rhs->imu)))
  {
    return false;
  }
  // mag
  if (!sensor_msgs__msg__MagneticField__are_equal(
      &(lhs->mag), &(rhs->mag)))
  {
    return false;
  }
  return true;
}

bool
horcrux_interfaces__msg__RobotState__copy(
  const horcrux_interfaces__msg__RobotState * input,
  horcrux_interfaces__msg__RobotState * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // motors
  if (!horcrux_interfaces__msg__MotorStates__copy(
      &(input->motors), &(output->motors)))
  {
    return false;
  }
  // joy
  if (!sensor_msgs__msg__Joy__copy(
      &(input->joy), &(output->joy)))
  {
    return false;
  }
  // imu
  if (!sensor_msgs__msg__Imu__copy(
      &(input->imu), &(output->imu)))
  {
    return false;
  }
  // mag
  if (!sensor_msgs__msg__MagneticField__copy(
      &(input->mag), &(output->mag)))
  {
    return false;
  }
  return true;
}

horcrux_interfaces__msg__RobotState *
horcrux_interfaces__msg__RobotState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  horcrux_interfaces__msg__RobotState * msg = (horcrux_interfaces__msg__RobotState *)allocator.allocate(sizeof(horcrux_interfaces__msg__RobotState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(horcrux_interfaces__msg__RobotState));
  bool success = horcrux_interfaces__msg__RobotState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
horcrux_interfaces__msg__RobotState__destroy(horcrux_interfaces__msg__RobotState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    horcrux_interfaces__msg__RobotState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
horcrux_interfaces__msg__RobotState__Sequence__init(horcrux_interfaces__msg__RobotState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  horcrux_interfaces__msg__RobotState * data = NULL;

  if (size) {
    data = (horcrux_interfaces__msg__RobotState *)allocator.zero_allocate(size, sizeof(horcrux_interfaces__msg__RobotState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = horcrux_interfaces__msg__RobotState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        horcrux_interfaces__msg__RobotState__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
horcrux_interfaces__msg__RobotState__Sequence__fini(horcrux_interfaces__msg__RobotState__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      horcrux_interfaces__msg__RobotState__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

horcrux_interfaces__msg__RobotState__Sequence *
horcrux_interfaces__msg__RobotState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  horcrux_interfaces__msg__RobotState__Sequence * array = (horcrux_interfaces__msg__RobotState__Sequence *)allocator.allocate(sizeof(horcrux_interfaces__msg__RobotState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = horcrux_interfaces__msg__RobotState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
horcrux_interfaces__msg__RobotState__Sequence__destroy(horcrux_interfaces__msg__RobotState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    horcrux_interfaces__msg__RobotState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
horcrux_interfaces__msg__RobotState__Sequence__are_equal(const horcrux_interfaces__msg__RobotState__Sequence * lhs, const horcrux_interfaces__msg__RobotState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!horcrux_interfaces__msg__RobotState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
horcrux_interfaces__msg__RobotState__Sequence__copy(
  const horcrux_interfaces__msg__RobotState__Sequence * input,
  horcrux_interfaces__msg__RobotState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(horcrux_interfaces__msg__RobotState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    horcrux_interfaces__msg__RobotState * data =
      (horcrux_interfaces__msg__RobotState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!horcrux_interfaces__msg__RobotState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          horcrux_interfaces__msg__RobotState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!horcrux_interfaces__msg__RobotState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
