// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from horcrux_interfaces:msg/MotorStates.idl
// generated code does not contain a copyright notice
#include "horcrux_interfaces/msg/detail/motor_states__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `motors`
#include "horcrux_interfaces/msg/detail/motor_state__functions.h"

bool
horcrux_interfaces__msg__MotorStates__init(horcrux_interfaces__msg__MotorStates * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    horcrux_interfaces__msg__MotorStates__fini(msg);
    return false;
  }
  // motors
  for (size_t i = 0; i < 14; ++i) {
    if (!horcrux_interfaces__msg__MotorState__init(&msg->motors[i])) {
      horcrux_interfaces__msg__MotorStates__fini(msg);
      return false;
    }
  }
  return true;
}

void
horcrux_interfaces__msg__MotorStates__fini(horcrux_interfaces__msg__MotorStates * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // motors
  for (size_t i = 0; i < 14; ++i) {
    horcrux_interfaces__msg__MotorState__fini(&msg->motors[i]);
  }
}

bool
horcrux_interfaces__msg__MotorStates__are_equal(const horcrux_interfaces__msg__MotorStates * lhs, const horcrux_interfaces__msg__MotorStates * rhs)
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
  for (size_t i = 0; i < 14; ++i) {
    if (!horcrux_interfaces__msg__MotorState__are_equal(
        &(lhs->motors[i]), &(rhs->motors[i])))
    {
      return false;
    }
  }
  return true;
}

bool
horcrux_interfaces__msg__MotorStates__copy(
  const horcrux_interfaces__msg__MotorStates * input,
  horcrux_interfaces__msg__MotorStates * output)
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
  for (size_t i = 0; i < 14; ++i) {
    if (!horcrux_interfaces__msg__MotorState__copy(
        &(input->motors[i]), &(output->motors[i])))
    {
      return false;
    }
  }
  return true;
}

horcrux_interfaces__msg__MotorStates *
horcrux_interfaces__msg__MotorStates__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  horcrux_interfaces__msg__MotorStates * msg = (horcrux_interfaces__msg__MotorStates *)allocator.allocate(sizeof(horcrux_interfaces__msg__MotorStates), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(horcrux_interfaces__msg__MotorStates));
  bool success = horcrux_interfaces__msg__MotorStates__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
horcrux_interfaces__msg__MotorStates__destroy(horcrux_interfaces__msg__MotorStates * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    horcrux_interfaces__msg__MotorStates__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
horcrux_interfaces__msg__MotorStates__Sequence__init(horcrux_interfaces__msg__MotorStates__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  horcrux_interfaces__msg__MotorStates * data = NULL;

  if (size) {
    data = (horcrux_interfaces__msg__MotorStates *)allocator.zero_allocate(size, sizeof(horcrux_interfaces__msg__MotorStates), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = horcrux_interfaces__msg__MotorStates__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        horcrux_interfaces__msg__MotorStates__fini(&data[i - 1]);
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
horcrux_interfaces__msg__MotorStates__Sequence__fini(horcrux_interfaces__msg__MotorStates__Sequence * array)
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
      horcrux_interfaces__msg__MotorStates__fini(&array->data[i]);
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

horcrux_interfaces__msg__MotorStates__Sequence *
horcrux_interfaces__msg__MotorStates__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  horcrux_interfaces__msg__MotorStates__Sequence * array = (horcrux_interfaces__msg__MotorStates__Sequence *)allocator.allocate(sizeof(horcrux_interfaces__msg__MotorStates__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = horcrux_interfaces__msg__MotorStates__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
horcrux_interfaces__msg__MotorStates__Sequence__destroy(horcrux_interfaces__msg__MotorStates__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    horcrux_interfaces__msg__MotorStates__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
horcrux_interfaces__msg__MotorStates__Sequence__are_equal(const horcrux_interfaces__msg__MotorStates__Sequence * lhs, const horcrux_interfaces__msg__MotorStates__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!horcrux_interfaces__msg__MotorStates__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
horcrux_interfaces__msg__MotorStates__Sequence__copy(
  const horcrux_interfaces__msg__MotorStates__Sequence * input,
  horcrux_interfaces__msg__MotorStates__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(horcrux_interfaces__msg__MotorStates);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    horcrux_interfaces__msg__MotorStates * data =
      (horcrux_interfaces__msg__MotorStates *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!horcrux_interfaces__msg__MotorStates__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          horcrux_interfaces__msg__MotorStates__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!horcrux_interfaces__msg__MotorStates__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
