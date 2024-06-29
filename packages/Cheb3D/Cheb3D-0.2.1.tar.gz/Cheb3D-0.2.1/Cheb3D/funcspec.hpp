#ifndef __FUNCSPEC__
#define __FUNCSPEC__
#include "tabspec.hpp"

class FuncSpec {
  
  //Data
  //----
protected:
  int nx, ny, nz ;
  double xmin, xmax, ymin, ymax, zmin, zmax ;
  TabSpec xx, yy, zz ;
  TabSpec values, coefs ;
  bool coefs_up_to_date ;
  bool values_up_to_date ;

  mutable FuncSpec* p_dfdx ;
  mutable FuncSpec* p_dfdy ;
  mutable FuncSpec* p_dfdz ;
  
  //Constructors - Destructor
  //-------------------------
public:
  explicit FuncSpec(int=2, int=2, int=2) ;
  explicit FuncSpec(const TabSpec&) ;
  /** Constructor from files.'coord_name' is a prefix for files containing 
   *  coordinate data (coord_namex.dat, coord_namey.dat, coord_namez.dat);
   *  'field', is the complete name of the file containing the field data.*/
  explicit FuncSpec(const string& coord_name, const string& field) ; 
  FuncSpec(const FuncSpec&) ; ///< Copy constructor

  virtual ~FuncSpec() ; ///< Destructor

protected:
  void del_deriv() const ;

  // Assignments
  //------------
public:
  void operator=(const FuncSpec&) ;
  void operator=(const TabSpec&) ;
  void operator=(double) ;

  // Accessors
  //-----------
  double get_xmin() const {return xmin ;} ;
  double get_xmax() const {return xmax ;} ;
  double get_ymin() const {return ymin ;} ;
  double get_ymax() const {return ymax ;} ;
  double get_zmin() const {return zmin ;} ;
  double get_zmax() const {return zmax ;} ;

  TabSpec get_values() const {return values; } ;
  TabSpec get_coefs() const {return coefs; } ;
  
  void set_grids(double, double, double, double, double, double) ;  
  void set_coefs(const TabSpec&) ;

  // Computing
  //----------
  void compute_coefs() ;
  double compute_in_xyz(double, double, double) const ;
  void compute_values() ;
  FuncSpec get_partial_x() ;
  FuncSpec get_partial_y() ;
  FuncSpec get_partial_z() ;

  // Saving into files
  //-------------------
  void write_grids(const string&) ;
  void write_values(const string&) ;

  // Display
  //---------
public:
  string string_display() const ;  ///< Display (output to a string)

  // Access to data
  //---------------
  TabSpec grid_x() const ;
  TabSpec grid_y() const ;
  TabSpec grid_z() const ;

  // Interpolate from a 3D TabSpec
  //------------------------------
  void interpolate_from_Tab(const TabSpec& values, const TabSpec& x_coord,
			    const TabSpec& y_coord, const TabSpec& z_coord) ;

  friend ostream& operator<<(ostream&, const FuncSpec&) ;
  friend bool check_grids(const FuncSpec&, const FuncSpec&) ;
  
  friend FuncSpec operator+(const FuncSpec&, const FuncSpec&) ;
  friend FuncSpec operator-(const FuncSpec&) ;
  friend FuncSpec operator+(const FuncSpec&, double) ;
  friend FuncSpec operator+(double, const FuncSpec&) ;
  friend FuncSpec operator-(const FuncSpec&, const FuncSpec&) ;
  friend FuncSpec operator-(const FuncSpec&, double) ;
  friend FuncSpec operator-(double, const FuncSpec&) ;
  friend FuncSpec operator*(const FuncSpec&, const FuncSpec&) ;
  friend FuncSpec operator*(const FuncSpec&, double) ;
  friend FuncSpec operator*(double, const FuncSpec&) ;
  friend FuncSpec operator/(const FuncSpec&, const FuncSpec&) ;
  friend FuncSpec operator/(const FuncSpec&, double) ;
  friend FuncSpec operator/(double, const FuncSpec&) ;

  friend FuncSpec apply(const FuncSpec& t, TabSpec (*p_fonc)(const TabSpec&));
  friend FuncSpec pow(const FuncSpec&, double) ;
  friend double max(const FuncSpec&) ;

};

ostream& operator<<(ostream&, const FuncSpec&) ;

FuncSpec operator-(const FuncSpec&) ;
FuncSpec operator+(const FuncSpec&, const FuncSpec&) ;
FuncSpec operator+(const FuncSpec&, double) ;
FuncSpec operator+(double, const FuncSpec&) ;
FuncSpec operator-(const FuncSpec&, const FuncSpec&) ;
FuncSpec operator-(const FuncSpec&, double) ;
FuncSpec operator-(double, const FuncSpec&) ;
FuncSpec operator*(const FuncSpec&, const FuncSpec&) ;
FuncSpec operator*(const FuncSpec&, double) ;
FuncSpec operator*(double, const FuncSpec&) ;
FuncSpec operator/(const FuncSpec&, const FuncSpec&) ;
FuncSpec operator/(const FuncSpec&, double) ;
FuncSpec operator/(double, const FuncSpec&) ;

FuncSpec sin(const FuncSpec&) ;
FuncSpec cos(const FuncSpec&) ;
FuncSpec tan(const FuncSpec&) ;
FuncSpec exp(const FuncSpec&) ;
FuncSpec log(const FuncSpec&) ;
FuncSpec sqrt(const FuncSpec&) ;
FuncSpec pow(const FuncSpec&, double) ;
FuncSpec abs(const FuncSpec&) ;
double max(const FuncSpec&) ;

#endif
