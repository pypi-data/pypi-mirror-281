# -*- encoding: utf-8 -*-
import dataclasses
import functools
import types
import typing as t
from dataclasses import dataclass

__all__ = [
    "READER",
    "ReadField",
    "parse_field",
]

T = t.TypeVar("T")


READER = t.Callable[[list[str], int, dict], tuple[int, T]]


@dataclass(slots=True)
class ReadField:
    f: dataclasses.Field
    reader: READER
    allow_none: bool = False
    many: bool = False
    extend: bool = False
    size_key: str | None = None


HOOK = t.Callable[[list[str], int, dict, ReadField], tuple[int, T]]


def read_tuple(words: list[str], start: int, context: dict, *, readers: tuple[READER]) -> tuple[int, tuple]:
    vars = []
    for arg in readers:
        start, var = arg(words, start, context)
        vars.append(var)
    return start, tuple(vars)


def read_dataclass(words: list[str], start: int, context: dict, *, clazz: t.Any, readers: tuple[READER]) -> tuple[int, object]:
    vars = []
    for arg in readers:
        start, var = arg(words, start, context)
        vars.append(var)
    return start, clazz(*vars)


def read_list(words: list[str], start: int, context: dict, *, reader: READER, **kwargs) -> tuple[int, list]:
    if start >= len(words):
        return start, []

    if "size" in kwargs and isinstance(kwargs["size"], int):
        size = kwargs["size"]
    elif "size_key" in kwargs and isinstance(kwargs["size_key"], str):
        size = context.get(kwargs["size_key"], None)
    else:
        size = None

    vars = []
    while start < len(words):
        if isinstance(size, int) and len(vars) >= size:
            break
        start, var = reader(words, start, context)
        vars.append(var)
    return start, vars


def read_optional(words: list[str], start: int, context: dict, *, reader: READER) -> tuple[int, list]:
    if start >= len(words):
        return start, None

    return reader(words, start, context)


def find_kwargs(field: dataclasses.Field = None) -> dict[str, t.Any]:
    kwargs: dict = dict()
    if isinstance(field, dataclasses.Field):
        for arg in t.get_args(field.type):
            if isinstance(arg, dict):
                kwargs.update(arg)
        kwargs.update(field.metadata)
    return kwargs


def find_reader(arg: type, reader_dict: dict[type, READER], field: dataclasses.Field = None) -> READER:
    origin = t.get_origin(arg)
    if origin is None:
        if arg in reader_dict:
            return reader_dict[arg]
        elif dataclasses.is_dataclass(arg):
            readers = [find_reader(f.type, reader_dict, field=f) for f in dataclasses.fields(arg)]
            if any((reader is None for reader in readers)):
                return None
            return functools.partial(read_dataclass, clazz=arg, readers=readers)
        else:
            return None
    elif origin == list:
        reader = find_reader(t.get_args(arg)[0], reader_dict)
        if callable(reader):
            return functools.partial(read_list, reader=reader, **find_kwargs(field))
        return None

    elif origin == tuple:
        readers = [find_reader(arg, reader_dict) for arg in t.get_args(arg)]
        if any((reader is None for reader in readers)):
            return None
        return functools.partial(read_tuple, readers=readers)
    else:
        return None


def parse_field(f: dataclasses.Field, ft: type, reader_dict: dict[str, READER]) -> ReadField:
    kwargs: dict = dict()
    for arg in t.get_args(f.type):
        if isinstance(arg, dict):
            kwargs.update(arg)
    kwargs.update(f.metadata)

    # ft = f.type

    origin = t.get_origin(ft)
    while origin and (origin == t.Union or issubclass(origin, types.UnionType)):
        it: type = None
        for arg in t.get_args(ft):
            if issubclass(arg, types.NoneType):
                kwargs.update(allow_none=True)
                continue
            else:
                if it is None:
                    it = arg
                else:
                    raise TypeError(f"unknown field: {f.name}, type={f.type}")
        if it is None:
            raise TypeError(f"unknown field: {f.name}, type={f.type}")

        ft = it
        origin = t.get_origin(ft)

    if origin == list and kwargs.get("many") is True and kwargs.get("extend") is not True:
        ft = t.get_args(ft)[0]
        origin = t.get_origin(ft)

    reader = find_reader(ft, reader_dict, field=f)
    if reader is None:
        raise TypeError(f"unknown field: {f.name}, type={f.type}")

    field = ReadField(f, reader, **kwargs)
    if field.allow_none is True:
        field.reader = functools.partial(read_optional, reader=field.reader)

    for arg in t.get_args(f.type):
        if isinstance(arg, dict):
            if "many" in arg and isinstance(arg["many"], bool):
                field.many = arg["many"]
            if "extend" in arg and isinstance(arg["extend"], bool):
                field.extend = arg["extend"]
            if "size_key" in arg and isinstance(arg["size_key"], str):
                field.size_key = arg["size_key"]
    return field
