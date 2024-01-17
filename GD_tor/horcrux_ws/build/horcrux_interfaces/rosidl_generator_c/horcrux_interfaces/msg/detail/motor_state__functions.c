// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from horcrux_interfaces:msg/MotorState.idl
// generated code does not contain a copyright notice
#include "horcrux_interfaces/msg/detail/motor_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
horcrux_interfaces__msg__MotorState__init(horcrux_interfaces__msg__MotorState * msg)
{
  if (!msg) {
    return false;
  }
  // id
  // baudrate
  // torque
  // goal_current
  // goal_velocity
  // goal_position
  // present_current
  // present_velocity
  // present_position
  // voltage
  // temperature
  return true;
}

void
horcrux_interfaces__msg__MotorState__fini(horcrux_interfaces__msg__MotorState * msg)
{
  if (!msg) {
    return;
  }
  // id
  // baudrate
  // torque
  // goal_current
  // goal_velocity
  // goal_position
  // present_current
  // present_velocity
  // present_position
  // voltage
  // temperature
}

bool
horcrux_interfaces__msg__MotorState__are_equal(const horcrux_interfaces__msg__MotorState * lhs, const horcrux_interfaces__msg__MotorState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // baudrate
  if (lhs->baudrate != rhs->baudrate) {
    return false;
  }
  // torque
  if (lhs->torque != rhs->torque) {
    return false;
  }
  // goal_current
  if (lhs->goal_current != rhs->goal_current) {
    return false;
  }
  // goal_velocity
  if (lhs->goal_velocity != rhs->goal_velocity) {
    return false;
  }
  // goal_position
  if (lhs->goal_position != rhs->goal_position) {
    return false;
  }
  // present_current
  if (lhs->present_current != rhs->present_current) {
    return false;
  }
  // present_velocity
  if (lhs->present_velocity != rhs->present_velocity) {
    return false;
  }
  // present_position
  if (lhs->present_position != rhs->present_position) {
    return false;
  }
  // voltage
  if (lhs->voltage != rhs->voltage) {
    return false;
  }
  // temperature
  if (lhs->temperature != rhs->temperature) {
    return false;
  }
  return true;
}

bool
horcrux_interfaces__msg__MotorState__copy(
  const horcrux_interfaces__msg__MotorState * input,
  horcrux_interfaces__msg__MotorState * output)
{
  if (!input || !output) {
    return false;
  }
  // id
  output->id = input->id;
  // baudrate
  output->baudrate = input->baudrate;
  // torque
  output->torque = input->torque;
  // goal_current
  output->goal_current = input->goal_current;
  // goal_velocity
  output->goal_velocity = input->goal_velocity;
  // goal_position
  output->goal_position = input->goal_position;
  // present_current
  output->present_current = input->present_current;
  // present_velocity
  output->present_velocity = input->present_velocity;
  // present_position
  output->present_position = input->present_position;
  // voltage
  output->voltage = input->voltage;
  // temperature
  output->temperature = input->temperature;
  return true;
}

horcrux_interfaces__msg__MotorState *
horcrux_interfaces__msg__MotorState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  horcrux_interfaces__msg__MotorState * msg = (horcrux_interfaces__msg__MotorState *)allocator.allocate(sizeof(horcrux_interfaces__msg__MotorState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(horcrux_interfaces__msg__MotorState));
  bool success = horcrux_interfaces__msg__MotorState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
horcrux_interfaces__msg__MotorState__destroy(horcrux_interfaces__msg__MotorState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    horcrux_interfaces__msg__MotorState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
horcrux_interfaces__msg__MotorState__Sequence__init(horcrux_interfaces__msg__MotorState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  horcrux_interfaces__msg__MotorState * data = NULL;

  if (size) {
    data = (horcrux_interfaces__msg__MotorState *)allocator.zero_allocate(size, sizeof(horcrux_interfaces__msg__MotorState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = horcrux_interfaces__msg__MotorState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        horcrux_interfaces__msg__MotorState__fini(&data[i - 1]);
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
horcrux_interfaces__msg__MotorState__Sequence__fini(horcrux_interfaces__msg__MotorState__Sequence * array)
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
      horcrux_interfaces__msg__MotorState__fini(&array->data[i]);
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

horcrux_interfaces__msg__MotorState__Sequence *
horcrux_interfaces__msg__MotorState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  horcrux_interfaces__msg__MotorState__Sequence * array = (horcrux_interfaces__msg__MotorState__Sequence *)allocator.allocate(sizeof(horcrux_interfaces__msg__MotorState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = horcrux_interfaces__msg__MotorState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
horcrux_interfaces__msg__MotorState__Sequence__destroy(horcrux_interfaces__msg__MotorState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    horcrux_interfaces__msg__MotorState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
horcrux_interfaces__msg__MotorState__Sequence__are_equal(const horcrux_interfaces__msg__MotorState__Sequence * lhs, const horcrux_interfaces__msg__MotorState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!horcrux_interfaces__msg__MotorState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
horcrux_interfaces__msg__MotorState__Sequence__copy(
  const horcrux_interfaces__msg__MotorState__Sequence * input,
  horcrux_interfaces__msg__MotorState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(horcrux_interfaces__msg__MotorState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    horcrux_interfaces__msg__MotorState * data =
      (horcrux_interfaces__msg__MotorState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!horcrux_interfaces__msg__MotorState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          horcrux_interfaces__msg__MotorState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!horcrux_interfaces__msg__MotorState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
