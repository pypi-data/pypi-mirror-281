# -*- encoding: utf-8 -*-
import dataclasses
import os
import re
from dataclasses import dataclass

# Local Modules
from xba2l.etc import GrammarError, NotMatch, OptionsUtil, tool

__all__ = ["read_a2l", "A2lNode"]


@dataclass(slots=True)
class A2lNode:
    key: str
    lineno: int
    words: list[str] = dataclasses.field(default_factory=list)
    children: list["A2lNode"] = dataclasses.field(default_factory=list)


def process(r: str, opts: OptionsUtil) -> A2lNode:
    a = A2lNode("", 0)
    c = a
    s = []
    t = False
    h = False
    i = 0

    l = 0

    b = 0

    im = opts.ignore_measurements

    def analyze(w):
        nonlocal h, t, c, i
        if h is True:
            h = False
            if w == "A2ML" or w == "IF_DATA" or (im and w == "MEASUREMENT"):
                i = i + 1

            n = A2lNode(w, l)
            if i == 0:
                c.children.append(n)
            s.append(c)
            c = n
        elif t is True:
            t = False
            if w != c.key:
                raise NotMatch("keyword", expect=c.key, actual=w, lineno=l + 1)
            c = s.pop()
            if i > 0:
                i = i - 1
        elif w == "/begin":
            h = True
        elif w == "/end":
            t = True
        else:
            if i == 0:
                c.words.append(w)

    cp = re.compile("[ \r\n\t\x0b\x0c]+")

    def split(words: str):
        for w in filter(lambda x: x, re.split(cp, words)):
            if len(w):
                analyze(w)
        return words.count("\n")

    p1 = r.find("/*", b)
    p2 = r.find("//", b)
    p3 = r.find('"', b)
    while True:
        if p3 >= 0 and (p3 < p1 or p1 == -1) and (p3 < p2 or p2 == -1):
            if p3 > b:
                # for w in filter(lambda x: x, re.split(cp, r[b:p3])):
                #     analyze(w)
                l += split(r[b:p3])
            n = r.find('"', p3 + 1)
            while n >= 0:
                m = n - 1
                while m > 0:
                    if r[m] == "\\"[0]:
                        m = m - 1
                    else:
                        break
                if (n - 1 - m) & 1 == 1:
                    n = r.find('"', n + 1)
                    continue
                if n + 1 < len(r) and r[n + 1] == '"'[0]:
                    n = r.find('"', n + 2)
                    continue
                break
            if n >= 0:
                l = l + r[p3 + 1 : n].count("\n")
                c.words.append(r[p3 + 1 : n])
                b = n + 1
            else:
                break
        elif p1 >= 0 and (p1 < p2 or p2 == -1) and (p1 < p3 or p3 == -1):
            if p1 > b:
                # for w in filter(lambda x: x, re.split(cp, r[b:p1])):
                #     analyze(w)
                l += split(r[b:p1])
            n = r.find("*/", p1 + 2)
            if n > 0:
                l = l + r[p1 + 2 : n].count("\n")
                b = n + 2
            else:
                break
        elif p2 >= 0 and (p2 < p1 or p1 == -1) and (p2 < p3 or p3 == -1):
            if p2 > b:
                # for w in filter(lambda x: x, re.split(cp, r[b:p2])):
                #     analyze(w)
                l += split(r[b:p2])
            n = r.find("\n", p2 + 2)
            if n > 0:
                l = l + 1
                b = n + 1
            else:
                break
        else:
            # for w in filter(lambda x: x, re.split(cp, r[b:])):
            #     analyze(w)
            l += split(r[b:])
            break

        if p1 >= 0 and p1 < b:
            p1 = r.find("/*", b)
        if p2 >= 0 and p2 < b:
            p2 = r.find("//", b)
        if p3 >= 0 and p3 < b:
            p3 = r.find('"', b)

    return a


def read_a2l(
    fn_or_content: str | bytes,
    opts: OptionsUtil,
    encoding: str | None,
    a2l_hash: bytes | None = None,
) -> tuple[Exception | None, bytes | None, A2lNode, str]:
    try:
        content, text, encoding = tool.read_file(fn_or_content, encoding=encoding)
        if a2l_hash is None:
            a2l_hash = tool.calc_sha1_bytes(content)
        del content
        root = process(text, opts)
        del text
        return None, a2l_hash, root, encoding
    except Exception as err:
        return GrammarError(err, opts=dataclasses.asdict(opts), encoding=encoding), a2l_hash, None, encoding


if __name__ == "__main__":
    a2l_filename = "tests\\example\\ASAP2_Demo_V171.a2l"

    if os.path.isfile(a2l_filename):
        err, a2l_hash, root, encoding = read_a2l(a2l_filename, encoding=None)
