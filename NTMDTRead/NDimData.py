import numpy as np

from .utils.units import toMag

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


class NDimData:
	def __init__(self, frame, data):
		self._data = data
		self.frame = frame

	def show(self, cmap):
		import matplotlib.pyplot as plt

		if self._data.shape[0] == 1:
			return self.doShow(cmap)
		else:
			fig, axes = plt.subplots(self._data.shape[0])
			for i in range(self._data.shape[0]):
				self.doShow(cmap, i, ax=axes[i])
			return fig, axes


class _Curve(NDimData):
	def doShow(self, cmap, i=0, ax=None):
		import matplotlib.pyplot as plt

		if ax is None:
			fig, ax = plt.subplots()
		else:
			fig = ax.get_figure()
		im = ax.plot(self.x, self.y)
		ax.set_title(self.frame.makePlotTitle())
		ax.set_xlabel(self.size[0])
		ax.set_ylabel(self.size[1])
		#cb=fig.colorbar(im)
		#cb.ax.set_ylabel(str(self.frame.mesurandsSizes[i]))

		fig.tight_layout()
		return fig, ax


class Curve(_Curve):
	@property
	def data(self, i=0):
		return self._data[i]

	@property
	def x(self):
		return np.linspace(0, toMag(self.frame.size[0]), self.y.shape[0])

	@property
	def y(self):
		return self.data[0]

	@property
	def size(self):
		return (self.frame.size[0], self.frame.mesurandsSizes[0])


class XYPoints(_Curve):
	@property
	def data(self, i=0):
		return self._data[i]

	@property
	def x(self):
		return self.data[0]

	@property
	def y(self):
		return self.data[1]

	@property
	def size(self):
		return self.frame.mesurandsSizes


class Image(NDimData):
	def doShow(self, cmap, i=0, ax=None):
		"""Displays a frame, returns an axis and a figure. If cmap is not set, it uses the color map available as colorMap property"""
		import matplotlib.pyplot as plt

		if ax is None:
			fig, ax = plt.subplots()
		else:
			fig = ax.get_figure()

		h_mag = toMag(self.frame.size[0])
		w_mag = toMag(self.frame.size[1])

		im = ax.imshow(np.flip(self._data[i], 0), cmap=cmap, extent=(0, w_mag, 0, h_mag))
		ax.set_title(self.frame.makePlotTitle())
		ax.set_xlabel(self.frame.size[1])
		ax.set_ylabel(self.frame.size[0])
		cb = fig.colorbar(im)
		cb.ax.set_ylabel(str(self.frame.mesurandsSizes[i]))

		fig.tight_layout()
		return fig, ax

	def show3d(self, cmap=None):
		from vispy import app, scene

		#fr.main.frame_data.data, cmap=random.choice(palettes), extent=(0, w_mag, 0, h_mag)
		xs = np.linspace(0, toMag(self.frame.size[0]), self._data.shape[0])
		ys = np.linspace(0, toMag(self.frame.size[1]), self._data.shape[1])

		canvas = scene.SceneCanvas(keys="interactive", title=self.frame.makePlotTitle())
		view = canvas.central_widget.add_view()
		view.camera = scene.TurntableCamera(up="z")

		sfc = scene.visuals.SurfacePlot(x=xs, y=ys, z=self._data)
		#sfc.attach(scene.filters.ZColormapFilter(cmap))
		#sfc.attach(scene.filters.ZColormapFilter("fire"))
		view.add(sfc)

		axis = scene.visuals.XYZAxis(parent=view.scene)
		canvas.show()
		app.run()
