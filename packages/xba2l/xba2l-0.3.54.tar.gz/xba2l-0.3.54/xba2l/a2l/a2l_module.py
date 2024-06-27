# -*- encoding: utf-8 -*-
import bisect
import dataclasses
import itertools
import typing as t

# Local Modules
from xba2l.a2l_lib import AxisDescr, AxisPts, AxisPtsXYZ45, Blob, Characteristic, Instance, Measurement, MemorySegment, Module, RecordElement, RecordLayout
from xba2l.a2l_lib import StructureComponent, TypedefAxis, TypedefBlob, TypedefCharacteristic, TypedefMeasurement, TypedefStructure
from xba2l.etc import OptionsUtil

__all__ = [
    "reform_module",
]


def clone_axis_pts(instance: Instance, typedef_axis: TypedefAxis, name: str) -> AxisPts:
    kwargs: dict = dict()
    kwargs.update({key: getattr(typedef_axis, key) for key in typedef_axis.__slots__ if key in AxisPts.__slots__})
    for key, val in {key: getattr(instance, key) for key in instance.__slots__ if key in AxisPts.__slots__}.items():
        if key not in ["LAYOUT", "MATRIX_DIM"] and val is not None:
            kwargs.update({key: val})
    if instance.overwrites is not None:
        for overwrite in instance.overwrites:
            if overwrite.name == instance.name and overwrite.axis_number == 0:
                for key, val in {key: getattr(overwrite, key) for key in overwrite.__slots__ if key in AxisPts.__slots__}.items():
                    if val is not None:
                        kwargs.update({key: val})
    kwargs.update(name=name)
    return AxisPts(**kwargs)


def component_axis_pts(
    component: StructureComponent,
    address: int,
    typedef_axis: TypedefAxis,
    instance: Instance,
    name: str,
) -> AxisPts:
    kwargs: dict = dict()
    kwargs.update({key: getattr(typedef_axis, key) for key in typedef_axis.__slots__ if key in AxisPts.__slots__})
    for key, val in {key: getattr(component, key) for key in component.__slots__ if key in AxisPts.__slots__}.items():
        if key not in ["LAYOUT", "MATRIX_DIM"] and val is not None:
            kwargs.update({key: val})
    if instance.overwrites is not None:
        for overwrite in instance.overwrites:
            if overwrite.name == component.name and overwrite.axis_number == 0:
                for key, val in {key: getattr(overwrite, key) for key in overwrite.__slots__ if key in AxisPts.__slots__}.items():
                    if val is not None:
                        kwargs.update({key: val})
    kwargs.update(name=name, address=address)
    return AxisPts(**kwargs)


def clone_characteristic(instance: Instance, typedef_characteristic: TypedefCharacteristic, name: str):
    kwargs: dict = {key: getattr(typedef_characteristic, key) for key in typedef_characteristic.__slots__ if key in Characteristic.__slots__}
    for key, val in {key: getattr(instance, key) for key in instance.__slots__ if key in Characteristic.__slots__}.items():
        if key not in ["LAYOUT", "MATRIX_DIM"] and val is not None:
            kwargs.update({key: val})
    if instance.overwrites is not None:
        for overwrite in instance.overwrites:
            if overwrite.name == instance.name and overwrite.axis_number == 0:
                for key, val in {key: getattr(overwrite, key) for key in overwrite.__slots__ if key in Characteristic.__slots__}.items():
                    if val is not None:
                        kwargs.update({key: val})

    if typedef_characteristic.axis_descrs is not None:
        axis_descrs: list[AxisDescr] = []
        for i, axis_descr in enumerate(typedef_characteristic.axis_descrs):
            axis_descr_kwargs: dict = dict()
            axis_descr_kwargs.update({key: getattr(axis_descr, key) for key in axis_descr.__slots__})
            if instance.overwrites is not None:
                for overwrite in instance.overwrites:
                    if overwrite.name == instance.name and overwrite.axis_number == i + 1:
                        for key, val in {key: getattr(overwrite, key) for key in overwrite.__slots__ if key in axis_descr.__slots__}.items():
                            if val is not None:
                                axis_descr_kwargs.update({key: val})
            axis_descrs.append(AxisDescr(**axis_descr_kwargs))
        kwargs.update(axis_descrs=axis_descrs)

    kwargs.update(name=name)
    return Characteristic(**kwargs)


def component_characteristic(
    component: StructureComponent,
    address: int,
    typedef_characteristic: TypedefCharacteristic,
    instance: Instance,
    name: str,
):
    kwargs: dict = dict()
    kwargs.update({key: getattr(typedef_characteristic, key) for key in typedef_characteristic.__slots__ if key in Characteristic.__slots__})
    for key, val in {key: getattr(component, key) for key in component.__slots__ if key in Characteristic.__slots__}.items():
        if key not in ["LAYOUT", "MATRIX_DIM"] and val is not None:
            kwargs.update({key: val})
    if instance.overwrites is not None:
        for overwrite in instance.overwrites:
            if overwrite.name == component.name and overwrite.axis_number == 0:
                for key, val in {key: getattr(overwrite, key) for key in overwrite.__slots__ if key in Characteristic.__slots__}.items():
                    if val is not None:
                        kwargs.update({key: val})

    if typedef_characteristic.axis_descrs is not None:
        axis_descrs: list[AxisDescr] = []
        for i, axis_descr in enumerate(typedef_characteristic.axis_descrs):
            axis_descr_kwargs: dict = dict()
            axis_descr_kwargs.update({key: getattr(axis_descr, key) for key in axis_descr.__slots__})
            if instance.overwrites is not None:
                for overwrite in instance.overwrites:
                    if overwrite.name == component.name and overwrite.axis_number == i + 1:
                        for key, val in {key: getattr(overwrite, key) for key in overwrite.__slots__ if key in axis_descr.__slots__}.items():
                            if val is not None:
                                axis_descr_kwargs.update({key: val})
            axis_descrs.append(AxisDescr(**axis_descr_kwargs))
        kwargs.update(axis_descrs=axis_descrs)

    kwargs.update(name=name, address=address)
    return Characteristic(**kwargs)


def clone_blob(instance: Instance, typedef_blob: TypedefBlob, name: str):
    kwargs: dict = dict()
    kwargs.update({key: getattr(typedef_blob, key) for key in typedef_blob.__slots__ if key in Blob.__slots__})
    for key, val in {key: getattr(instance, key) for key in instance.__slots__ if key in Blob.__slots__}.items():
        if key not in ["LAYOUT", "MATRIX_DIM"] and val is not None:
            kwargs.update({key: val})
    if instance.overwrites is not None:
        for overwrite in instance.overwrites:
            if overwrite.name == instance.name and overwrite.axis_number == 0:
                for key, val in {key: getattr(overwrite, key) for key in overwrite.__slots__ if key in Blob.__slots__}.items():
                    if val is not None:
                        kwargs.update({key: val})
    kwargs.update(name=name)
    return Blob(**kwargs)


def component_blob(
    component: StructureComponent,
    address: int,
    typedef_blob: TypedefBlob,
    instance: Instance,
    name: str,
):
    kwargs: dict = dict()
    kwargs.update({key: getattr(typedef_blob, key) for key in typedef_blob.__slots__ if key in Blob.__slots__})
    for key, val in {key: getattr(component, key) for key in component.__slots__ if key in Blob.__slots__}.items():
        if key not in ["LAYOUT", "MATRIX_DIM"] and val is not None:
            kwargs.update({key: val})
    if instance.overwrites is not None:
        for overwrite in instance.overwrites:
            if overwrite.name == component.name and overwrite.axis_number == 0:
                for key, val in {key: getattr(overwrite, key) for key in overwrite.__slots__ if key in Blob.__slots__}.items():
                    if val is not None:
                        kwargs.update({key: val})
    kwargs.update(name=name, address=address)
    return Blob(**kwargs)


def clone_measurement(instance: Instance, typedef_measurement: TypedefMeasurement):
    kwargs: dict = dict()
    kwargs.update({key: getattr(typedef_measurement, key) for key in typedef_measurement.__slots__ if key in Measurement.__slots__})
    for key, val in {key: getattr(instance, key) for key in instance.__slots__ if key in Measurement.__slots__}.items():
        if val is not None:
            kwargs.update({key: val})
    if instance.overwrites is not None:
        for overwrite in instance.overwrites:
            if overwrite.name == instance.name and overwrite.axis_number == 0:
                for key, val in {key: getattr(overwrite, key) for key in overwrite.__slots__ if key in Measurement.__slots__}.items():
                    if val is not None:
                        kwargs.update({key: val})
    kwargs.update(name=instance.name)
    return Blob(**kwargs)


def component_measurement(
    component: StructureComponent,
    typedef_measurement: TypedefMeasurement,
    instance: Instance,
    name: str,
):
    kwargs: dict = dict()
    kwargs.update({key: getattr(typedef_measurement, key) for key in typedef_measurement.__slots__ if key in Measurement.__slots__})
    for key, val in {key: getattr(component, key) for key in component.__slots__ if key in Measurement.__slots__}.items():
        if val is not None:
            kwargs.update({key: val})
    if instance.overwrites is not None:
        for overwrite in instance.overwrites:
            if overwrite.name == component.name and overwrite.axis_number == 0:
                for key, val in {key: getattr(overwrite, key) for key in overwrite.__slots__ if key in Measurement.__slots__}.items():
                    if val is not None:
                        kwargs.update({key: val})
    kwargs.update(name=name)
    return Blob(**kwargs)


def find_memory_segment(address: int, module: Module) -> MemorySegment:
    if module.mod_par is not None:
        i = bisect.bisect_right(module.mod_par.memory_segments, address, key=lambda memory_segment: memory_segment.address)
        if i > 0:
            memory_segment = module.mod_par.memory_segments[i - 1]
            if memory_segment.address <= address and address < memory_segment.address + memory_segment.size:
                return memory_segment
    return None


def clone_structure(
    instance: Instance,
    structure: TypedefStructure,
    module: Module,
) -> dict[str, t.Union[dict, AxisPts, Characteristic, Blob]]:
    def func(base_name: str, structure_components: list[StructureComponent], address: int):
        label_dict: dict[str, t.Union[dict, AxisPts, Characteristic, Blob]] = dict()
        for structure_component in structure_components:
            typedef_axis = module.typedef_axis_dict.get(structure_component.typedef_name)
            if typedef_axis is not None:
                if structure_component.matrix_dim is not None:
                    for indexes in itertools.product(*(range(num) for num in structure_component.matrix_dim)):
                        axis_pts = component_axis_pts(
                            structure_component,
                            address + structure_component.address_offset,
                            typedef_axis,
                            instance=instance,
                            name=f"{base_name}.{structure_component.name}" + "".join([f"[{index}]" for index in indexes]),
                        )
                        label_dict.update({axis_pts.name: axis_pts})
                    continue
                else:
                    axis_pts = component_axis_pts(
                        structure_component,
                        address + structure_component.address_offset,
                        typedef_axis,
                        instance,
                        name=f"{base_name}.{structure_component.name}",
                    )
                    label_dict.update({axis_pts.name: axis_pts})
                    continue

            typedef_characteristic = module.typedef_characteristic_dict.get(structure_component.typedef_name)
            if typedef_characteristic is not None:
                if structure_component.matrix_dim is not None:
                    for indexes in itertools.product(*(range(num) for num in structure_component.matrix_dim)):
                        characteristic = component_characteristic(
                            structure_component,
                            address + structure_component.address_offset,
                            typedef_characteristic,
                            instance=instance,
                            name=f"{base_name}.{structure_component.name}" + "".join([f"[{index}]" for index in indexes]),
                        )
                        label_dict.update({characteristic.name: characteristic})
                    continue
                else:
                    characteristic = component_characteristic(
                        structure_component,
                        address + structure_component.address_offset,
                        typedef_characteristic,
                        instance,
                        name=f"{base_name}.{structure_component.name}",
                    )
                    label_dict.update({characteristic.name: characteristic})
                    continue

            typedef_blob = module.typedef_blob_dict.get(structure_component.typedef_name)
            if typedef_blob is not None:
                if structure_component.matrix_dim is not None:
                    for indexes in itertools.product(*(range(num) for num in structure_component.matrix_dim)):
                        blob = component_blob(
                            structure_component,
                            address + structure_component.address_offset,
                            typedef_blob,
                            instance=instance,
                            name=f"{base_name}.{structure_component.name}" + "".join([f"[{index}]" for index in indexes]),
                        )
                        label_dict.update({blob.name: blob})
                    continue
                else:
                    blob = component_blob(
                        structure_component,
                        address + structure_component.address_offset,
                        typedef_blob,
                        instance,
                        name=f"{base_name}.{structure_component.name}",
                    )
                    label_dict.update({blob.name: blob})
                    continue

            typedef_measurement = module.typedef_measurement_dict.get(structure_component.typedef_name)
            if typedef_measurement is not None:
                if structure_component.matrix_dim is not None:
                    for indexes in itertools.product(*(range(num) for num in structure_component.matrix_dim)):
                        measurement = component_measurement(
                            structure_component,
                            typedef_blob,
                            instance=instance,
                            name=f"{base_name}.{structure_component.name}" + "".join([f"[{index}]" for index in indexes]),
                        )
                        label_dict.update({measurement.name: measurement})
                    continue
                else:
                    measurement = component_measurement(
                        structure_component,
                        typedef_blob,
                        instance,
                        name=f"{base_name}.{structure_component.name}",
                    )
                    label_dict.update({measurement.name: measurement})
                    continue

            typedef_structure = module.typedef_structure_dict.get(structure_component.typedef_name)
            if typedef_structure is not None:
                label_dict.update(func(f"{base_name}.{structure_component.name}", structure_component, address + structure_component.address_offset))
                continue

        return label_dict

    label_dict: dict[str, t.Union[dict, AxisPts, Characteristic, Blob]] = dict()
    if structure.structure_components is not None:
        label_dict.update(func(instance.name, structure.structure_components, instance.address))

    return label_dict


def reform_module(module: Module, opts: OptionsUtil):
    module.axis_pts_dict = {}
    for axis_pts in module.axis_ptses:
        if axis_pts.name in module.axis_pts_dict:
            axis_pts.name = f"{axis_pts.name}_a"
            module.axis_pts_dict[axis_pts.name] = axis_pts
        else:
            module.axis_pts_dict[axis_pts.name] = axis_pts
    module.blob_dict = {blob.name: blob for blob in module.blobs}
    module.characteristic_dict = dict()
    for characteristic in module.characteristics:
        if characteristic.name in module.characteristic_dict:
            characteristic.name = f"{characteristic.name}_c"
            module.characteristic_dict[characteristic.name] = characteristic
        else:
            module.characteristic_dict[characteristic.name] = characteristic
    for compu_method in module.compu_methods:
        if compu_method.format and not compu_method.format.startswith("%"):
            compu_method.format = "%" + compu_method.format
    module.compu_method_dict = {compu_method.name: compu_method for compu_method in module.compu_methods}
    module.compu_tab_dict = {compu_tab.name: compu_tab for compu_tab in module.compu_tabs}
    for compu_vtab in module.compu_vtabs:
        compu_vtab.read_dict = {pair_value[0]: (pair_value[1].strip() or pair_value[1]) for pair_value in compu_vtab.pair_values}
        compu_vtab.write_dict = {(pair_value[1].strip() or pair_value[1]): pair_value[0] for pair_value in compu_vtab.pair_values}
    module.compu_vtab_dict = {compu_vtab.name: compu_vtab for compu_vtab in module.compu_vtabs}
    for compu_vtab_range in module.compu_vtab_ranges:
        compu_vtab_range.write_dict = {
            (triple_value[2].strip() or triple_value[2]): (triple_value[0], triple_value[1]) for triple_value in compu_vtab_range.triple_values
        }
    module.compu_vtab_range_dict = {compu_vtab_range.name: compu_vtab_range for compu_vtab_range in module.compu_vtab_ranges}
    module.frame_dict = {frame.name: frame for frame in module.frames}
    module.function_dict = {function.name: function for function in module.functions}
    module.group_dict = {group.name: group for group in module.groups}
    module.instance_dict = {instance.name: instance for instance in module.instances}
    module.measurement_dict = {measurement.name: measurement for measurement in module.measurements}

    layout_fields = dataclasses.fields(RecordLayout)
    for layout in module.record_layouts:
        layout.elements = [("RESERVED", reserved) for reserved in layout.reserveds or []]
        for f in layout_fields:
            element = getattr(layout, f.name, None)
            if isinstance(element, RecordElement):
                layout.elements.append((f.name.upper(), element))
        layout.elements.sort(key=lambda pair: pair[1].position)

    module.record_layout_dict = {record_layout.name: record_layout for record_layout in module.record_layouts}
    module.typedef_axis_dict = {typedef_axis.name: typedef_axis for typedef_axis in module.typedef_axises}
    module.typedef_blob_dict = {typedef_blob.name: typedef_blob for typedef_blob in module.typedef_blobs}
    module.typedef_characteristic_dict = {typedef_characteristic.name: typedef_characteristic for typedef_characteristic in module.typedef_characteristics}
    module.typedef_measurement_dict = {typedef_measurement.name: typedef_measurement for typedef_measurement in module.typedef_measurements}
    module.typedef_structure_dict = {typedef_structure.name: typedef_structure for typedef_structure in module.typedef_structures}
    module.unit_dict = {unit.name: unit for unit in module.units}

    if opts.read_instance is True:
        for instance in module.instances:
            typedef_axis = module.typedef_axis_dict.get(instance.typedef_name)
            if typedef_axis is not None:
                if instance.matrix_dim is not None:
                    for indexes in itertools.product(*(range(num) for num in instance.matrix_dim)):
                        label_name = instance.name + "".join([f"[{index}]" for index in indexes])
                        module.axis_pts_dict[label_name] = clone_axis_pts(instance, typedef_axis, name=label_name)
                    continue
                else:
                    module.axis_pts_dict[instance.name] = clone_axis_pts(instance, typedef_axis, name=instance.name)
                    continue

            typedef_characteristic = module.typedef_characteristic_dict.get(instance.typedef_name)
            if typedef_characteristic is not None:
                if instance.matrix_dim is not None:
                    for indexes in itertools.product(*(range(num) for num in instance.matrix_dim)):
                        label_name = instance.name + "".join([f"[{index}]" for index in indexes])
                        module.characteristic_dict[label_name] = clone_characteristic(instance, typedef_characteristic, name=label_name)
                    continue
                else:
                    module.characteristic_dict[instance.name] = clone_characteristic(instance, typedef_characteristic, name=instance.name)
                    continue

            typedef_blob = module.typedef_blob_dict.get(instance.typedef_name)
            if typedef_blob is not None:
                if instance.matrix_dim is not None:
                    for indexes in itertools.product(*(range(num) for num in instance.matrix_dim)):
                        label_name = instance.name + "".join([f"[{index}]" for index in indexes])
                        module.characteristic_dict[label_name] = clone_blob(instance, typedef_blob, name=label_name)
                    continue
                else:
                    module.blob_dict[instance.name] = clone_blob(instance, typedef_blob, name=instance.name)
                    continue

            typedef_measurement = module.typedef_measurement_dict.get(instance.typedef_name)
            if typedef_measurement is not None:
                if instance.matrix_dim is not None:
                    for indexes in itertools.product(*(range(num) for num in instance.matrix_dim)):
                        label_name = instance.name + "".join([f"[{index}]" for index in indexes])
                        module.measurement_dict[label_name] = clone_measurement(instance, typedef_measurement, name=label_name)
                    continue
                else:
                    measurement = clone_measurement(instance, typedef_measurement)
                    module.measurement_dict[measurement.name] = measurement
                    continue

            typedef_structure = module.typedef_structure_dict.get(instance.typedef_name)
            if typedef_structure is not None:
                label_dict = clone_structure(instance, typedef_structure, module=module)
                for label_name, label in label_dict.items():
                    if isinstance(label, AxisPts):
                        module.axis_pts_dict[label_name] = label
                    elif isinstance(label, Characteristic):
                        module.characteristic_dict[label_name] = label
                    elif isinstance(label, Blob):
                        module.blob_dict[label_name] = label
                    elif isinstance(label, Measurement):
                        module.measurement_dict[label_name] = label
                    else:
                        pass
                continue

    prg_types_non_configurable = ["DATA", "CODE", "OFFLINE_DATA"]

    for axis_pts in module.axis_pts_dict.values():
        if axis_pts.address:
            memory_segment = find_memory_segment(axis_pts.address, module)
            if memory_segment is not None:
                axis_pts.configurable = memory_segment.prg_type not in prg_types_non_configurable

        compu_method = module.compu_method_dict.get(axis_pts.conversion)
        if compu_method is not None:
            axis_pts.textual = compu_method.conversion_type == "TAB_VERB"
            axis_pts.unit_name = axis_pts.phys_unit or compu_method.unit
            axis_pts.format_string = axis_pts.format or compu_method.format
        else:
            axis_pts.unit_name = axis_pts.phys_unit
            axis_pts.format_string = axis_pts.format

        record_layout = module.record_layout_dict.get(axis_pts.record_layout)
        if record_layout is not None:
            if record_layout.axis_rescale_x is not None:
                axis_pts.data_type = record_layout.axis_rescale_x.data_type
            if record_layout.axis_pts_x is not None:
                axis_pts.data_type = record_layout.axis_pts_x.data_type

        record_layout = module.record_layout_dict.get(axis_pts.record_layout, None)
        if record_layout is not None and record_layout.axis_rescale_x is not None:
            axis_pts.extended_type = "RES_AXIS"
        else:
            axis_pts.extended_type = "AXIS"

    for characteristic in module.characteristic_dict.values():
        if characteristic.address:
            memory_segment = find_memory_segment(characteristic.address, module)
            if memory_segment is not None:
                characteristic.configurable = memory_segment.prg_type not in prg_types_non_configurable

        compu_method = module.compu_method_dict.get(characteristic.conversion)
        if compu_method is not None:
            characteristic.textual = compu_method.conversion_type == "TAB_VERB"
            characteristic.unit_name = characteristic.phys_unit or compu_method.unit
            characteristic.format_string = characteristic.format or compu_method.format
        else:
            characteristic.unit_name = characteristic.phys_unit
            characteristic.format_string = characteristic.format
        if characteristic.type == "ASCII":
            characteristic.textual = True

        record_layout = module.record_layout_dict.get(characteristic.record_layout)
        if record_layout is not None:
            if record_layout.fnc_values is not None:
                characteristic.data_type = record_layout.fnc_values.data_type

        for i, axis_descr in enumerate(characteristic.axis_descrs or []):
            flag = "xyz45"[i]
            if axis_descr.axis_pts_ref is not None:
                share_axis_pts = module.axis_pts_dict.get(axis_descr.axis_pts_ref)
                if share_axis_pts is not None:
                    axis_descr.textual = share_axis_pts.textual
                    axis_descr.unit_name = share_axis_pts.unit_name
                    axis_descr.format_string = share_axis_pts.format_string
                    axis_descr.data_type = share_axis_pts.data_type
                    continue

            if axis_descr.curve_axis_ref is not None:
                share_characteristic = module.characteristic_dict.get(axis_descr.curve_axis_ref)
                if share_characteristic is not None:
                    share_compu_method = module.compu_method_dict.get(share_characteristic.conversion)
                    if share_compu_method is not None:
                        axis_descr.textual = share_compu_method.conversion_type == "TAB_VERB"
                        axis_descr.unit_name = share_characteristic.phys_unit or share_compu_method.unit
                        axis_descr.format_string = share_characteristic.format or share_compu_method.format

                    share_record_layout = module.record_layout_dict.get(share_characteristic.record_layout)
                    if share_record_layout is not None:
                        if share_record_layout.fnc_values is not None:
                            axis_descr.data_type = share_record_layout.fnc_values.data_type
                    continue

            compu_method = module.compu_method_dict.get(axis_descr.conversion)
            if compu_method is not None:
                axis_descr.textual = compu_method.conversion_type == "TAB_VERB"
                axis_descr.unit_name = axis_descr.phys_unit or compu_method.unit
                axis_descr.format_string = axis_descr.format or compu_method.format
            else:
                axis_descr.unit_name = axis_descr.phys_unit
                axis_descr.format_string = axis_descr.format

            if record_layout is not None:
                layout_elment: AxisPtsXYZ45 | None = getattr(record_layout, f"axis_pts_{flag}", None)
                if layout_elment is not None:
                    axis_descr.data_type = layout_elment.data_type

        if characteristic.type == "VALUE":
            if characteristic.textual is not True and characteristic.bit_mask is not None and any((characteristic.bit_mask == (1 << i) for i in range(64))):
                characteristic.extended_type = "BOOLEAN"
            else:
                characteristic.extended_type = "VALUE"
        elif characteristic.type == "VAL_BLK":
            if characteristic.number == 1:
                characteristic.extended_type = "VALUE"
            elif isinstance(characteristic.matrix_dim, list) and all([v == 1 for v in characteristic.matrix_dim]):
                characteristic.extended_type = "VALUE"
            elif isinstance(characteristic.matrix_dim, list) and len([v for v in characteristic.matrix_dim if v > 1]) >= 2:
                characteristic.extended_type = "MATRIX"
            else:
                characteristic.extended_type = "VAL_BLK"
        elif characteristic.type == "CURVE":
            if characteristic.axis_descrs and any((axis_descr.attribute == "CURVE_AXIS" for axis_descr in characteristic.axis_descrs)):
                characteristic.extended_type = "CURVE_AXIS"
            else:
                characteristic.extended_type = "CURVE"
        else:
            characteristic.extended_type = characteristic.type

    for blob in module.blob_dict.values():
        blob.extended_type = "BLOB"

        if blob.address:
            memory_segment = find_memory_segment(blob.address, module)
            if memory_segment is not None:
                blob.configurable = memory_segment.prg_type not in prg_types_non_configurable

    for function in module.functions:
        if function.def_characteristic is not None:
            for identifier in function.def_characteristic.identifiers:
                axis_pts = module.axis_pts_dict.get(identifier)
                if axis_pts is not None:
                    axis_pts.function_name = function.name
                    axis_pts.function_version = function.function_version
                characteristic = module.characteristic_dict.get(identifier)
                if characteristic is not None:
                    characteristic.function_name = function.name
                    characteristic.function_version = function.function_version
                blob = module.blob_dict.get(identifier)
                if blob is not None:
                    blob.function_name = function.name
                    blob.function_version = function.function_version

    if module.mod_par is not None:
        module.mod_par.system_constant_dict = {system_constant.name: system_constant.value for system_constant in module.mod_par.system_constants}
