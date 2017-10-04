__all__ = ("enumNameToUnitName", "unitNameToPint", "unitEnumToPint", "makeSizeQuantityFromSizeAndUnitName", "toMag")
import re
from pathlib import Path

import pint

thisDir = Path(__file__).parent
unitsFilePath = thisDir / "units.txt"

ureg = pint.UnitRegistry(default_as_delta=True, autoconvert_offset_to_baseunit=True)
ureg.load_definitions(str(unitsFilePath))
ureg.default_format = "~P"

digitRx = re.compile(r"\d")


def enumNameToUnitName(name: str):
	name = digitRx.sub("", name)
	name = name.replace("_", "")
	return name


unitsEnumPintMapping = {}


def unitNameToPint(unitName: str):
	try:
		return getattr(ureg, unitName)
	except Exception as ex:
		return ureg.parse_expression(unitName)


def unitEnumToPint(enumValue):
	"""Converts a member of NtMdt.Unit into a ```pint``` unit"""
	if enumValue not in unitsEnumPintMapping:
		unitsEnumPintMapping[enumValue] = unitNameToPint(enumNameToUnitName(enumValue.name))
	return unitsEnumPintMapping[enumValue]


def makeSizeQuantityFromSizeAndUnitName(size, unitName, transform=True):
	try:
		size *= unitNameToPint(unitName)
		if transform:
			size = size.to_base_units().to_compact()
	except BaseException as ex:
		pass
	return size


def toMag(dimensional):
	if hasattr(dimensional, "magnitude"):
		return dimensional.magnitude
	else:
		return dimensional
