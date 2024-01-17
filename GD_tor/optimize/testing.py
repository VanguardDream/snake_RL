import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0, 2 * np.pi, 0.1).transpose()
v = -1 + (1+1) * np.random.random(9)
# v = np.ones(9, dtype= np.float32)

v_0 = v[0] # base DC component
v_s = v[1::2] # Fourier coff for sin
v_c = v[2::2] # Fourier coff for cos
k_t = np.arange(1, np.shape(v_s)[0] + 1, 1) # Fourier hamonic

n = np.arange(1,15, dtype=np.float32) # number of joints

# t = np.outer(t, k_t)

# n[0::2] *= np.radians(gait_param[0])
# n[1::2] *= np.radians(gait_param[1])
# n[1::2] += np.radians(gait_param[-1])

n[0::2] *= np.radians(30) # Dorsal spatial param
n[1::2] *= np.radians(30) # lateral spatial param
n[1::2] += np.radians(90) # Delta

e_t = t[np.newaxis, np.newaxis, :] * k_t[:, np.newaxis, np.newaxis]
n_t = n[np.newaxis, :, np.newaxis] + e_t[:, :, :]

# n_t = n[:,np.newaxis] + t[np.newaxis,:] # Joint weighted time
# k_n_t = n_t[np.newaxis, :, :] * k_t[:, np.newaxis, np.newaxis]

mat_s = np.sin(n_t[:, :, :]) * v_s[:, np.newaxis, np.newaxis] # tensor of sin
mat_c = np.cos(n_t[:, :, :]) * v_c[:, np.newaxis, np.newaxis] # tensor of cos


f = np.abs(v_0 + np.sum(mat_s + mat_c, axis=0))

print(f)

fig, axs = plt.subplots(14)
axs[0].plot(t, f[0, :])
axs[1].plot(t, f[1, :])
axs[2].plot(t, f[2, :])
axs[3].plot(t, f[3, :])
axs[4].plot(t, f[4, :])
axs[5].plot(t, f[5, :])
axs[6].plot(t, f[6, :])
axs[7].plot(t, f[7, :])
axs[8].plot(t, f[8, :])
axs[9].plot(t, f[9, :])
axs[10].plot(t, f[10, :])
axs[11].plot(t, f[11, :])
axs[12].plot(t, f[12, :])
axs[13].plot(t, f[13, :])

plt.show()