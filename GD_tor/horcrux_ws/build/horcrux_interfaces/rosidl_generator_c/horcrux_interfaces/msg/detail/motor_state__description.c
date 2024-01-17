// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from horcrux_interfaces:msg/MotorState.idl
// generated code does not contain a copyright notice

#include "horcrux_interfaces/msg/detail/motor_state__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_horcrux_interfaces
const rosidl_type_hash_t *
horcrux_interfaces__msg__MotorState__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x4a, 0x9f, 0xb9, 0xd3, 0x97, 0x2a, 0xa9, 0xf8,
      0x98, 0xc6, 0x62, 0x39, 0x01, 0xa6, 0x7b, 0x43,
      0x9d, 0xe1, 0xb3, 0xce, 0xa2, 0xef, 0x2b, 0x6a,
      0xac, 0xb1, 0xf7, 0xa1, 0x75, 0x95, 0xd7, 0xe8,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char horcrux_interfaces__msg__MotorState__TYPE_NAME[] = "horcrux_interfaces/msg/MotorState";

// Define type names, field names, and default values
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__id[] = "id";
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__baudrate[] = "baudrate";
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__torque[] = "torque";
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__goal_current[] = "goal_current";
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__goal_velocity[] = "goal_velocity";
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__goal_position[] = "goal_position";
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__present_current[] = "present_current";
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__present_velocity[] = "present_velocity";
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__present_position[] = "present_position";
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__voltage[] = "voltage";
static char horcrux_interfaces__msg__MotorState__FIELD_NAME__temperature[] = "temperature";

static rosidl_runtime_c__type_description__Field horcrux_interfaces__msg__MotorState__FIELDS[] = {
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__id, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT16,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__baudrate, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__torque, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__goal_current, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__goal_velocity, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__goal_position, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__present_current, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__present_velocity, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__present_position, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__voltage, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {horcrux_interfaces__msg__MotorState__FIELD_NAME__temperature, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
horcrux_interfaces__msg__MotorState__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {horcrux_interfaces__msg__MotorState__TYPE_NAME, 33, 33},
      {horcrux_interfaces__msg__MotorState__FIELDS, 11, 11},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "#ROM Area\n"
  "uint16 id\n"
  "uint32 baudrate\n"
  "\n"
  "#RAM Area\n"
  "bool torque\n"
  "float32 goal_current\n"
  "float32 goal_velocity\n"
  "float32 goal_position\n"
  "float32 present_current\n"
  "float32 present_velocity\n"
  "float32 present_position\n"
  "float32 voltage\n"
  "float32 temperature";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
horcrux_interfaces__msg__MotorState__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {horcrux_interfaces__msg__MotorState__TYPE_NAME, 33, 33},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 233, 233},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
horcrux_interfaces__msg__MotorState__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *horcrux_interfaces__msg__MotorState__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
