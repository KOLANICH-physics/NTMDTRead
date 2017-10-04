import numpy as np
from configobj import ConfigObj
from configobj.validate import Validator

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

cfgspec = ConfigObj(os.path.join(__path__[0], "NT-MDTFileSchema.ini"), list_values=False)


class NTMDTReaderTSV:
	def __init__(self, fileName, sep="\t"):
		self.sep = sep
		with open(fileName, "rb") as f:
			self.lines = f.readlines()

		self.meta = ConfigObj(self.lines, invalid=True, configspec=cfgspec)
		self.meta.validate(Validator())
		# seems like a bug in nt-mdt software:
		# "Table" is actually 2 tables with pair of columns,
		# "Columns" is actually table with all columns
		if self.meta["State"] == "Table":
			self.data = np.vstack((self.readColumnsTSVPart(fileName, "Fw"), self.readColumnsTSVPart(fileName, "Bk", usecols=(1))))
		elif self.meta["State"] == "Row":
			self.data = np.vstack((np.linspace(self.meta["Bias X"], self.meta["Bias X"] + self.meta["Scale X"] * self.meta["FwSize"], num=self.meta["FwSize"]), self.readRowTSVPart(fileName, "Fw"), self.readRowTSVPart(fileName, "Bk")))
		elif self.meta["State"] == "Columns":
			raise NotImplementedError("Because in this case meta is parsed not quite correctly")

		self.scaleData()

		del self.lines

	def readColumnsTSVPart(self, fileName, partName, usecols=None):
		return np.transpose(np.genfromtxt(fileName, usecols=usecols, skip_header=self.meta.lines[partName + "Size"][1] + 1, max_rows=self.meta[partName + "Size"], delimiter=self.sep, invalid_raise=True))

	def readRowTSVPart(self, fileName, partName):
		return np.fromstring(self.lines[self.meta.lines[partName + "Size"][1] + 1], sep=self.sep)

	def readTableTSVPart(self, fileName, partName):
		raise NotImplementedError("Because in this case meta is parsed not quite correctly")

	def scaleData(self):
		if self.meta["DataScaleNeeded"]:
			if self.meta["State"] != "Row":  # in that case the data is generated already scaled
				self.data[0] *= self.meta["Scale X"]
				self.data[0] += self.meta["Bias X"]

			self.data[1:] *= self.meta["Scale Data"]
			self.data[1:] += self.meta["Bias Data"]

			self.meta["DataScaleNeeded"] = False
