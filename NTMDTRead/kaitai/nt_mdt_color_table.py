# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class NtMdtColorTable(KaitaiStruct):
    """It is a reusable part of a color scheme for visualising SPM scans."""
    def __init__(self, colors_count, title_len, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.colors_count = colors_count
        self.title_len = title_len
        self._read()

    def _read(self):
        self.title = (self._io.read_bytes(self.title_len)).decode(u"UTF-16")
        self.colors = [None] * (self.colors_count)
        for i in range(self.colors_count):
            self.colors[i] = NtMdtColorTable.Color(self._io, self, self._root)


    class Color(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.blue = self._io.read_u1()
            self.green = self._io.read_u1()
            self.red = self._io.read_u1()
            self.alpha = self._io.read_u1()



