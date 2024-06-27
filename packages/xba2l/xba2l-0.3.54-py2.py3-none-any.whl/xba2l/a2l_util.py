# -*- encoding: utf-8 -*-
# Local Modules
from xba2l.a2l import a2l_reader
from xba2l.a2l_base import Options
from xba2l.a2l_lib import Asap2, Module
from xba2l.etc.options import OptionsUtil

__all__ = [
    "parse_a2l",
]


def parse_a2l(fn_or_content: str | bytes, encoding: str | None = None, options: Options | None = None) -> tuple[Exception | None, Asap2 | None, Module | None]:
    return a2l_reader.parse_a2l(fn_or_content, encoding=encoding, opts=OptionsUtil.from_options(options))
