from _typeshed import Incomplete

PYOPENGL_PLATFORM: Incomplete

def create_initialized_egl_device_display(): ...

EGL_DISPLAY: Incomplete
EGL_ATTRIBUTES: Incomplete

class GLContext:
    def __init__(self, max_width, max_height) -> None: ...
    def make_current(self) -> None: ...
    def free(self) -> None: ...
    def __del__(self) -> None: ...
