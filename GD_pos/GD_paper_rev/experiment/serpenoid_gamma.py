import numpy as np

class Gait():
    def __init__(self, param:tuple[float, float, float, float, float, float, float, float], param_bar:tuple[float, float, float, float, float, float, float, float], gamma:float = 0.7071) -> None:
        self.gait_sampling_interval = 0.1

        # For motion matrix
        self._ad1 = param[0]
        self._ed1 = param[2]
        self._ed2 = param[4]

        self._al1 = param[1]
        self._el1 = param[3]
        self._el2 = param[5]

        self._delta = param[6]

        self._time_step = param[7]

        # For optimizing...
        self._ad1_bar = param_bar[0]
        self._ed1_bar = param_bar[2]
        self._ed2_bar = param_bar[4]

        self._al1_bar = param_bar[1]
        self._el1_bar = param_bar[3]
        self._el2_bar = param_bar[5]

        self._delta_bar = param_bar[6]

        self._time_step_bar = param_bar[7]

        self._gamma = gamma

        self._t = np.arange(0, 10, self._time_step).transpose()

        self.MotionMatrix = self.getMotionMat()
        self.CurveFunction = self.getCurveFunction()
        self.Gk = self.MotionMatrix * self.CurveFunction
        self.joints = self.MotionMatrix.shape[0]
        self.Mvecs = self.MotionMatrix.shape[1]
        self.curves = self.CurveFunction.shape[1]

        assert self.Mvecs == self.curves

    # def getMotionMat(self)->np.ndarray:
    #     raw_serp = self.serpenoid(self._t, self._ed1, self._el1, self._ed2 / 10, self._el2 / 10, self._delta)
    #     M_mat = self.__genMotionMat(raw_serp)

    #     return M_mat
    
    def getMotionMat(self)->np.ndarray:
        raw_serp = self.serpenoid_dot(self._t, self._ed1, self._el1, self._ed2 / 10, self._el2 / 10, self._delta)
        max = np.max(raw_serp, axis=1)
        gamma = self._gamma
        # gamma = 0.38

        M_mat = np.where(np.abs(raw_serp.transpose()) > max * gamma, 1, 0)

        return M_mat.transpose()
    def getCurveFunction(self)->np.ndarray:
        raw_curve = self.serpenoid_amp(self._t, self._ad1_bar, self._al1_bar, self._ed1_bar, self._el1_bar, self._ed2_bar / 10, self._el2_bar / 10, self._delta_bar)
    
        return raw_curve
        
    def getMvec(self, k):
        k = k % self.Mvecs

        return self.MotionMatrix[:,k]
    
    def getCurve(self, k):
        k = k % self.Mvecs

        return self.CurveFunction[:,k]

    def getGk(self, k):
        g_k = self.getMvec(k) * self.getCurve(k)

        return g_k
    
    def getGk_all(self, k):
        g_k = np.ones((self.joints,)) * self.getCurve(k)

        return g_k
        
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
    
    ## Predefined functions
    def serpenoid_dot(self, t, e_d1, e_l1, e_d2, e_l2, delta)->np.ndarray:
        #Hirose (1993) serpenoid curve implementations
        e_d1 = np.radians(e_d1)
        e_l1 = np.radians(e_l1)
        delta = np.radians(delta)

        f1 = e_d2 * t
        f2 = e_l2 * t

        j_1 = np.cos(e_d1 + f1) * e_d2
        j_2 = np.cos(e_l1 * 2 + f2 + delta) * e_l2

        j_3 = np.cos(e_d1 * 3 + f1) * e_d2
        j_4 = np.cos(e_l1 * 4 + f2 + delta) * e_l2

        j_5 = np.cos(e_d1 * 5 + f1) * e_d2
        j_6 = np.cos(e_l1 * 6 + f2 + delta) * e_l2

        j_7 = np.cos(e_d1 * 7 + f1) * e_d2
        j_8 = np.cos(e_l1 * 8 + f2 + delta) * e_l2

        j_9 = np.cos(e_d1 * 9 + f1) * e_d2
        j_10 = np.cos(e_l1 * 10 + f2 + delta) * e_l2

        j_11 = np.cos(e_d1 * 11 + f1) * e_d2
        j_12 = np.cos(e_l1 * 12 + f2 + delta) * e_l2

        j_13 = np.cos(e_d1 * 13 + f1) * e_d2
        j_14 = np.cos(e_l1 * 14 + f2 + delta) * e_l2

        return np.array([j_1, j_2, j_3, j_4, j_5, j_6, j_7, j_8, j_9, j_10, j_11, j_12, j_13, j_14])

    ## Predefined functions
    def serpenoid_amp(self, t, a_d, a_l, e_d1, e_l1, e_d2, e_l2, delta)->np.ndarray:
        #Hirose (1993) serpenoid curve implementations
        a_d = np.radians(a_d)
        a_l = np.radians(a_l)
        e_d1 = np.radians(e_d1)
        e_l1 = np.radians(e_l1)
        delta = np.radians(delta)

        f1 = e_d2 * t
        f2 = e_l2 * t

        j_1 = np.sin(e_d1 + f1) * a_d
        j_2 = np.sin(e_l1 * 2 + f2 + delta) * a_l

        j_3 = np.sin(e_d1 * 3 + f1) * a_d
        j_4 = np.sin(e_l1 * 4 + f2 + delta) * a_l

        j_5 = np.sin(e_d1 * 5 + f1) * a_d
        j_6 = np.sin(e_l1 * 6 + f2 + delta) * a_l

        j_7 = np.sin(e_d1 * 7 + f1) * a_d
        j_8 = np.sin(e_l1 * 8 + f2 + delta) * a_l

        j_9 = np.sin(e_d1 * 9 + f1) * a_d
        j_10 = np.sin(e_l1 * 10 + f2 + delta) * a_l

        j_11 = np.sin(e_d1 * 11 + f1) * a_d
        j_12 = np.sin(e_l1 * 12 + f2 + delta) * a_l

        j_13 = np.sin(e_d1 * 13 + f1) * a_d
        j_14 = np.sin(e_l1 * 14 + f2 + delta) * a_l

        return np.array([j_1, j_2, j_3, j_4, j_5, j_6, j_7, j_8, j_9, j_10, j_11, j_12, j_13, j_14])

    def __genMotionMat(self, serp_pos : np.array)->np.ndarray:
        serp_vel = np.diff(serp_pos.copy()) * (1 / self.gait_sampling_interval)
        serp_tor = np.diff(serp_vel.copy()) * (1 / self.gait_sampling_interval)

        motionMat = np.sign(serp_tor)

        return motionMat