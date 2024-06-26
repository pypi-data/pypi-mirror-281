# -*- encoding: utf-8 -*-
import dataclasses
import json
import os
import re
import time

# Local Modules
from xba2l import a2l_base, a2l_lib, a2l_util
from xba2l.etc import tool


def find_names(text: str, key: str) -> list[str]:
    return re.findall(r"/begin\s+{}\s+([^\s]+)\s+.*?/end\s+{}\s+".format(key, key), text, flags=re.DOTALL | re.MULTILINE)


def process_a2l(a2l_filename: str, **kwargs) -> a2l_lib.Asap2:
    options = a2l_base.Options(ignore_measurements=False)
    print("\n{:s}".format(a2l_filename))
    begin_time = time.time()
    err, asap2, module = a2l_util.parse_a2l(a2l_filename, options=options)
    if err is not None:
        print(str(err))
        raise err

    print(
        "time: {:.2f} s, characteristic: {:d}, axis_pts: {:d}".format(
            time.time() - begin_time,
            len(module.characteristics),
            len(module.axis_ptses),
        )
    )

    _, content, encoding = tool.read_file(a2l_filename, encoding=None)

    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL | re.MULTILINE)
    content = re.sub(r"//.*?$", "", content, flags=re.DOTALL | re.MULTILINE)

    memory_segment_names = find_names(content, "MEMORY_SEGMENT")
    if module.mod_par is None:
        if len(memory_segment_names) > 0:
            for name in memory_segment_names:
                print("\tlost memory_segment: {:s}".format(name))
    else:
        lost = set(memory_segment_names) - set([memory_segment.name for memory_segment in module.mod_par.memory_segments])
        for name in lost:
            print("\tlost memory_segment: {:s}".format(name))

    for key in [
        "AXIS_PTS",
        "BLOB",
        "CHARACTERISTIC",
        "COMPU_METHOD",
        "COMPU_TAB",
        "COMPU_VTAB",
        "COMPU_VTAB_RANGE",
        "FUNCTION",
        "GROUP",
        "INSTANCE",
        "MEASUREMENT",
        "RECORD_LAYOUT",
    ]:
        names = find_names(content, key)
        lost = set(names) - set([getattr(item, "name") for item in getattr(module, key.lower() + ("es" if key.endswith("S") else "s"))])
        for name in lost:
            print("\tlost {:s}: {:s}".format(key.lower(), name))

    return asap2


def test_example():
    a2l_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "example/ASAP2_Demo_V171.a2l"))
    process_a2l(a2l_filename)


if __name__ == "__main__":
    a2l_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "example/ASAP2_Demo_V171.a2l"))
    asap2 = process_a2l(a2l_filename)
    with open(a2l_filename + ".json", "w", encoding="utf-8") as f:
        json.dump(
            dataclasses.asdict(
                asap2,
                dict_factory=lambda pairs: {
                    pair[0]: pair[1] for pair in pairs if pair[1] is not None and pair[0] != "elements" and not pair[0].endswith("_dict")
                },
            ),
            f,
            indent=4,
            cls=tool.JsonEncoder,
        )
