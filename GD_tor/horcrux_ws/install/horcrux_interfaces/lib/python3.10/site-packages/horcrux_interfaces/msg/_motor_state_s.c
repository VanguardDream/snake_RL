// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from horcrux_interfaces:msg/MotorState.idl
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
#include "horcrux_interfaces/msg/detail/motor_state__struct.h"
#include "horcrux_interfaces/msg/detail/motor_state__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool horcrux_interfaces__msg__motor_state__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[47];
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
    assert(strncmp("horcrux_interfaces.msg._motor_state.MotorState", full_classname_dest, 46) == 0);
  }
  horcrux_interfaces__msg__MotorState * ros_message = _ros_message;
  {  // id
    PyObject * field = PyObject_GetAttrString(_pymsg, "id");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->id = (uint16_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // baudrate
    PyObject * field = PyObject_GetAttrString(_pymsg, "baudrate");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->baudrate = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // torque
    PyObject * field = PyObject_GetAttrString(_pymsg, "torque");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->torque = (Py_True == field);
    Py_DECREF(field);
  }
  {  // goal_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "goal_current");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->goal_current = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // goal_velocity
    PyObject * field = PyObject_GetAttrString(_pymsg, "goal_velocity");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->goal_velocity = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // goal_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "goal_position");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->goal_position = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // present_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "present_current");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->present_current = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // present_velocity
    PyObject * field = PyObject_GetAttrString(_pymsg, "present_velocity");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->present_velocity = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // present_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "present_position");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->present_position = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // voltage
    PyObject * field = PyObject_GetAttrString(_pymsg, "voltage");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->voltage = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // temperature
    PyObject * field = PyObject_GetAttrString(_pymsg, "temperature");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->temperature = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * horcrux_interfaces__msg__motor_state__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of MotorState */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("horcrux_interfaces.msg._motor_state");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "MotorState");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  horcrux_interfaces__msg__MotorState * ros_message = (horcrux_interfaces__msg__MotorState *)raw_ros_message;
  {  // id
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->id);
    {
      int rc = PyObject_SetAttrString(_pymessage, "id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // baudrate
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->baudrate);
    {
      int rc = PyObject_SetAttrString(_pymessage, "baudrate", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // torque
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->torque ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "torque", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // goal_current
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->goal_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "goal_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // goal_velocity
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->goal_velocity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "goal_velocity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // goal_position
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->goal_position);
    {
      int rc = PyObject_SetAttrString(_pymessage, "goal_position", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // present_current
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->present_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "present_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // present_velocity
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->present_velocity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "present_velocity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // present_position
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->present_position);
    {
      int rc = PyObject_SetAttrString(_pymessage, "present_position", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // voltage
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->voltage);
    {
      int rc = PyObject_SetAttrString(_pymessage, "voltage", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // temperature
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->temperature);
    {
      int rc = PyObject_SetAttrString(_pymessage, "temperature", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
