# Cheb3D library

## Installation

### Compile the C++ library

- Install the package [fftw3](https://www.fftw.org/) (devel version).
- Compile the library
```bash
cd Chab3D/Lib
make
```

### Create a virtual environment and source it
```bash
cd ..
python -m virtualenv venv
source venv/bin/activate
pip install cython
```

### Cythonize the library
```bash
python setup.py build_ext --inplace
```


### Test it
```bash
export LD_LIBRARY_PATH=./Lib
python Test/verif.py
```

### Notes
A try to explain how the library works is given in [Test_explaination.md](Test_explaination.md)






## Packaging in PIP:

``` bash
pip install wheel
```

``` bash
python setup.py sdist bdist_wheel
```
This will create two packages in the directory `dist/`:
.A file .tar.gz (source distribution)
.A file .whl (built distribution)

### Chargiing on PyPI

``` bash
pip install twine
```

then

``` bash
twine upload dist/*

```
