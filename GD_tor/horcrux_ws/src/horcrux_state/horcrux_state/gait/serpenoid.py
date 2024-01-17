import numpy as np

class util():
    def __init__(self) -> None:
        self.gait_sampling_interval = 0.1

    def getMotionMat(self,t, e_d1, e_l1, e_d2, e_l2, delta):
        raw_serp = self.serpenoid(t, e_d1, e_l1, e_d2, e_l2, delta)
        M_mat = self.__genMotionMat(raw_serp)

        return M_mat
        
    ## Predefined functions
    def serpenoid(self, t, e_d1, e_l1, e_d2, e_l2, delta):
        #Hirose (1993) serpenoid curve implementations
        e_d1 = np.radians(e_d1)
        e_l1 = np.radians(e_l1)
        delta = np.radians(delta)

        f1 = e_d2 * t
        f2 = e_l2 * t

        j_1 = np.sin(e_d1 + f1)
        j_2 = np.sin(e_l1 * 2 + f2 + delta)

        j_3 = np.sin(e_d1 * 3 + f1)
        j_4 = np.sin(e_l1 * 4 + f2 + delta)

        j_5 = np.sin(e_d1 * 5 + f1)
        j_6 = np.sin(e_l1 * 6 + f2 + delta)

        j_7 = np.sin(e_d1 * 7 + f1)
        j_8 = np.sin(e_l1 * 8 + f2 + delta)

        j_9 = np.sin(e_d1 * 9 + f1)
        j_10 = np.sin(e_l1 * 10 + f2 + delta)

        j_11 = np.sin(e_d1 * 11 + f1)
        j_12 = np.sin(e_l1 * 12 + f2 + delta)

        j_13 = np.sin(e_d1 * 13 + f1)
        j_14 = np.sin(e_l1 * 14 + f2 + delta)

        return np.array([j_1, j_2, j_3, j_4, j_5, j_6, j_7, j_8, j_9, j_10, j_11, j_12, j_13, j_14])

    def __genMotionMat(self, serp_pos : np.array):
        serp_vel = np.diff(serp_pos.copy()) * (1 / self.gait_sampling_interval)
        serp_tor = np.diff(serp_vel.copy()) * (1 / self.gait_sampling_interval)

        motionMat = np.sign(serp_tor)

        return motionMat