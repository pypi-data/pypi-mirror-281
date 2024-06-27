# -*- encoding: utf-8 -*-
import dataclasses
import os
from dataclasses import dataclass

# Local Modules
from xba2l.a2l_base import Options

__all__ = [
    "OptionsUtil",
]


@dataclass(kw_only=True)
class OptionsUtil(Options):
    def __add__(self, other: "OptionsUtil") -> "OptionsUtil":
        kwargs: dict = {}
        for f in dataclasses.fields(OptionsUtil):
            v1 = getattr(self, f.name)
            v2 = getattr(other, f.name)
            if v2 == f.default:
                kwargs.update({f.name: v1})
            else:
                kwargs.update({f.name: v2})
        opts = OptionsUtil(**kwargs)
        return opts

    def asdict(self, exclude_defaults: bool = True) -> dict:
        if exclude_defaults is True:
            return {f.name: getattr(self, f.name) for f in dataclasses.fields(self) if f.default != getattr(self, f.name)}
        else:
            return {f.name: getattr(self, f.name) for f in dataclasses.fields(self)}

    @staticmethod
    def from_options(options: Options | None = None) -> "OptionsUtil":
        if isinstance(options, Options):
            return OptionsUtil.from_dict(dataclasses.asdict(options))
        else:
            return OptionsUtil.from_dict()

    @staticmethod
    def from_dict(options: dict | None = None) -> "OptionsUtil":
        data = dict()
        for f in dataclasses.fields(OptionsUtil):
            if f.init is False:
                continue
            key = "XBA2L_{:s}".format(f.name.upper())
            if key in os.environ:
                if issubclass(f.type, int) and os.environ[key].isdigit():
                    data.update({f.name: int(os.environ[key])})
                elif issubclass(f.type, float):
                    try:
                        data.update({f.name: float(os.environ[key])})
                    except:
                        pass
                elif issubclass(f.type, bool) and os.environ[key].upper() in ["TRUE", "1", "-1"]:
                    data.update({f.name: True})
                elif issubclass(f.type, bool) and os.environ[key].upper() in ["FALSE", "0"]:
                    data.update({f.name: False})
                elif issubclass(f.type, str):
                    data.update({f.name: os.environ[key]})
                else:
                    pass

        if isinstance(options, dict):
            data.update(options)

        kwargs = dict()
        for f in dataclasses.fields(OptionsUtil):
            if f.init is False:
                continue
            val = data.get(f.name, None)
            if isinstance(val, f.type):
                kwargs.update({f.name: val})

        return OptionsUtil(**kwargs)
