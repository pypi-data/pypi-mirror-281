from libcpp.string cimport string
cdef extern from "tabspec.hpp":
	cdef cppclass TabSpec:
		TabSpec() except+
		TabSpec(int, int, int) except +
		TabSpec(TabSpec) except+
		TabSpec(string) except +
		string string_display()
		void fill_val "operator="(double)
		double read_item "operator()"(int, int, int) except+
		double& set(int, int, int) except+
		int get_dim()
		int get_sizex()
		int get_sizey()
		int get_sizez()

	TabSpec operator-(TabSpec)
	TabSpec operator+(TabSpec, TabSpec) except+
	TabSpec operator+(TabSpec, double)
	TabSpec operator-(TabSpec, TabSpec) except+
	TabSpec operator*(TabSpec, TabSpec) except+
	TabSpec operator*(TabSpec, double)
	TabSpec operator/(TabSpec, TabSpec) except+
	TabSpec operator/(double, TabSpec) except+

	TabSpec tcos "cos"(TabSpec)
	TabSpec tsin "sin"(TabSpec)
	TabSpec ttan "tan"(TabSpec)
	TabSpec texp "exp"(TabSpec)
	TabSpec tlog "log"(TabSpec)
	TabSpec tsqrt "sqrt"(TabSpec)
	TabSpec tpow "pow"(TabSpec, double)
	TabSpec tabs "abs"(TabSpec)
	double tmax "max"(TabSpec)

cdef extern from "funcspec.hpp":
	cdef cppclass FuncSpec:
		FuncSpec() except+
		FuncSpec(int, int, int) except+
		FuncSpec(FuncSpec) except+
		FuncSpec(TabSpec) except+
		FuncSpec(string, string) except+
		string string_display()
		void set_grids(double, double, double, double, double, double)
		void fill_val "operator="(double)
		void set_values "operator="(TabSpec) except+
		void set_coefs(TabSpec) except+
		TabSpec grid_x()
		TabSpec grid_y()
		TabSpec grid_z()
		double get_xmin()
		double get_xmax()
		double get_ymin()
		double get_ymax()
		double get_zmin()
		double get_zmax()
		TabSpec get_values()
		TabSpec get_coefs()
		void compute_coefs() except+
		void compute_values() except+
		double compute_in_xyz(double, double, double) except+
		FuncSpec get_partial_x()
		FuncSpec get_partial_y()
		FuncSpec get_partial_z()
		void interpolate_from_Tab(TabSpec, TabSpec, TabSpec, TabSpec)
		void write_grids(string) except+
		void write_values(string) except+

	FuncSpec operator-(FuncSpec)
	FuncSpec operator+(FuncSpec, FuncSpec) except+
	FuncSpec operator+(FuncSpec, double)
	FuncSpec operator-(FuncSpec, FuncSpec) except+
	FuncSpec operator*(FuncSpec, FuncSpec) except+
	FuncSpec operator*(FuncSpec, double)
	FuncSpec operator/(FuncSpec, FuncSpec) except+
	FuncSpec operator/(double, FuncSpec) except+

	FuncSpec fcos "cos"(FuncSpec)
	FuncSpec fsin "sin"(FuncSpec)
	FuncSpec ftan "tan"(FuncSpec)
	FuncSpec fexp "exp"(FuncSpec)
	FuncSpec flog "log"(FuncSpec)
	FuncSpec fsqrt "sqrt"(FuncSpec)
	FuncSpec fpow "pow"(FuncSpec, double)
	FuncSpec fabs "abs"(FuncSpec)
	double fmax "max"(FuncSpec)
