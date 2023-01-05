from typing import Any, ClassVar

from typing import overload
import mujoco._enums
import numpy

class MjContact:
    __hash__: ClassVar[None] = ...
    H: numpy.ndarray[numpy.float64]
    dim: int
    dist: float
    efc_address: int
    exclude: int
    frame: numpy.ndarray[numpy.float64]
    friction: numpy.ndarray[numpy.float64]
    geom1: int
    geom2: int
    includemargin: float
    mu: float
    pos: numpy.ndarray[numpy.float64]
    solimp: numpy.ndarray[numpy.float64]
    solref: numpy.ndarray[numpy.float64]
    def __init__(self) -> None: ...
    def __copy__(self) -> MjContact: ...
    def __deepcopy__(self, arg0: dict) -> MjContact: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjData:
    D_colind: numpy.ndarray[numpy.int32]
    D_rowadr: numpy.ndarray[numpy.int32]
    D_rownnz: numpy.ndarray[numpy.int32]
    act: numpy.ndarray[numpy.float64]
    act_dot: numpy.ndarray[numpy.float64]
    actuator_force: numpy.ndarray[numpy.float64]
    actuator_length: numpy.ndarray[numpy.float64]
    actuator_moment: numpy.ndarray[numpy.float64]
    actuator_velocity: numpy.ndarray[numpy.float64]
    cacc: numpy.ndarray[numpy.float64]
    cam_xmat: numpy.ndarray[numpy.float64]
    cam_xpos: numpy.ndarray[numpy.float64]
    cdof: numpy.ndarray[numpy.float64]
    cdof_dot: numpy.ndarray[numpy.float64]
    cfrc_ext: numpy.ndarray[numpy.float64]
    cfrc_int: numpy.ndarray[numpy.float64]
    cinert: numpy.ndarray[numpy.float64]
    crb: numpy.ndarray[numpy.float64]
    ctrl: numpy.ndarray[numpy.float64]
    cvel: numpy.ndarray[numpy.float64]
    energy: numpy.ndarray[numpy.float64]
    geom_xmat: numpy.ndarray[numpy.float64]
    geom_xpos: numpy.ndarray[numpy.float64]
    light_xdir: numpy.ndarray[numpy.float64]
    light_xpos: numpy.ndarray[numpy.float64]
    maxuse_con: int
    maxuse_efc: int
    maxuse_stack: int
    mocap_pos: numpy.ndarray[numpy.float64]
    mocap_quat: numpy.ndarray[numpy.float64]
    nbuffer: int
    ncon: int
    ne: int
    nefc: int
    nf: int
    nstack: int
    plugin: numpy.ndarray[numpy.int32]
    plugin_data: numpy.ndarray[numpy.uint64]
    plugin_state: numpy.ndarray[numpy.float64]
    pstack: int
    qDeriv: numpy.ndarray[numpy.float64]
    qH: numpy.ndarray[numpy.float64]
    qHDiagInv: numpy.ndarray[numpy.float64]
    qLD: numpy.ndarray[numpy.float64]
    qLDiagInv: numpy.ndarray[numpy.float64]
    qLDiagSqrtInv: numpy.ndarray[numpy.float64]
    qLU: numpy.ndarray[numpy.float64]
    qM: numpy.ndarray[numpy.float64]
    qacc: numpy.ndarray[numpy.float64]
    qacc_smooth: numpy.ndarray[numpy.float64]
    qacc_warmstart: numpy.ndarray[numpy.float64]
    qfrc_actuator: numpy.ndarray[numpy.float64]
    qfrc_applied: numpy.ndarray[numpy.float64]
    qfrc_bias: numpy.ndarray[numpy.float64]
    qfrc_constraint: numpy.ndarray[numpy.float64]
    qfrc_inverse: numpy.ndarray[numpy.float64]
    qfrc_passive: numpy.ndarray[numpy.float64]
    qfrc_smooth: numpy.ndarray[numpy.float64]
    qpos: numpy.ndarray[numpy.float64]
    qvel: numpy.ndarray[numpy.float64]
    sensordata: numpy.ndarray[numpy.float64]
    site_xmat: numpy.ndarray[numpy.float64]
    site_xpos: numpy.ndarray[numpy.float64]
    solver_fwdinv: numpy.ndarray[numpy.float64]
    solver_iter: int
    solver_nnz: int
    subtree_angmom: numpy.ndarray[numpy.float64]
    subtree_com: numpy.ndarray[numpy.float64]
    subtree_linvel: numpy.ndarray[numpy.float64]
    ten_J: numpy.ndarray[numpy.float64]
    ten_J_colind: numpy.ndarray[numpy.int32]
    ten_J_rowadr: numpy.ndarray[numpy.int32]
    ten_J_rownnz: numpy.ndarray[numpy.int32]
    ten_length: numpy.ndarray[numpy.float64]
    ten_velocity: numpy.ndarray[numpy.float64]
    ten_wrapadr: numpy.ndarray[numpy.int32]
    ten_wrapnum: numpy.ndarray[numpy.int32]
    time: float
    userdata: numpy.ndarray[numpy.float64]
    wrap_obj: numpy.ndarray[numpy.int32]
    wrap_xpos: numpy.ndarray[numpy.float64]
    xanchor: numpy.ndarray[numpy.float64]
    xaxis: numpy.ndarray[numpy.float64]
    xfrc_applied: numpy.ndarray[numpy.float64]
    ximat: numpy.ndarray[numpy.float64]
    xipos: numpy.ndarray[numpy.float64]
    xmat: numpy.ndarray[numpy.float64]
    xpos: numpy.ndarray[numpy.float64]
    xquat: numpy.ndarray[numpy.float64]
    def __init__(self, arg0: MjModel) -> None: ...
    def actuator(self, *args, **kwargs) -> Any: ...
    def body(self, *args, **kwargs) -> Any: ...
    def cam(self, *args, **kwargs) -> Any: ...
    def camera(self, *args, **kwargs) -> Any: ...
    def geom(self, *args, **kwargs) -> Any: ...
    def jnt(self, *args, **kwargs) -> Any: ...
    def joint(self, *args, **kwargs) -> Any: ...
    def light(self, *args, **kwargs) -> Any: ...
    def sensor(self, *args, **kwargs) -> Any: ...
    def site(self, *args, **kwargs) -> Any: ...
    def ten(self, *args, **kwargs) -> Any: ...
    def tendon(self, *args, **kwargs) -> Any: ...
    def __copy__(self) -> MjData: ...
    def __deepcopy__(self, arg0: dict) -> MjData: ...
    def __getstate__(self) -> bytes: ...
    def __setstate__(self, arg0: bytes) -> None: ...
    @property
    def _address(self) -> int: ...
    @property
    def contact(self) -> _MjContactList: ...
    @property
    def efc_AR(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_AR_colind(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_AR_rowadr(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_AR_rownnz(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_D(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_J(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_JT(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_JT_colind(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_JT_rowadr(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_JT_rownnz(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_JT_rowsuper(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_J_colind(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_J_rowadr(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_J_rownnz(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_J_rowsuper(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_KBIP(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_R(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_aref(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_b(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_diagApprox(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_force(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_frictionloss(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_id(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_margin(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_pos(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_state(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_type(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def efc_vel(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def solver(self) -> _MjSolverStatList: ...
    @property
    def timer(self) -> _MjTimerStatList: ...
    @property
    def warning(self) -> _MjWarningStatList: ...

class MjLROpt:
    __hash__: ClassVar[None] = ...
    accel: float
    inteval: float
    inttotal: float
    maxforce: float
    mode: int
    timeconst: float
    timestep: float
    tolrange: float
    useexisting: int
    uselimit: int
    def __init__(self) -> None: ...
    def __copy__(self) -> MjLROpt: ...
    def __deepcopy__(self, arg0: dict) -> MjLROpt: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjModel:
    actuator_acc0: numpy.ndarray[numpy.float64]
    actuator_actadr: numpy.ndarray[numpy.int32]
    actuator_actlimited: numpy.ndarray[numpy.uint8]
    actuator_actnum: numpy.ndarray[numpy.int32]
    actuator_actrange: numpy.ndarray[numpy.float64]
    actuator_biasprm: numpy.ndarray[numpy.float64]
    actuator_biastype: numpy.ndarray[numpy.int32]
    actuator_cranklength: numpy.ndarray[numpy.float64]
    actuator_ctrllimited: numpy.ndarray[numpy.uint8]
    actuator_ctrlrange: numpy.ndarray[numpy.float64]
    actuator_dynprm: numpy.ndarray[numpy.float64]
    actuator_dyntype: numpy.ndarray[numpy.int32]
    actuator_forcelimited: numpy.ndarray[numpy.uint8]
    actuator_forcerange: numpy.ndarray[numpy.float64]
    actuator_gainprm: numpy.ndarray[numpy.float64]
    actuator_gaintype: numpy.ndarray[numpy.int32]
    actuator_gear: numpy.ndarray[numpy.float64]
    actuator_group: numpy.ndarray[numpy.int32]
    actuator_length0: numpy.ndarray[numpy.float64]
    actuator_lengthrange: numpy.ndarray[numpy.float64]
    actuator_plugin: numpy.ndarray[numpy.int32]
    actuator_trnid: numpy.ndarray[numpy.int32]
    actuator_trntype: numpy.ndarray[numpy.int32]
    actuator_user: numpy.ndarray[numpy.float64]
    body_dofadr: numpy.ndarray[numpy.int32]
    body_dofnum: numpy.ndarray[numpy.int32]
    body_geomadr: numpy.ndarray[numpy.int32]
    body_geomnum: numpy.ndarray[numpy.int32]
    body_gravcomp: numpy.ndarray[numpy.float64]
    body_inertia: numpy.ndarray[numpy.float64]
    body_invweight0: numpy.ndarray[numpy.float64]
    body_ipos: numpy.ndarray[numpy.float64]
    body_iquat: numpy.ndarray[numpy.float64]
    body_jntadr: numpy.ndarray[numpy.int32]
    body_jntnum: numpy.ndarray[numpy.int32]
    body_mass: numpy.ndarray[numpy.float64]
    body_mocapid: numpy.ndarray[numpy.int32]
    body_parentid: numpy.ndarray[numpy.int32]
    body_plugin: numpy.ndarray[numpy.int32]
    body_pos: numpy.ndarray[numpy.float64]
    body_quat: numpy.ndarray[numpy.float64]
    body_rootid: numpy.ndarray[numpy.int32]
    body_sameframe: numpy.ndarray[numpy.uint8]
    body_simple: numpy.ndarray[numpy.uint8]
    body_subtreemass: numpy.ndarray[numpy.float64]
    body_user: numpy.ndarray[numpy.float64]
    body_weldid: numpy.ndarray[numpy.int32]
    cam_bodyid: numpy.ndarray[numpy.int32]
    cam_fovy: numpy.ndarray[numpy.float64]
    cam_ipd: numpy.ndarray[numpy.float64]
    cam_mat0: numpy.ndarray[numpy.float64]
    cam_mode: numpy.ndarray[numpy.int32]
    cam_pos: numpy.ndarray[numpy.float64]
    cam_pos0: numpy.ndarray[numpy.float64]
    cam_poscom0: numpy.ndarray[numpy.float64]
    cam_quat: numpy.ndarray[numpy.float64]
    cam_targetbodyid: numpy.ndarray[numpy.int32]
    cam_user: numpy.ndarray[numpy.float64]
    dof_M0: numpy.ndarray[numpy.float64]
    dof_Madr: numpy.ndarray[numpy.int32]
    dof_armature: numpy.ndarray[numpy.float64]
    dof_bodyid: numpy.ndarray[numpy.int32]
    dof_damping: numpy.ndarray[numpy.float64]
    dof_frictionloss: numpy.ndarray[numpy.float64]
    dof_invweight0: numpy.ndarray[numpy.float64]
    dof_jntid: numpy.ndarray[numpy.int32]
    dof_parentid: numpy.ndarray[numpy.int32]
    dof_simplenum: numpy.ndarray[numpy.int32]
    dof_solimp: numpy.ndarray[numpy.float64]
    dof_solref: numpy.ndarray[numpy.float64]
    eq_active: numpy.ndarray[numpy.uint8]
    eq_data: numpy.ndarray[numpy.float64]
    eq_obj1id: numpy.ndarray[numpy.int32]
    eq_obj2id: numpy.ndarray[numpy.int32]
    eq_solimp: numpy.ndarray[numpy.float64]
    eq_solref: numpy.ndarray[numpy.float64]
    eq_type: numpy.ndarray[numpy.int32]
    exclude_signature: numpy.ndarray[numpy.int32]
    geom_bodyid: numpy.ndarray[numpy.int32]
    geom_conaffinity: numpy.ndarray[numpy.int32]
    geom_condim: numpy.ndarray[numpy.int32]
    geom_contype: numpy.ndarray[numpy.int32]
    geom_dataid: numpy.ndarray[numpy.int32]
    geom_fluid: numpy.ndarray[numpy.float64]
    geom_friction: numpy.ndarray[numpy.float64]
    geom_gap: numpy.ndarray[numpy.float64]
    geom_group: numpy.ndarray[numpy.int32]
    geom_margin: numpy.ndarray[numpy.float64]
    geom_matid: numpy.ndarray[numpy.int32]
    geom_pos: numpy.ndarray[numpy.float64]
    geom_priority: numpy.ndarray[numpy.int32]
    geom_quat: numpy.ndarray[numpy.float64]
    geom_rbound: numpy.ndarray[numpy.float64]
    geom_rgba: numpy.ndarray[numpy.float32]
    geom_sameframe: numpy.ndarray[numpy.uint8]
    geom_size: numpy.ndarray[numpy.float64]
    geom_solimp: numpy.ndarray[numpy.float64]
    geom_solmix: numpy.ndarray[numpy.float64]
    geom_solref: numpy.ndarray[numpy.float64]
    geom_type: numpy.ndarray[numpy.int32]
    geom_user: numpy.ndarray[numpy.float64]
    hfield_adr: numpy.ndarray[numpy.int32]
    hfield_data: numpy.ndarray[numpy.float32]
    hfield_ncol: numpy.ndarray[numpy.int32]
    hfield_nrow: numpy.ndarray[numpy.int32]
    hfield_size: numpy.ndarray[numpy.float64]
    jnt_axis: numpy.ndarray[numpy.float64]
    jnt_bodyid: numpy.ndarray[numpy.int32]
    jnt_dofadr: numpy.ndarray[numpy.int32]
    jnt_group: numpy.ndarray[numpy.int32]
    jnt_limited: numpy.ndarray[numpy.uint8]
    jnt_margin: numpy.ndarray[numpy.float64]
    jnt_pos: numpy.ndarray[numpy.float64]
    jnt_qposadr: numpy.ndarray[numpy.int32]
    jnt_range: numpy.ndarray[numpy.float64]
    jnt_solimp: numpy.ndarray[numpy.float64]
    jnt_solref: numpy.ndarray[numpy.float64]
    jnt_stiffness: numpy.ndarray[numpy.float64]
    jnt_type: numpy.ndarray[numpy.int32]
    jnt_user: numpy.ndarray[numpy.float64]
    key_act: numpy.ndarray[numpy.float64]
    key_ctrl: numpy.ndarray[numpy.float64]
    key_mpos: numpy.ndarray[numpy.float64]
    key_mquat: numpy.ndarray[numpy.float64]
    key_qpos: numpy.ndarray[numpy.float64]
    key_qvel: numpy.ndarray[numpy.float64]
    key_time: numpy.ndarray[numpy.float64]
    light_active: numpy.ndarray[numpy.uint8]
    light_ambient: numpy.ndarray[numpy.float32]
    light_attenuation: numpy.ndarray[numpy.float32]
    light_bodyid: numpy.ndarray[numpy.int32]
    light_castshadow: numpy.ndarray[numpy.uint8]
    light_cutoff: numpy.ndarray[numpy.float32]
    light_diffuse: numpy.ndarray[numpy.float32]
    light_dir: numpy.ndarray[numpy.float64]
    light_dir0: numpy.ndarray[numpy.float64]
    light_directional: numpy.ndarray[numpy.uint8]
    light_exponent: numpy.ndarray[numpy.float32]
    light_mode: numpy.ndarray[numpy.int32]
    light_pos: numpy.ndarray[numpy.float64]
    light_pos0: numpy.ndarray[numpy.float64]
    light_poscom0: numpy.ndarray[numpy.float64]
    light_specular: numpy.ndarray[numpy.float32]
    light_targetbodyid: numpy.ndarray[numpy.int32]
    mat_emission: numpy.ndarray[numpy.float32]
    mat_reflectance: numpy.ndarray[numpy.float32]
    mat_rgba: numpy.ndarray[numpy.float32]
    mat_shininess: numpy.ndarray[numpy.float32]
    mat_specular: numpy.ndarray[numpy.float32]
    mat_texid: numpy.ndarray[numpy.int32]
    mat_texrepeat: numpy.ndarray[numpy.float32]
    mat_texuniform: numpy.ndarray[numpy.uint8]
    mesh_face: numpy.ndarray[numpy.int32]
    mesh_faceadr: numpy.ndarray[numpy.int32]
    mesh_facenum: numpy.ndarray[numpy.int32]
    mesh_graph: numpy.ndarray[numpy.int32]
    mesh_graphadr: numpy.ndarray[numpy.int32]
    mesh_normal: numpy.ndarray[numpy.float32]
    mesh_texcoord: numpy.ndarray[numpy.float32]
    mesh_texcoordadr: numpy.ndarray[numpy.int32]
    mesh_vert: numpy.ndarray[numpy.float32]
    mesh_vertadr: numpy.ndarray[numpy.int32]
    mesh_vertnum: numpy.ndarray[numpy.int32]
    name_actuatoradr: numpy.ndarray[numpy.int32]
    name_bodyadr: numpy.ndarray[numpy.int32]
    name_camadr: numpy.ndarray[numpy.int32]
    name_eqadr: numpy.ndarray[numpy.int32]
    name_excludeadr: numpy.ndarray[numpy.int32]
    name_geomadr: numpy.ndarray[numpy.int32]
    name_hfieldadr: numpy.ndarray[numpy.int32]
    name_jntadr: numpy.ndarray[numpy.int32]
    name_keyadr: numpy.ndarray[numpy.int32]
    name_lightadr: numpy.ndarray[numpy.int32]
    name_matadr: numpy.ndarray[numpy.int32]
    name_meshadr: numpy.ndarray[numpy.int32]
    name_numericadr: numpy.ndarray[numpy.int32]
    name_pairadr: numpy.ndarray[numpy.int32]
    name_pluginadr: numpy.ndarray[numpy.int32]
    name_sensoradr: numpy.ndarray[numpy.int32]
    name_siteadr: numpy.ndarray[numpy.int32]
    name_skinadr: numpy.ndarray[numpy.int32]
    name_tendonadr: numpy.ndarray[numpy.int32]
    name_texadr: numpy.ndarray[numpy.int32]
    name_textadr: numpy.ndarray[numpy.int32]
    name_tupleadr: numpy.ndarray[numpy.int32]
    numeric_adr: numpy.ndarray[numpy.int32]
    numeric_data: numpy.ndarray[numpy.float64]
    numeric_size: numpy.ndarray[numpy.int32]
    pair_dim: numpy.ndarray[numpy.int32]
    pair_friction: numpy.ndarray[numpy.float64]
    pair_gap: numpy.ndarray[numpy.float64]
    pair_geom1: numpy.ndarray[numpy.int32]
    pair_geom2: numpy.ndarray[numpy.int32]
    pair_margin: numpy.ndarray[numpy.float64]
    pair_signature: numpy.ndarray[numpy.int32]
    pair_solimp: numpy.ndarray[numpy.float64]
    pair_solref: numpy.ndarray[numpy.float64]
    plugin: numpy.ndarray[numpy.int32]
    plugin_attr: numpy.ndarray[numpy.int8]
    plugin_attradr: numpy.ndarray[numpy.int32]
    plugin_stateadr: numpy.ndarray[numpy.int32]
    plugin_statenum: numpy.ndarray[numpy.int32]
    qpos0: numpy.ndarray[numpy.float64]
    qpos_spring: numpy.ndarray[numpy.float64]
    sensor_adr: numpy.ndarray[numpy.int32]
    sensor_cutoff: numpy.ndarray[numpy.float64]
    sensor_datatype: numpy.ndarray[numpy.int32]
    sensor_dim: numpy.ndarray[numpy.int32]
    sensor_needstage: numpy.ndarray[numpy.int32]
    sensor_noise: numpy.ndarray[numpy.float64]
    sensor_objid: numpy.ndarray[numpy.int32]
    sensor_objtype: numpy.ndarray[numpy.int32]
    sensor_plugin: numpy.ndarray[numpy.int32]
    sensor_refid: numpy.ndarray[numpy.int32]
    sensor_reftype: numpy.ndarray[numpy.int32]
    sensor_type: numpy.ndarray[numpy.int32]
    sensor_user: numpy.ndarray[numpy.float64]
    site_bodyid: numpy.ndarray[numpy.int32]
    site_group: numpy.ndarray[numpy.int32]
    site_matid: numpy.ndarray[numpy.int32]
    site_pos: numpy.ndarray[numpy.float64]
    site_quat: numpy.ndarray[numpy.float64]
    site_rgba: numpy.ndarray[numpy.float32]
    site_sameframe: numpy.ndarray[numpy.uint8]
    site_size: numpy.ndarray[numpy.float64]
    site_type: numpy.ndarray[numpy.int32]
    site_user: numpy.ndarray[numpy.float64]
    skin_boneadr: numpy.ndarray[numpy.int32]
    skin_bonebindpos: numpy.ndarray[numpy.float32]
    skin_bonebindquat: numpy.ndarray[numpy.float32]
    skin_bonebodyid: numpy.ndarray[numpy.int32]
    skin_bonenum: numpy.ndarray[numpy.int32]
    skin_bonevertadr: numpy.ndarray[numpy.int32]
    skin_bonevertid: numpy.ndarray[numpy.int32]
    skin_bonevertnum: numpy.ndarray[numpy.int32]
    skin_bonevertweight: numpy.ndarray[numpy.float32]
    skin_face: numpy.ndarray[numpy.int32]
    skin_faceadr: numpy.ndarray[numpy.int32]
    skin_facenum: numpy.ndarray[numpy.int32]
    skin_group: numpy.ndarray[numpy.int32]
    skin_inflate: numpy.ndarray[numpy.float32]
    skin_matid: numpy.ndarray[numpy.int32]
    skin_rgba: numpy.ndarray[numpy.float32]
    skin_texcoord: numpy.ndarray[numpy.float32]
    skin_texcoordadr: numpy.ndarray[numpy.int32]
    skin_vert: numpy.ndarray[numpy.float32]
    skin_vertadr: numpy.ndarray[numpy.int32]
    skin_vertnum: numpy.ndarray[numpy.int32]
    tendon_adr: numpy.ndarray[numpy.int32]
    tendon_damping: numpy.ndarray[numpy.float64]
    tendon_frictionloss: numpy.ndarray[numpy.float64]
    tendon_group: numpy.ndarray[numpy.int32]
    tendon_invweight0: numpy.ndarray[numpy.float64]
    tendon_length0: numpy.ndarray[numpy.float64]
    tendon_lengthspring: numpy.ndarray[numpy.float64]
    tendon_limited: numpy.ndarray[numpy.uint8]
    tendon_margin: numpy.ndarray[numpy.float64]
    tendon_matid: numpy.ndarray[numpy.int32]
    tendon_num: numpy.ndarray[numpy.int32]
    tendon_range: numpy.ndarray[numpy.float64]
    tendon_rgba: numpy.ndarray[numpy.float32]
    tendon_solimp_fri: numpy.ndarray[numpy.float64]
    tendon_solimp_lim: numpy.ndarray[numpy.float64]
    tendon_solref_fri: numpy.ndarray[numpy.float64]
    tendon_solref_lim: numpy.ndarray[numpy.float64]
    tendon_stiffness: numpy.ndarray[numpy.float64]
    tendon_user: numpy.ndarray[numpy.float64]
    tendon_width: numpy.ndarray[numpy.float64]
    tex_adr: numpy.ndarray[numpy.int32]
    tex_height: numpy.ndarray[numpy.int32]
    tex_rgb: numpy.ndarray[numpy.uint8]
    tex_type: numpy.ndarray[numpy.int32]
    tex_width: numpy.ndarray[numpy.int32]
    text_adr: numpy.ndarray[numpy.int32]
    text_size: numpy.ndarray[numpy.int32]
    tuple_adr: numpy.ndarray[numpy.int32]
    tuple_objid: numpy.ndarray[numpy.int32]
    tuple_objprm: numpy.ndarray[numpy.float64]
    tuple_objtype: numpy.ndarray[numpy.int32]
    tuple_size: numpy.ndarray[numpy.int32]
    wrap_objid: numpy.ndarray[numpy.int32]
    wrap_prm: numpy.ndarray[numpy.float64]
    wrap_type: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    def actuator(self, *args, **kwargs) -> Any: ...
    def body(self, *args, **kwargs) -> Any: ...
    def cam(self, *args, **kwargs) -> Any: ...
    def camera(self, *args, **kwargs) -> Any: ...
    def eq(self, *args, **kwargs) -> Any: ...
    def equality(self, *args, **kwargs) -> Any: ...
    def exclude(self, *args, **kwargs) -> Any: ...
    def from_binary_path(self, *args, **kwargs) -> Any: ...
    def from_xml_path(self, *args, **kwargs) -> Any: ...
    def from_xml_string(self, *args, **kwargs) -> Any: ...
    def geom(self, *args, **kwargs) -> Any: ...
    def hfield(self, *args, **kwargs) -> Any: ...
    def jnt(self, *args, **kwargs) -> Any: ...
    def joint(self, *args, **kwargs) -> Any: ...
    def key(self, *args, **kwargs) -> Any: ...
    def keyframe(self, *args, **kwargs) -> Any: ...
    def light(self, *args, **kwargs) -> Any: ...
    def mat(self, *args, **kwargs) -> Any: ...
    def material(self, *args, **kwargs) -> Any: ...
    def mesh(self, *args, **kwargs) -> Any: ...
    def numeric(self, *args, **kwargs) -> Any: ...
    def pair(self, *args, **kwargs) -> Any: ...
    def sensor(self, *args, **kwargs) -> Any: ...
    def site(self, *args, **kwargs) -> Any: ...
    def skin(self, *args, **kwargs) -> Any: ...
    def tendon(self, *args, **kwargs) -> Any: ...
    def tex(self, *args, **kwargs) -> Any: ...
    def texture(self, *args, **kwargs) -> Any: ...
    def tuple(self, *args, **kwargs) -> Any: ...
    def __copy__(self) -> MjModel: ...
    def __deepcopy__(self, arg0: dict) -> MjModel: ...
    def __getstate__(self) -> bytes: ...
    def __setstate__(self, arg0: bytes) -> None: ...
    @property
    def _address(self) -> int: ...
    @property
    def nD(self) -> int: ...
    @property
    def nM(self) -> int: ...
    @property
    def na(self) -> int: ...
    @property
    def names(self) -> bytes: ...
    @property
    def nbody(self) -> int: ...
    @property
    def nbuffer(self) -> int: ...
    @property
    def ncam(self) -> int: ...
    @property
    def nconmax(self) -> int: ...
    @property
    def nemax(self) -> int: ...
    @property
    def neq(self) -> int: ...
    @property
    def nexclude(self) -> int: ...
    @property
    def ngeom(self) -> int: ...
    @property
    def nhfield(self) -> int: ...
    @property
    def nhfielddata(self) -> int: ...
    @property
    def njmax(self) -> int: ...
    @property
    def njnt(self) -> int: ...
    @property
    def nkey(self) -> int: ...
    @property
    def nlight(self) -> int: ...
    @property
    def nmat(self) -> int: ...
    @property
    def nmesh(self) -> int: ...
    @property
    def nmeshface(self) -> int: ...
    @property
    def nmeshgraph(self) -> int: ...
    @property
    def nmeshtexvert(self) -> int: ...
    @property
    def nmeshvert(self) -> int: ...
    @property
    def nmocap(self) -> int: ...
    @property
    def nnames(self) -> int: ...
    @property
    def nnumeric(self) -> int: ...
    @property
    def nnumericdata(self) -> int: ...
    @property
    def npair(self) -> int: ...
    @property
    def nplugin(self) -> int: ...
    @property
    def npluginattr(self) -> int: ...
    @property
    def npluginstate(self) -> int: ...
    @property
    def nq(self) -> int: ...
    @property
    def nsensor(self) -> int: ...
    @property
    def nsensordata(self) -> int: ...
    @property
    def nsite(self) -> int: ...
    @property
    def nskin(self) -> int: ...
    @property
    def nskinbone(self) -> int: ...
    @property
    def nskinbonevert(self) -> int: ...
    @property
    def nskinface(self) -> int: ...
    @property
    def nskintexvert(self) -> int: ...
    @property
    def nskinvert(self) -> int: ...
    @property
    def nstack(self) -> int: ...
    @property
    def ntendon(self) -> int: ...
    @property
    def ntex(self) -> int: ...
    @property
    def ntexdata(self) -> int: ...
    @property
    def ntext(self) -> int: ...
    @property
    def ntextdata(self) -> int: ...
    @property
    def ntuple(self) -> int: ...
    @property
    def ntupledata(self) -> int: ...
    @property
    def nu(self) -> int: ...
    @property
    def nuser_actuator(self) -> int: ...
    @property
    def nuser_body(self) -> int: ...
    @property
    def nuser_cam(self) -> int: ...
    @property
    def nuser_geom(self) -> int: ...
    @property
    def nuser_jnt(self) -> int: ...
    @property
    def nuser_sensor(self) -> int: ...
    @property
    def nuser_site(self) -> int: ...
    @property
    def nuser_tendon(self) -> int: ...
    @property
    def nuserdata(self) -> int: ...
    @property
    def nv(self) -> int: ...
    @property
    def nwrap(self) -> int: ...
    @property
    def opt(self) -> MjOption: ...
    @property
    def stat(self) -> Any: ...
    @property
    def text_data(self) -> bytes: ...
    @property
    def vis(self) -> MjVisual: ...

class MjOption:
    __hash__: ClassVar[None] = ...
    apirate: float
    collision: int
    cone: int
    density: float
    disableflags: int
    enableflags: int
    gravity: numpy.ndarray[numpy.float64]
    impratio: float
    integrator: int
    iterations: int
    jacobian: int
    magnetic: numpy.ndarray[numpy.float64]
    mpr_iterations: int
    mpr_tolerance: float
    noslip_iterations: int
    noslip_tolerance: float
    o_margin: float
    o_solimp: numpy.ndarray[numpy.float64]
    o_solref: numpy.ndarray[numpy.float64]
    solver: int
    timestep: float
    tolerance: float
    viscosity: float
    wind: numpy.ndarray[numpy.float64]
    def __init__(self) -> None: ...
    def __copy__(self) -> MjOption: ...
    def __deepcopy__(self, arg0: dict) -> MjOption: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjSolverStat:
    __hash__: ClassVar[None] = ...
    gradient: float
    improvement: float
    lineslope: float
    nactive: int
    nchange: int
    neval: int
    nupdate: int
    def __init__(self) -> None: ...
    def __copy__(self) -> MjSolverStat: ...
    def __deepcopy__(self, arg0: dict) -> MjSolverStat: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjStatistic:
    __hash__: ClassVar[None] = ...
    center: numpy.ndarray[numpy.float64]
    extent: float
    meaninertia: float
    meanmass: float
    meansize: float
    def __init__(self) -> None: ...
    def __copy__(self) -> MjStatistic: ...
    def __deepcopy__(self, arg0: dict) -> MjStatistic: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjTimerStat:
    __hash__: ClassVar[None] = ...
    duration: float
    number: int
    def __init__(self) -> None: ...
    def __copy__(self) -> MjTimerStat: ...
    def __deepcopy__(self, arg0: dict) -> MjTimerStat: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjVisual:
    class Global:
        __hash__: ClassVar[None] = ...
        fovy: float
        glow: float
        ipd: float
        linewidth: float
        offheight: int
        offwidth: int
        def __init__(self, *args, **kwargs) -> None: ...
        def __copy__(self) -> MjVisual.Global: ...
        def __deepcopy__(self, arg0: dict) -> MjVisual.Global: ...
        def __eq__(self, arg0: object) -> bool: ...

    class Headlight:
        __hash__: ClassVar[None] = ...
        active: int
        ambient: numpy.ndarray[numpy.float32]
        diffuse: numpy.ndarray[numpy.float32]
        specular: numpy.ndarray[numpy.float32]
        def __init__(self, *args, **kwargs) -> None: ...
        def __copy__(self) -> MjVisual.Headlight: ...
        def __deepcopy__(self, arg0: dict) -> MjVisual.Headlight: ...
        def __eq__(self, arg0: object) -> bool: ...

    class Map:
        __hash__: ClassVar[None] = ...
        actuatortendon: float
        alpha: float
        fogend: float
        fogstart: float
        force: float
        haze: float
        shadowclip: float
        shadowscale: float
        stiffness: float
        stiffnessrot: float
        torque: float
        zfar: float
        znear: float
        def __init__(self, *args, **kwargs) -> None: ...
        def __copy__(self) -> MjVisual.Map: ...
        def __deepcopy__(self, arg0: dict) -> MjVisual.Map: ...
        def __eq__(self, arg0: object) -> bool: ...

    class Quality:
        __hash__: ClassVar[None] = ...
        numquads: int
        numslices: int
        numstacks: int
        offsamples: int
        shadowsize: int
        def __init__(self, *args, **kwargs) -> None: ...
        def __copy__(self) -> MjVisual.Quality: ...
        def __deepcopy__(self, arg0: dict) -> MjVisual.Quality: ...
        def __eq__(self, arg0: object) -> bool: ...

    class Rgba:
        __hash__: ClassVar[None] = ...
        actuator: numpy.ndarray[numpy.float32]
        actuatornegative: numpy.ndarray[numpy.float32]
        actuatorpositive: numpy.ndarray[numpy.float32]
        camera: numpy.ndarray[numpy.float32]
        com: numpy.ndarray[numpy.float32]
        connect: numpy.ndarray[numpy.float32]
        constraint: numpy.ndarray[numpy.float32]
        contactforce: numpy.ndarray[numpy.float32]
        contactfriction: numpy.ndarray[numpy.float32]
        contactgap: numpy.ndarray[numpy.float32]
        contactpoint: numpy.ndarray[numpy.float32]
        contacttorque: numpy.ndarray[numpy.float32]
        crankbroken: numpy.ndarray[numpy.float32]
        fog: numpy.ndarray[numpy.float32]
        force: numpy.ndarray[numpy.float32]
        haze: numpy.ndarray[numpy.float32]
        inertia: numpy.ndarray[numpy.float32]
        joint: numpy.ndarray[numpy.float32]
        light: numpy.ndarray[numpy.float32]
        rangefinder: numpy.ndarray[numpy.float32]
        selectpoint: numpy.ndarray[numpy.float32]
        slidercrank: numpy.ndarray[numpy.float32]
        def __init__(self, *args, **kwargs) -> None: ...
        def __copy__(self) -> MjVisual.Rgba: ...
        def __deepcopy__(self, arg0: dict) -> MjVisual.Rgba: ...
        def __eq__(self, arg0: object) -> bool: ...

    class Scale:
        __hash__: ClassVar[None] = ...
        actuatorlength: float
        actuatorwidth: float
        camera: float
        com: float
        connect: float
        constraint: float
        contactheight: float
        contactwidth: float
        forcewidth: float
        framelength: float
        framewidth: float
        jointlength: float
        jointwidth: float
        light: float
        selectpoint: float
        slidercrank: float
        def __init__(self, *args, **kwargs) -> None: ...
        def __copy__(self) -> MjVisual.Scale: ...
        def __deepcopy__(self, arg0: dict) -> MjVisual.Scale: ...
        def __eq__(self, arg0: object) -> bool: ...
    __hash__: ClassVar[None] = ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __copy__(self) -> MjVisual: ...
    def __deepcopy__(self, arg0: dict) -> MjVisual: ...
    def __eq__(self, arg0: object) -> bool: ...
    @property
    def global_(self) -> MjVisual.Global: ...
    @property
    def headlight(self) -> MjVisual.Headlight: ...
    @property
    def map(self) -> MjVisual.Map: ...
    @property
    def quality(self) -> MjVisual.Quality: ...
    @property
    def rgba(self) -> MjVisual.Rgba: ...
    @property
    def scale(self) -> MjVisual.Scale: ...

class MjWarningStat:
    __hash__: ClassVar[None] = ...
    lastinfo: int
    number: int
    def __init__(self) -> None: ...
    def __copy__(self) -> MjWarningStat: ...
    def __deepcopy__(self, arg0: dict) -> MjWarningStat: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjvCamera:
    __hash__: ClassVar[None] = ...
    azimuth: float
    distance: float
    elevation: float
    fixedcamid: int
    lookat: numpy.ndarray[numpy.float64]
    trackbodyid: int
    type: int
    def __init__(self) -> None: ...
    def __copy__(self) -> MjvCamera: ...
    def __deepcopy__(self, arg0: dict) -> MjvCamera: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjvFigure:
    figurergba: numpy.ndarray[numpy.float32]
    flg_barplot: int
    flg_extend: int
    flg_legend: int
    flg_selection: int
    flg_symmetric: int
    flg_ticklabel: numpy.ndarray[numpy.int32]
    gridrgb: numpy.ndarray[numpy.float32]
    gridsize: numpy.ndarray[numpy.int32]
    gridwidth: float
    highlightid: int
    legendoffset: int
    legendrgba: numpy.ndarray[numpy.float32]
    linedata: numpy.ndarray[numpy.float32]
    linepnt: numpy.ndarray[numpy.int32]
    linergb: numpy.ndarray[numpy.float32]
    linewidth: float
    minwidth: str
    panergba: numpy.ndarray[numpy.float32]
    range: numpy.ndarray[numpy.float32]
    selection: float
    subplot: int
    textrgb: numpy.ndarray[numpy.float32]
    title: str
    xaxisdata: numpy.ndarray[numpy.float32]
    xaxispixel: numpy.ndarray[numpy.int32]
    xformat: str
    xlabel: str
    yaxisdata: numpy.ndarray[numpy.float32]
    yaxispixel: numpy.ndarray[numpy.int32]
    yformat: str
    def __init__(self) -> None: ...
    def __copy__(self) -> MjvFigure: ...
    def __deepcopy__(self, arg0: dict) -> MjvFigure: ...
    @property
    def linename(self) -> numpy.ndarray: ...

class MjvGLCamera:
    __hash__: ClassVar[None] = ...
    forward: numpy.ndarray[numpy.float32]
    frustum_bottom: float
    frustum_center: float
    frustum_far: float
    frustum_near: float
    frustum_top: float
    pos: numpy.ndarray[numpy.float32]
    up: numpy.ndarray[numpy.float32]
    def __init__(self) -> None: ...
    def __copy__(self) -> MjvGLCamera: ...
    def __deepcopy__(self, arg0: dict) -> MjvGLCamera: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjvGeom:
    __hash__: ClassVar[None] = ...
    camdist: float
    category: int
    dataid: int
    emission: float
    label: str
    mat: numpy.ndarray[numpy.float32]
    modelrbound: float
    objid: int
    objtype: int
    pos: numpy.ndarray[numpy.float32]
    reflectance: float
    rgba: numpy.ndarray[numpy.float32]
    segid: int
    shininess: float
    size: numpy.ndarray[numpy.float32]
    specular: float
    texcoord: int
    texid: int
    texrepeat: numpy.ndarray[numpy.float32]
    texuniform: int
    transparent: int
    type: int
    def __init__(self) -> None: ...
    def __copy__(self) -> MjvGeom: ...
    def __deepcopy__(self, arg0: dict) -> MjvGeom: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjvLight:
    __hash__: ClassVar[None] = ...
    ambient: numpy.ndarray[numpy.float32]
    attenuation: numpy.ndarray[numpy.float32]
    castshadow: int
    cutoff: float
    diffuse: numpy.ndarray[numpy.float32]
    dir: numpy.ndarray[numpy.float32]
    directional: int
    exponent: float
    headlight: int
    pos: numpy.ndarray[numpy.float32]
    specular: numpy.ndarray[numpy.float32]
    def __init__(self) -> None: ...
    def __copy__(self) -> MjvLight: ...
    def __deepcopy__(self, arg0: dict) -> MjvLight: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjvOption:
    __hash__: ClassVar[None] = ...
    actuatorgroup: numpy.ndarray[numpy.uint8]
    flags: numpy.ndarray[numpy.uint8]
    frame: int
    geomgroup: numpy.ndarray[numpy.uint8]
    jointgroup: numpy.ndarray[numpy.uint8]
    label: int
    sitegroup: numpy.ndarray[numpy.uint8]
    skingroup: numpy.ndarray[numpy.uint8]
    tendongroup: numpy.ndarray[numpy.uint8]
    def __init__(self) -> None: ...
    def __copy__(self) -> MjvOption: ...
    def __deepcopy__(self, arg0: dict) -> MjvOption: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjvPerturb:
    __hash__: ClassVar[None] = ...
    active: int
    active2: int
    localpos: numpy.ndarray[numpy.float64]
    refpos: numpy.ndarray[numpy.float64]
    refquat: numpy.ndarray[numpy.float64]
    select: int
    skinselect: int
    def __init__(self) -> None: ...
    def __copy__(self) -> MjvPerturb: ...
    def __deepcopy__(self, arg0: dict) -> MjvPerturb: ...
    def __eq__(self, arg0: object) -> bool: ...

class MjvScene:
    enabletransform: int
    flags: numpy.ndarray[numpy.uint8]
    framergb: numpy.ndarray[numpy.float32]
    framewidth: int
    geomorder: numpy.ndarray[numpy.int32]
    maxgeom: int
    ngeom: int
    nlight: int
    rotate: numpy.ndarray[numpy.float32]
    scale: float
    skinfacenum: numpy.ndarray[numpy.int32]
    skinnormal: numpy.ndarray[numpy.float32]
    skinvert: numpy.ndarray[numpy.float32]
    skinvertadr: numpy.ndarray[numpy.int32]
    skinvertnum: numpy.ndarray[numpy.int32]
    stereo: int
    translate: numpy.ndarray[numpy.float32]
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, model: MjModel, maxgeom: int) -> None: ...
    def __copy__(self) -> MjvScene: ...
    def __deepcopy__(self, arg0: dict) -> MjvScene: ...
    @property
    def camera(self) -> tuple: ...
    @property
    def geoms(self) -> tuple: ...
    @property
    def lights(self) -> tuple: ...

class _MjContactList:
    __hash__: ClassVar[None] = ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __eq__(self, arg0: object) -> bool: ...
    @overload
    def __getitem__(self, arg0: int) -> MjContact: ...
    @overload
    def __getitem__(self, arg0: slice) -> _MjContactList: ...
    def __len__(self) -> int: ...
    @property
    def H(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def dim(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def dist(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def efc_address(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def exclude(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def frame(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def friction(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def geom1(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def geom2(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def includemargin(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def mu(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def pos(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def solimp(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def solref(self) -> numpy.ndarray[numpy.float64]: ...

class _MjDataActuatorViews:
    ctrl: numpy.ndarray[numpy.float64]
    force: numpy.ndarray[numpy.float64]
    length: numpy.ndarray[numpy.float64]
    moment: numpy.ndarray[numpy.float64]
    velocity: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjDataBodyViews:
    cacc: numpy.ndarray[numpy.float64]
    cfrc_ext: numpy.ndarray[numpy.float64]
    cfrc_int: numpy.ndarray[numpy.float64]
    cinert: numpy.ndarray[numpy.float64]
    crb: numpy.ndarray[numpy.float64]
    cvel: numpy.ndarray[numpy.float64]
    subtree_angmom: numpy.ndarray[numpy.float64]
    subtree_com: numpy.ndarray[numpy.float64]
    subtree_linvel: numpy.ndarray[numpy.float64]
    xfrc_applied: numpy.ndarray[numpy.float64]
    ximat: numpy.ndarray[numpy.float64]
    xipos: numpy.ndarray[numpy.float64]
    xmat: numpy.ndarray[numpy.float64]
    xpos: numpy.ndarray[numpy.float64]
    xquat: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjDataCameraViews:
    xmat: numpy.ndarray[numpy.float64]
    xpos: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjDataGeomViews:
    xmat: numpy.ndarray[numpy.float64]
    xpos: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjDataJointViews:
    cdof: numpy.ndarray[numpy.float64]
    cdof_dot: numpy.ndarray[numpy.float64]
    efc_JT: numpy.ndarray[numpy.float64]
    efc_JT_colind: numpy.ndarray[numpy.int32]
    efc_JT_rowadr: numpy.ndarray[numpy.int32]
    efc_JT_rownnz: numpy.ndarray[numpy.int32]
    efc_JT_rowsuper: numpy.ndarray[numpy.int32]
    qLDiagInv: numpy.ndarray[numpy.float64]
    qLDiagSqrtInv: numpy.ndarray[numpy.float64]
    qacc: numpy.ndarray[numpy.float64]
    qacc_smooth: numpy.ndarray[numpy.float64]
    qacc_warmstart: numpy.ndarray[numpy.float64]
    qfrc_actuator: numpy.ndarray[numpy.float64]
    qfrc_applied: numpy.ndarray[numpy.float64]
    qfrc_bias: numpy.ndarray[numpy.float64]
    qfrc_constraint: numpy.ndarray[numpy.float64]
    qfrc_inverse: numpy.ndarray[numpy.float64]
    qfrc_passive: numpy.ndarray[numpy.float64]
    qfrc_smooth: numpy.ndarray[numpy.float64]
    qpos: numpy.ndarray[numpy.float64]
    qvel: numpy.ndarray[numpy.float64]
    xanchor: numpy.ndarray[numpy.float64]
    xaxis: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjDataLightViews:
    xdir: numpy.ndarray[numpy.float64]
    xpos: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjDataSensorViews:
    data: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjDataSiteViews:
    xmat: numpy.ndarray[numpy.float64]
    xpos: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjDataTendonViews:
    J: numpy.ndarray[numpy.float64]
    J_colind: numpy.ndarray[numpy.int32]
    J_rowadr: numpy.ndarray[numpy.int32]
    J_rownnz: numpy.ndarray[numpy.int32]
    length: numpy.ndarray[numpy.float64]
    velocity: numpy.ndarray[numpy.float64]
    wrapadr: numpy.ndarray[numpy.int32]
    wrapnum: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelActuatorViews:
    acc0: numpy.ndarray[numpy.float64]
    actadr: numpy.ndarray[numpy.int32]
    actlimited: numpy.ndarray[numpy.uint8]
    actnum: numpy.ndarray[numpy.int32]
    actrange: numpy.ndarray[numpy.float64]
    biasprm: numpy.ndarray[numpy.float64]
    biastype: numpy.ndarray[numpy.int32]
    cranklength: numpy.ndarray[numpy.float64]
    ctrllimited: numpy.ndarray[numpy.uint8]
    ctrlrange: numpy.ndarray[numpy.float64]
    dynprm: numpy.ndarray[numpy.float64]
    dyntype: numpy.ndarray[numpy.int32]
    forcelimited: numpy.ndarray[numpy.uint8]
    forcerange: numpy.ndarray[numpy.float64]
    gainprm: numpy.ndarray[numpy.float64]
    gaintype: numpy.ndarray[numpy.int32]
    gear: numpy.ndarray[numpy.float64]
    group: numpy.ndarray[numpy.int32]
    length0: numpy.ndarray[numpy.float64]
    lengthrange: numpy.ndarray[numpy.float64]
    trnid: numpy.ndarray[numpy.int32]
    trntype: numpy.ndarray[numpy.int32]
    user: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelBodyViews:
    dofadr: numpy.ndarray[numpy.int32]
    dofnum: numpy.ndarray[numpy.int32]
    geomadr: numpy.ndarray[numpy.int32]
    geomnum: numpy.ndarray[numpy.int32]
    inertia: numpy.ndarray[numpy.float64]
    invweight0: numpy.ndarray[numpy.float64]
    ipos: numpy.ndarray[numpy.float64]
    iquat: numpy.ndarray[numpy.float64]
    jntadr: numpy.ndarray[numpy.int32]
    jntnum: numpy.ndarray[numpy.int32]
    mass: numpy.ndarray[numpy.float64]
    mocapid: numpy.ndarray[numpy.int32]
    parentid: numpy.ndarray[numpy.int32]
    pos: numpy.ndarray[numpy.float64]
    quat: numpy.ndarray[numpy.float64]
    rootid: numpy.ndarray[numpy.int32]
    sameframe: numpy.ndarray[numpy.uint8]
    simple: numpy.ndarray[numpy.uint8]
    subtreemass: numpy.ndarray[numpy.float64]
    user: numpy.ndarray[numpy.float64]
    weldid: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelCameraViews:
    bodyid: numpy.ndarray[numpy.int32]
    fovy: numpy.ndarray[numpy.float64]
    ipd: numpy.ndarray[numpy.float64]
    mat0: numpy.ndarray[numpy.float64]
    mode: numpy.ndarray[numpy.int32]
    pos: numpy.ndarray[numpy.float64]
    pos0: numpy.ndarray[numpy.float64]
    poscom0: numpy.ndarray[numpy.float64]
    quat: numpy.ndarray[numpy.float64]
    targetbodyid: numpy.ndarray[numpy.int32]
    user: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelEqualityViews:
    active: numpy.ndarray[numpy.uint8]
    data: numpy.ndarray[numpy.float64]
    obj1id: numpy.ndarray[numpy.int32]
    obj2id: numpy.ndarray[numpy.int32]
    solimp: numpy.ndarray[numpy.float64]
    solref: numpy.ndarray[numpy.float64]
    type: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelExcludeViews:
    signature: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelGeomViews:
    bodyid: numpy.ndarray[numpy.int32]
    conaffinity: numpy.ndarray[numpy.int32]
    condim: numpy.ndarray[numpy.int32]
    contype: numpy.ndarray[numpy.int32]
    dataid: numpy.ndarray[numpy.int32]
    friction: numpy.ndarray[numpy.float64]
    gap: numpy.ndarray[numpy.float64]
    group: numpy.ndarray[numpy.int32]
    margin: numpy.ndarray[numpy.float64]
    matid: numpy.ndarray[numpy.int32]
    pos: numpy.ndarray[numpy.float64]
    priority: numpy.ndarray[numpy.int32]
    quat: numpy.ndarray[numpy.float64]
    rbound: numpy.ndarray[numpy.float64]
    rgba: numpy.ndarray[numpy.float32]
    sameframe: numpy.ndarray[numpy.uint8]
    size: numpy.ndarray[numpy.float64]
    solimp: numpy.ndarray[numpy.float64]
    solmix: numpy.ndarray[numpy.float64]
    solref: numpy.ndarray[numpy.float64]
    type: numpy.ndarray[numpy.int32]
    user: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelHfieldViews:
    adr: numpy.ndarray[numpy.int32]
    data: numpy.ndarray[numpy.float32]
    ncol: numpy.ndarray[numpy.int32]
    nrow: numpy.ndarray[numpy.int32]
    size: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelJointViews:
    M0: numpy.ndarray[numpy.float64]
    Madr: numpy.ndarray[numpy.int32]
    armature: numpy.ndarray[numpy.float64]
    axis: numpy.ndarray[numpy.float64]
    bodyid: numpy.ndarray[numpy.int32]
    damping: numpy.ndarray[numpy.float64]
    dofadr: numpy.ndarray[numpy.int32]
    frictionloss: numpy.ndarray[numpy.float64]
    group: numpy.ndarray[numpy.int32]
    invweight0: numpy.ndarray[numpy.float64]
    jntid: numpy.ndarray[numpy.int32]
    limited: numpy.ndarray[numpy.uint8]
    margin: numpy.ndarray[numpy.float64]
    parentid: numpy.ndarray[numpy.int32]
    pos: numpy.ndarray[numpy.float64]
    qpos0: numpy.ndarray[numpy.float64]
    qpos_spring: numpy.ndarray[numpy.float64]
    qposadr: numpy.ndarray[numpy.int32]
    range: numpy.ndarray[numpy.float64]
    simplenum: numpy.ndarray[numpy.int32]
    solimp: numpy.ndarray[numpy.float64]
    solref: numpy.ndarray[numpy.float64]
    stiffness: numpy.ndarray[numpy.float64]
    type: numpy.ndarray[numpy.int32]
    user: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelKeyframeViews:
    act: numpy.ndarray[numpy.float64]
    mpos: numpy.ndarray[numpy.float64]
    mquat: numpy.ndarray[numpy.float64]
    qpos: numpy.ndarray[numpy.float64]
    qvel: numpy.ndarray[numpy.float64]
    time: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelLightViews:
    active: numpy.ndarray[numpy.uint8]
    ambient: numpy.ndarray[numpy.float32]
    attenuation: numpy.ndarray[numpy.float32]
    bodyid: numpy.ndarray[numpy.int32]
    castshadow: numpy.ndarray[numpy.uint8]
    cutoff: numpy.ndarray[numpy.float32]
    diffuse: numpy.ndarray[numpy.float32]
    dir: numpy.ndarray[numpy.float64]
    dir0: numpy.ndarray[numpy.float64]
    directional: numpy.ndarray[numpy.uint8]
    exponent: numpy.ndarray[numpy.float32]
    mode: numpy.ndarray[numpy.int32]
    pos: numpy.ndarray[numpy.float64]
    pos0: numpy.ndarray[numpy.float64]
    poscom0: numpy.ndarray[numpy.float64]
    specular: numpy.ndarray[numpy.float32]
    targetbodyid: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelMaterialViews:
    emission: numpy.ndarray[numpy.float32]
    reflectance: numpy.ndarray[numpy.float32]
    rgba: numpy.ndarray[numpy.float32]
    shininess: numpy.ndarray[numpy.float32]
    specular: numpy.ndarray[numpy.float32]
    texid: numpy.ndarray[numpy.int32]
    texrepeat: numpy.ndarray[numpy.float32]
    texuniform: numpy.ndarray[numpy.uint8]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelMeshViews:
    faceadr: numpy.ndarray[numpy.int32]
    facenum: numpy.ndarray[numpy.int32]
    graphadr: numpy.ndarray[numpy.int32]
    texcoordadr: numpy.ndarray[numpy.int32]
    vertadr: numpy.ndarray[numpy.int32]
    vertnum: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelNumericViews:
    adr: numpy.ndarray[numpy.int32]
    data: numpy.ndarray[numpy.float64]
    size: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelPairViews:
    dim: numpy.ndarray[numpy.int32]
    friction: numpy.ndarray[numpy.float64]
    gap: numpy.ndarray[numpy.float64]
    geom1: numpy.ndarray[numpy.int32]
    geom2: numpy.ndarray[numpy.int32]
    margin: numpy.ndarray[numpy.float64]
    signature: numpy.ndarray[numpy.int32]
    solimp: numpy.ndarray[numpy.float64]
    solref: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelSensorViews:
    adr: numpy.ndarray[numpy.int32]
    cutoff: numpy.ndarray[numpy.float64]
    datatype: numpy.ndarray[numpy.int32]
    dim: numpy.ndarray[numpy.int32]
    needstage: numpy.ndarray[numpy.int32]
    noise: numpy.ndarray[numpy.float64]
    objid: numpy.ndarray[numpy.int32]
    objtype: numpy.ndarray[numpy.int32]
    refid: numpy.ndarray[numpy.int32]
    reftype: numpy.ndarray[numpy.int32]
    type: numpy.ndarray[numpy.int32]
    user: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelSiteViews:
    bodyid: numpy.ndarray[numpy.int32]
    group: numpy.ndarray[numpy.int32]
    matid: numpy.ndarray[numpy.int32]
    pos: numpy.ndarray[numpy.float64]
    quat: numpy.ndarray[numpy.float64]
    rgba: numpy.ndarray[numpy.float32]
    sameframe: numpy.ndarray[numpy.uint8]
    size: numpy.ndarray[numpy.float64]
    type: numpy.ndarray[numpy.int32]
    user: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelSkinViews:
    boneadr: numpy.ndarray[numpy.int32]
    bonenum: numpy.ndarray[numpy.int32]
    faceadr: numpy.ndarray[numpy.int32]
    facenum: numpy.ndarray[numpy.int32]
    inflate: numpy.ndarray[numpy.float32]
    matid: numpy.ndarray[numpy.int32]
    rgba: numpy.ndarray[numpy.float32]
    texcoordadr: numpy.ndarray[numpy.int32]
    vertadr: numpy.ndarray[numpy.int32]
    vertnum: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelTendonViews:
    _adr: numpy.ndarray[numpy.int32]
    _damping: numpy.ndarray[numpy.float64]
    _frictionloss: numpy.ndarray[numpy.float64]
    _group: numpy.ndarray[numpy.int32]
    _invweight0: numpy.ndarray[numpy.float64]
    _length0: numpy.ndarray[numpy.float64]
    _lengthspring: numpy.ndarray[numpy.float64]
    _limited: numpy.ndarray[numpy.uint8]
    _margin: numpy.ndarray[numpy.float64]
    _matid: numpy.ndarray[numpy.int32]
    _num: numpy.ndarray[numpy.int32]
    _range: numpy.ndarray[numpy.float64]
    _rgba: numpy.ndarray[numpy.float32]
    _solimp_fri: numpy.ndarray[numpy.float64]
    _solimp_lim: numpy.ndarray[numpy.float64]
    _solref_fri: numpy.ndarray[numpy.float64]
    _solref_lim: numpy.ndarray[numpy.float64]
    _stiffness: numpy.ndarray[numpy.float64]
    _user: numpy.ndarray[numpy.float64]
    _width: numpy.ndarray[numpy.float64]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelTextureViews:
    adr: numpy.ndarray[numpy.int32]
    height: numpy.ndarray[numpy.int32]
    rgb: numpy.ndarray[numpy.uint8]
    type: numpy.ndarray[numpy.int32]
    width: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjModelTupleViews:
    adr: numpy.ndarray[numpy.int32]
    objid: numpy.ndarray[numpy.int32]
    objprm: numpy.ndarray[numpy.float64]
    objtype: numpy.ndarray[numpy.int32]
    size: numpy.ndarray[numpy.int32]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...

class _MjSolverStatList:
    __hash__: ClassVar[None] = ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __eq__(self, arg0: object) -> bool: ...
    @overload
    def __getitem__(self, arg0: int) -> MjSolverStat: ...
    @overload
    def __getitem__(self, arg0: slice) -> _MjSolverStatList: ...
    def __len__(self) -> int: ...
    @property
    def gradient(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def improvement(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def lineslope(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def nactive(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def nchange(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def neval(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def nupdate(self) -> numpy.ndarray[numpy.int32]: ...

class _MjTimerStatList:
    __hash__: ClassVar[None] = ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __eq__(self, arg0: object) -> bool: ...
    @overload
    def __getitem__(self, arg0: int) -> MjTimerStat: ...
    @overload
    def __getitem__(self, arg0: mujoco._enums.mjtTimer) -> MjTimerStat: ...
    @overload
    def __getitem__(self, arg0: slice) -> _MjTimerStatList: ...
    def __len__(self) -> int: ...
    @property
    def duration(self) -> numpy.ndarray[numpy.float64]: ...
    @property
    def number(self) -> numpy.ndarray[numpy.int32]: ...

class _MjWarningStatList:
    __hash__: ClassVar[None] = ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __eq__(self, arg0: object) -> bool: ...
    @overload
    def __getitem__(self, arg0: int) -> MjWarningStat: ...
    @overload
    def __getitem__(self, arg0: mujoco._enums.mjtWarning) -> MjWarningStat: ...
    @overload
    def __getitem__(self, arg0: slice) -> _MjWarningStatList: ...
    def __len__(self) -> int: ...
    @property
    def lastinfo(self) -> numpy.ndarray[numpy.int32]: ...
    @property
    def number(self) -> numpy.ndarray[numpy.int32]: ...

def mjv_averageCamera(cam1: MjvGLCamera, cam2: MjvGLCamera) -> MjvGLCamera: ...
