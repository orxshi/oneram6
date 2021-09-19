# FreeCAD python script to generate ONERA M6 mesh

The script generates a file with .geo extension to be read by Gmsh mesh generator.

The geometry is based on https://www.grc.nasa.gov/www/wind/valid/m6wing/m6wing.html.  
For boundary conditions see https://su2code.github.io/tutorials/Inviscid_ONERAM6.

## Tested with
FreeCAD version: 0.18.4  
Gmsh version: 4.7.1

## FreeCAD images

<figure>
  <img src="/images/1.png" width="300">
  <figcaption>Orthonormal view of the wing.</figcaption>
</figure>

<figure>
  <img src="/images/2.png" width="300">
  <figcaption>Top view of the wing.</figcaption>
</figure>

## Gmsh images

<figure>
  <img src="/images/6.png" width="300">
  <figcaption>Geometry from isometric view.</figcaption>
</figure>

<figure>
  <img src="/images/7.png" width="300">
  <figcaption>Geometry from another view to show symmetry plane.</figcaption>
</figure>

<figure>
  <img src="/images/10.png" width="300">
  <figcaption>Tetrahedral mesh.</figcaption>
</figure>

<figure>
  <img src="/images/11.png" width="300">
  <figcaption>Close-up view to airfoil.</figcaption>
</figure>
