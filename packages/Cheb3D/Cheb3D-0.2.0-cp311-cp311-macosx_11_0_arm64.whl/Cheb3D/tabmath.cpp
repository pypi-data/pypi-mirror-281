#include <cmath>
#include "tabspec.hpp"

// reecriture de l'arithmetique
double myminus(double r)                {return -r;}
double add(double r1, double r2)      {return r1+r2;}
double subtract(double r1, double r2) {return r1-r2;}
double multiply(double r1, double r2) {return r1*r2;}
double divide(double r1, double r2)   {return r1/r2;}

// operations mathematiques
TabSpec apply(const TabSpec& t, double (*p_fonc)(double)) {
  TabSpec result(t);
  int taille=result.get_nelt();
  for(int i=0; i<taille; i++)
    result.tableau[i] = (*p_fonc)(result.tableau[i]);
  return result;
}

TabSpec sin(const TabSpec& t) {return apply(t,sin);}
TabSpec cos(const TabSpec& t) {return apply(t,cos);}
TabSpec tan(const TabSpec& t) {return apply(t,tan);}
TabSpec exp(const TabSpec& t) {return apply(t,exp);}
TabSpec log(const TabSpec& t) {return apply(t,log);}
TabSpec sqrt(const TabSpec& t) {return apply(t,sqrt);}
TabSpec abs(const TabSpec& t) {return apply(t,fabs);}

// operateurs binaires
TabSpec apply(const TabSpec& t1, const TabSpec& t2, double (*p_fonc)(double,double)) {
  if (!t1.check_sizes(t2))
    throw(std::out_of_range("Invalid composition of two TabSpec")) ;
  TabSpec result(t1);
  int taille=result.get_nelt();
  for(int i=0; i<taille; i++)
    result.tableau[i] = (*p_fonc)(t1.tableau[i],t2.tableau[i]);
  return result;
}
TabSpec apply(const TabSpec& t, double r, double (*p_fonc)(double,double)) {
  TabSpec result(t);
  int taille=result.get_nelt();
  for(int i=0; i<taille; i++)
    result.tableau[i] = (*p_fonc)(t.tableau[i],r);
  return result;
}
TabSpec apply(double r, const TabSpec& t, double (*p_fonc)(double,double)) {
  TabSpec result(t);
  int taille=result.get_nelt();
  for(int i=0; i<taille; i++)
    result.tableau[i] = (*p_fonc)(r,t.tableau[i]);
  return result;
}

// operateurs arithmetiques:
TabSpec operator-(const TabSpec& t) {return apply(t, myminus);}
TabSpec operator+(const TabSpec& t1, const TabSpec& t2) {return apply(t1,t2,add);}
TabSpec operator+(const TabSpec& t, double r) {return apply(t,r,add);}
TabSpec operator+(double r, const TabSpec& t) {return apply(r,t,add);}
TabSpec operator-(const TabSpec& t1, const TabSpec& t2) {return apply(t1,t2,subtract);}
TabSpec operator-(const TabSpec& t, double r) {return apply(t,r,subtract);}
TabSpec operator-(double r, const TabSpec& t) {return apply(r,t,subtract);}
TabSpec operator/(const TabSpec& t1, const TabSpec& t2) {return apply(t1,t2,divide);}
TabSpec operator/(const TabSpec& t, double r) {return apply(t,r,divide);}
TabSpec operator/(double r, const TabSpec& t) {return apply(r,t,divide);}
TabSpec operator*(const TabSpec& t1, const TabSpec& t2) {return apply(t1,t2,multiply);}
TabSpec operator*(const TabSpec& t, double r) {return apply(t,r,multiply);}
TabSpec operator*(double r, const TabSpec& t) {return apply(r,t,multiply);}

TabSpec pow(const TabSpec& t, double r) {return apply(t, r, pow);}

double max(const TabSpec& tin) {
  int taille = tin.get_nelt() ;
  double resu = tin.tableau[0] ;
  for (int i=1; i<taille; i++)
      resu = (resu > tin.tableau[i] ? resu : tin.tableau[i] ) ;
  return resu ;
}
