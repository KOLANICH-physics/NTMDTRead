# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class NtMdt256(KaitaiStruct):
    """It is an old format for a color scheme for visualising SPM scans."""
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.color_tables = []
        i = 0
        while not self._io.is_eof():
            self.color_tables.append(NtMdt256.ColorTable(self._io, self, self._root))
            i += 1


    class ColorTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.colors = [None] * (85)
            for i in range(85):
                self.colors[i] = NtMdt256.Color(self._io, self, self._root)

            self._unnamed1 = self._io.read_bytes(1)


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



