[![Build Status](https://github.com/UCBerkeleySETI/blimpy/workflows/Test%20Blimpy/badge.svg)](https://github.com/UCBerkeleySETI/blimpy/actions)
[![Documentation Status](https://readthedocs.org/projects/blimpy/badge/?version=latest)](https://blimpy.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/UCBerkeleySETI/blimpy/branch/master/graph/badge.svg)](https://codecov.io/gh/UCBerkeleySETI/blimpy)
 [![JOSS status](http://joss.theoj.org/papers/e58ef21f0a924041bf9438fd75f8aed0/status.svg)](http://joss.theoj.org/papers/e58ef21f0a924041bf9438fd75f8aed0)

# Breakthrough Listen I/O Methods for Python

## Introduction
This README file details the installation instructions for Breakthrough Listen I/O Methods for Python (blimpy). Developers should also read [CODE_OF_CONDUCT](https://github.com/UCBerkeleySETI/blimpy/CODE_OF_CONDUCT.md) and [CONTRIBUTING](https://github.com/UCBerkeleySETI/blimpy/CONTRIBUTING.md).

### Filterbank + Raw file readers
This repository contains Python 2/3 readers for interacting with [Sigproc filterbank](http://sigproc.sourceforge.net/sigproc.pdf) (.fil), HDF5 (.h5) and [guppi raw](https://baseband.readthedocs.io/en/stable/guppi/) (.raw) files, as used in the [Breakthrough Listen](https://seti.berkeley.edu) search for intelligent life.

## Installation

### System Dependencies
The installation can fail if a system dependency is not installed. Please refer to the [dependencies.txt](https://github.com/UCBerkeleySETI/blimpy/dependencies.txt)  file for a list of system dependencies.

#### Debian/Ubuntu
For Debian/Ubuntu systems, make sure that `curl` installed and you have `sudo` access. Install the required system dependencies with the follwoing command:
```
curl https://raw.githubusercontent.com/UCBerkeleySETI/blimpy/master/dependencies.txt | xargs -n 1 sudo apt install --no-install-recommends -y
```

### Python Dependencies
blimpy requires `numpy`, `h5py`, `astropy`, `scipy`, `hdf5plugin`and `matplotlib` packages and will attempt to automatically install them.

Please note when undertaking an installation h5py generally needs to be installed using the following:
```
$ python3 -m pip install --no-binary=h5py h5py

```

### PyPI Installation

#### User based installation
```
python3 -m pip install blimpy --user
```

#### System wide installation
```
sudo python3 -m pip install blimpy
```

#### (Optional) Install the latest release from the repository
The latest release can be installed via `pip` directly from this repository:
```
python3 -m pip install -U git+https://github.com/UCBerkeleySETI/blimpy
```

### Developer Installation
The latest version of the development code can be installed from cloning the github [repo](https://github.com/UCBerkeleySETI/blimpy) and then run:

#### User based installation
```
python3 setup.py install --user
```

#### System wide installation
```
sudo python3 setup.py install
```

#### (Optional) Install using PyPI
```
python3 -m pip install -U https://github.com/UCBerkeleySETI/blimpy/tarball/master
```

### Unit tests
To install packages needed to run the unit tests, use the following:

#### User based installation
```
python3 -m pip install --user --no-use-pep517 -e '.[full]'
```

#### System wide installation
```
sudo python3 -m pip install -e '.[full]'
```

## Using blimpy inside Docker
The blimpy Docker images are pushed to a public repository after each successful build on Travis.

If you have Docker installed, you can run the following commands to pull our images, which have the environment and dependencies all ready set up.

`docker pull fx196/blimpy:py3_kern_stable`

Here is a [more complete guide](./docker_guide.md) on using blimpy in Docker.

## Command line utilities
After installation, some command line utilities will be installed:
* `watutil`, Read/write/plot an .h5 file or a .fil file.
* `rawutil`, Plot data in a guppi raw file.
* `fil2h5`, Convert a .fil file into .h5 format.
* `h52fil`, Convert an .h5 file into .fil format.
* `bldice`, Dice a smaller frequency region from (either from/to .h5 or .fil).
* `matchfils`, Check if two .fil files are the same.
* `calcload`, Calculate the Waterfall max_load value needed to load the data array for a given file.
* `rawhdr`, Display the header fields of a raw guppi file.

Use the `-h` flag to any of the above command line utilities to display their available arguments.

## Reading blimpy filterbank files in .fil or .h5 format
The `blimpy.Waterfall`  provides a Python API for interacting with filterbank data. It supports all BL filterbank data products; see this [example Jupyter notebook](https://github.com/UCBerkeleySETI/blimpy/blob/master/examples/voyager.ipynb) for an overview.

From the python, ipython or jupiter notebook environments.

```python
from blimpy import Waterfall
fb = Waterfall('/path/to/filterbank.fil')
#fb = Waterfall('/path/to/filterbank.h5') #works the same way
fb.info()
data = fb.data
```

## Reading guppi raw files
The [Guppi Raw format](https://github.com/UCBerkeleySETI/breakthrough/blob/master/doc/RAW-File-Format.md) can be read using the `GuppiRaw` class from `guppi.py`:

```python
from blimpy import GuppiRaw
gr = GuppiRaw('/path/to/guppirawfile.raw')

header, data = gr.read_next_data_block()
```

or

```python
from blimpy import GuppiRaw
gr = GuppiRaw('/path/to/guppirawfile.raw')

for header, data_x, data_y in gr.get_data():
    # process data
```

Note: most users should start analysis with filterbank files, which are smaller in size and have been generated from the guppi raw files.

## Further reading
A detailed overview of the data formats used in Breakthrough Listen can be found in our [data format paper](https://ui.adsabs.harvard.edu/abs/2019arXiv190607391L/abstract). 

## Data archive
An archive of data files from the Breakthrough Listen program is provided at [seti.berkeley.edu/opendata](http://seti.berkeley.edu/opendata).

## If you have any requests or questions, please lets us know!
