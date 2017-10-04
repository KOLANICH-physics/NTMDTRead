import sys
import os
import re
from pathlib import Path
from glob import glob
import imp
import functools
from collections import defaultdict
import lazy_object_proxy
from ..utils.softwarePaths import softwarePaths
from ..colors import importColorMap

__author__ = "KOLANICH"
__license__ = "Unlicense"
__copyright__ = r"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org/>
"""


def joinPalettesWithSameFileNames(paletteFileNames):
	res = defaultdict(list)
	for p in paletteFileNames:
		res[p.stem].append(p)
	return res


def getPallettesPaths():
	for dirPath in softwarePaths:
		dirPath = dirPath / "palettes"
		if not dirPath.is_dir():
			continue
		yield from dirPath.glob("*.pal")
		yield from dirPath.glob("*.256")


pallettesPaths = lazy_object_proxy.Proxy(getPallettesPaths)
palettesFilesIndex = lazy_object_proxy.Proxy(functools.partial(joinPalettesWithSameFileNames, pallettesPaths))

invalidCharRx = re.compile(r"\W")


def sanitizeName(name):
	return invalidCharRx.sub("", name)


class PaletteImporter:
	marker = __name__

	def parsePath(self, fullName):
		if fullName.startswith(__class__.marker):
			restOfName = fullName.split(".")[2:]
		if len(restOfName) == 0:
			return True
		elif len(restOfName) == 1:
			return {"palette": restOfName[0]}
		elif len(restOfName) == 2:
			return {"palette": restOfName[0], "table": restOfName[1]}
		else:
			return False

	def load_module(self, fullName, *args, **kwargs):
		if fullName is sys.modules:
			return sys.modules[fullName]

		m = imp.new_module(fullName)
		m.__loader__ = self
		m.__path__ = []
		sys.modules[fullName] = m
		restOfName = self.parsePath(fullName)
		if restOfName is True:
			return m

		if "palette" in restOfName and "table" not in restOfName:
			palletteFilePath = palettesFilesIndex[restOfName["palette"]][0]
			res = importColorMap(palletteFilePath)
			m.__path__.append(palletteFilePath)
			for name in res["name"]:
				setattr(m, sanitizeName(name), res["name"][name])
			setattr(m, "index", res["index"])
		elif "palette" in restOfName and "table" in restOfName:
			basePath = __class__.marker + "." + restOfName["palette"]
			if basePath in sys.modules and hasattr(sys.modules[basePath], restOfName["table"]):
				return getattr(sys.modules[basePath], restOfName["table"])
			else:
				res = importColorMap(palettesFilesIndex[restOfName["palette"]][0], (restOfName["palette"],))
				return res["name"][name]

	def find_module(self, fullName, *args, **kwargs):
		if fullName.startswith(__class__.marker):
			restOfName = self.parsePath(fullName)
			if not restOfName:
				raise ImportError("Palette name must be in format " + __class__.marker + ".palette_File_name_without_extension.name_of_palette_from_table")
			if restOfName is True:
				return self
			if "palette" in restOfName and "table" not in restOfName:
				if restOfName["palette"] in palettesFilesIndex:
					return self
				else:
					raise ImportError("Palette file not found")

			elif "palette" in restOfName and "table" in restOfName:
				res = importColorMap(palettesFilesIndex[restOfName["palette"]][0])
				if res["name"] and restOfName["table"]:
					names = {sanitizeName(name) for name in res["name"].keys()}
					if restOfName["table"] in names:
						return self
				else:
					raise ImportError("Palette in file not found")
		return None


sys.meta_path.append(PaletteImporter())
