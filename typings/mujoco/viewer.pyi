import mujoco
from _typeshed import Incomplete
from typing import Optional

PERCENT_REALTIME: Incomplete
MAX_SYNC_MISALIGN: float
SIM_REFRESH_FRACTION: float
CallbackType: Incomplete
LoaderType: Incomplete
Simulate: Incomplete

def launch(model: Optional[mujoco.MjModel] = ..., data: Optional[mujoco.MjData] = ..., *, run_physics_thread: bool = ..., loader: Optional[LoaderType] = ...) -> None: ...
def launch_from_path(path: str) -> None: ...
def launch_repl(model: mujoco.MjModel, data: mujoco.MjData) -> None: ...
