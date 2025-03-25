import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.linalg import logm, expm

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

angles_deg = [175, -160, 15, -179, 160, 110]  # 다양한 회전 각도
rotations = []

np.random.seed(42)  # 결과 재현을 위한 고정 시드

for ang_deg in angles_deg:
    axis = np.random.randn(3)  # 3차원 랜덤 벡터
    axis /= np.linalg.norm(axis)  # 단위 벡터로 정규화
    angle_rad = np.deg2rad(ang_deg)
    
    rotvec = axis * angle_rad  # axis-angle 형식
    rot = R.from_rotvec(rotvec)
    rotations.append(rot)
    
    print(f"angle = {ang_deg:>5}°, axis = {axis}, rotvec = {rotvec}")

# Chordal 평균 (고유값 기반 쿼터니언 평균)
def chordal_mean_quaternion(rot_list):
    quats = np.array([r.as_quat() for r in rot_list])  # x, y, z, w
    A = np.zeros((4, 4))
    for q in quats:
        if np.dot(q, quats[0]) < 0:  # 부호 정렬
            q = -q
        A += np.outer(q, q)
    A /= len(quats)
    eigvals, eigvecs = np.linalg.eigh(A)
    avg_q = eigvecs[:, np.argmax(eigvals)]
    return R.from_quat(avg_q)

# Karcher 평균 (Log-Exp 기반)
def log_exp_karcher_mean(rot_list, max_iter=100, tol=1e-6):
    R_mean = rot_list[0].as_matrix()
    for _ in range(max_iter):
        delta_sum = np.zeros((3, 3))
        for r in rot_list:
            delta = logm(r.as_matrix() @ R_mean.T)
            delta_sum += delta
        delta_avg = delta_sum / len(rot_list)
        norm = np.linalg.norm(delta_avg, ord='fro')
        R_mean = expm(delta_avg) @ R_mean
        if norm < tol:
            break
    return R.from_matrix(R_mean)

def plot_rotations_on_sphere(rotations, mean_chordal, mean_karcher, scale=1.0):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Rotation Axes on Unit Sphere")

    # 단위구 그리기
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, color='lightgrey', alpha=0.2)

    # 샘플 회전 그리기
    for i, rot in enumerate(rotations):
        rotvec = rot.as_rotvec()
        axis = rotvec / np.linalg.norm(rotvec)
        ax.quiver(0, 0, 0, axis[0], axis[1], axis[2], color='blue', linewidth=1.5)
        ax.text(axis[0]*1.1, axis[1]*1.1, axis[2]*1.1, f"{i}", color='blue')

    # 평균 회전 - Chordal
    axis_chordal = mean_chordal.as_rotvec()
    axis_chordal /= np.linalg.norm(axis_chordal)
    ax.quiver(0, 0, 0, axis_chordal[0], axis_chordal[1], axis_chordal[2],
              color='red', linewidth=3, label='Chordal Mean')

    # 평균 회전 - Karcher
    axis_karcher = mean_karcher.as_rotvec()
    axis_karcher /= np.linalg.norm(axis_karcher)
    ax.quiver(0, 0, 0, axis_karcher[0], axis_karcher[1], axis_karcher[2],
              color='green', linewidth=3, label='Karcher Mean')

    # 축 설정
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.set_box_aspect([1, 1, 1])
    ax.legend()
    plt.show()

# 평균 계산
mean_chordal = chordal_mean_quaternion(rotations)
mean_karcher = log_exp_karcher_mean(rotations)

# 결과 출력
print("🎯 입력 회전 각들:", angles_deg)
print("▶ Chordal 평균:", mean_chordal.as_euler('ZYX', degrees=True))
print("▶ Karcher 평균:", mean_karcher.as_euler('ZYX', degrees=True))

plot_rotations_on_sphere(rotations, mean_chordal, mean_karcher)