# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

from . import nt_mdt_color_table
class NtMdtPal(KaitaiStruct):
    """It is a color scheme for visualising SPM scans."""
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.signature = self._io.read_bytes(26)
        if not self.signature == b"\x4E\x54\x2D\x4D\x44\x54\x20\x50\x61\x6C\x65\x74\x74\x65\x20\x46\x69\x6C\x65\x20\x20\x31\x2E\x30\x30\x21":
            raise kaitaistruct.ValidationNotEqualError(b"\x4E\x54\x2D\x4D\x44\x54\x20\x50\x61\x6C\x65\x74\x74\x65\x20\x46\x69\x6C\x65\x20\x20\x31\x2E\x30\x30\x21", self.signature, self._io, u"/seq/0")
        self.count = self._io.read_u4be()
        self.meta = [None] * (self.count)
        for i in range(self.count):
            self.meta[i] = NtMdtPal.Meta(self._io, self, self._root)

        self.unkn = self._io.read_bytes(3)

    class Meta(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unkn00 = self._io.read_bytes(3)
            self.color_table_ptr = self._io.read_u4le()
            self.colors_count = self._io.read_u4le()
            self.unkn11 = self._io.read_bytes(1)
            self.unkn12 = self._io.read_bytes(2)
            self.title_len = self._io.read_u2be()

        @property
        def color_table(self):
            if hasattr(self, '_m_color_table'):
                return self._m_color_table if hasattr(self, '_m_color_table') else None

            io = self._root._io
            _pos = io.pos()
            io.seek(self.color_table_ptr)
            self._m_color_table = nt_mdt_color_table.NtMdtColorTable(self.colors_count, self.title_len, io)
            io.seek(_pos)
            return self._m_color_table if hasattr(self, '_m_color_table') else None



