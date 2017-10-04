__all__ = ("softwarePaths",)
# HKEY_CLASSES_ROOT\TypeLib\{1AFB341D-77DC-4C0C-BD3E-926FE318EB68}\1.0\0\win32
# HKEY_CLASSES_ROOT\Image Analysis
# HKEY_CLASSES_ROOT\MDT\Shell\Open\Command

import os
import winreg
from pathlib import Path

import lazy_object_proxy


def fileTypeOpenRegKeyToExecutablePath(key: tuple):
	return next((p for p in key[0].split('"') if p and os.path.exists(p)))


def getNTMDTSoftwarePathsFromRegistry():
	fileTypesClassesNames = [
		"Image Analysis",
		"MDT",
		r"Applications\Nova.exe",
		r"Applications\IA_P9.exe"
	]
	for classname in fileTypesClassesNames:
		try:
			with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, classname + r"\shell\open\command", 0, winreg.KEY_READ) as reg:
				yield Path(fileTypeOpenRegKeyToExecutablePath(winreg.QueryValueEx(reg, ""))).parent
		except BaseException:
			pass


softwarePaths = lazy_object_proxy.Proxy(lambda: set(getNTMDTSoftwarePathsFromRegistry()))
