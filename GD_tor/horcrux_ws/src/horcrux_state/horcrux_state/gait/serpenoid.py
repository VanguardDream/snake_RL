import numpy as np

class util():
    def __init__(self, e_d1, e_l1, e_d2:int, e_l2:int, delta) -> None:
        self.gait_sampling_interval = 0.1
        self._ed1 = e_d1
        self._ed2 = e_d2
        self._el1 = e_l1
        self._el2 = e_l2
        self._delta = delta
        self._t = np.arange(0, 2 * np.pi * np.lcm(self._el2, self._ed2) / 10, 0.1).transpose()

    def getMotionMat(self)->np.ndarray:
        raw_serp = self.serpenoid(self._t, self._ed1, self._el1, self._ed2 / 10, self._el2 / 10, self._delta)
        M_mat = self.__genMotionMat(raw_serp)

        return M_mat
        
    ## Predefined functions
    def serpenoid(self, t, e_d1, e_l1, e_d2, e_l2, delta)->np.ndarray:
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

    def __genMotionMat(self, serp_pos : np.array)->np.ndarray:
        serp_vel = np.diff(serp_pos.copy()) * (1 / self.gait_sampling_interval)
        serp_tor = np.diff(serp_vel.copy()) * (1 / self.gait_sampling_interval)

        motionMat = np.sign(serp_tor)

        return motionMat