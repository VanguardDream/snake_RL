from typing import Optional

import mujoco._structs
import numpy

def rollout(model: mujoco._structs.MjModel, data: mujoco._structs.MjData, nstate: int, nstep: int, initial_state: Optional[numpy.ndarray[numpy.float64]] = ..., initial_time: Optional[numpy.ndarray[numpy.float64]] = ..., initial_warmstart: Optional[numpy.ndarray[numpy.float64]] = ..., ctrl: Optional[numpy.ndarray[numpy.float64]] = ..., qfrc_applied: Optional[numpy.ndarray[numpy.float64]] = ..., xfrc_applied: Optional[numpy.ndarray[numpy.float64]] = ..., mocap: Optional[numpy.ndarray[numpy.float64]] = ..., state: Optional[numpy.ndarray[numpy.float64]] = ..., sensordata: Optional[numpy.ndarray[numpy.float64]] = ...) -> None: ...
