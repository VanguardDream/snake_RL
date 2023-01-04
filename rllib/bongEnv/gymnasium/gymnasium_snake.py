import numpy as np

from gymnasium import utils
from gymnasium.envs.mujoco import MujocoEnv
from gymnasium.spaces import Box


DEFAULT_CAMERA_CONFIG = {
    "trackbodyid": 1,
    "distance": 4.0,
    "lookat": np.array((0.0, 0.0, 2.0)),
    "elevation": -20.0,
}

def mass_center(model, data):
    mass = np.expand_dims(model.body_mass, axis=1)
    xpos = data.xipos
    return (np.sum(mass * xpos, axis=0) / np.sum(mass))[0:2].copy()

def orientatin_center(model, data):
    pass

class bongSnakeEnv(MujocoEnv):
    # Action space order of this Env is         :   
    # Observation space order of this Env is    :
    def __init__(
        self, 
        model_path, 
        frame_skip, 
        observation_space: Space, 
        render_mode: Optional[str] = None, 
        width: int = ..., 
        height: int = ..., 
        camera_id: Optional[int] = None, 
        camera_name: Optional[str] = None, 
        default_camera_config: Optional[dict] = None):
        
        super().__init__(model_path, frame_skip, observation_space, render_mode, width, height, camera_id, camera_name, default_camera_config)
    pass
