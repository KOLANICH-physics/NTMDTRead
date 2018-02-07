import sys, os
import random
from pathlib import Path

import matplotlib.pyplot as plt
import scipy as np
from vispy import app, scene

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


currentDir = Path(__file__).parent.absolute()
baseDir = currentDir.parent.absolute()
sys.path.insert(0, str(baseDir))

from NTMDTRead.NTMDTReader import NTMDTReader

testDataDir = baseDir / "test_data"

# you can import pallettes this way:
from NTMDTRead.palettes.Rainbows import Rainbow1
from NTMDTRead.palettes.Stylish import BasicRed
palettes = [Rainbow1, BasicRed]


def plot3d(m, bn):
	for i, fr in enumerate(m.parsed.frames.frames):
		#fr.main.frame_data.image, cmap=random.choice(palettes), extent=(0, w_mag, 0, h_mag)
		xs = np.linspace(0, 1, fr.main.frame_data.image.shape[0])
		ys = np.linspace(0, 1, fr.main.frame_data.image.shape[1])

		canvas = scene.SceneCanvas(keys="interactive", title=bn)
		view = canvas.central_widget.add_view()
		view.camera = scene.TurntableCamera(up="z")

		# Simple surface plot example
		# x, y values are not specified, so assumed to be 0:50
		p1 = scene.visuals.SurfacePlot(
			x=xs, y=ys,
			z=fr.main.frame_data.image
			#,shading='smooth'
		)
		#p1.attach(scene.filters.ZColormapFilter(random.choice(palettes)))
		#p1.attach(scene.filters.ZColormapFilter("fire"))
		view.add(p1)

		# Add a 3D axis to keep us oriented
		axis = scene.visuals.XYZAxis(parent=view.scene)
		canvas.show()
		app.run()


def processFilesFromTestFolder(mdts, moveBad=None, saveImages=None):
	"""Shows frames from scans and moves badly parsed ones into a specified folder for investigation"""
	for fn in mdts:
		print(str(fn))
		dir = fn.parent
		bn = fn.name
		try:
			m = NTMDTReader(str(fn))
			for i, fr in enumerate(m.frames):
				pass
				#print(fr.xml)
				res = fr.show()
				if res:
					fig, ax = res
					fig.show()
					plt.show(block=True)
		except Exception as ex:
			print("failed:", ex)
			if moveBad:
				badPath = dir / moveBad / bn
				os.rename(str(fn), str(badPath))


if __name__ == "__main__":
	#testOnFiles(moveBad="bad")
	print(__license__)
	globExpr = "./*.mdt"
	if not globExpr.endswith(".mdt"):
		globExpr = os.path.join(dir, "*.mdt")
	mdts = testDataDir.glob(globExpr)
	if not mdts:
		print("No files were selected!")
	mdts = list(mdts)
	#mdts=mdts[12:]
	#print(mdts)
	workingDir = Path(".").absolute()
	mdts = (fn.relative_to(workingDir) for fn in mdts)
	processFilesFromTestFolder(mdts)
