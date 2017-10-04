import mmap
from pathlib import Path

from _io import _IOBase
from kaitaistruct import KaitaiStream

__author__ = "KOLANICH"
__license__ = "Unlicense"
__copyright__ = r"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org/>
"""


def kaitaiParseBase(cls: type, data: (str, Path, _IOBase, KaitaiStream)):
	"""Parses a Kaitai Struct type"""
	if isinstance(data, str):
		return kaitaiParseBase(cls, Path(data))
	elif isinstance(data, Path):
		with data.open("rb") as f:
			return kaitaiParseBase(cls, f)
	elif isinstance(data, _IOBase):
		with mmap.mmap(data.fileno(), 0, access=mmap.ACCESS_READ) as data:  # causes hang?
			return kaitaiParseBase(cls, data)
	elif isinstance(data, KaitaiStream):
		return cls(data)
	else:
		with KaitaiStream(data) as data:
			return kaitaiParseBase(cls, data)
