# -*- encoding: utf-8 -*-
import typing as t

# Local Modules
from .i18n import _

__all__ = [
    "Error",
    "GrammarError",
    "NotMatch",
    "Unknown",
    "Warn",
]


def Error(*args, code: str | None = None, label_name: str | None = None, **kwargs):
    real_args = []
    code_list: list[str] = []
    if code is not None:
        code_list.append(code)

    for arg in args:
        if isinstance(arg, Exception):
            arg_code = getattr(arg, "code", None)
            if arg_code is not None and arg_code not in code_list:
                code_list.append(arg_code)
        real_args.append(str(arg))

    real_args.extend([f"{_(key)}: {val}" for key, val in kwargs.items()])

    formated_text = ", ".join(real_args)
    if code is not None:
        formated_text = f"{code}: {formated_text}"
    if bool(label_name):
        formated_text = f"{label_name}, {formated_text}"

    err = Exception(formated_text)
    if len(code_list) >= 1:
        setattr(err, "code", code_list[0])
    if bool(label_name):
        setattr(err, "label_name", label_name)

    return err


def Warn(*args, code: str | None = None, label_name: str | None = None, **kwargs):
    real_args = []
    code_list: list[str] = []
    if code is not None:
        code_list.append(code)

    for arg in args:
        if isinstance(arg, Exception):
            arg_code = getattr(arg, "code", None)
            if arg_code is not None and arg_code not in code_list:
                code_list.append(arg_code)
        real_args.append(str(arg))

    real_args.extend([f"{_(key)}: {val}" for key, val in kwargs.items()])

    formated_text = ", ".join(real_args)
    if code is not None:
        formated_text = f"{code}: {formated_text}"
    if bool(label_name):
        formated_text = f"{label_name}, {formated_text}"

    err = Warning(formated_text)
    if code is not None:
        setattr(err, "code", code)
    if bool(label_name):
        setattr(err, "label_name", label_name)

    return err


def NotMatch(key, *args, expect: t.Any = ..., actual: t.Any = ..., **kwargs):
    if expect is not Ellipsis:
        kwargs.update(expect=expect)
    if actual is not Ellipsis:
        kwargs.update(actual=actual)
    return Error(_("{:s} not match").format(str(key)), *args, **kwargs)


def Unknown(key, *args, **kwargs):
    return Error(_("unknown {:s}").format(str(key)), *args, **kwargs)


def GrammarError(*args, code: str = "E03", **kwargs):
    return Error(_("grammar error"), *args, code=code, **kwargs)
