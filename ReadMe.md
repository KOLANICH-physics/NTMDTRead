NTMDTRead
==========
[wheel](https://gitlab.com/KOLANICH1/NTMDTRead/-/jobs/artifacts/master/raw/wheels/NTMDTRead-0.CI-py3-none-any.whl?job=build)
[![PyPi Status](https://img.shields.io/pypi/v/NTMDTRead.svg)](https://pypi.org/pypi/NTMDTRead)
![GitLab Build Status](https://gitlab.com/KOLANICH1/NTMDTRead/badges/master/pipeline.svg)
[![TravisCI Build Status](https://travis-ci.org/KOLANICH/NTMDTRead.svg?branch=master)](https://travis-ci.org/KOLANICH/NTMDTRead)
![GitLab Coverage](https://gitlab.com/KOLANICH1/NTMDTRead/badges/master/coverage.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/NTMDTRead.svg)](https://coveralls.io/r/KOLANICH/NTMDTRead)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/NTMDTRead.svg)](https://libraries.io/github/KOLANICH/NTMDTRead)

An **unofficial** set of tools to read the files produced by [NT-MDT](http://www.ntmdt-si.ru/) software.

* `NTMDTReader` - Reads `.mdt` file format. Not very ready: some files are not read at all, some are read incorrectly, some frames are not yet implemented. But for large share of files it works pretty fine. Since it is based on the [Kaitai Struct](https://github.com/kaitai-io/kaitai_struct) [description](https://github.com/kaitai-io/kaitai_struct_formats/blob/master/scientific/nt_mdt/nt_mdt.ksy) reverse-engineered from [gwyddion implementation](https://svn.code.sf.net/p/gwyddion/code/trunk/gwyddion/modules/file/nt-mdt.c), it is licensed on the terms of [![GNU General Public License v3](https://www.gnu.org/graphics/gplv3-88x31.png)](./gpl-3.0.md). I'm sorry for that I'm too lazy to black box reverse engineer it from scratch entirely.

* `colors` - Reads `.pal` palette files and transforms them into ```matplotlib``` colormaps. Also allows transforming matplotlib colormaps into NT-MDT format for using them in the original software. The format parsing code is based on the Kaitai Struct [description](https://github.com/kaitai-io/kaitai_struct_formats/blob/master/scientific/nt_mdt/nt_mdt_pal.ksy). Its license is [Unlicense](https://unlicense.org/). [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/).

* `palettes` - A convenient importer for palettes. You may prefer to use it instead of ```colors```.
```python
from NTMDTRead.palettes.Rainbows import Rainbow1
from NTMDTRead.palettes import Rainbows
import NTMDTRead.palettes.Rainbows
```
The names under `NTMDTRead.palettes.` are the names of `*.pal` files, and the names under them are the names of palettes in files.
Its license is [Unlicense](https://unlicense.org/). [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/).

* `NTMDTReaderTSV` - Reads TSV file exported by ```Nova``` or ```ImageAnalysis```. The license is [Unlicense](https://unlicense.org/). [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/).

* `examples/` - obviously, contains some usage examples
  * `show.py` contains a very stupid example of a viewer. It loops over all the mdt files in the dir and tries to show them.

  * `matplotlibColorMapConvert.py` converts matplotlib colormaps to the format available for ImageAnalysis/Nova.
    * [matplotlib.pal](https://gitlab.com/KOLANICH1/NTMDTRead/-/jobs/artifacts/master/raw/palletes/matplotlib.pal?job=build). The license of this file is the same as [the one matplotlib has](https://matplotlib.org/users/license.html).
    * [colorcet.pal](https://gitlab.com/KOLANICH1/NTMDTRead/-/jobs/artifacts/master/raw/palletes/colorcet.pal?job=build). The license of this file is the same as [the one colorcet has](https://github.com/bokeh/colorcet/blob/master/LICENSE.txt).
    * [cmocean.pal](https://gitlab.com/KOLANICH1/NTMDTRead/-/jobs/artifacts/master/raw/palletes/cmocean.pal?job=build). The license of this file is the same as [the one cmocean has](https://github.com/matplotlib/cmocean/blob/master/LICENSE.txt).

