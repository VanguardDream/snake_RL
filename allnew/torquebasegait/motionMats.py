from mmap import mmap
import numpy as np

class motionMats:
    def __init__(self) -> None:

        self.Mmats = []

        self._m_00 = np.eye(14)

                # self.m_sinuous = np.random.randint(2, size=(14,14))

                # self.m_sinuous = np.array([
                #     [1,0,0,0,0,0,0,0,1,0,0,0,0,0],
                #     [0,1,0,0,0,0,0,0,0,1,0,0,0,0],
                #     [0,0,1,0,0,0,0,0,0,0,1,0,0,0],
                #     [0,0,0,1,0,0,0,0,0,0,0,1,0,0],
                #     [0,0,0,0,1,0,0,0,0,0,0,0,1,0],
                #     [0,0,0,0,0,1,0,0,0,0,0,0,0,1],
                #     [1,0,0,0,0,0,1,0,0,0,0,0,0,0],
                #     [0,1,0,0,0,0,0,1,0,0,0,0,0,0],
                #     [0,0,1,0,0,0,0,0,1,0,0,0,0,0],
                #     [0,0,0,1,0,0,0,0,0,1,0,0,0,0], 
                #     [0,0,0,0,1,0,0,0,0,0,1,0,0,0], 
                #     [0,0,0,0,0,1,0,0,0,0,0,1,0,0], 
                #     [0,0,0,0,0,0,1,0,0,0,0,0,1,0], 
                #     [0,0,0,0,0,0,0,1,0,0,0,0,0,1]  
                #     ],dtype='float')

        self._m_01 = np.array([ [0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                                [1,0,0,0,1,0,0,0,1,0,0,0,1,0],
                                [0,0,0,1,0,0,0,1,0,0,0,1,0,0],
                                [0,0,1,0,0,0,1,0,0,0,1,0,0,0],
                                [0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                                [1,0,0,0,1,0,0,0,1,0,0,0,1,0],
                                [0,0,0,1,0,0,0,1,0,0,0,1,0,0],
                                [0,0,1,0,0,0,1,0,0,0,1,0,0,0],
                                [0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                                [1,0,0,0,1,0,0,0,1,0,0,0,1,0],
                                [0,0,0,1,0,0,0,1,0,0,0,1,0,0],
                                [0,0,1,0,0,0,1,0,0,0,1,0,0,0],
                                [0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                                [1,0,0,0,1,0,0,0,1,0,0,0,1,0]],dtype='int')

        self._m_02 = np.flip(np.eye(14),1) #m4 게이트는 단위행렬의 대칭으로 실험함.

        self._m_03 = np.flip(self._m_02,1) #m5 게이트는 Sidewind행렬의 대칭으로 실험함.

        self._m_04 = np.array([ [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
                                [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0],
                                [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
                                [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                                [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
                                [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0],
                                [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
                                [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                                [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
                                [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0],
                                [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
                                [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                                [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
                                [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0]   ],dtype='int')

        self.Mmats.append(self._m_00)
        self.Mmats.append(self._m_01)
        self.Mmats.append(self._m_02)
        self.Mmats.append(self._m_03)


        self.Mmats = np.array(self.Mmats)