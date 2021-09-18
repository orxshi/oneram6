# FreeCAD python script to generate ONERA M6 mesh.

The script generates a file with .geo extension to be read by Gmsh mesh generator

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

<figure>
  <img src="/images/3.png" width="300">
  <figcaption>Close-up view of the base section.</figcaption>
</figure>

<figure>
  <img src="/images/4.png" width="300">
  <figcaption>Close-up view of the base section showing blunt trailing edge.</figcaption>
</figure>

<figure>
  <img src="/images/5.png" width="300">
  <figcaption>Outer boundary in shape of a box.</figcaption>
</figure>

## Gmsh images

<figure>
  <img src="/images/6.png" width="300">
  <figcaption>geo file in Gmsh.</figcaption>
</figure>
