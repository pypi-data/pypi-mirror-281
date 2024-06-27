# -*- encoding: utf-8 -*-
import argparse
import os
import time
import typing as t

# Local Modules
from xba2l import a2l_base, a2l_util


def process_a2l(a2l_filename: str, measurement: str, repeat_count: int = 10, index: int = None):
    if not os.path.isfile(a2l_filename):
        raise Exception("file not exists: {:s}".format(a2l_filename))

    with open(a2l_filename, "rb") as f:
        content = f.read()

    begin_time = time.time()
    for i in range(repeat_count):
        err, asap2, module = a2l_util.parse_a2l(content, options=a2l_base.Options(ignore_measurements=measurement == "off"))
        if err is not None:
            raise err
    average_time = (time.time() - begin_time) / repeat_count

    num_axis = len(module.axis_pts_dict)
    num_charecteristic = len(module.characteristic_dict)
    num_blob = len(module.blob_dict)
    num_measurement = len(module.measurement_dict)

    if index == 0:
        print(("{:20s}" * 7).format("File_Size[MB]", "Axis", "Charecteristic", "Blob", "Measurement", "Used_Time[s]", "Filename"))
        print("-" * 180)

    fmt = "{:<20.1f}" + "{:<20d}" * 4 + "{:<20.1f}" + "{:s}"
    print(
        fmt.format(
            len(content) / 1024.0 / 1024.0,
            num_axis,
            num_charecteristic,
            num_blob,
            num_measurement,
            average_time,
            a2l_filename,
        )
    )


if __name__ == "__main__":

    def scandir(dir: str) -> t.Iterable[str]:
        with os.scandir(dir) as it:
            for entry in it:
                if entry.is_file():
                    if os.path.splitext(entry.name)[1].lower() == ".a2l":
                        yield os.path.join(dir, entry.name)
                elif entry.is_dir():
                    yield from scandir(os.path.join(dir, entry.name))
                else:
                    pass

    class Namespace(argparse.Namespace):
        measurement: str
        repeat_count: int
        filename_list: list[str]

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--measurement", type=str, choices=["on", "off"], default="on", required=False)
    parser.add_argument("-c", "--repeat_count", type=int, default=10, required=False)
    parser.add_argument("filename_list", type=str, nargs="+")
    opt = parser.parse_args(namespace=Namespace)

    a2l_filename_list: list[str] = []
    for filename in opt.filename_list:
        if os.path.isfile(filename) and os.path.splitext(filename)[1].lower() == ".a2l":
            a2l_filename_list.append(filename)
        elif os.path.isdir(filename):
            for fn in scandir(filename):
                a2l_filename_list.append(fn)
        else:
            pass

    print("run performance test")
    print("measurement: {:s}".format(opt.measurement))
    print("repeat_count: {:d}".format(opt.repeat_count))
    print("")
    for index, a2l_filename in enumerate(a2l_filename_list):
        process_a2l(a2l_filename, opt.measurement, opt.repeat_count, index=index)
