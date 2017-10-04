import numpy as np

from .kaitai.nt_mdt import *
from .kaitaiParseBase import kaitaiParseBase
from .NDimData import *
from .utils.units import *

__author__ = "KOLANICH"
__license__ = "GPL-3.0+"
__copyright__ = r"""Copyright (C) 2004 David Necas (Yeti), Petr Klapetek.
E-mail: yeti@gwyddion.net, klapetek@gwyddion.net.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA."""

# TODO:
# nova has COM interface NT-MDT\Nova\nova.tlb HKEY_LOCAL_MACHINE\SOFTWARE\Classes\TypeLib\{1AFB341D-77DC-4C0C-BD3E-926FE318EB68}\1.0\0\win32

imNumType = np.float64


def parseXML(source):
	import bs4

	return bs4.BeautifulSoup(source, "lxml")


class NTMDTFrame(object):
	def __init__(self, fr):
		super().__init__()
		self._frame = fr
		self._xml = None

	@property
	def xml(self):
		if self._xml is None:
			if hasattr(self._frame.main.frame_data, "xml") and hasattr(self._frame.main.frame_data.xml, "xml"):
				self._xml = parseXML(self._frame.main.frame_data.xml.xml)
			else:
				return None
		return self._xml

	@property
	def title(self):
		if hasattr(self._frame.main.frame_data, "title") and hasattr(self._frame.main.frame_data.title, "title"):
			return self._frame.main.frame_data.title.title
		else:
			return None

	@property
	def dateTime(self):
		from datetime import datetime

		dt = self._frame.main.date_time
		d = dt.date
		t = dt.time
		return datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)

	@property
	def type(self):
		return self._frame.main.type

	def makePlotTitle(self):
		return str(self.reader.fileName) + "\n[" + str(self.index) + "] " + str(self.title) + "\n" + str(self.dateTime) + "\n" + str(self.type)

	def __repr__(self):
		return self.__class__.__name__ + " " + str(self.type) + " " + str(self.date) + " [" + str(self.index) + "]"

	def show(self):
		raise NotImplementedError("Showing is not implemented for frame type " + str(self.type))


class NTMDTTextFrame(NTMDTFrame):
	def __init__(self, fr):
		super().__init__(fr)
		main = fr.main
		data = main.frame_data
		try:
			self.text = parseXML(data.text)
		except BaseException:
			self.text = data.text

	def show(self):
		"""Shows the frame contents on screen"""
		print(self.text)


class NTMDTNDimensionalDataFrame(NTMDTFrame):
	def show(self, cmap=None):
		if cmap is None:
			cmap = self.colorMap
		return self.data.show(cmap=cmap)

	def fixShape(self):
		while len(self.data.shape) < 3:
			self.data.shape = np.insert(self.data.shape, 0, 1)


class NTMDTGraphicFrame(NTMDTNDimensionalDataFrame):
	def __init__(self, fr):
		super().__init__(fr)
		main = fr.main
		data = main.frame_data
		self.data = None
		self.size = None
		self.mesurandsSizes = None
		self._colorMap = None

	def __repr__(self):
		return super().__repr__() + " <" + repr(self.size) + ", (" + repr(self.data.shape) + ")>"

	@property
	def colorMap(self):
		"""Returns the default colormap to display the frame:
		1 if a colormap is embedded into the frame returns it
		2 if it isn't tries to from `.palettes.Stylish import BasicRed`
		3 If it fails too returns None
		"""
		if self._colorMap is None:
			frameSpec = self.frameSpec
			if frameSpec and frameSpec.colors_count:
				from io import BytesIO

				from .colors import convertColorTable
				from .kaitai.nt_mdt_color_table import NtMdtColorTable  # a temporary workaround to KS bug with importing parametric types

				colTable = NtMdtColorTable(frameSpec.colors_count, 0, KaitaiStream(BytesIO(frameSpec.color_scheme)))
				colTable.title = self.title + " color table"
				self._colorMap = convertColorTable(colTable)
			else:
				try:
					from .palettes.Stylish import BasicRed

					self._colorMap = BasicRed
				except BaseException:
					return None
		return self._colorMap


class NTMDTCurveFrame(NTMDTNDimensionalDataFrame):
	def __repr__(self):
		return super().__repr__() + " <" + repr(self.size) + ", (" + repr(self.data.shape) + ")>"

	def __init__(self, fr):
		super().__init__(fr)


class NTMDTMetadataFrame(NTMDTGraphicFrame, NTMDTCurveFrame):
	@property
	def frameSpec(self):
		if hasattr(self._frame.main.frame_data, "frame_spec") and self._frame.main.frame_data.frame_spec:
			return self._frame.main.frame_data.frame_spec
		else:
			return None

	@property
	def title(self):
		return self._frame.main.frame_data.title  # there title len is in header

	def getNDimDataCtor(self):
		cals = self._frame.main.frame_data.calibrations
		if len(self.size) == 2:  # it's an image
			contentType = Image
		elif len(self.size) == 1:
			contentType = Curve
		elif len(self.size) == 0:
			if len(cals.mesurands) == 2:
				contentType = XYPoints
			#elif len(cals.mesurands) == 3:
			#	self.contentType = XYZPoints
		print(self.size, self.mesurandsSizes, self.data.shape, contentType)
		return contentType

	def makePlotTitle(self):
		return super().makePlotTitle()

	def makeSizeQuantity(dim, transform=True):
		try:
			return makeSizeQuantityFromSizeAndUnitName(size=dim.internal.header.semireal, unitName=dim.internal.unit.lower(), transform=transform)
		except BaseException:
			return dim.internal.header.semireal

	def makeSizeQuantities(dims, transform=True):
		return tuple((__class__.makeSizeQuantity(dim, transform) for dim in dims))

	def __init__(self, fr):
		super().__init__(fr)
		main = fr.main
		data = main.frame_data
		cals = data.calibrations

		self.size = __class__.makeSizeQuantities(cals.dimensions)
		self.size = tuple(reversed(self.size))

		self.mesurandsSizes = __class__.makeSizeQuantities(cals.mesurands, False)  # don't transform, otherwise we'll have to transform the image
		print(self.mesurandsSizes)

		self.data = np.array([np.array(cell.values, dtype=imNumType) for cell in data.data.values], dtype=imNumType)
		data._m_data = None  # to free memory, this backs `data`

		shape = [int(dim.internal.header.count) for dim in cals.dimensions]
		shape = list(reversed(shape))
		#print("shape before", shape)

		if not shape:
			shape = self.data.shape
		else:
			shape.append(self.data.shape[-1])

		#print("shape after", shape)

		self.data.shape = shape

		# making measurands index a zero one
		# [0, 1, 2]  -> [1, 0, 2] -> [2, 0, 1]
		# -  -          -     -
		for i in range(1, len(self.data.shape)):
			self.data = np.swapaxes(self.data, 0, i)
			#print("swapped", i, self.data.shape)

		for i, meas in enumerate(cals.mesurands):
			#self.data*=toMag(self.mesurandsSizes[i])
			self.data[i] *= meas.internal.header.scale
			self.data[i] += meas.internal.header.bias

		self.fixShape()
		self.data = self.getNDimDataCtor()(self, self.data)


class NTMDTScannedFrame(NTMDTGraphicFrame, NTMDTCurveFrame):
	@property
	def frameSpec(self):
		if hasattr(self._frame.main.frame_data, "frame_spec_with_size") and hasattr(self._frame.main.frame_data.frame_spec_with_size, "frame_spec"):
			return self._frame.main.frame_data.frame_spec_with_size.frame_spec
		else:
			return None

	def makeSizeQuantity(sizeInDots, scale, transform=True):
		semireal = sizeInDots * scale.step
		try:
			return makeSizeQuantityFromSizeAndUnitName(size=semireal, unitName=enumNameToUnitName(scale.unit.name), transform=transform)
		except BaseException:
			return semireal

	def makeSizeQuantities(sizesInDots, scales, transform=True):
		return tuple((__class__.makeSizeQuantity(*a, transform=transform) for a in zip(sizesInDots, scales)))

	def __init__(self, fr):
		super().__init__(fr)
		main = fr.main
		frame_data = main.frame_data

		self.data = np.array(frame_data.data.data, dtype=imNumType)
		frame_data.data.data = None  # to free memory

		self.data *= frame_data.vars.scales.z.step
		self.data += frame_data.vars.scales.z.offset

		self.data.shape = np.flip(frame_data.data.size.value, 0)
		self.fixShape()

		if self.type == NtMdt.Frame.FrameType.scanned:
			contentType = Image
			xyScales = (frame_data.vars.scales.y, frame_data.vars.scales.x)
			self.size = __class__.makeSizeQuantities(self.data.shape[1:], xyScales)
			self.mesurandsSizes = (unitEnumToPint(frame_data.vars.scales.z.unit),)
		elif self.type == NtMdt.Frame.FrameType.spectroscopy or self.type == NtMdt.Frame.FrameType.curves:
			if self.data.shape[1] == 1:
				contentType = Curve
				self.size = (__class__.makeSizeQuantity(self.data.shape[2], frame_data.vars.scales.x),)
				self.mesurandsSizes = (unitEnumToPint(frame_data.vars.scales.z.unit),)
			elif self.data.shape[1] == 2:
				contentType = XYPoints
				self.size = tuple()
				self.mesurandsSizes = (unitEnumToPint(frame_data.vars.scales.x.unit), unitEnumToPint(frame_data.vars.scales.z.unit))
			#elif self.data.shape[1]==3
			#	self.contentType = XYZPoints

		self.data = contentType(self, self.data)

	@property
	def mode(self):
		if isinstance(self.data, Image):
			return self._frame.main.frame_data.vars.tvars.mode

	@property
	def ADCMode(self):
		if isinstance(self.data, Image):
			return self._frame.main.frame_data.vars.tvars.adc_mode

	@property
	def filter(self):
		if isinstance(self.data, _Curve):
			return self._frame.main.frame_data.vars.tvars.filter  # ?

	@property
	def spMode(self):
		if isinstance(self.data, _Curve):
			return self._frame.main.frame_data.vars.tvars.mode  # ?

	def makePlotTitle(self):
		if isinstance(self.data, Image):
			return super().makePlotTitle() + " " + str(self.mode) + " " + str(self.ADCMode)
		elif isinstance(self.data, _Curve):
			return super().makePlotTitle() + " " + str(self.spMode) + " " + str(self.filter)


framesCtorMap = {
	NtMdt.Frame.FrameType.scanned: NTMDTScannedFrame,
	NtMdt.Frame.FrameType.spectroscopy: NTMDTScannedFrame,
	NtMdt.Frame.FrameType.curves: NTMDTScannedFrame,
	NtMdt.Frame.FrameType.metadata: NTMDTMetadataFrame,
	NtMdt.Frame.FrameType.text: NTMDTTextFrame,
}


class NTMDTReader:
	"""A class to read .mdt files. Wraps Kaitai Struct-generated parser for more convenience."""

	def __init__(self, file: str):
		if isinstance(file, str):
			self.fileName = file
		else:
			self.fileName = None
		#self.parsed=kaitaiParseBase(NtMdt, file)
		self.parsed = NtMdt.from_file(file)  # problems with closed files
		self.frames = []
		for i, fr in enumerate(self.parsed.frames.frames):
			fr = self.makeFrame(fr)
			fr.index = i
			fr.reader = self
			self.frames.append(fr)

	def getCtor(fr):
		tp = fr.main.type
		if tp in framesCtorMap:
			return framesCtorMap[tp]
		else:
			return NTMDTFrame

	def makeFrame(self, fr):
		return self.__class__.getCtor(fr)(fr)
