from Cheb3D.PyNumSpec cimport TabSpec, FuncSpec

from libcpp.string cimport string
from cython.operator cimport dereference

cdef class PyTabSpec:
	cdef TabSpec c_tab

	def __cinit__(self, int nx=1, int ny=1, int nz=1) :
		self.c_tab = TabSpec(nx, ny, nz)

	@staticmethod
	cdef Init(TabSpec entree) :
		cdef PyTabSpec result = PyTabSpec()
		result.c_tab = TabSpec(entree)
		return result

	def init_from_file(self, name):
		cdef string toto = bytes(name, 'utf-8') #or should it be 'ASCII'?
		self.c_tab = TabSpec(toto)

	def __repr__(self):
		return self.c_tab.string_display().decode('utf-8')

	def __getitem__(self, tup):
		if type(tup) is int:
			return self.c_tab.read_item(tup, 0, 0)
		else:
			ind = tup + (0,0)
			i, j, k, *other = ind
			return self.c_tab.read_item(i, j, k)

	def __setitem__(self, tup, val):
		if type(tup) is int:
			(&self.c_tab.set(tup, 0, 0))[0] = float(val)
		else:
			ind = tup + (0,0)
			i, j, k, *other = ind
			(&self.c_tab.set(i, j, k))[0] = float(val)

	def dimensions(self):
		return self.c_tab.get_dim()

	def sizex(self):
		return self.c_tab.get_sizex()

	def sizey(self):
		return self.c_tab.get_sizey()

	def sizez(self):
		return self.c_tab.get_sizez()

	def fill(self, val) :
		self.c_tab.fill_val(float(val))

	def __add__(self, right):
		if isinstance(right, (int, float)):
			return PyTabSpec.Init(self.c_tab + float(right))
		elif type(right) is PyTabSpec:
			tright = <PyTabSpec>right
			return PyTabSpec.Init(self.c_tab + tright.c_tab)
		else:
			raise TypeError("Incorrect type in PyTabSpec.__add__")

	def __radd__(self, left) :
		return self + left

	def __neg__(self) :
		return PyTabSpec.Init(-self.c_tab)

	def __sub__(self, right):
		return self + (-right)

	def __rsub__(self, right):
		return -self + right

	def __mul__(self, right):
		if isinstance(right, (int, float)):
			fright = float(right)
			return PyTabSpec.Init(self.c_tab * fright)
		elif type(right) is PyTabSpec:
			tright = <PyTabSpec>right
			return PyTabSpec.Init(self.c_tab * tright.c_tab)
		else:
			raise TypeError("Incorrect type in PyTabSpec.__mul__")

	def __rmul__(self, left):
		return self*left

	def __truediv__(self, right):
		if isinstance(right, (int, float)):
			return self * (1./right)
		elif type(right) is PyTabSpec:
			tright = <PyTabSpec>right
			return PyTabSpec.Init(self.c_tab / tright.c_tab)
		else:
			raise TypeError("Incorrect type in PyTabSpec.__true_div__")

	def __rtruediv__(self, left):
		if isinstance(left, (int, float)):
			fleft = float(left)
			return PyTabSpec.Init(fleft / self.c_tab)
		elif type(left) is PyTabSpec:
			tleft = <PyTabSpec>left
			return PyTabSpec.Init(tleft.c_tab / self.c_tab)
		else:
			raise TypeError("Incorrect type in PyTabSpec.__rtrue_div__")

	def __pow__(self, ind):
		return PyTabSpec.Init(tpow(self.c_tab, float(ind)))



cdef class PyFuncSpec:
	cdef FuncSpec c_func

	def __cinit__(self, int nx=2, int ny=2, int nz=2) :
		self.c_func = FuncSpec(nx, ny, nz)

	@staticmethod
	cdef Init(FuncSpec entree) :
		cdef PyFuncSpec result = PyFuncSpec()
		result.c_func = FuncSpec(entree)
		return result

	def init_from_files(self, name_coords, name_field):
		cdef string coords = bytes(name_coords, 'utf-8') #or should it be 'ASCII'?
		cdef string field = bytes(name_field, 'utf-8') #or should it be 'ASCII'?
		self.c_func = FuncSpec(coords, field)

	def init_from_values(self, tab):
		cdef PyTabSpec pytab = tab
		self.c_func = FuncSpec(pytab.c_tab)

	def __repr__(self):
		return self.c_func.string_display().decode('utf-8')

	def grid(self):
		return (self.c_func.get_xmin(), self.c_func.get_xmax(), self.c_func.get_ymin(), self.c_func.get_ymax(), self.c_func.get_zmin(), self.c_func.get_zmax())

	def set_grid(self, bounds):
		xmin, xmax, ymin, ymax, zmin, zmax = bounds
		self.c_func.set_grids(xmin, xmax, ymin, ymax, zmin, zmax)

	def fill(self, val) :
		self.c_func.fill_val(float(val))

	def values(self) :
		return PyTabSpec.Init(self.c_func.get_values())

	def coefs(self) :
		return PyTabSpec.Init(self.c_func.get_coefs())

	def set_values(self, val):
		cdef PyTabSpec pytab = val
		self.c_func.set_values(pytab.c_tab)

	def set_coefs(self, coefs):
		cdef PyTabSpec pytab = coefs
		self.c_func.set_coefs(pytab.c_tab)

	def compute_coefs(self):
		self.c_func.compute_coefs()

	def compute_values(self):
		self.c_func.compute_values()

	def __call__(self, x, y, z):
		return self.c_func.compute_in_xyz(x, y, z)

	def grid_x(self):
		cdef result = PyTabSpec.Init(self.c_func.grid_x())
		return result

	def grid_y(self):
		return PyTabSpec.Init(self.c_func.grid_y())

	def grid_z(self):
		return PyTabSpec.Init(self.c_func.grid_z())

	def partial_x(self):
		cdef result = PyFuncSpec.Init(self.c_func.get_partial_x())
		return result

	def partial_y(self):
		cdef result = PyFuncSpec.Init(self.c_func.get_partial_y())
		return result

	def partial_z(self):
		cdef result = PyFuncSpec.Init(self.c_func.get_partial_z())
		return result

	def interpolate_from_PyTabSpec(self, field, xcoord, ycoord, zcoord):
		cdef PyTabSpec pyfield = field
		cdef PyTabSpec py_x = xcoord
		cdef PyTabSpec py_y = ycoord
		cdef PyTabSpec py_z = zcoord
		self.c_func.interpolate_from_Tab(pyfield.c_tab, py_x.c_tab, py_y.c_tab, py_z.c_tab)

	def write_to_files(self, name_field, name_coords):
		cdef string coords = bytes(name_coords, 'utf-8') #or should it be 'ASCII'?
		self.c_func.write_grids(coords)
		cdef string field = bytes(name_field, 'utf-8') #or should it be 'ASCII'?
		self.c_func.write_values(field)

	def __add__(self, right):
		if isinstance(right, (int, float)):
			return PyFuncSpec.Init(self.c_func + float(right))
		elif type(right) is PyFuncSpec:
			tright = <PyFuncSpec>right
			return PyFuncSpec.Init(self.c_func + tright.c_func)
		else:
			raise TypeError("Incorrect type in PyFuncSpec.__add__")

	def __radd__(self, left) :
		return self + left

	def __neg__(self) :
		return PyFuncSpec.Init(-self.c_func)

	def __sub__(self, right):
		return self + (-right)

	def __rsub__(self, right):
		return -self + right

	def __mul__(self, right):
		if isinstance(right, (int, float)):
			fright = float(right)
			return PyFuncSpec.Init(self.c_func * fright)
		elif type(right) is PyFuncSpec:
			tright = <PyFuncSpec>right
			return PyFuncSpec.Init(self.c_func * tright.c_func)
		else:
			raise TypeError("Incorrect type in PyFuncSpec.__mul__")

	def __rmul__(self, left):
		return self*left

	def __truediv__(self, right):
		if isinstance(right, (int, float)):
			return self * (1./right)
		elif type(right) is PyFuncSpec:
			tright = <PyFuncSpec>right
			return PyFuncSpec.Init(self.c_func / tright.c_func)
		else:
			raise TypeError("Incorrect type in PyFuncSpec.__true_div__")

	def __rtruediv__(self, left):
		if isinstance(left, (int, float)):
			fleft = float(left)
			return PyFuncSpec.Init(fleft / self.c_func)
		elif type(left) is PyFuncSpec:
			tleft = <PyFuncSpec>left
			return PyFuncSpec.Init(tleft.c_func / self.c_func)
		else:
			raise TypeError("Incorrect type in PyFuncSpec.__rtrue_div__")

	def __pow__(self, ind):
		return PyFuncSpec.Init(fpow(self.c_func, float(ind)))

# maths

def cos(val):
	if type(val) is PyTabSpec:
		tval = <PyTabSpec>val
		return PyTabSpec.Init(tcos(tval.c_tab))
	elif type(val) is PyFuncSpec:
		fval = <PyFuncSpec>val
		return PyFuncSpec.Init(fcos(fval.c_func))
	else:
		raise TypeError("Incorrect type in cos(PyNumSpec)")

def sin(val):
	if type(val) is PyTabSpec:
		tval = <PyTabSpec>val
		return PyTabSpec.Init(tsin(tval.c_tab))
	elif type(val) is PyFuncSpec:
		fval = <PyFuncSpec>val
		return PyFuncSpec.Init(fsin(fval.c_func))
	else:
		raise TypeError("Incorrect type in sin(PyNumSpec)")

def tan(val):
	if type(val) is PyTabSpec:
		tval = <PyTabSpec>val
		return PyTabSpec.Init(ttan(tval.c_tab))
	elif type(val) is PyFuncSpec:
		fval = <PyFuncSpec>val
		return PyFuncSpec.Init(ftan(fval.c_func))
	else:
		raise TypeError("Incorrect type in tan(PyNumSpec)")

def exp(val):
	if type(val) is PyTabSpec:
		tval = <PyTabSpec>val
		return PyTabSpec.Init(texp(tval.c_tab))
	elif type(val) is PyFuncSpec:
		fval = <PyFuncSpec>val
		return PyFuncSpec.Init(fexp(fval.c_func))
	else:
		raise TypeError("Incorrect type in exp(PyNumSpec)")

def log(val):
	if type(val) is PyTabSpec:
		tval = <PyTabSpec>val
		return PyTabSpec.Init(tlog(tval.c_tab))
	elif type(val) is PyFuncSpec:
		fval = <PyFuncSpec>val
		return PyFuncSpec.Init(flog(fval.c_func))
	else:
		raise TypeError("Incorrect type in log(PyNumSpec)")

def sqrt(val):
	if type(val) is PyTabSpec:
		tval = <PyTabSpec>val
		return PyTabSpec.Init(tsqrt(tval.c_tab))
	elif type(val) is PyFuncSpec:
		fval = <PyFuncSpec>val
		return PyFuncSpec.Init(fsqrt(fval.c_func))
	else:
		raise TypeError("Incorrect type in sqrt(PyNumSpec)")

def abs(val):
	if type(val) is PyTabSpec:
		tval = <PyTabSpec>val
		return PyTabSpec.Init(tabs(tval.c_tab))
	elif type(val) is PyFuncSpec:
		fval = <PyFuncSpec>val
		return PyFuncSpec.Init(fabs(fval.c_func))
	else:
		raise TypeError("Incorrect type in abs(PyNumSpec)")

def max(val):
	if type(val) is PyTabSpec:
		tval = <PyTabSpec>val
		return tmax(tval.c_tab)
	elif type(val) is PyFuncSpec:
		fval = <PyFuncSpec>val
		return fmax(fval.c_func)
	else:
		raise TypeError("Incorrect type in max(PyNumSpec)")
