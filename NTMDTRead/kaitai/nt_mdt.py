# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

from . import f10le
from . import nt_mdt_color_table
class NtMdt(KaitaiStruct):
    """A native file format of NT-MDT scientific software. Usually contains
    any of:
    
    * [Scanning probe](https://en.wikipedia.org/wiki/Scanning_probe_microscopy) microscopy scans and spectra
    * [Raman spectra](https://en.wikipedia.org/wiki/Raman_spectroscopy)
    * results of their analysis
    
    Some examples of mdt files can be downloaded at:
    
    * http://www.ntmdt-si.ru/scan-gallery
    * http://callistosoft.narod.ru/Resources/Mdt.zip
    
    .. seealso::
       Source - https://svn.code.sf.net/p/gwyddion/code/trunk/gwyddion/modules/file/nt-mdt.c
    """

    class AdcMode(Enum):
        height = 0
        dfl = 1
        lateral_f = 2
        bias_v = 3
        current = 4
        fb_out = 5
        mag = 6
        mag_sin = 7
        mag_cos = 8
        rms = 9
        calc_mag = 10
        phase1 = 11
        phase2 = 12
        calc_phase = 13
        ex1 = 14
        ex2 = 15
        hv_x = 16
        hv_y = 17
        snap_back = 18
        false = 255

    class XmlScanLocation(Enum):
        hlt = 0
        hlb = 1
        hrt = 2
        hrb = 3
        vlt = 4
        vlb = 5
        vrt = 6
        vrb = 7

    class DataType(Enum):
        floatfix = -65544
        float80 = -16138
        float64 = -13320
        float48 = -9990
        float32 = -5892
        int64 = -8
        int32 = -4
        int16 = -2
        int8 = -1
        unknown0 = 0
        uint8 = 1
        uint16 = 2
        uint32 = 4
        uint64 = 8

    class XmlParamType(Enum):
        none = 0
        laser_wavelength = 1
        units = 2
        data_array = 255

    class SpmMode(Enum):
        constant_force = 0
        contact_constant_height = 1
        contact_error = 2
        lateral_force = 3
        force_modulation = 4
        spreading_resistance_imaging = 5
        semicontact_topography = 6
        semicontact_error = 7
        phase_contrast = 8
        ac_magnetic_force = 9
        dc_magnetic_force = 10
        electrostatic_force = 11
        capacitance_contrast = 12
        kelvin_probe = 13
        constant_current = 14
        barrier_height = 15
        constant_height = 16
        afam = 17
        contact_efm = 18
        shear_force_topography = 19
        sfom = 20
        contact_capacitance = 21
        snom_transmission = 22
        snom_reflection = 23
        snom_all = 24
        snom = 25

    class Unit(Enum):
        raman_shift = -10
        reserved0 = -9
        reserved1 = -8
        reserved2 = -7
        reserved3 = -6
        meter = -5
        centi_meter = -4
        milli_meter = -3
        micro_meter = -2
        nano_meter = -1
        angstrom = 0
        nano_ampere = 1
        volt = 2
        none = 3
        kilo_hertz = 4
        degrees = 5
        percent = 6
        celsius_degree = 7
        volt_high = 8
        second = 9
        milli_second = 10
        micro_second = 11
        nano_second = 12
        counts = 13
        pixels = 14
        reserved_sfom0 = 15
        reserved_sfom1 = 16
        reserved_sfom2 = 17
        reserved_sfom3 = 18
        reserved_sfom4 = 19
        ampere2 = 20
        milli_ampere = 21
        micro_ampere = 22
        nano_ampere2 = 23
        pico_ampere = 24
        volt2 = 25
        milli_volt = 26
        micro_volt = 27
        nano_volt = 28
        pico_volt = 29
        newton = 30
        milli_newton = 31
        micro_newton = 32
        nano_newton = 33
        pico_newton = 34
        reserved_dos0 = 35
        reserved_dos1 = 36
        reserved_dos2 = 37
        reserved_dos3 = 38
        reserved_dos4 = 39
        unknown87 = 87

    class SpmTechnique(Enum):
        contact_mode = 0
        semicontact_mode = 1
        tunnel_current = 2
        snom = 3

    class Consts(Enum):
        frame_mode_size = 8
        frame_header_size = 22
        axis_scales_size = 30
        file_header_size = 32
        spectro_vars_min_size = 38
        scan_vars_min_size = 77
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.signature = self._io.read_bytes(4)
        if not self.signature == b"\x01\xB0\x93\xFF":
            raise kaitaistruct.ValidationNotEqualError(b"\x01\xB0\x93\xFF", self.signature, self._io, u"/seq/0")
        self.size = self._io.read_u4le()
        self.reserved0 = self._io.read_bytes(4)
        self.last_frame_index = self._io.read_u2le()
        self.reserved1 = self._io.read_bytes(18)
        self.wrong_doc = self._io.read_bytes(1)
        self._raw_frames = self._io.read_bytes(self.size)
        _io__raw_frames = KaitaiStream(BytesIO(self._raw_frames))
        self.frames = NtMdt.Framez(_io__raw_frames, self, self._root)

    class Uuid(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = [None] * (16)
            for i in range(16):
                self.data[i] = self._io.read_u1()



    class Framez(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.frames = [None] * ((self._root.last_frame_index + 1))
            for i in range((self._root.last_frame_index + 1)):
                self.frames[i] = NtMdt.Frame(self._io, self, self._root)



    class Placeholder(KaitaiStruct):
        """needed only to have _io."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._unnamed0 = self._io.read_bytes_full()


    class Frame(KaitaiStruct):

        class FrameType(Enum):
            scanned = 0
            spectroscopy = 1
            text = 3
            old_metadata = 105
            metadata = 106
            palette = 107
            curves_new = 190
            curves = 201
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u4le()
            self._raw_main = self._io.read_bytes((self.size - 4))
            _io__raw_main = KaitaiStream(BytesIO(self._raw_main))
            self.main = NtMdt.Frame.FrameMain(_io__raw_main, self, self._root)

        class FrameMain(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.type = KaitaiStream.resolve_enum(NtMdt.Frame.FrameType, self._io.read_u2le())
                self.version = NtMdt.Version(self._io, self, self._root)
                self.date_time = NtMdt.Frame.DateTime(self._io, self, self._root)
                self.var_size = self._io.read_u2le()
                _on = self.type
                if _on == NtMdt.Frame.FrameType.metadata:
                    self._raw_frame_data = self._io.read_bytes_full()
                    _io__raw_frame_data = KaitaiStream(BytesIO(self._raw_frame_data))
                    self.frame_data = NtMdt.Frame.FrameMain.MetaData(_io__raw_frame_data, self, self._root)
                elif _on == NtMdt.Frame.FrameType.curves_new:
                    self._raw_frame_data = self._io.read_bytes_full()
                    _io__raw_frame_data = KaitaiStream(BytesIO(self._raw_frame_data))
                    self.frame_data = NtMdt.Frame.FrameMain.CurvesNew(_io__raw_frame_data, self, self._root)
                elif _on == NtMdt.Frame.FrameType.text:
                    self._raw_frame_data = self._io.read_bytes_full()
                    _io__raw_frame_data = KaitaiStream(BytesIO(self._raw_frame_data))
                    self.frame_data = NtMdt.Frame.FrameMain.Text(_io__raw_frame_data, self, self._root)
                elif _on == NtMdt.Frame.FrameType.curves:
                    self._raw_frame_data = self._io.read_bytes_full()
                    _io__raw_frame_data = KaitaiStream(BytesIO(self._raw_frame_data))
                    self.frame_data = NtMdt.Frame.FrameMain.Scanned(_io__raw_frame_data, self, self._root)
                elif _on == NtMdt.Frame.FrameType.spectroscopy:
                    self._raw_frame_data = self._io.read_bytes_full()
                    _io__raw_frame_data = KaitaiStream(BytesIO(self._raw_frame_data))
                    self.frame_data = NtMdt.Frame.FrameMain.Scanned(_io__raw_frame_data, self, self._root)
                elif _on == NtMdt.Frame.FrameType.scanned:
                    self._raw_frame_data = self._io.read_bytes_full()
                    _io__raw_frame_data = KaitaiStream(BytesIO(self._raw_frame_data))
                    self.frame_data = NtMdt.Frame.FrameMain.Scanned(_io__raw_frame_data, self, self._root)
                else:
                    self.frame_data = self._io.read_bytes_full()

            class CurvesNew(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.block_count = self._io.read_u4le()
                    self.blocks_headers = [None] * (self.block_count)
                    for i in range(self.block_count):
                        self.blocks_headers[i] = NtMdt.Frame.FrameMain.CurvesNew.BlockDescr(self._io, self, self._root)

                    self.blocks_names = [None] * (self.block_count)
                    for i in range(self.block_count):
                        self.blocks_names[i] = (self._io.read_bytes(self.blocks_headers[i].name_len)).decode(u"UTF-8")

                    self.blocks_data = [None] * (self.block_count)
                    for i in range(self.block_count):
                        self.blocks_data[i] = self._io.read_bytes(self.blocks_headers[i].len)


                class BlockDescr(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.name_len = self._io.read_u4le()
                        self.len = self._io.read_u4le()



            class MetaData(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.head_size = self._io.read_u4le()
                    self._raw_header = self._io.read_bytes((self.head_size - 4))
                    _io__raw_header = KaitaiStream(BytesIO(self._raw_header))
                    self.header = NtMdt.Frame.FrameMain.MetaData.Header(_io__raw_header, self, self._root)
                    self.title = (self._io.read_bytes(self.header.name_size)).decode(u"UTF-8")
                    self.xml = (self._io.read_bytes(self.header.comm_size)).decode(u"UTF-8")
                    if self.header.spec_size != 0:
                        self._raw_frame_spec = self._io.read_bytes(self.header.spec_size)
                        _io__raw_frame_spec = KaitaiStream(BytesIO(self._raw_frame_spec))
                        self.frame_spec = NtMdt.Frame.FrameSpec(_io__raw_frame_spec, self, self._root)

                    self.view_info = self._io.read_bytes(self.header.view_info_size)
                    self.source_info = self._io.read_bytes(self.header.source_info_size)
                    self.total_size = self._io.read_u4le()
                    self.calibrations = NtMdt.Frame.FrameMain.MetaData.Calibrations(self._io, self, self._root)

                class Header(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.tot_len = self._io.read_u4le()
                        self.guids = [None] * (2)
                        for i in range(2):
                            self.guids[i] = NtMdt.Uuid(self._io, self, self._root)

                        self.frame_status = self._io.read_bytes(4)
                        self.name_size = self._io.read_u4le()
                        self.comm_size = self._io.read_u4le()
                        self.view_info_size = self._io.read_u4le()
                        self.spec_size = self._io.read_u4le()
                        self.source_info_size = self._io.read_u4le()
                        self.var_size = self._io.read_u4le()
                        self.data_offset = self._io.read_u4le()
                        self.data_size = self._io.read_u4le()


                class Calibrations(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.header_len = self._io.read_u4le()
                        self._raw_header = self._io.read_bytes(self.header_len)
                        _io__raw_header = KaitaiStream(BytesIO(self._raw_header))
                        self.header = NtMdt.Frame.FrameMain.MetaData.Calibrations.Header(_io__raw_header, self, self._root)
                        self.dimensions = [None] * (self.header.n_dimensions)
                        for i in range(self.header.n_dimensions):
                            self.dimensions[i] = NtMdt.Frame.FrameMain.MetaData.Calibrations.Calibration(self._io, self, self._root)

                        self.mesurands = [None] * (self.header.n_mesurands)
                        for i in range(self.header.n_mesurands):
                            self.mesurands[i] = NtMdt.Frame.FrameMain.MetaData.Calibrations.Calibration(self._io, self, self._root)


                    class Header(KaitaiStruct):
                        def __init__(self, _io, _parent=None, _root=None):
                            self._io = _io
                            self._parent = _parent
                            self._root = _root if _root else self
                            self._read()

                        def _read(self):
                            self.array_size = self._io.read_u8le()
                            self.cell_size = self._io.read_u4le()
                            self.n_dimensions = self._io.read_u4le()
                            self.n_mesurands = self._io.read_u4le()


                    class Calibration(KaitaiStruct):
                        def __init__(self, _io, _parent=None, _root=None):
                            self._io = _io
                            self._parent = _parent
                            self._root = _root if _root else self
                            self._read()

                        def _read(self):
                            self.len_tot = self._io.read_u4le()
                            self.internal = NtMdt.Frame.FrameMain.MetaData.Calibrations.Calibration.CalibrationInternal(self._io, self, self._root)

                        class CalibrationInternal(KaitaiStruct):
                            def __init__(self, _io, _parent=None, _root=None):
                                self._io = _io
                                self._parent = _parent
                                self._root = _root if _root else self
                                self._read()

                            def _read(self):
                                self.len_header = self._io.read_u4le()
                                self._raw_header = self._io.read_bytes(self.len_header)
                                _io__raw_header = KaitaiStream(BytesIO(self._raw_header))
                                self.header = NtMdt.Frame.FrameMain.MetaData.Calibrations.Calibration.CalibrationInternal.Header(_io__raw_header, self, self._root)
                                self.name = (self._io.read_bytes(self.header.len_name)).decode(u"utf-8")
                                self.comment = (self._io.read_bytes(self.header.len_comment)).decode(u"utf-8")
                                self.unit = (self._io.read_bytes(self.header.len_unit)).decode(u"cp1251")
                                self.author = (self._io.read_bytes(self.header.len_author)).decode(u"utf-8")

                            class Header(KaitaiStruct):

                                class UnitSiCode(Enum):
                                    none = 1
                                    meter = 257
                                    ampere2 = 1048577
                                    second = 16777217
                                    volt2 = 1099461362176
                                def __init__(self, _io, _parent=None, _root=None):
                                    self._io = _io
                                    self._parent = _parent
                                    self._root = _root if _root else self
                                    self._read()

                                def _read(self):
                                    self.len_name = self._io.read_u4le()
                                    self.len_comment = self._io.read_u4le()
                                    self.len_unit = self._io.read_u4le()
                                    self.unit_si_code = KaitaiStream.resolve_enum(NtMdt.Frame.FrameMain.MetaData.Calibrations.Calibration.CalibrationInternal.Header.UnitSiCode, self._io.read_u8le())
                                    self.accuracy = self._io.read_f8le()
                                    self.function_id_and_dimensions = self._io.read_u8le()
                                    self.bias = self._io.read_f8le()
                                    self.scale = self._io.read_f8le()
                                    self._raw_min_index_placeholder = self._io.read_bytes(8)
                                    _io__raw_min_index_placeholder = KaitaiStream(BytesIO(self._raw_min_index_placeholder))
                                    self.min_index_placeholder = NtMdt.Placeholder(_io__raw_min_index_placeholder, self, self._root)
                                    self._raw_max_index_placeholder = self._io.read_bytes(8)
                                    _io__raw_max_index_placeholder = KaitaiStream(BytesIO(self._raw_max_index_placeholder))
                                    self.max_index_placeholder = NtMdt.Placeholder(_io__raw_max_index_placeholder, self, self._root)
                                    self.data_type = KaitaiStream.resolve_enum(NtMdt.DataType, self._io.read_s4le())
                                    self.len_author = self._io.read_u4le()
                                    self.garbage = self._io.read_bytes_full()

                                @property
                                def min_index(self):
                                    if hasattr(self, '_m_min_index'):
                                        return self._m_min_index if hasattr(self, '_m_min_index') else None

                                    io = self.min_index_placeholder._io
                                    _pos = io.pos()
                                    io.seek(0)
                                    self._m_min_index = NtMdt.Scalar(self.data_type, io, self, self._root)
                                    io.seek(_pos)
                                    return self._m_min_index if hasattr(self, '_m_min_index') else None

                                @property
                                def max_index(self):
                                    if hasattr(self, '_m_max_index'):
                                        return self._m_max_index if hasattr(self, '_m_max_index') else None

                                    io = self.max_index_placeholder._io
                                    _pos = io.pos()
                                    io.seek(0)
                                    self._m_max_index = NtMdt.Scalar(self.data_type, io, self, self._root)
                                    io.seek(_pos)
                                    return self._m_max_index if hasattr(self, '_m_max_index') else None

                                @property
                                def count(self):
                                    if hasattr(self, '_m_count'):
                                        return self._m_count if hasattr(self, '_m_count') else None

                                    self._m_count = ((self.max_index.value - self.min_index.value) + 1)
                                    return self._m_count if hasattr(self, '_m_count') else None

                                @property
                                def semireal(self):
                                    if hasattr(self, '_m_semireal'):
                                        return self._m_semireal if hasattr(self, '_m_semireal') else None

                                    self._m_semireal = (self.scale * (self.count - 1))
                                    return self._m_semireal if hasattr(self, '_m_semireal') else None





                class Data(KaitaiStruct):
                    """a vector of data."""
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.values = []
                        i = 0
                        while not self._io.is_eof():
                            self.values.append(NtMdt.Frame.FrameMain.MetaData.Data.Cell(self._io, self, self._root))
                            i += 1


                    class Cell(KaitaiStruct):
                        def __init__(self, _io, _parent=None, _root=None):
                            self._io = _io
                            self._parent = _parent
                            self._root = _root if _root else self
                            self._read()

                        def _read(self):
                            self.values = [None] * (self._parent._parent.calibrations.header.n_mesurands)
                            for i in range(self._parent._parent.calibrations.header.n_mesurands):
                                _on = self._parent._parent.calibrations.mesurands[i].internal.header.data_type
                                if _on == NtMdt.DataType.uint64:
                                    self.values[i] = self._io.read_u8le()
                                elif _on == NtMdt.DataType.uint8:
                                    self.values[i] = self._io.read_u1()
                                elif _on == NtMdt.DataType.float32:
                                    self.values[i] = self._io.read_f4le()
                                elif _on == NtMdt.DataType.int8:
                                    self.values[i] = self._io.read_s1()
                                elif _on == NtMdt.DataType.uint16:
                                    self.values[i] = self._io.read_u2le()
                                elif _on == NtMdt.DataType.int64:
                                    self.values[i] = self._io.read_s8le()
                                elif _on == NtMdt.DataType.float80:
                                    self.values[i] = f10le.F10le(self._io)
                                elif _on == NtMdt.DataType.uint32:
                                    self.values[i] = self._io.read_u4le()
                                elif _on == NtMdt.DataType.float64:
                                    self.values[i] = self._io.read_f8le()
                                elif _on == NtMdt.DataType.int16:
                                    self.values[i] = self._io.read_s2le()
                                elif _on == NtMdt.DataType.int32:
                                    self.values[i] = self._io.read_s4le()




                @property
                def data(self):
                    if hasattr(self, '_m_data'):
                        return self._m_data if hasattr(self, '_m_data') else None

                    io = self._root._io
                    _pos = io.pos()
                    io.seek(self.header.data_offset)
                    self._raw__m_data = io.read_bytes(self.header.data_size)
                    _io__raw__m_data = KaitaiStream(BytesIO(self._raw__m_data))
                    self._m_data = NtMdt.Frame.FrameMain.MetaData.Data(_io__raw__m_data, self, self._root)
                    io.seek(_pos)
                    return self._m_data if hasattr(self, '_m_data') else None


            class Scanned(KaitaiStruct):

                class Mode(Enum):
                    stm = 0
                    afm = 1
                    unknown2 = 2
                    unknown3 = 3
                    unknown4 = 4
                    unknown5 = 5

                class InputSignal(Enum):
                    extension_slot = 0
                    bias_v = 1
                    ground = 2

                class LiftMode(Enum):
                    step = 0
                    fine = 1
                    slope = 2
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self._raw_vars = self._io.read_bytes(self._parent.var_size)
                    _io__raw_vars = KaitaiStream(BytesIO(self._raw_vars))
                    self.vars = NtMdt.Frame.FrameMain.Scanned.Vars(_io__raw_vars, self, self._root)
                    if False:
                        self.orig_format = self._io.read_u4le()

                    if False:
                        self.tune = KaitaiStream.resolve_enum(NtMdt.Frame.FrameMain.Scanned.LiftMode, self._io.read_u4le())

                    if False:
                        self.feedback_gain = self._io.read_f8le()

                    if False:
                        self.dac_scale = self._io.read_s4le()

                    if False:
                        self.overscan = self._io.read_s4le()

                    self.data = NtMdt.Frame.FrameMain.Scanned.Data(self._io, self, self._root)
                    if self._io.size() >= (self._io.pos() + 4):
                        self.title = NtMdt.Title(self._io, self, self._root)

                    if self._io.size() >= (self._io.pos() + 4):
                        self.xml = NtMdt.Xml(self._io, self, self._root)

                    if self._io.size() >= (self._io.pos() + 4):
                        self.unkn = self._io.read_u4le()

                    if self._io.size() >= (self._io.pos() + 4):
                        self.frame_spec_with_size = NtMdt.Frame.FrameMain.Scanned.FrameSpecWithSize(self._io, self, self._root)

                    if self._io.size() >= (self._io.pos() + 4):
                        self.unkn1 = self._io.read_u4le()

                    if self._io.size() >= (self._io.pos() + 4):
                        self.additional_guids = NtMdt.Frame.AdditionalGuids(self._io, self, self._root)


                class Dot(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.x = self._io.read_s2le()
                        self.y = self._io.read_s2le()


                class Vars(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.scales = NtMdt.Frame.Scales(self._io, self, self._root)
                        _on = self._parent._parent.type
                        if _on == NtMdt.Frame.FrameType.scanned:
                            self.tvars = NtMdt.Frame.FrameMain.Scanned.Vars.Image(self._io, self, self._root)
                        elif _on == NtMdt.Frame.FrameType.spectroscopy:
                            self.tvars = NtMdt.Frame.FrameMain.Scanned.Vars.Curve(self._io, self, self._root)
                        elif _on == NtMdt.Frame.FrameType.curves:
                            self.tvars = NtMdt.Frame.FrameMain.Scanned.Vars.Curve(self._io, self, self._root)

                    class Image(KaitaiStruct):
                        def __init__(self, _io, _parent=None, _root=None):
                            self._io = _io
                            self._parent = _parent
                            self._root = _root if _root else self
                            self._read()

                        def _read(self):
                            self.adc_mode = KaitaiStream.resolve_enum(NtMdt.AdcMode, self._io.read_u1())
                            self.mode = KaitaiStream.resolve_enum(NtMdt.Frame.FrameMain.Scanned.Mode, self._io.read_u1())
                            self.size = NtMdt.Vec2U2(self._io, self, self._root)
                            self.ndacq = self._io.read_u2le()
                            self.step_length = self._io.read_f4le()
                            self.adt = self._io.read_u2le()
                            self.adc_gain_amp_log10 = self._io.read_u1()
                            self.adc_index = self._io.read_u1()
                            self.input_signal_or_version = self._io.read_u1()
                            self.substr_plane_order_or_pass_num = self._io.read_u1()
                            self.scan_dir = NtMdt.Frame.FrameMain.Scanned.ScanDir(self._io, self, self._root)
                            self.power_of_2 = self._io.read_u1()
                            self.velocity = self._io.read_f4le()
                            self.setpoint = self._io.read_f4le()
                            self.bias_voltage = self._io.read_f4le()
                            self.draw = self._io.read_u1()
                            self.reserved = self._io.read_u1()
                            self.xoff = self._io.read_s4le()
                            self.yoff = self._io.read_s4le()
                            self.nl_corr = self._io.read_u1()
                            self.unkn1 = self._io.read_u2le()
                            self.unkn2 = self._io.read_u2le()
                            self.feedback_gain = self._io.read_f4le()
                            self.unkn3 = self._io.read_bytes(((4 * 16) + 4))
                            self.generator_freq_sweep_range = [None] * (2)
                            for i in range(2):
                                self.generator_freq_sweep_range[i] = self._io.read_f4le()

                            self.generator_freq = self._io.read_f4le()
                            self.generator_amplitude = self._io.read_f4le()
                            self.unkn4 = self._io.read_bytes(4)
                            self.unkn5 = self._io.read_f4le()
                            self.generator_phase = self._io.read_f4le()
                            self.sd_gain = self._io.read_f4le()
                            self.unkn6 = self._io.read_bytes(((2 * 16) + 10))
                            self.unkn7 = self._io.read_f4le()
                            self.unkn8 = self._io.read_f4le()
                            self.unkn9 = self._io.read_f4le()
                            self.unkn10 = self._io.read_f4le()
                            self.unkn11 = self._io.read_bytes(16)
                            self.unkn12 = self._io.read_f4le()


                    class Curve(KaitaiStruct):
                        def __init__(self, _io, _parent=None, _root=None):
                            self._io = _io
                            self._parent = _parent
                            self._root = _root if _root else self
                            self._read()

                        def _read(self):
                            self.mode = self._io.read_u2le()
                            self.filter = self._io.read_u2le()
                            self.u_begin = self._io.read_f4le()
                            self.u_end = self._io.read_f4le()
                            self.z_up = self._io.read_s2le()
                            self.z_down = self._io.read_s2le()
                            self.averaging = self._io.read_u2le()
                            self.repeat = self._io.read_u1()
                            self.back = self._io.read_u1()
                            self.sp_4nx = self._io.read_s2le()
                            self.osc = self._io.read_u1()
                            self.n4 = self._io.read_u1()
                            self.sp_4x0 = self._io.read_f4le()
                            self.sp_4xr = self._io.read_f4le()
                            self.sp_4u = self._io.read_s2le()
                            self.sp_4i = self._io.read_s2le()
                            self.nx = self._io.read_s2le()



                class Data(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.mode = self._io.read_u2le()
                        self.size = NtMdt.Vec2U2(self._io, self, self._root)
                        self.dots = NtMdt.Frame.FrameMain.Scanned.Data.Dots(self._io, self, self._root)
                        self.data = [None] * ((self.size.x * self.size.y))
                        for i in range((self.size.x * self.size.y)):
                            self.data[i] = self._io.read_s2le()


                    class Dots(KaitaiStruct):
                        def __init__(self, _io, _parent=None, _root=None):
                            self._io = _io
                            self._parent = _parent
                            self._root = _root if _root else self
                            self._read()

                        def _read(self):
                            self.count = self._io.read_u2le()
                            if self.count > 0:
                                self.header = NtMdt.Frame.FrameMain.Scanned.Data.Dots.Header(self._io, self, self._root)

                            self.coordinates = [None] * (self.count)
                            for i in range(self.count):
                                self.coordinates[i] = NtMdt.Frame.FrameMain.Scanned.Data.Dots.Data(self._io, self, self._root)

                            self.data = [None] * (self.count)
                            for i in range(self.count):
                                self.data[i] = NtMdt.Frame.FrameMain.Scanned.Data.Dots.DataLine(i, self._io, self, self._root)


                        class Header(KaitaiStruct):
                            def __init__(self, _io, _parent=None, _root=None):
                                self._io = _io
                                self._parent = _parent
                                self._root = _root if _root else self
                                self._read()

                            def _read(self):
                                self.size = self._io.read_s4le()
                                self._raw_header = self._io.read_bytes(self.size)
                                _io__raw_header = KaitaiStream(BytesIO(self._raw_header))
                                self.header = NtMdt.Frame.FrameMain.Scanned.Data.Dots.Header.Internal(_io__raw_header, self, self._root)

                            class Internal(KaitaiStruct):
                                def __init__(self, _io, _parent=None, _root=None):
                                    self._io = _io
                                    self._parent = _parent
                                    self._root = _root if _root else self
                                    self._read()

                                def _read(self):
                                    self.coord_size = self._io.read_s4le()
                                    self.version = self._io.read_s4le()
                                    self.xyunits = KaitaiStream.resolve_enum(NtMdt.Unit, self._io.read_s2le())



                        class Data(KaitaiStruct):
                            def __init__(self, _io, _parent=None, _root=None):
                                self._io = _io
                                self._parent = _parent
                                self._root = _root if _root else self
                                self._read()

                            def _read(self):
                                self.coords = [None] * (2)
                                for i in range(2):
                                    self.coords[i] = self._io.read_f4le()

                                self.forward_size = self._io.read_s4le()
                                self.backward_size = self._io.read_s4le()

                            @property
                            def x(self):
                                if hasattr(self, '_m_x'):
                                    return self._m_x if hasattr(self, '_m_x') else None

                                self._m_x = self.coords[0]
                                return self._m_x if hasattr(self, '_m_x') else None

                            @property
                            def y(self):
                                if hasattr(self, '_m_y'):
                                    return self._m_y if hasattr(self, '_m_y') else None

                                self._m_y = self.coords[1]
                                return self._m_y if hasattr(self, '_m_y') else None


                        class DataLine(KaitaiStruct):
                            def __init__(self, index, _io, _parent=None, _root=None):
                                self._io = _io
                                self._parent = _parent
                                self._root = _root if _root else self
                                self.index = index
                                self._read()

                            def _read(self):
                                self.forward = [None] * (self._parent.coordinates[self.index].forward_size)
                                for i in range(self._parent.coordinates[self.index].forward_size):
                                    self.forward[i] = self._io.read_s2le()

                                self.backward = [None] * (self._parent.coordinates[self.index].backward_size)
                                for i in range(self._parent.coordinates[self.index].backward_size):
                                    self.backward[i] = self._io.read_s2le()





                class ScanDir(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.unkn = self._io.read_bits_int_be(4)
                        self.double_pass = self._io.read_bits_int_be(1) != 0
                        self.bottom = self._io.read_bits_int_be(1) != 0
                        self.left = self._io.read_bits_int_be(1) != 0
                        self.horizontal = self._io.read_bits_int_be(1) != 0


                class FrameSpecWithSize(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.size = self._io.read_u4le()
                        if self.size != 0:
                            self._raw_frame_spec = self._io.read_bytes(self.size)
                            _io__raw_frame_spec = KaitaiStream(BytesIO(self._raw_frame_spec))
                            self.frame_spec = NtMdt.Frame.FrameSpec(_io__raw_frame_spec, self, self._root)




            class Text(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.size = self._io.read_u4le()
                    self.unkn0 = self._io.read_u4le()
                    self.vars = self._io.read_bytes(self._parent.var_size)
                    self.text = (KaitaiStream.bytes_terminate(self._io.read_bytes(self.size), 0, False)).decode(u"cp1251")
                    if self._io.size() >= (self._io.pos() + 4):
                        self.title = NtMdt.Title(self._io, self, self._root)

                    if self._io.size() >= (self._io.pos() + 4):
                        self.xml = NtMdt.Xml(self._io, self, self._root)

                    if self._io.size() >= (self._io.pos() + 4):
                        self.unkn1 = self._io.read_u4le()

                    if self._io.size() >= (self._io.pos() + 4):
                        self.unkn2 = self._io.read_u4le()

                    if self._io.size() >= (self._io.pos() + 4):
                        self.unkn3 = self._io.read_u4le()

                    if self._io.size() >= (self._io.pos() + 4):
                        self.additional_guids = NtMdt.Frame.AdditionalGuids(self._io, self, self._root)




        class AdditionalGuids(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.size = self._io.read_u4le()
                if self.size != 0:
                    self._raw_guids = self._io.read_bytes(self.size)
                    _io__raw_guids = KaitaiStream(BytesIO(self._raw_guids))
                    self.guids = NtMdt.Frame.AdditionalGuids.Guids(_io__raw_guids, self, self._root)


            class Guids(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.guids = []
                    i = 0
                    while not self._io.is_eof():
                        self.guids.append(NtMdt.Uuid(self._io, self, self._root))
                        i += 1




        class Scales(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.scales = [None] * (3)
                for i in range(3):
                    self.scales[i] = NtMdt.Frame.Scales.AxisScale(self._io, self, self._root)


            class AxisScale(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.offset = self._io.read_f4le()
                    self.step = self._io.read_f4le()
                    self.unit = KaitaiStream.resolve_enum(NtMdt.Unit, self._io.read_s2le())


            @property
            def x(self):
                if hasattr(self, '_m_x'):
                    return self._m_x if hasattr(self, '_m_x') else None

                self._m_x = self.scales[0]
                return self._m_x if hasattr(self, '_m_x') else None

            @property
            def y(self):
                if hasattr(self, '_m_y'):
                    return self._m_y if hasattr(self, '_m_y') else None

                self._m_y = self.scales[1]
                return self._m_y if hasattr(self, '_m_y') else None

            @property
            def z(self):
                if hasattr(self, '_m_z'):
                    return self._m_z if hasattr(self, '_m_z') else None

                self._m_z = self.scales[2]
                return self._m_z if hasattr(self, '_m_z') else None


        class DateTime(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.date = NtMdt.Frame.DateTime.Date(self._io, self, self._root)
                self.time = NtMdt.Frame.DateTime.Time(self._io, self, self._root)

            class Date(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.year = self._io.read_u2le()
                    self.month = self._io.read_u2le()
                    self.day = self._io.read_u2le()


            class Time(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.hour = self._io.read_u2le()
                    self.minute = self._io.read_u2le()
                    self.second = self._io.read_u2le()



        class FrameSpec(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.unkn = self._io.read_bytes(((8 * 16) + 8))
                self.colors_count = self._io.read_u4le()
                self._raw_color_scheme = self._io.read_bytes_full()
                _io__raw_color_scheme = KaitaiStream(BytesIO(self._raw_color_scheme))
                self.color_scheme = nt_mdt_color_table.NtMdtColorTable(self.colors_count, 0, _io__raw_color_scheme)



    class Vec2U2(KaitaiStruct):
        """usually sizes of the image."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.value = [None] * (2)
            for i in range(2):
                self.value[i] = self._io.read_u2le()


        @property
        def x(self):
            if hasattr(self, '_m_x'):
                return self._m_x if hasattr(self, '_m_x') else None

            self._m_x = self.value[0]
            return self._m_x if hasattr(self, '_m_x') else None

        @property
        def y(self):
            if hasattr(self, '_m_y'):
                return self._m_y if hasattr(self, '_m_y') else None

            self._m_y = self.value[1]
            return self._m_y if hasattr(self, '_m_y') else None


    class Version(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.minor = self._io.read_u1()
            self.major = self._io.read_u1()


    class Scalar(KaitaiStruct):
        def __init__(self, type, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.type = type
            self._read()

        def _read(self):
            _on = self.type
            if _on == NtMdt.DataType.uint64:
                self.value = self._io.read_u8le()
            elif _on == NtMdt.DataType.uint8:
                self.value = self._io.read_u1()
            elif _on == NtMdt.DataType.float32:
                self.value = self._io.read_f4le()
            elif _on == NtMdt.DataType.int8:
                self.value = self._io.read_s1()
            elif _on == NtMdt.DataType.uint16:
                self.value = self._io.read_u2le()
            elif _on == NtMdt.DataType.int64:
                self.value = self._io.read_s8le()
            elif _on == NtMdt.DataType.uint32:
                self.value = self._io.read_u4le()
            elif _on == NtMdt.DataType.float64:
                self.value = self._io.read_f8le()
            elif _on == NtMdt.DataType.int16:
                self.value = self._io.read_s2le()
            elif _on == NtMdt.DataType.int32:
                self.value = self._io.read_s4le()


    class Xml(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.xml_len = self._io.read_u4le()
            self.xml = (self._io.read_bytes(self.xml_len)).decode(u"UTF-16LE")


    class Title(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.title_len = self._io.read_u4le()
            self.title = (self._io.read_bytes(self.title_len)).decode(u"cp1251")



