"""
setup.py -- setup script for use of packages.
"""
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
import os
import sys

__version__ = '1.5.0'
__here__ = os.path.abspath(os.path.dirname(__file__))

class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


ext_modules = [
    Extension(
        'blimpy_read_module',
        sources=[
            'src/bound_reader.cpp',
        ],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
            os.path.join(__here__, 'src'),
        ],
        extra_compile_args = ['-fPIC', '-fopenmp', '-std=c++14'],
        language='c++'
    ),
]

# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.
    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support '
                           'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)



with open("README.md", "r") as fh:
    long_description = fh.read()

# create entry points
# see http://astropy.readthedocs.org/en/latest/development/scripts.html
entry_points = {
    'console_scripts' : [
        'filutil = blimpy.filterbank:cmd_tool',
        'watutil = blimpy.waterfall:cmd_tool',
        'rawutil = blimpy.guppi:cmd_tool',
        'fil2h5 = blimpy.fil2h5:cmd_tool',
        'h52fil = blimpy.h52fil:cmd_tool',
        'matchfils = blimpy.match_fils:cmd_tool',
        'bldice = blimpy.dice:cmd_tool'
     ]
}

install_requires = [
        'matplotlib<3.0;python_version=="2.7"',
        'matplotlib;python_version>"2.7"',
        'astropy<3.0;python_version=="2.7"',
        'astropy;python_version>"2.7"',
        'numpy',
        'cython',
        'h5py',
        'scipy',
        'six',
        'hdf5plugin'
]

extras_require = {
        'full': [
            'bitshuffle',
            'pyslalib',
        ]
}

setup(name='blimpy',
      version=__version__,
      description='Python utilities for Breakthrough Listen SETI observations',
      long_description=long_description,
      long_description_content_type='text/markdown',
      platform=['*nix'],
      license='BSD',
      install_requires=install_requires,
      extras_require=extras_require,
      url='https://github.com/ucberkeleyseti/blimpy',
      author='Danny Price, Emilio Enriquez, Yuhong Chen, Mark Siebert, and BL contributors',
      author_email='dancpr@berkeley.edu',
      entry_points=entry_points,
      packages=find_packages(),
      zip_safe=False,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.7',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Topic :: Scientific/Engineering :: Astronomy',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      test_suite="blimpytests",
      ext_modules = ext_modules,
      cmdclass={'build_ext': BuildExt},
)
