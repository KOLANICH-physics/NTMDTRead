# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

from . import ieee754_float
class F10le(KaitaiStruct):
    """see the doc for `ieee754_float`.
    ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff ffffffff ifffffff eeeeeeee seeeeeee
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.frac_lo_lo = self._io.read_u4le()
        self.frac_lo = self._io.read_u2le()
        self.frac_mid = self._io.read_u1()
        self.integer = self._io.read_bits_int_be(1) != 0
        self.frac_hi = self._io.read_bits_int_be(7)
        self._io.align_to_byte()
        self.biased_exponent_lo = self._io.read_u1()
        self.sign = self._io.read_bits_int_be(1) != 0
        self.biased_exponent_hi = self._io.read_bits_int_be(7)

    @property
    def fraction(self):
        if hasattr(self, '_m_fraction'):
            return self._m_fraction if hasattr(self, '_m_fraction') else None

        self._m_fraction = ((((((self.frac_hi << 8) | self.frac_mid) << 16) | self.frac_lo) << 32) | self.frac_lo_lo)
        return self._m_fraction if hasattr(self, '_m_fraction') else None

    @property
    def biased_exponent(self):
        if hasattr(self, '_m_biased_exponent'):
            return self._m_biased_exponent if hasattr(self, '_m_biased_exponent') else None

        self._m_biased_exponent = ((self.biased_exponent_hi << 8) | self.biased_exponent_lo)
        return self._m_biased_exponent if hasattr(self, '_m_biased_exponent') else None

    @property
    def value(self):
        if hasattr(self, '_m_value'):
            return self._m_value if hasattr(self, '_m_value') else None

        _pos = self._io.pos()
        self._io.seek(0)
        self._m_value = ieee754_float.Ieee754Float(((1 << (15 - 1)) - 1), 63, 15, self.sign, self.biased_exponent, self.fraction, self._io)
        self._io.seek(_pos)
        return self._m_value if hasattr(self, '_m_value') else None


