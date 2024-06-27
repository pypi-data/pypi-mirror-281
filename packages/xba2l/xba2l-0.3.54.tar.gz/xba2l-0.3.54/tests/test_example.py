# -*- encoding: utf-8 -*-
import re

# Local Modules
from xba2l import a2l_base, a2l_lib, a2l_util
from xba2l.etc import tool


def test_load_asap2(asap2: a2l_lib.Asap2):
    print(asap2.asap2_version)
    assert asap2.project is not None and len(asap2.project.modules) >= 1
    print("module num:", len(asap2.project.modules))


def test_load_module(module: a2l_lib.Module):
    assert isinstance(module, a2l_lib.Module)

    assert len(module.axis_ptses) == 2
    print("axis_ptses num:", len(module.axis_ptses))

    assert len(module.characteristics) >= 87
    print("characteristics num:", len(module.characteristics))

    assert len(module.blobs) >= 1
    print("blobs num:", len(module.blobs))

    assert len(module.instances) >= 1
    print("instances num:", len(module.instances))


def test_a2l_error(a2l_filename: str, options: a2l_base.Options):
    with open(a2l_filename, "rb") as f:
        content = f.read()

    err, asap2, module = a2l_util.parse_a2l(content, options=options)
    assert err is None
    assert isinstance(asap2, a2l_lib.Asap2)

    new_content = re.sub(b"/end[ ]+HEADER", b"/end WRONG", content, count=1)
    err, asap2, module = a2l_util.parse_a2l(new_content, options=options)
    assert err is not None
    assert tool.contain_error([err], code="E03", warning=False)

    new_content = re.sub(b"/begin PROJECT \\w+", b"/begin PROJECT", content, count=1)
    err, asap2, module = a2l_util.parse_a2l(new_content, options=options)
    assert err is not None
    assert tool.contain_error([err], code="E03", warning=False)
