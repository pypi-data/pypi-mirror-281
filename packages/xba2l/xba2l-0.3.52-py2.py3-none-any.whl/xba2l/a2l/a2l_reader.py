# -*- encoding: utf-8 -*-
import dataclasses
import functools
import json
import os
import types
import typing as t

from pympler import asizeof

# Local Modules
from .a2l_core import A2lNode, read_a2l
from .a2l_module import reform_module
from xba2l.a2l_lib import Annotation, AnnotationText, Asap2, AxisDescr, AxisPts, BitOperation, Blob, CalibrationHandler, CalibrationMethod, Characteristic
from xba2l.a2l_lib import CompuMethod, CompuTab, CompuVtab, CompuVtabRange, DefCharacteristic, DependentCharacteristic, FixAxisParList, Formula, Frame
from xba2l.a2l_lib import FrameMeasurement, Function, FunctionList, Group, Header, InMeasurement, Instance, LocMeasurement, MapList, Measurement, MemoryLayout
from xba2l.a2l_lib import MemorySegment, ModCommon, ModPar, Module, OutMeasurement, Overwrite, Project, RecordLayout, RefCharacteristic, RefGroup
from xba2l.a2l_lib import RefMeasurement, StructureComponent, SubFunction, SubGroup, Transformer, TransformerInObjects, TransformerOutObjects, TypedefAxis
from xba2l.a2l_lib import TypedefBlob, TypedefCharacteristic, TypedefMeasurement, TypedefStructure, Unit, UserRights, VarAddress, VarCharacteristic
from xba2l.a2l_lib import VarCriterion, VarForbiddenComb, VariantCoding, Virtual, VirtualCharacteristic
from xba2l.etc import GrammarError, OptionsUtil, Unknown, tool
from xba2l.etc.reader import READER, ReadField, parse_field

__all__ = [
    "parse_a2l",
]


def read_int(words: list[str], start: int, _: dict) -> tuple[int, int]:
    if start >= len(words):
        raise GrammarError("missing words", method="read_int")
    if words[start].startswith("0x"):
        return start + 1, int(words[start][2:], base=16)
    else:
        return start + 1, round(float(words[start]))


def read_float(words: list[str], start: int, _: dict) -> tuple[int, float]:
    if start >= len(words):
        raise GrammarError("missing words", method="read_float")
    if words[start].startswith("0x"):
        return start + 1, float(int(words[start][2:], base=16))
    else:
        return start + 1, float(words[start])


def read_str(words: list[str], start: int, _: dict) -> tuple[int, str]:
    if start >= len(words):
        raise GrammarError("missing words", method="read_str")
    return start + 1, words[start]


def read_bool(words: list[str], start: int, _: dict) -> tuple[int, bool]:
    return start, True


def read_keyword(words: list[str], start: int, _: dict) -> tuple[int, str]:
    if start >= len(words):
        return start, None

    return start + 1, words[start].lower()


def read_int_list(words: list[str], start: int, context: dict, reader: READER) -> tuple[int, str]:
    size: int = 0
    while start + size < len(words):
        if words[start + size].isdigit():
            size += 1
        else:
            break
    return reader(words[: start + size], start, context)


def read_function_list(words: list[str], start: int, context: dict, clazz: type, reader: READER) -> tuple[int, str]:
    size: int = 0
    while start + size < len(words):
        key = words[start + size].lower()
        if key in clazz.__slots__:
            break
        key = key + ("es" if key.endswith("s") else "s")
        if key in clazz.__slots__:
            break
        size += 1
    return reader(words[: start + size], start, context)


def parse_hook(clazz: type, descr: ReadField) -> ReadField:
    if descr.f.name == "matrix_dim":
        descr.reader = functools.partial(read_int_list, reader=descr.reader)

    if descr.f.name == "function_list":
        descr.reader = functools.partial(read_function_list, clazz=clazz, reader=descr.reader)

    origin = t.get_origin(descr.f.type)
    if origin and (origin == t.Union or issubclass(origin, types.UnionType)) and t.get_args(descr.f.type)[0] == bool:
        descr.reader = lambda words, start, context: (start, True)
    return descr


def read_clazz(
    clazz: type,
    reader_dict: dict[type, READER],
    read_keyword: READER[str],
    parse_hook: t.Callable[[type, ReadField], ReadField] | None = None,
):
    assert dataclasses.is_dataclass(clazz)

    if issubclass(clazz, Characteristic):
        pass

    fields = dataclasses.fields(clazz)

    attribute_fields: list[dataclasses.Field] = []
    for f in dataclasses.fields(clazz):
        if f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING:
            attribute_fields.append(f)
        else:
            break

    attribute_descrs: list[ReadField] = []
    annotations = t.get_type_hints(clazz)
    for f in attribute_fields:
        descr = parse_field(f, annotations[f.name], reader_dict)
        if callable(parse_hook):
            descr = parse_hook(clazz, descr)
        attribute_descrs.append(descr)

    property_fields: list[dataclasses.Field] = fields[len(attribute_fields) :]
    property_dict: dict[str, dataclasses.Field] = {f.name: f for f in property_fields}

    property_descr_dict: dict[str, ReadField] = dict()

    def wrapper(words: list[str], other_lines: list[list[str | None]] = None):
        context: dict[str, t.Any] = dict()

        # attribute
        start: int = 0

        args = []
        for descr in attribute_descrs:
            start, arg = descr.reader(words, start, context)
            context.update({descr.f.name: arg})
            args.append(arg)

        # make target
        obj = clazz(*args)

        lines: list[list[str]] = []
        if start < len(words):
            lines.append(words[start:])
        if isinstance(other_lines, list):
            lines.extend(other_lines)

        for words in lines:
            start = 0
            while start < len(words):
                start, key = read_keyword(words, start, context)
                if isinstance(key, str):
                    if key not in property_descr_dict:
                        f = property_dict.get(key, None)
                        if f is None:
                            keys = key + ("es" if key.endswith("s") else "s")
                            f = property_dict.get(keys, None)
                        if f is None:
                            if __debug__:
                                print(Unknown("keyword", keyword=key))
                            continue
                        descr = parse_field(f, annotations[f.name], reader_dict)
                        if callable(parse_hook):
                            descr = parse_hook(clazz, descr)
                        property_descr_dict.update({key: descr})
                    else:
                        descr = property_descr_dict[key]

                    start, vars = descr.reader(words, start, context)
                    if descr.many is True:
                        if descr.extend is True:
                            assert isinstance(vars, list)
                            prop = getattr(obj, descr.f.name, None)
                            if isinstance(prop, list):
                                prop.extend(vars)
                            else:
                                setattr(obj, descr.f.name, vars)
                        else:
                            prop = getattr(obj, descr.f.name, None)
                            if isinstance(prop, list):
                                prop.append(vars)
                            else:
                                setattr(obj, descr.f.name, [vars])
                    else:
                        setattr(obj, descr.f.name, vars)

        return obj

    return wrapper


T = t.TypeVar("T")


def read_node(clazz: T) -> t.Callable[[A2lNode, OptionsUtil], T]:
    reader_dict: dict[str, READER] = {
        int: read_int,
        float: read_float,
        str: read_str,
        bool: read_bool,
    }

    clazz_reader = read_clazz(
        clazz,
        reader_dict=reader_dict,
        read_keyword=read_keyword,
        parse_hook=parse_hook,
    )

    def wrapper(node: A2lNode, opts: OptionsUtil):
        obj = clazz_reader(node.words)

        for child in node.children:
            key = child.key.lower()
            node_reader = a2l_reader_dict.get(key, None)
            if callable(node_reader):
                if hasattr(obj, key):
                    try:
                        var = node_reader(child, opts)
                    except Exception as err:
                        print(GrammarError("read node fail", err, key=key, lineno=child.lineno))
                        continue
                    setattr(obj, key, var)
                    continue
                new_key = key + ("es" if key.endswith("s") else "s")
                if hasattr(obj, new_key):
                    try:
                        var = node_reader(child, opts)
                    except Exception as err:
                        print(GrammarError("read node fail", err, key=key, lineno=child.lineno))
                        continue
                    prop = getattr(obj, new_key, None)
                    if isinstance(prop, list):
                        prop.append(var)
                    else:
                        setattr(obj, new_key, [var])
            else:
                if __debug__:
                    print(Unknown("node: ", keyword=key, lineno=child.lineno))

        return obj

    return wrapper


def read_module():
    module_reader = read_node(Module)

    def wrapper(node: A2lNode, opts: OptionsUtil):
        obj: Module = module_reader(node, opts)
        reform_module(obj, opts)

        return obj

    return wrapper


a2l_reader_dict: dict[str, type] = dict(
    annotation=read_node(Annotation),
    annotation_text=read_node(AnnotationText),
    axis_descr=read_node(AxisDescr),
    axis_pts=read_node(AxisPts),
    bit_operation=read_node(BitOperation),
    blob=read_node(Blob),
    calibration_handle=read_node(CalibrationHandler),
    calibration_method=read_node(CalibrationMethod),
    characteristic=read_node(Characteristic),
    compu_method=read_node(CompuMethod),
    compu_tab=read_node(CompuTab),
    compu_vtab=read_node(CompuVtab),
    compu_vtab_range=read_node(CompuVtabRange),
    def_characteristic=read_node(DefCharacteristic),
    dependent_characteristic=read_node(DependentCharacteristic),
    fix_axis_par_list=read_node(FixAxisParList),
    formula=read_node(Formula),
    frame=read_node(Frame),
    frame_measurement=read_node(FrameMeasurement),
    function=read_node(Function),
    function_list=read_node(FunctionList),
    group=read_node(Group),
    header=read_node(Header),
    in_measurement=read_node(InMeasurement),
    instance=read_node(Instance),
    loc_measurement=read_node(LocMeasurement),
    map_list=read_node(MapList),
    measurement=read_node(Measurement),
    memory_layout=read_node(MemoryLayout),
    memory_segment=read_node(MemorySegment),
    mod_common=read_node(ModCommon),
    mod_par=read_node(ModPar),
    module=read_module(),
    out_measurement=read_node(OutMeasurement),
    overwrite=read_node(Overwrite),
    project=read_node(Project),
    record_layout=read_node(RecordLayout),
    ref_characteristic=read_node(RefCharacteristic),
    ref_group=read_node(RefGroup),
    ref_measurement=read_node(RefMeasurement),
    structure_component=read_node(StructureComponent),
    sub_function=read_node(SubFunction),
    sub_group=read_node(SubGroup),
    transformer=read_node(Transformer),
    transformer_in_objects=read_node(TransformerInObjects),
    transformer_out_objects=read_node(TransformerOutObjects),
    typedef_axis=read_node(TypedefAxis),
    typedef_blob=read_node(TypedefBlob),
    typedef_characteristic=read_node(TypedefCharacteristic),
    typedef_measurement=read_node(TypedefMeasurement),
    typedef_structure=read_node(TypedefStructure),
    unit=read_node(Unit),
    user_rights=read_node(UserRights),
    var_address=read_node(VarAddress),
    var_characteristic=read_node(VarCharacteristic),
    var_criterion=read_node(VarCriterion),
    var_forbidden_comb=read_node(VarForbiddenComb),
    variant_coding=read_node(VariantCoding),
    virtual=read_node(Virtual),
    virtual_characteristic=read_node(VirtualCharacteristic),
)


def free_node(node: A2lNode):
    for child in node.children:
        free_node(child)
    del node.children[:]
    del node.words[:]
    del node


def parse_a2l(
    fn_or_content: str | bytes,
    opts: OptionsUtil,
    encoding: str | None,
    a2l_hash: bytes | None = None,
) -> tuple[Exception | None, Asap2, Module]:
    err, a2l_hash, root, encoding = read_a2l(fn_or_content, encoding=encoding, opts=opts, a2l_hash=a2l_hash)
    if err is not None:
        if root is not None:
            free_node(root)
        return err, None, None

    try:
        assert root is not None
        asap2_reader = read_node(Asap2)
        asap2 = asap2_reader(root, opts)
        free_node(root)

        asap2.a2l_hash = a2l_hash
        asap2.encoding = encoding
        if asap2.project is None:
            raise GrammarError("project not found")
        if len(asap2.project.modules) == 0:
            raise GrammarError("module not found")

        for module in asap2.project.modules:
            if opts.calculate_memory_size is True:
                module.memory_size = asizeof.asizeof(module)
            module.a2l_hash = a2l_hash

        return None, asap2, asap2.project.modules[0]
    except Exception as err:
        return GrammarError(err), None, None
