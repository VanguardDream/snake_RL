// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from horcrux_interfaces:msg/MotorStates.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "horcrux_interfaces/msg/detail/motor_states__struct.h"
#include "horcrux_interfaces/msg/detail/motor_states__functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"

// Nested array functions includes
#include "horcrux_interfaces/msg/detail/motor_state__functions.h"
// end nested array functions include
ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);
bool horcrux_interfaces__msg__motor_state__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * horcrux_interfaces__msg__motor_state__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool horcrux_interfaces__msg__motor_states__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[49];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("horcrux_interfaces.msg._motor_states.MotorStates", full_classname_dest, 48) == 0);
  }
  horcrux_interfaces__msg__MotorStates * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // motors
    PyObject * field = PyObject_GetAttrString(_pymsg, "motors");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'motors'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = 14;
    horcrux_interfaces__msg__MotorState * dest = ros_message->motors;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!horcrux_interfaces__msg__motor_state__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * horcrux_interfaces__msg__motor_states__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of MotorStates */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("horcrux_interfaces.msg._motor_states");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "MotorStates");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  horcrux_interfaces__msg__MotorStates * ros_message = (horcrux_interfaces__msg__MotorStates *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // motors
    PyObject * field = NULL;
    size_t size = 14;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    horcrux_interfaces__msg__MotorState * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->motors[i]);
      PyObject * pyitem = horcrux_interfaces__msg__motor_state__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "motors", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}