import numpy as np

class snake_gait:
    def __init__(self, gait_type: int = 1, start_k: int = 0):
        self.k = start_k

        if gait_type == 0: #Vertical
            self.M = np.array([[1,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0],
                                [0,1,0,0,0,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,1,0,0,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,1,0,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,0,1,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,0,0,1,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,1],
                                [0,0,0,0,0,0,0]],dtype='int')

        elif gait_type == 1: #Serpentine
            self.M = np.eye(14)

        elif gait_type == 2: #Sidewinding
            self.M = np.array([[0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                                [1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                [0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                                [0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                                [0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                                [0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                                [0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                                [0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                                [0,0,0,0,0,0,0,0,0,0,0,0,1,0]],dtype='int')

        else:
            self.M = np.ones((14,1))

        self.M_cols = self.M.shape[1]

        self.k = self.k % self.M_cols

    def get_next_joints(self) -> np.ndarray:
        return self.M[:,self.k]

    def gait_step(self):
        self.k = (self.k + 1) % self.M_cols