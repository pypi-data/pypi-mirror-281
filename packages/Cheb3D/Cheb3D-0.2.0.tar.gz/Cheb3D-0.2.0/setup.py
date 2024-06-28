
from setuptools import Extension, setup
from Cython.Build import cythonize
import os
from sys import platform


app_dir = 'Cheb3D'

files = ["PyNumSpec.pyx",
         "funccoefs.cpp",
	 "funcder.cpp" ,
	 "funcmath.cpp" ,
	 "funcspec.cpp" ,
	 "funcspec_interp.cpp" ,
	 #"ppl.cpp" ,
	 "tabmath.cpp" ,
	 "tabspec.cpp",
         ]

sources = [ f"{app_dir}/{ii}" for ii in files]

# Detect OS
if platform == 'darwin':  # macOS
    fftw_include_dir = "/usr/local/include"
    fftw_lib_dir = "/usr/local/lib"
elif platform == 'linux':  # Linux
    fftw_include_dir = "/usr/include"
    fftw_lib_dir = "/usr/lib"
else:
    raise RuntimeError(f"Unsupported platform: {sys.platform}")


os.environ["CC"] = "gcc"
os.environ["CXX"] = "g++"

extensions = [
    Extension(
        name="Cheb3D.PyNumSpec",  # library name
        sources=sources,
        include_dirs=[app_dir,fftw_include_dir],  # where to find .h files
        library_dirs=[fftw_lib_dir],
        language="c++",
        undef_macros = [ "NDEBUG" ],
        libraries=['fftw3'],  # add here libraries FFTW3
    )
]

setup(
    name="Cheb3D",
    version="0.2.0",
    author="Marco Mancini",
    author_email="marco.mancini@obspm.fr",
    description="Description du package Cheb3D",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    ext_modules=cythonize(extensions),
    packages=["Cheb3D"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
