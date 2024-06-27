# -*- encoding: utf-8 -*-
import array
import codecs
import hashlib
import json
import typing as t

import chardet

__all__ = [
    "JsonEncoder",
    "calc_sha1_bytes",
    "contain_error",
    "read_file",
]


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dict):
            return {k: v for k, v in obj.items() if v is not None}
        if isinstance(obj, bytes):
            return obj.hex()
        if isinstance(obj, array.array):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def read_file(fn_or_content: t.Union[bytes, str], encoding: str | None = None) -> tuple[bytes, str, str]:
    if isinstance(fn_or_content, bytes):
        content = fn_or_content
    elif isinstance(fn_or_content, str):
        with open(fn_or_content, "rb") as f:
            content = f.read()
    else:
        raise Exception("read_file fail, unsupported type: {:s}").format(type(fn_or_content))

    if len(content) == 0:
        raise Exception("read_file fail, file is empty")

    if content.startswith(codecs.BOM_UTF8):
        data = content[len(codecs.BOM_UTF8) :]
        encoding = "utf-8"
    else:
        data = content

    text: str | None = None
    offset: int = 0
    encoding_dict: dict[str, int] = dict()
    while text is None:
        if encoding is None:
            ret = chardet.detect(data[offset : offset + 16 * 1024])
            encoding = ret.get("encoding") or ""
            if encoding.upper() in ("ISO-8859-1",):
                encoding = "windows-1252"
            if encoding.upper() in ("ASCII",):
                encoding = "utf-8"
            if encoding.upper() in ("GB2312", "GB18030"):
                encoding = "gbk"

        try:
            if encoding in encoding_dict:
                encoding_dict[encoding] += 1
            else:
                encoding_dict[encoding] = 1

            if encoding_dict[encoding] > 3:
                text = data.decode(encoding, errors="replace")
            else:
                text = data.decode(encoding)
        except UnicodeDecodeError as err:
            offset = err.start - 4
            if offset >= len(data) or err.start < offset:
                raise err
            else:
                offset = err.start - 4
                if offset < 0:
                    offset = 0
                encoding = None

    return content, text, encoding or ""


def calc_sha1_bytes(content: t.Union[bytes, str], *args) -> bytes:
    calc = hashlib.sha1()
    if isinstance(content, str):
        content = content.encode()
    calc.update(content)
    calc.update(len(content).to_bytes(4, "big"))
    for arg in args:
        if bool(arg):
            calc.update(str(arg).encode())
    return calc.digest()


def contain_error(
    err_list: list[Exception],
    code: str | None = None,
    warning: bool | None = None,
    label_name: str | None = None,
    include: str | None = None,
):
    def match(e: Exception) -> bool:
        if label_name is not None and label_name != getattr(e, "label_name", None):
            return False

        if code is not None and code != getattr(e, "code", None):
            return False

        if include is not None and str(e).find(include) == -1:
            return False

        if warning is True and not isinstance(e, Warning):
            return False

        if warning is False and isinstance(e, Warning):
            return False

        return True

    return any((match(e) for e in err_list))
