# © 2022 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Date : 2022-09-20 (YYYYMMDD)
# Description : torque base gait class

from decimal import DivisionByZero
import numpy as np

class torque_gait:      
        def __init__(self, M = np.eye(14), tau = 1):
                self.motion_M = M
                self.tau = tau
                self.command = np.zeros(np.shape(self.motion_M)[0])

        def _mcol_weighten(self, t:int, weight_vector:float = 2.7)->np.ndarray:
                time_slot = t % (np.shape(self.motion_M)[0])
                m_t = self.motion_M[:,time_slot]

                # assert np.shape(weight_vector) == np.shape(m_t), 'Dimension of m_t and weight vector are not match.'
                return np.dot(weight_vector,m_t)


        def make_motion(self, t,  weight_vector = 2.7)->np.ndarray:
                if t % self.tau == 0:
                        t = int(t / self.tau)

                        current_m = self._mcol_weighten(t,weight_vector)
                        ctrl_idx = np.nonzero(current_m)[0]

                        for idx in ctrl_idx:
                                if self.command[idx] <= 0:
                                        self.command[idx] = current_m[idx]
                                else:
                                        self.command[idx] = -current_m[idx]

                        return self.command
                else:
                        return self.command
                                
        def get_stride_ratio(self, i) -> float:
                i_step = i % (np.shape(self.motion_M)[1] * self.tau)
                try:
                        if np.shape(self.motion_M)[1] == 0:
                                raise ValueError("Maybe the gait class should not be initiated correctly check gait class again (m_column value is zero now)")
                        
                        stride_ratio = (i_step + 1) / (self.tau * np.shape(self.motion_M)[1])

                except DivisionByZero:
                        exit()
                except ValueError:
                        exit()

                return stride_ratio
