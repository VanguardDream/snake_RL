from typing import ClassVar, Optional

from typing import overload
import mujoco._structs
import numpy

class MjrContext:
    auxColor: numpy.ndarray[numpy.float64]
    auxColor_r: numpy.ndarray[numpy.float64]
    auxFBO: numpy.ndarray[numpy.float64]
    auxFBO_r: numpy.ndarray[numpy.float64]
    auxHeight: numpy.ndarray[numpy.float64]
    auxSamples: numpy.ndarray[numpy.float64]
    auxWidth: numpy.ndarray[numpy.float64]
    baseBuiltin: int
    baseFontBig: int
    baseFontNormal: int
    baseFontShadow: int
    baseHField: int
    baseMesh: int
    basePlane: int
    charHeight: int
    charHeightBig: int
    charWidth: numpy.ndarray[numpy.float64]
    charWidthBig: numpy.ndarray[numpy.float64]
    currentBuffer: int
    fogEnd: float
    fogRGBA: numpy.ndarray[numpy.float64]
    fogStart: float
    fontScale: int
    glInitialized: int
    lineWidth: float
    ntexture: int
    offColor: int
    offColor_r: int
    offDepthStencil: int
    offDepthStencil_r: int
    offFBO: int
    offFBO_r: int
    offHeight: int
    offSamples: int
    offWidth: int
    rangeBuiltin: int
    rangeFont: int
    rangeHField: int
    rangeMesh: int
    rangePlane: int
    shadowClip: float
    shadowFBO: int
    shadowScale: float
    shadowSize: int
    shadowTex: int
    skinfaceVBO: numpy.ndarray[numpy.float64]
    skinnormalVBO: numpy.ndarray[numpy.float64]
    skintexcoordVBO: numpy.ndarray[numpy.float64]
    skinvertVBO: numpy.ndarray[numpy.float64]
    texture: numpy.ndarray[numpy.float64]
    textureType: numpy.ndarray[numpy.float64]
    windowAvailable: int
    windowDoublebuffer: int
    windowSamples: int
    windowStereo: int
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: mujoco._structs.MjModel, arg1: int) -> None: ...
    def free(self) -> None: ...
    @property
    def nskin(self) -> int: ...

class MjrRect:
    __hash__: ClassVar[None] = ...
    bottom: int
    height: int
    left: int
    width: int
    def __init__(self, left: int, bottom: int, width: int, height: int) -> None: ...
    def __copy__(self) -> MjrRect: ...
    def __deepcopy__(self, arg0: dict) -> MjrRect: ...
    def __eq__(self, arg0: object) -> bool: ...

def mjr_addAux(index: int, width: int, height: int, samples: int, con: MjrContext) -> None: ...
def mjr_blitAux(index: int, src: MjrRect, left: int, bottom: int, con: MjrContext) -> None: ...
def mjr_blitBuffer(src: MjrRect, dst: MjrRect, flg_color: int, flg_depth: int, con: MjrContext) -> None: ...
def mjr_changeFont(fontscale: int, con: MjrContext) -> None: ...
def mjr_drawPixels(rgb: Optional[numpy.ndarray[numpy.uint8[m,1]]], depth: Optional[numpy.ndarray[numpy.float32[m,1]]], viewport: MjrRect, con: MjrContext) -> None: ...
def mjr_figure(viewport: MjrRect, fig: mujoco._structs.MjvFigure, con: MjrContext) -> None: ...
def mjr_findRect(x: int, y: int, nrect: int, rect: MjrRect) -> int: ...
def mjr_finish() -> None: ...
def mjr_getError() -> int: ...
def mjr_label(viewport: MjrRect, font: int, txt: str, r: float, g: float, b: float, a: float, rt: float, gt: float, bt: float, con: MjrContext) -> None: ...
def mjr_maxViewport(con: MjrContext) -> MjrRect: ...
def mjr_overlay(font: int, gridpos: int, viewport: MjrRect, overlay: str, overlay2: str, con: MjrContext) -> None: ...
def mjr_readPixels(rgb: Optional[numpy.ndarray[numpy.uint8]], depth: Optional[numpy.ndarray[numpy.float32]], viewport: MjrRect, con: MjrContext) -> None: ...
def mjr_rectangle(viewport: MjrRect, r: float, g: float, b: float, a: float) -> None: ...
def mjr_render(viewport: MjrRect, scn: mujoco._structs.MjvScene, con: MjrContext) -> None: ...
def mjr_restoreBuffer(con: MjrContext) -> None: ...
def mjr_setAux(index: int, con: MjrContext) -> None: ...
def mjr_setBuffer(framebuffer: int, con: MjrContext) -> None: ...
def mjr_text(font: int, txt: str, con: MjrContext, x: float, y: float, r: float, g: float, b: float) -> None: ...
def mjr_uploadHField(m: mujoco._structs.MjModel, con: MjrContext, hfieldid: int) -> None: ...
def mjr_uploadMesh(m: mujoco._structs.MjModel, con: MjrContext, meshid: int) -> None: ...
def mjr_uploadTexture(m: mujoco._structs.MjModel, con: MjrContext, texid: int) -> None: ...