# For NN input
std_msgs/Header header

# Motor states
float32[14] currents
float32[14] velocities
float32[14] positions

# IMU states
geometry_msgs/Quaternion head_q
geometry_msgs/Vector3 haed_angular_vel
geometry_msgs/Vector3 head_linear_acc

# FSR states
int16[14] fsr_top
int16[14] fsr_bottom

# Motion vector
int8[14] motion_vector

# Joy states
float32[2] axes

# Recurrent
int8[14] prior_d_action
float32[14] prior_c_action