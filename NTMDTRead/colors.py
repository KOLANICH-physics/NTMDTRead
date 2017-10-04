import functools
import sys
from pathlib import Path

import lazy_object_proxy
import numpy as np
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

from .kaitai.nt_mdt_256 import *
from .kaitai.nt_mdt_pal import *
from .kaitaiParseBase import kaitaiParseBase

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


def mplColorMapToRGBAArray(cmap, interpolatedColorsCount: int = None):
	"""Transforms a matplotlib colormap into a RGBA array"""
	if interpolatedColorsCount is None:
		res = cmap(np.arange(cmap.N))
	else:
		res = cmap(np.linspace(0, 1, interpolatedColorsCount))
	res *= 255
	res = np.around(res)
	res = np.array(res, dtype=np.uint8)
	return res


def cmap2ColorTable(arr, title: str = ""):
	"""Transforms a RGBA array into NTMDT color table.
	Since we don't have a serializer in KS, we use the manual one."""
	arr = np.flip(arr, 1)  # abgr
	arr = arr[:, 1:]  # bgr
	arr = np.array(np.hstack((arr, np.zeros((arr.shape[0], 1)))), dtype=np.uint8)  # bgr_unkn

	res = bytearray()
	res += title.encode("UTF-16le")
	arr.shape = (arr.shape[0] * arr.shape[1],)
	res += bytes(arr)
	return res


def makePalMeta(color_table_ptr: int, colors_count: int, title_len: int):
	"""Generates a metadata record for a palette in a pal file.
	Since we don't have a serializer in KS, we use the manual one."""
	from struct import pack

	res = bytearray()
	res += b"\0\0\0"
	res += pack("<I", color_table_ptr)
	res += pack("<I", colors_count)
	res += b"\4"  # unkn11
	res += b"\0\0"  # unkn12
	res += pack(">H", title_len * 2)  # title is utf-16, it's size
	return res


def matplotlibColorMaps2Pal(tables=None):
	"""This function transforms matplotlib colormaps into NTMDT palette *.pal file contents.
	Since we don't have a serializer in KS, we use the manual one."""
	from struct import pack

	if tables is None:
		tables = cm.cmap_d
	elif isinstance(tables, dict):
		tables = tables.values()
	else:
		tables = (tables,)

	tablesCount = len(tables)
	res = bytearray()
	res += b"NT-MDT Palette File  1.00!"  # the signature
	res += pack(">I", tablesCount)
	metaBase = len(res)
	metaSize = len(makePalMeta(0, 0, 0))

	res += b"\0" * metaSize * tablesCount  # reserving space for metas
	res += b"\0\0\0"  # unkn
	for i, cmap in enumerate(tables):
		lastFreeIdx = len(res)
		if isinstance(cmap, str):
			cmap = cm.cmap_d[cmap]
		arr = mplColorMapToRGBAArray(cmap)
		res += cmap2ColorTable(arr, cmap.name)
		metaOffset = metaBase + metaSize * i
		res[metaOffset : metaOffset + metaSize] = makePalMeta(lastFreeIdx, arr.shape[0], len(cmap.name))
	return res


def convertColorTable(table):
	"""Converts a Kaitai Struct-parsed color table to a list of matplotlib color maps"""
	cdict = {
		"red": [],
		"green": [],
		"blue": []
	}
	countOfColors = len(table.colors)
	maxColorIndex = countOfColors - 1
	for i, col in enumerate(table.colors):
		for compName in cdict:
			comp = getattr(col, compName) / 255
			cdict[compName].append((i / maxColorIndex, comp, comp))
	for compName in cdict:
		cdict[compName] = np.array(cdict[compName])
	return LinearSegmentedColormap(table.title, cdict)


def import256ColorMap(palFileName: (str, Path), index: int = None):
	return convertParsed256ColorMapIntoMatplotlib(NtMdt256.from_file(str(palFileName)), index)


def importPalColorMap(palFileName: (str, Path), index: (str, int) = None):
	"""Converts an NT-MDT .pal file into matplotlib colormaps"""
	return convertParsedPalColorMapIntoMatplotlib(NtMdtPal.from_file(str(palFileName)), index)  # using my wrapper here causes io on a closed file, must be fixed!


importFunctionsDispatchDict = {
	".pal": importPalColorMap,
	".256": import256ColorMap
}


def importColorMap(fileName: (str, Path), index=None, *args, **kwargs):
	"""Dispatches on importer function depending on pallette extension"""
	fileName = Path(fileName)
	ext = fileName.ext

	if ext in importFunctionsDispatchDict:
		return importFunctionsDispatchDict[ext](fileName, index, *args, **kwargs)
	else:
		NotImplementedError("For now parsing " + ext + " palettes is not imiplemented yet.")


def convertParsed256ColorMapIntoMatplotlib(parsed, index):
	"""Converts Kaitai Struct parsed colormap into matplotlib colormap"""
	if index is None:
		index = range(len(parsed.color_tables))
	if isinstance(index, (int, str)):
		index = [index]
	res = {"index": {}}
	for i in index:
		table = parsed.color_tables[i].color_table
		converted = lazy_object_proxy.Proxy(functools.partial(convertColorTable, table))
		res["index"][el] = converted
	return res


def convertParsedPalColorMapIntoMatplotlib(parsed, index):
	"""Converts Kaitai Struct parsed colormap into matplotlib colormap"""
	if index is None:
		index = range(len(parsed.meta))
	if isinstance(index, (int, str)):
		index = [index]
	res = {"name": {}, "index": {}}
	nameIndex = {}
	for i, el in enumerate(index):
		if isinstance(el, int):
			pass
		elif isinstance(el, str):
			if not nameIndex:
				nameIndex = {table.title: i for table in enumerate(parsed.meta)}
			el = nameIndex[el]
		table = parsed.meta[el].color_table
		converted = lazy_object_proxy.Proxy(functools.partial(convertColorTable, table))
		res["index"][el] = converted
		res["name"][res["index"][el].name] = converted
	return res
