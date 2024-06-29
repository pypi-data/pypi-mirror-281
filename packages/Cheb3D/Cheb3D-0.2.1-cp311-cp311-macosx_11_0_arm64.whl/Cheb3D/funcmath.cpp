#include <cmath>
#include "funcspec.hpp"

// Operators+
//-------------
FuncSpec operator+(const FuncSpec& t1, const FuncSpec& t2) {

  if (!check_grids(t1, t2))
    throw invalid_argument("Different grids") ;
  FuncSpec resu(t1) ;
  
  if (t1.values_up_to_date) {
    if (t2.values_up_to_date) {
      resu = t1.values + t2.values ;
      if (t1.coefs_up_to_date && t2.coefs_up_to_date) {
	resu.coefs = t1.coefs + t2.coefs ;
	resu.coefs_up_to_date = true ;
      }
    }
    else {
      if (!t2.coefs_up_to_date)
	throw invalid_argument("Ill-formed second argument in operator+(FuncSpec)") ;
      if (t1.coefs_up_to_date) {
	resu.set_coefs(t1.coefs + t2.coefs) ;
      }
      else {
	resu.set_coefs(t2.coefs) ;
	resu.compute_values() ;
	resu = t1.values + resu.values ;
      }
    }
  }
  else {
    if (!t1.coefs_up_to_date)
      throw invalid_argument("Ill-formed first argument in operator+(FuncSpec)") ;
    if (t2.coefs_up_to_date) {
      resu.set_coefs(t1.coefs + t2.coefs) ;
    }
    else {
      if (!t2.values_up_to_date)
	throw invalid_argument("Ill-formed second argument in operator+(FuncSpec)") ;
      resu.set_coefs(t1.coefs) ;
      resu.compute_values() ;
      resu = resu.values + t2.values ;
    }
  }
  return resu ;

}

FuncSpec operator+(const FuncSpec& t1, double x) {

  FuncSpec resu(t1) ;
  
  if (t1.values_up_to_date) {
      resu.values = t1.values + x ;
      resu.values_up_to_date = true ;
      if (t1.coefs_up_to_date) {
	resu.coefs = t1.coefs ;
	resu.coefs.set(0) += x ;
	resu.coefs_up_to_date = true ;
      }
  }
  else {
    if (!t1.coefs_up_to_date)
      throw invalid_argument("Ill-formed first argument in operator+(FuncSpec)") ;
    resu.set_coefs(t1.coefs) ;
    resu.coefs.set(0) += x ;
  }
  return resu ;
}

FuncSpec operator+(double x, const FuncSpec& t1) {

  FuncSpec resu(t1) ;
  
  if (t1.values_up_to_date) {
      resu.values = t1.values + x ;
      resu.values_up_to_date = true ;
      if (t1.coefs_up_to_date) {
	resu.coefs = t1.coefs ;
	resu.coefs.set(0) += x ;
	resu.coefs_up_to_date = true ;
      }
  }
  else {
    if (!t1.coefs_up_to_date)
      throw invalid_argument("Ill-formed first argument in operator+(FuncSpec)") ;
    resu.set_coefs(t1.coefs) ;
    resu.coefs.set(0) += x ;
  }
  return resu ;
}

// Operators-
//-------------

FuncSpec operator-(const FuncSpec& t1) {

  FuncSpec resu(t1) ;
  
  if (t1.values_up_to_date) {
      resu.values = -t1.values ;
      resu.values_up_to_date = true ;
      if (t1.coefs_up_to_date) {
	resu.coefs = -t1.coefs ;
	resu.coefs_up_to_date = true ;
      }
  }
  else {
    if (!t1.coefs_up_to_date)
      throw invalid_argument("Ill-formed first argument in operator-(FuncSpec)") ;
    resu.set_coefs(-t1.coefs) ;
  }
  return resu ;
}

FuncSpec operator-(const FuncSpec& t1, const FuncSpec& t2) {

  if (!check_grids(t1, t2))
    throw invalid_argument("Different grids") ;
  FuncSpec resu(t1) ;
  
  if (t1.values_up_to_date) {
    if (t2.values_up_to_date) {
      resu = t1.values - t2.values ;
      if (t1.coefs_up_to_date && t2.coefs_up_to_date) {
	resu.coefs = t1.coefs - t2.coefs ;
	resu.coefs_up_to_date = true ;
      }
    }
    else {
      if (!t2.coefs_up_to_date)
	throw invalid_argument("Ill-formed second argument in operator-(FuncSpec)") ;
      if (t1.coefs_up_to_date) {
	resu.set_coefs(t1.coefs - t2.coefs) ;
      }
      else {
	resu.set_coefs(t2.coefs) ;
	resu.compute_values() ;
	resu = t1.values - resu.values ;
      }
    }
  }
  else {
    if (!t1.coefs_up_to_date)
      throw invalid_argument("Ill-formed first argument in operator-(FuncSpec)") ;
    if (t2.coefs_up_to_date) {
      resu.set_coefs(t1.coefs - t2.coefs) ;
    }
    else {
      if (!t2.values_up_to_date)
	throw invalid_argument("Ill-formed second argument in operator-(FuncSpec)") ;
      resu.set_coefs(t1.coefs) ;
      resu.compute_values() ;
      resu = resu.values - t2.values ;
    }
  }
  return resu ;

}

FuncSpec operator-(const FuncSpec& t1, double x) {

  FuncSpec resu(t1) ;
  
  if (t1.values_up_to_date) {
      resu.values = t1.values - x ;
      resu.values_up_to_date = true ;
      if (t1.coefs_up_to_date) {
	resu.coefs = t1.coefs ;
	resu.coefs.set(0) -= x ;
	resu.coefs_up_to_date = true ;
      }
  }
  else {
    if (!t1.coefs_up_to_date)
      throw invalid_argument("Ill-formed first argument in operator-(FuncSpec)") ;
    resu.set_coefs(t1.coefs) ;
    resu.coefs.set(0) -= x ;
  }
  return resu ;
}

FuncSpec operator-(double x, const FuncSpec& t1) {

  FuncSpec resu(t1) ;
  
  if (t1.values_up_to_date) {
      resu.values = x - t1.values ;
      resu.values_up_to_date = true ;
      if (t1.coefs_up_to_date) {
	resu.coefs = -t1.coefs ;
	resu.coefs.set(0) += x ;
	resu.coefs_up_to_date = true ;
      }
  }
  else {
    if (!t1.coefs_up_to_date)
      throw invalid_argument("Ill-formed first argument in operator-(FuncSpec)") ;
    resu.set_coefs(-t1.coefs) ;
    resu.coefs.set(0) += x ;
  }
  return resu ;
}

// Operators*
//------------

FuncSpec operator*(const FuncSpec& t1, const FuncSpec& t2) {

  if (!check_grids(t1, t2))
    throw invalid_argument("Different grids") ;
  FuncSpec resu(t1) ;
  if (!resu.values_up_to_date) resu.compute_values() ;
  if (t2.values_up_to_date) {
    resu.values = resu.values*t2.values ;
    resu.values_up_to_date = true ;
    resu.coefs_up_to_date = false ;
  }
  else {
    FuncSpec tmp(t2) ;
    tmp.compute_values() ;
    resu.values = resu.values*tmp.values ;
    resu.values_up_to_date = true ;
    resu.coefs_up_to_date = false ;
  }
  return resu ;
}

FuncSpec operator*(const FuncSpec& t1, double x) {

  FuncSpec resu(t1) ;
  
  if (t1.values_up_to_date) {
      resu.values = t1.values * x ;
      resu.values_up_to_date = true ;
      if (t1.coefs_up_to_date) {
	resu.coefs = t1.coefs * x ;
	resu.coefs_up_to_date = true ;
      }
  }
  else {
    if (!t1.coefs_up_to_date)
      throw invalid_argument("Ill-formed first argument in operator*(FuncSpec)") ;
    resu.set_coefs(x*t1.coefs) ;
  }
  return resu ;
}

FuncSpec operator*(double x, const FuncSpec& t1) {

  FuncSpec resu(t1) ;
  
  if (t1.values_up_to_date) {
      resu.values = t1.values * x ;
      resu.values_up_to_date = true ;
      if (t1.coefs_up_to_date) {
	resu.coefs = t1.coefs * x ;
	resu.coefs_up_to_date = true ;
      }
  }
  else {
    if (!t1.coefs_up_to_date)
      throw invalid_argument("Ill-formed first argument in operator*(FuncSpec)") ;
    resu.set_coefs(x*t1.coefs) ;
  }
  return resu ;
}

// Operators/
//------------

FuncSpec operator/(const FuncSpec& t1, const FuncSpec& t2) {

  if (!check_grids(t1, t2))
    throw invalid_argument("Different grids") ;
  FuncSpec resu(t1) ;
  if (!resu.values_up_to_date) resu.compute_values() ;
  if (t2.values_up_to_date) {
    resu.values = resu.values/t2.values ;
    resu.values_up_to_date = true ;
    resu.coefs_up_to_date = false ;
  }
  else {
    FuncSpec tmp(t2) ;
    tmp.compute_values() ;
    resu.values = resu.values/tmp.values ;
    resu.values_up_to_date = true ;
    resu.coefs_up_to_date = false ;
  }
  return resu ;
}

FuncSpec operator/(const FuncSpec& t1, double x) {

  return (1./x)*t1 ;
}

FuncSpec operator/(double x, const FuncSpec& t1) {

  FuncSpec resu(t1) ;
  if (!resu.values_up_to_date) resu.compute_values() ;
  resu.values = x / resu.values ;
  resu.values_up_to_date = true ;
  resu.coefs_up_to_date = false ;

  return resu ;
}

// operations mathematiques
FuncSpec apply(const FuncSpec& t, TabSpec (*p_fonc)(const TabSpec&)) {

  FuncSpec resu(t) ;

  if (t.values_up_to_date) {
    resu.values = (*p_fonc)(t.values) ;
    resu.values_up_to_date = true ;
    resu.coefs_up_to_date = false ;
  }
  else {
    if (!t.coefs_up_to_date)
      throw invalid_argument("Ill-formed argument in abs(FuncSpec)") ;
    FuncSpec tmp = t ;
    tmp.compute_values() ;
    resu.values = (*p_fonc)(tmp.values) ;
    resu.values_up_to_date = true ;
    resu.coefs_up_to_date = false ;
  }
  return resu ;  
}

FuncSpec sin(const FuncSpec& t) {return apply(t,sin);}
FuncSpec cos(const FuncSpec& t) {return apply(t,cos);}
FuncSpec tan(const FuncSpec& t) {return apply(t,tan);}
FuncSpec exp(const FuncSpec& t) {return apply(t,exp);}
FuncSpec log(const FuncSpec& t) {return apply(t,log);}
FuncSpec sqrt(const FuncSpec& t) {return apply(t,sqrt);}
FuncSpec abs(const FuncSpec& t) {return apply(t,abs);}

// Function pow
FuncSpec pow(const FuncSpec& t, double r) {

  FuncSpec resu(t) ;

  if (t.values_up_to_date) {
    resu.values = pow(t.values, r) ;
    resu.values_up_to_date = true ;
    resu.coefs_up_to_date = false ;
  }
  else {
    if (!t.coefs_up_to_date)
      throw invalid_argument("Ill-formed argument in abs(FuncSpec)") ;
    FuncSpec tmp = t ;
    tmp.compute_values() ;
    resu.values = pow(tmp.values, r) ;
    resu.values_up_to_date = true ;
    resu.coefs_up_to_date = false ;
  }
  return resu ;  
}

// Function max
//---------------

double max(const FuncSpec& fs) {

  if (!fs.values_up_to_date)
    throw(std::runtime_error("Values not up to date in max(FuncSpec)")) ;  
  return max(fs.values) ;

}
