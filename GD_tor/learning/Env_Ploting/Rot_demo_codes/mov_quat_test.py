import numpy as np
from collections import deque
from scipy.spatial.transform import Rotation as R

def generate_random_axis_angle_samples(n=8, max_angle_deg=5):
    quaternions = []
    np.random.seed(42)

    for i in range(n):
        # 무작위 단위 벡터 (회전축)
        axis = np.random.randn(3)
        axis = axis / np.linalg.norm(axis)

        # 회전각: -max_angle ~ +max_angle 범위
        angle = np.deg2rad(np.random.uniform(-max_angle_deg, max_angle_deg))

        # 회전 생성
        r = R.from_rotvec(axis * angle)
        q = r.as_quat(scalar_first=True)  # (x, y, z, w)
        quaternions.append(q)

        # print(f"[{i}] axis={axis}, angle={np.rad2deg(angle):.2f} deg → quat={q}")

    return np.array(quaternions)

class MovingAverageFilterQuaternion0:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.w_queue = deque(maxlen=window_size)
        self.x_queue = deque(maxlen=window_size)
        self.y_queue = deque(maxlen=window_size)
        self.z_queue = deque(maxlen=window_size)

    def update(self, quat):
        self.w_queue.append(quat[0])
        self.x_queue.append(quat[1])
        self.y_queue.append(quat[2])
        self.z_queue.append(quat[3])

        _raw_quat = np.array([self.w_queue, self.x_queue, self.y_queue, self.z_queue]).T

        _rot = R.from_quat(_raw_quat, scalar_first=True)
        _avg_rot = _rot.mean().as_quat(scalar_first=True)

        return _avg_rot

class MovingAverageFilterQuaternion:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.quat_queue = deque(maxlen=window_size)  # (x, y, z, w) 형식

    def update(self, new_quat):  # new_quat: (x, y, z, w) or (4,) ndarray
        # 부호 일관성 유지
        if self.quat_queue:
            last_quat = self.quat_queue[-1]
            if np.dot(last_quat, new_quat) < 0:
                new_quat = -new_quat

        self.quat_queue.append(new_quat)

        # if len(self.quat_queue) < 2:
        #     return R.from_quat(new_quat, scalar_first=True)  # 초기값은 그대로 반환

        # 고유값 기반 평균
        A = np.zeros((4, 4))
        for q in self.quat_queue:
            q = q / np.linalg.norm(q)
            A += np.outer(q, q)
        A /= len(self.quat_queue)

        eigvals, eigvecs = np.linalg.eigh(A)
        avg_quat = eigvecs[:, np.argmax(eigvals)]  # 최대 고유값의 고유벡터

        if avg_quat[3] < 0:  # w<0이면 부호 반전
            avg_quat = -avg_quat

        # scipy는 (x, y, z, w) 형식 사용
        rot_avg = R.from_quat(avg_quat, scalar_first=True)

        # print("Quaternion sequence (Euler angles):")
        for q in self.quat_queue:
            # print(R.from_quat(q).as_euler('XYZ', degrees=True))
            pass

        # print("Averaged (Euler):", rot_avg.as_euler('XYZ', degrees=True))

        return rot_avg.as_quat(scalar_first=True)
    

# a = MovingAverageFilterQuaternion()
# a.update((1,0,0,0))
# a.update((0,1,0,0))
# a.update((0,0,1,0))
# a.update((0,0,0,1))

# b = MovingAverageFilterQuaternion0()
# b.update(1, 0, 0, 0)
# b.update(0, 1, 0, 0)
# b.update(0, 0, 1, 0)
# b.update(0, 0, 0, 1)

sample = generate_random_axis_angle_samples()

a = MovingAverageFilterQuaternion()
b = MovingAverageFilterQuaternion0()

print(a.update(sample[0]))
print(b.update(sample[0]))
print(a.update(sample[1]))
print(b.update(sample[1]))
print(a.update(sample[2]))
print(b.update(sample[2]))
print(a.update(sample[3]))
print(b.update(sample[3]))