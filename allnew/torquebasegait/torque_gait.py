# © 2022 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Date : 2022-09-20 (YYYYMMDD)
# Description : torque base gait class

import math
import numpy as np

class torque_gait:      
        def __init__(self, M = np.eye(14)):
                self.motion_M = M
                self.command = np.array([])     

        def _mcol_weighten(self, t, weight_vector = 2.7)->np.ndarray:
                time_slot = t % (np.shape(self.motion_M)[0])
                m_t = self.motion_M[:,time_slot]

                # assert np.shape(weight_vector) == np.shape(m_t), 'Dimension of m_t and weight vector are not match.'
                return np.dot(weight_vector,m_t)


        def make_motion(self, t,  weight_vector = 2.7)->np.ndarray:
                current_m = self._mcol_weighten(t,weight_vector)
                ctrl_idx = np.nonzero(current_m)[0]

                for idx in ctrl_idx:
                        
