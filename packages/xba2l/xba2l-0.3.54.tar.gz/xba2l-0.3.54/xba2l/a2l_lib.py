# -*- encoding: utf-8 -*-
import dataclasses
import typing as t
from dataclasses import dataclass

__all__ = [
    "Asap2",
    "Module",
]


@dataclass(slots=True)
class A2mlVersion:
    version_no: int
    upgrade_no: int


@dataclass(slots=True)
class Asap2Version:
    version_no: int
    upgrade_no: int


@dataclass(slots=True)
class IfData:
    pass


@dataclass(slots=True)
class LayoutElement:
    key: str
    position: int
    # optional
    addr_type: str | None = None
    data_size: str | None = None
    data_type: str | None = None
    index_mode: str | None = None
    index_order: str | None = None
    max_number_of_rescale_pairs: int | None = None


@dataclass(slots=True)
class ExtendedLimits:
    lower_limit: float
    upper_limit: float


@dataclass(slots=True)
class Limits:
    lower_limit: float
    upper_limit: float


@dataclass(slots=True)
class FixAxisPar:
    offset: float
    shift: float
    numberapo: int


@dataclass(slots=True)
class FixAxisParDist:
    offset: float
    distance: float
    numberapo: int


@dataclass(slots=True)
class InMeasurement:
    identifiers: list[str]


@dataclass(slots=True)
class OutMeasurement:
    identifiers: list[str]


@dataclass(slots=True)
class FrameMeasurement:
    identifiers: list[str]


@dataclass(slots=True)
class LocMeasurement:
    identifiers: list[str]


@dataclass(slots=True)
class RefGroup:
    identifiers: list[str]


@dataclass(slots=True)
class RefMeasurement:
    identifiers: list[str]


@dataclass(slots=True)
class MaxRefresh:
    scaling_unit: int
    rate: int


@dataclass(slots=True)
class MemoryLayout:
    prg_type: str
    address: int
    size: int
    offset: tuple[int, int, int, int, int]
    # optional
    # IF_DATA


@dataclass(slots=True)
class SiExponents:
    length: int
    mass: int
    time: int
    electric_current: int
    temperature: int
    amount_of_substance: int
    luminous_intensity: int


@dataclass(slots=True)
class SymbolLink:
    symbol_name: str
    offset: int


@dataclass(slots=True)
class SystemConstant:
    name: str
    value: str


@dataclass(slots=True)
class UnitConversion:
    gradient: float
    offset: float


@dataclass(slots=True)
class UserRights:
    user_level_id: str
    # optional
    read_only: bool | None = None
    ref_groups: t.Annotated[list[RefGroup] | None, dict(many=True)] = None


@dataclass(slots=True)
class VarAddress:
    addresses: list[int]


@dataclass(slots=True)
class VarCharacteristic:
    name: str
    criterion_names: list[str]
    # optional
    var_address: VarAddress | None = None


@dataclass(slots=True)
class VarCriterion:
    name: str
    long_identifier: str
    values: list[str]
    # optional
    var_measurement: str | None = None
    var_selection_characteristic: str | None = None


@dataclass(slots=True)
class VarForbiddenComb:
    criterion_name: str
    criterion_values: list[str]


@dataclass(slots=True)
class VariantCoding:
    # optional
    var_characteristics: t.Annotated[list[VarCharacteristic] | None, dict(many=True)] = None
    var_criterions: t.Annotated[list[VarCriterion] | None, dict(many=True)] = None
    var_forbidden_combs: t.Annotated[list[VarForbiddenComb] | None, dict(many=True)] = None
    var_naming: str | None = None
    var_separator: str | None = None


@dataclass(slots=True)
class AnnotationText:
    texts: list[str]


@dataclass(slots=True)
class Annotation:
    # optional
    annotation_label: str | None = None
    annotation_origin: str | None = None
    annotation_text: AnnotationText | None = None


@dataclass(slots=True)
class Overwrite:
    name: str
    axis_number: int
    # optional
    conversion: str | None = None
    extended_limits: ExtendedLimits | None = None
    format: str | None = None
    input_quantity: str | None = None
    limits: Limits | None = None
    monotony: str | None = None
    phys_unit: str | None = None


@dataclass(slots=True)
class Instance:
    name: str
    long_identifier: str
    typedef_name: str
    address: int
    # optional
    address_type: str | None = None
    annotations: t.Annotated[list[Annotation] | None, dict(many=True)] = None
    calibration_access: str | None = None
    display_identifier: str | None = None
    ecu_address_extension: int | None = None
    if_datas: t.Annotated[list[IfData] | None, dict(many=True)] = None
    layout: str | None = None
    matrix_dim: list[int] | None = None
    max_refresh: MaxRefresh | None = None
    model_link: str | None = None
    overwrites: t.Annotated[list[Overwrite] | None, dict(many=True)] = None
    read_write: bool | None = None
    symbol_link: SymbolLink | None = None
    # enhenced
    configurable: bool | None = None
    function_name: str | None = None
    function_version: str | None = None


@dataclass(slots=True)
class TypedefAxis:
    name: str
    long_identifier: str
    input_quantity: str
    record_layout: str
    max_diff: float
    conversion: str
    max_axis_points: int
    lower_limit: float
    upper_limit: float
    # optional
    byte_order: str | None = None
    deposit: str | None = None
    extended_limits: ExtendedLimits | None = None
    format: str | None = None
    monotony: str | None = None
    phys_unit: str | None = None
    step_size: float | None = None


@dataclass(slots=True)
class Formula:
    expression: str
    # optional
    formula_inv: str | None = None


@dataclass(slots=True)
class CompuMethod:
    name: str
    long_identifier: str
    conversion_type: str
    format: str
    unit: str
    # optional
    coeffs: tuple[float, float, float, float, float, float] | None = None
    coeffs_linear: tuple[float, float] | None = None
    compu_tab_ref: str | None = None
    formula: Formula | None = None
    ref_unit: str | None = None
    status_string_ref: str | None = None


@dataclass(slots=True)
class FunctionList:
    identifiers: list[str]


@dataclass(slots=True)
class AxisPts:
    name: str
    long_identifier: str
    address: int
    input_quantity: str
    record_layout: str
    max_diff: float
    conversion: str
    max_axis_points: int
    lower_limit: float
    upper_limit: float
    # optional
    annotations: t.Annotated[list[Annotation] | None, dict(many=True)] = None
    byte_order: str | None = None
    calibration_access: str | None = None
    deposit: str | None = None
    display_identifier: str | None = None
    ecu_address_extension: int | None = None
    extended_limits: ExtendedLimits | None = None
    format: str | None = None
    function_list: FunctionList | None = None
    guard_rails: bool | None = None
    if_datas: t.Annotated[list[IfData] | None, dict(many=True)] = None
    max_refresh: MaxRefresh | None = None
    model_link: str | None = None
    monotony: str | None = None
    phys_unit: str | None = None
    read_only: bool | None = None
    ref_memory_segment: str | None = None
    step_size: float | None = None
    symbol_link: SymbolLink | None = None
    # enhenced
    data_type: str | None = None
    format_string: str | None = None
    textual: bool | None = None
    unit_name: str | None = None

    configurable: bool | None = None
    function_name: str | None = None
    function_version: str | None = None
    extended_type: str | None = None


@dataclass(slots=True)
class FixAxisParList:
    axis_pts_values: list[float]


@dataclass(slots=True)
class AxisDescr:
    attribute: str
    input_quantity: str
    conversion: str
    max_axis_points: int
    lower_limit: float
    upper_limit: float
    # optional
    annotations: t.Annotated[list[Annotation] | None, dict(many=True)] = None
    axis_pts_ref: str | None = None
    byte_order: str | None = None
    curve_axis_ref: str | None = None
    deposit: str | None = None
    extended_limits: ExtendedLimits | None = None
    fix_axis_par: FixAxisPar | None = None
    fix_axis_par_dist: FixAxisParDist | None = None
    fix_axis_par_list: FixAxisParList | None = None
    format: str | None = None
    max_grad: float | None = None
    monotony: str | None = None
    phys_unit: str | None = None
    read_only: bool | None = None
    step_size: float | None = None
    # enhenced
    data_type: str | None = None
    format_string: str | None = None
    textual: bool | None = None
    unit_name: str | None = None


@dataclass(slots=True)
class TypedefCharacteristic:
    name: str
    long_identifier: str
    type: str
    record_layout: str
    max_diff: float
    conversion: str
    lower_limit: float
    upper_limit: float
    # optional
    axis_descrs: t.Annotated[list[AxisDescr] | None, dict(many=True)] = None
    bit_mask: int | None = None
    byte_order: str | None = None
    discrete: bool | None = None
    extended_limits: ExtendedLimits | None = None
    format: str | None = None
    matrix_dim: list[int] | None = None
    number: int | None = None
    phys_unit: str | None = None
    step_size: float | None = None


@dataclass(slots=True)
class VirtualCharacteristic:
    formula: str
    identifiers: list[str]


@dataclass(slots=True)
class MapList:
    identifiers: list[str]


@dataclass(slots=True)
class DependentCharacteristic:
    formula: str
    identifiers: list[str]


@dataclass(slots=True)
class Characteristic:
    name: str
    long_identifier: str
    type: str
    address: int
    record_layout: str
    max_diff: float
    conversion: str
    lower_limit: float
    upper_limit: float
    # optional
    annotations: t.Annotated[list[Annotation] | None, dict(many=True)] = None
    axis_descrs: t.Annotated[list[AxisDescr] | None, dict(many=True)] = None
    bit_mask: int | None = None
    byte_order: str | None = None
    calibration_access: str | None = None
    comparison_quantity: str | None = None
    dependent_characteristic: DependentCharacteristic | None = None
    discrete: bool | None = None
    display_identifier: str | None = None
    ecu_address_extension: int | None = None
    encoding: str | None = None
    extended_limits: ExtendedLimits | None = None
    format: str | None = None
    function_list: FunctionList | None = None
    guard_rails: bool | None = None
    if_datas: t.Annotated[list[IfData] | None, dict(many=True)] = None
    map_list: MapList | None = None
    matrix_dim: list[int] | None = None
    max_refresh: MaxRefresh | None = None
    model_link: str | None = None
    number: int | None = None
    phys_unit: str | None = None
    read_only: bool | None = None
    ref_memory_segment: str | None = None
    step_size: float | None = None
    symbol_link: SymbolLink | None = None
    virtual_characteristic: VirtualCharacteristic | None = None
    # enhenced
    data_type: str | None = None
    format_string: str | None = None
    textual: bool | None = None
    unit_name: str | None = None

    configurable: bool | None = None
    function_name: str | None = None
    function_version: str | None = None
    extended_type: str | None = None


@dataclass(slots=True)
class CompuTab:
    name: str
    long_identifier: str
    conversion_type: str
    number_value_pairs: int
    pair_values: t.Annotated[list[tuple[float, float]], dict(size_key="number_value_pairs")]
    # optional
    default_value: str | None = None
    default_value_numeric: float | None = None


@dataclass(slots=True)
class CompuVtab:
    name: str
    long_identifier: str
    conversion_type: str
    number_value_pairs: int
    pair_values: t.Annotated[list[tuple[int, str]], dict(size_key="number_value_pairs")]
    # optional
    default_value: str | None = None
    # enhenced
    read_dict: dict[int, str] = dataclasses.field(default_factory=dict)
    write_dict: dict[str, int] = dataclasses.field(default_factory=dict)


@dataclass(slots=True)
class CompuVtabRange:
    name: str
    long_identifier: str
    number_value_triples: int
    triple_values: t.Annotated[list[tuple[float, float, str]], dict(size_key="number_value_triples")]
    # optional
    default_value: str | None = None
    # enhenced
    write_dict: dict[str, tuple[float, float]] = dataclasses.field(default_factory=dict)


@dataclass(slots=True)
class Frame:
    name: str
    long_identifier: str
    scaling_unit: int
    rate: int
    # optional
    frame_measurement: FrameMeasurement | None = None
    if_datas: t.Annotated[list[IfData] | None, dict(many=True)] = None


@dataclass(slots=True)
class RefCharacteristic:
    identifiers: list[str]


@dataclass(slots=True)
class DefCharacteristic:
    identifiers: list[str]


@dataclass(slots=True)
class SubFunction:
    identifiers: list[str]


@dataclass(slots=True)
class Function:
    name: str
    long_identifier: str
    # optional
    annotations: t.Annotated[list[Annotation] | None, dict(many=True)] = None
    def_characteristic: DefCharacteristic | None = None
    function_version: str | None = None
    if_datas: t.Annotated[list[IfData] | None, dict(many=True)] = None
    in_measurement: InMeasurement | None = None
    loc_measurement: LocMeasurement | None = None
    out_measurement: OutMeasurement | None = None
    ref_characteristic: RefCharacteristic | None = None
    sub_function: SubFunction | None = None


@dataclass(slots=True)
class SubGroup:
    identifiers: list[str]


@dataclass(slots=True)
class Group:
    name: str
    long_identifier: str
    # optional
    annotations: t.Annotated[list[Annotation] | None, dict(many=True)] = None
    function_list: FunctionList | None = None
    if_datas: t.Annotated[list[IfData] | None, dict(many=True)] = None
    ref_characteristic: RefCharacteristic | None = None
    ref_measurement: RefMeasurement | None = None
    root: bool | None = None
    sub_group: SubGroup | None = None


@dataclass(slots=True)
class ModCommon:
    comment: str
    # optional
    alignment_byte: int | None = None
    alignment_float16_ieee: int | None = None
    alignment_float32_ieee: int | None = None
    alignment_float64_ieee: int | None = None
    alignment_int64: int | None = None
    alignment_long: int | None = None
    alignment_word: int | None = None
    byte_order: str | None = None
    data_size: int | None = None
    deposit: str | None = None
    s_rec_layout: str | None = None


@dataclass(slots=True)
class MemorySegment:
    name: str
    long_identifier: str
    prg_type: str
    memory_type: str
    attribute: str
    address: int
    size: int
    offset: tuple[int, int, int, int, int]


@dataclass(slots=True)
class CalibrationHandler:
    handles: list[int]
    # optional
    calibration_handle_text: str | None = None


@dataclass(slots=True)
class CalibrationMethod:
    method: str
    version: int
    # optional
    calibration_handle: t.Annotated[list[CalibrationHandler] | None, dict(many=True)] = None


@dataclass(slots=True)
class RecordElement:
    position: int


@dataclass(slots=True)
class AxisPtsXYZ45(RecordElement):
    data_type: str
    index_incr: str
    addressing: str


@dataclass(slots=True)
class AxisRescaleX(RecordElement):
    data_type: str
    max_number_of_rescale_pairs: int
    index_incr: str
    addressing: str


@dataclass(slots=True)
class DistOpXYZ45(RecordElement):
    data_type: str


@dataclass(slots=True)
class FncValues(RecordElement):
    data_type: str
    index_mode: str
    address_type: str


@dataclass(slots=True)
class Identification(RecordElement):
    data_type: str


@dataclass(slots=True)
class NoAxisPtsXYZ45(RecordElement):
    data_type: str


@dataclass(slots=True)
class NoRescaleX(RecordElement):
    data_type: str


@dataclass(slots=True)
class OffsetXYZ45(RecordElement):
    data_type: str


@dataclass(slots=True)
class Reserved(RecordElement):
    data_size: str


@dataclass(slots=True)
class RipAddrWXYZ45(RecordElement):
    data_type: str


@dataclass(slots=True)
class SrcAddrXYZ45(RecordElement):
    data_type: str


@dataclass(slots=True)
class ShiftOpXYZ45(RecordElement):
    data_type: str


@dataclass(slots=True)
class RecordLayout:
    name: str
    # optional
    alignment_byte: int | None = None
    alignment_float16_ieee: int | None = None
    alignment_float32_ieee: int | None = None
    alignment_float64_ieee: int | None = None
    alignment_int64: int | None = None
    alignment_long: int | None = None
    alignment_word: int | None = None

    axis_pts_x: AxisPtsXYZ45 | None = None
    axis_pts_y: AxisPtsXYZ45 | None = None
    axis_pts_z: AxisPtsXYZ45 | None = None
    axis_pts_4: AxisPtsXYZ45 | None = None
    axis_pts_5: AxisPtsXYZ45 | None = None

    axis_rescale_x: AxisRescaleX | None = None

    dist_op_x: DistOpXYZ45 | None = None
    dist_op_y: DistOpXYZ45 | None = None
    dist_op_z: DistOpXYZ45 | None = None
    dist_op_4: DistOpXYZ45 | None = None
    dist_op_5: DistOpXYZ45 | None = None

    fix_no_axis_pts_x: int | None = None
    fix_no_axis_pts_y: int | None = None
    fix_no_axis_pts_z: int | None = None
    fix_no_axis_pts_4: int | None = None
    fix_no_axis_pts_5: int | None = None

    fnc_values: FncValues | None = None

    identification: Identification | None = None

    no_axis_pts_x: NoAxisPtsXYZ45 | None = None
    no_axis_pts_y: NoAxisPtsXYZ45 | None = None
    no_axis_pts_z: NoAxisPtsXYZ45 | None = None
    no_axis_pts_4: NoAxisPtsXYZ45 | None = None
    no_axis_pts_5: NoAxisPtsXYZ45 | None = None

    no_rescale_x: NoRescaleX | None = None

    offset_x: OffsetXYZ45 | None = None
    offset_y: OffsetXYZ45 | None = None
    offset_z: OffsetXYZ45 | None = None
    offset_4: OffsetXYZ45 | None = None
    offset_5: OffsetXYZ45 | None = None

    reserveds: t.Annotated[list[Reserved] | None, dict(many=True)] = None

    rip_addr_w: RipAddrWXYZ45 | None = None
    rip_addr_x: RipAddrWXYZ45 | None = None
    rip_addr_y: RipAddrWXYZ45 | None = None
    rip_addr_z: RipAddrWXYZ45 | None = None
    rip_addr_4: RipAddrWXYZ45 | None = None
    rip_addr_5: RipAddrWXYZ45 | None = None

    src_addr_x: SrcAddrXYZ45 | None = None
    src_addr_y: SrcAddrXYZ45 | None = None
    src_addr_z: SrcAddrXYZ45 | None = None
    src_addr_4: SrcAddrXYZ45 | None = None
    src_addr_5: SrcAddrXYZ45 | None = None

    shift_op_x: ShiftOpXYZ45 | None = None
    shift_op_y: ShiftOpXYZ45 | None = None
    shift_op_z: ShiftOpXYZ45 | None = None
    shift_op_4: ShiftOpXYZ45 | None = None
    shift_op_5: ShiftOpXYZ45 | None = None

    static_address_offsets: bool | None = None
    static_record_layout: bool | None = None
    # enhenced

    elements: list[tuple[str, RecordElement]] = dataclasses.field(default_factory=list)


@dataclass(slots=True)
class Unit:
    name: str
    long_identifier: str
    display: str
    type: str
    # optional
    ref_unit: str | None = None
    si_exponents: SiExponents | None = None
    unit_conversion: UnitConversion | None = None


@dataclass(slots=True)
class BitOperation:
    # optional
    left_shift: int | None = None
    right_shift: int | None = None
    sign_extend: bool | None = None


@dataclass(slots=True)
class Virtual:
    measuring_channels: list[str]


@dataclass(slots=True)
class Measurement:
    name: str
    long_identifier: str
    data_type: str
    conversion: str
    resolution: int
    accuracy: float
    lower_limit: float
    upper_limit: float
    # optional
    address_type: str | None = None
    annotations: t.Annotated[list[Annotation] | None, dict(many=True)] = None
    array_size: int | None = None
    bit_mask: int | None = None
    bit_operation: BitOperation | None = None
    byte_order: str | None = None
    discrete: bool | None = None
    display_identifier: str | None = None
    ecu_address: int | None = None
    ecu_address_extension: int | None = None
    error_mask: int | None = None
    format: str | None = None
    function_list: FunctionList | None = None
    if_datas: t.Annotated[list[IfData] | None, dict(many=True)] = None
    layout: str | None = None
    matrix_dim: list[int] | None = None
    max_refresh: MaxRefresh | None = None
    model_link: str | None = None
    phys_unit: str | None = None
    read_write: bool | None = None
    ref_memory_segment: str | None = None
    symbol_link: SymbolLink | None = None
    virtual: Virtual | None = None


@dataclass(slots=True)
class TypedefBlob:
    name: str
    long_identifier: str
    size: int
    # optional
    address_type: str | None = None


@dataclass(slots=True)
class Blob:
    name: str
    long_identifier: str
    address: int
    size: int
    # optional
    address_type: str | None = None
    annotations: t.Annotated[list[Annotation] | None, dict(many=True)] = None
    calibration_access: str | None = None
    display_identifier: str | None = None
    ecu_address_extension: int | None = None
    if_datas: t.Annotated[list[IfData] | None, dict(many=True)] = None
    max_refresh: MaxRefresh | None = None
    model_link: str | None = None
    symbol_link: SymbolLink | None = None
    # enhenced
    configurable: bool | None = None
    function_name: str | None = None
    function_version: str | None = None
    extended_type: str | None = None


@dataclass(slots=True)
class TypedefMeasurement:
    name: str
    long_identifier: str
    data_type: str
    conversion: str
    resolution: int
    accuracy: float
    lower_limit: float
    upper_limit: float
    # optional
    address_type: str | None = None
    bit_mask: int | None = None
    bit_operation: BitOperation | None = None
    byte_order: str | None = None
    discrete: bool | None = None
    error_mask: int | None = None
    format: str | None = None
    layout: str | None = None
    matrix_dim: list[int] | None = None
    phys_unit: str | None = None


@dataclass(slots=True)
class StructureComponent:
    name: str
    typedef_name: str
    address_offset: int
    # optional
    layout: str | None = None
    matrix_dim: list[int] | None = None


@dataclass(slots=True)
class TypedefStructure:
    name: str
    long_identifier: str
    size: int
    # optional
    address_type: str | None = None
    consistent_exchange: bool | None = None
    structure_components: t.Annotated[list[StructureComponent], dict(many=True)] = None


@dataclass(slots=True)
class TransformerInObjects:
    names: list[str]


@dataclass(slots=True)
class TransformerOutObjects:
    names: list[str]


@dataclass(slots=True)
class Transformer:
    name: str
    version: str
    executable_32: str
    executable_64: str
    timeout: int
    trigger: str
    inverse_transformer: str
    # optional
    transformer_in_objects: TransformerInObjects | None = None
    transformer_out_objects: TransformerOutObjects | None = None


@dataclass(slots=True)
class ModPar:
    comment: str
    # optional
    addr_epks: t.Annotated[list[int], dict(many=True)] = dataclasses.field(default_factory=list)
    calibration_methods: t.Annotated[list[CalibrationMethod], dict(many=True)] = dataclasses.field(default_factory=list)
    cpu_type: str | None = None
    customer: str | None = None
    customer_no: str | None = None
    ecu: str | None = None
    ecu_calibration_offset: int | None = None
    epk: str | None = None
    memory_layouts: t.Annotated[list[MemoryLayout], dict(many=True)] = dataclasses.field(default_factory=list)
    memory_segments: t.Annotated[list[MemorySegment], dict(many=True)] = dataclasses.field(default_factory=list)
    no_of_interfaces: int | None = None
    phone_no: str | None = None
    supplier: str | None = None
    system_constants: t.Annotated[list[SystemConstant], dict(many=True)] = dataclasses.field(default_factory=list)
    user: str | None = None
    version: str | None = None
    # enhenced
    system_constant_dict: dict[str, str] = dataclasses.field(default_factory=dict)


@dataclass()
class Module:
    name: str
    long_identifier: str
    # optional
    # [A2ML]
    axis_ptses: t.Annotated[list[AxisPts], dict(many=True)] = dataclasses.field(default_factory=list)
    blobs: t.Annotated[list[Blob], dict(many=True)] = dataclasses.field(default_factory=list)
    characteristics: t.Annotated[list[Characteristic], dict(many=True)] = dataclasses.field(default_factory=list)
    compu_methods: t.Annotated[list[CompuMethod], dict(many=True)] = dataclasses.field(default_factory=list)
    compu_tabs: t.Annotated[list[CompuTab], dict(many=True)] = dataclasses.field(default_factory=list)
    compu_vtabs: t.Annotated[list[CompuVtab], dict(many=True)] = dataclasses.field(default_factory=list)
    compu_vtab_ranges: t.Annotated[list[CompuVtabRange], dict(many=True)] = dataclasses.field(default_factory=list)
    frames: t.Annotated[list[Frame], dict(many=True)] = dataclasses.field(default_factory=list)
    functions: t.Annotated[list[Function], dict(many=True)] = dataclasses.field(default_factory=list)
    groups: t.Annotated[list[Group], dict(many=True)] = dataclasses.field(default_factory=list)
    if_datas: t.Annotated[list[IfData], dict(many=True)] = dataclasses.field(default_factory=list)
    instances: t.Annotated[list[Instance], dict(many=True)] = dataclasses.field(default_factory=list)
    measurements: t.Annotated[list[Measurement], dict(many=True)] = dataclasses.field(default_factory=list)
    mod_common: ModCommon | None = None
    mod_par: ModPar | None = None
    record_layouts: t.Annotated[list[RecordLayout], dict(many=True)] = dataclasses.field(default_factory=list)
    transformers: t.Annotated[list[Transformer], dict(many=True)] = dataclasses.field(default_factory=list)
    typedef_axises: t.Annotated[list[TypedefAxis], dict(many=True)] = dataclasses.field(default_factory=list)
    typedef_blobs: t.Annotated[list[TypedefBlob], dict(many=True)] = dataclasses.field(default_factory=list)
    typedef_characteristics: t.Annotated[list[TypedefCharacteristic], dict(many=True)] = dataclasses.field(default_factory=list)
    typedef_measurements: t.Annotated[list[TypedefMeasurement], dict(many=True)] = dataclasses.field(default_factory=list)
    typedef_structures: t.Annotated[list[TypedefStructure], dict(many=True)] = dataclasses.field(default_factory=list)
    units: t.Annotated[list[Unit], dict(many=True)] = dataclasses.field(default_factory=list)
    user_rights: t.Annotated[list[UserRights], dict(many=True)] = dataclasses.field(default_factory=list)
    variant_coding: VariantCoding | None = None
    # enhenced
    axis_pts_dict: dict[str, AxisPts] = dataclasses.field(default_factory=dict)
    blob_dict: dict[str, Blob] = dataclasses.field(default_factory=dict)
    characteristic_dict: dict[str, Characteristic] = dataclasses.field(default_factory=dict)
    compu_method_dict: dict[str, CompuMethod] = dataclasses.field(default_factory=dict)
    compu_tab_dict: dict[str, CompuTab] = dataclasses.field(default_factory=dict)
    compu_vtab_dict: dict[str, CompuVtab] = dataclasses.field(default_factory=dict)
    compu_vtab_range_dict: dict[str, CompuVtabRange] = dataclasses.field(default_factory=dict)
    frame_dict: dict[str, Frame] = dataclasses.field(default_factory=dict)
    function_dict: dict[str, Function] = dataclasses.field(default_factory=dict)
    group_dict: dict[str, Group] = dataclasses.field(default_factory=dict)
    instance_dict: dict[str, Instance] = dataclasses.field(default_factory=dict)
    measurement_dict: dict[str, Measurement] = dataclasses.field(default_factory=dict)
    record_layout_dict: dict[str, RecordLayout] = dataclasses.field(default_factory=dict)
    typedef_axis_dict: dict[str, TypedefAxis] = dataclasses.field(default_factory=dict)
    typedef_blob_dict: dict[str, TypedefBlob] = dataclasses.field(default_factory=dict)
    typedef_characteristic_dict: dict[str, TypedefCharacteristic] = dataclasses.field(default_factory=dict)
    typedef_measurement_dict: dict[str, TypedefMeasurement] = dataclasses.field(default_factory=dict)
    typedef_structure_dict: dict[str, TypedefStructure] = dataclasses.field(default_factory=dict)
    unit_dict: dict[str, Unit] = dataclasses.field(default_factory=dict)

    a2l_hash: bytes | None = None
    memory_size: int | None = None

    def __hash__(self):
        return id(self)


@dataclass(slots=True)
class Header:
    comment: str
    # optional
    project_no: str | None = None
    version: str | None = None


@dataclass(slots=True)
class Project:
    name: str
    long_identifier: str
    # optional
    header: Header | None = None
    modules: t.Annotated[list[Module], dict(many=True)] = dataclasses.field(default_factory=list)


@dataclass(slots=True)
class Asap2:
    # optional
    asap2_version: Asap2Version | None = None
    project: Project | None = None
    # enhenced
    a2l_hash: bytes | None = dataclasses.field(default=None)
    encoding: str | None = dataclasses.field(default=None)
