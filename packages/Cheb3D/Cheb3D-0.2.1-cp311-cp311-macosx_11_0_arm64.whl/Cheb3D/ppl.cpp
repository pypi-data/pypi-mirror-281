#include <cstdlib>
#include <cmath>
#include <iostream>
#include <iomanip>

#include "funcspec.hpp"

int main() {

  string coordx = "xcoord.dat" ;
  string coordy = "ycoord.dat" ;
  string coordz = "zcoord.dat" ;
  string field = "phi.dat" ;

  int nx = 17, ny = 15, nz = 19 ;
  FuncSpec f(nx, ny, nz) ;
  f.set_grids(-1.1, 0.8, -0.8, 1.1, 0., 1.) ;

  TabSpec xfd(coordx) ;
  TabSpec yfd(coordy) ;
  TabSpec zfd(coordz) ;
  TabSpec champ(field) ;
  
  FuncSpec q(f) ;
  TabSpec x = q.grid_x() ;
  TabSpec y = q.grid_y() ;
  TabSpec z = q.grid_z() ;
  q = 3./(2. + x*x + y*y + z*z) ;

  f.interpolate_from_Tab(champ, xfd, yfd, zfd) ;
  
  cout << max(abs(f - q)) << endl ;
  
  return EXIT_SUCCESS ; 
}
