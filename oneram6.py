# This python/freecad script generates an ONERA M6 wing.
# The script generates a file with .geo extension to be read by Gmsh which is a mesh generator.
# The geometry is based on https://www.grc.nasa.gov/www/wind/valid/m6wing/m6wing.html.
# For boundary conditions see https://su2code.github.io/tutorials/Inviscid_ONERAM6.

import sys
import math
import numpy

sys.path.append('/usr/lib/freecad/lib/')

import FreeCAD
import Draft
import Part
import BOPTools.JoinFeatures
import ObjectsFem
import femmesh.gmshtools
from modify_geo import *

def compute_tip_section(xl_base, le_sweep, te_sweep, span):

    # Computes and returns the x-distance between leading edges at the base and the tip sections, dxl
    # Computes the x-coordinate of leading edge at the base section, xl_base
    # Computes the x-coordinate of leading edge at the tip section, xl_tip
    # Computes and returns the chord at the tip section.

    # x-coordinate of leading edge at tip section.
    dxl = span * math.tan(math.radians(le_sweep))
    xl_tip = xl_base + dxl 

    # x-coordinate of trailing edge at tip section.
    dxt = span * math.tan(math.radians(te_sweep))
    xt_tip = xt_base + dxt 

    # Chord at the tip section.
    chord_tip = xt_tip - xl_tip

    return dxl, chord_tip


def make_wing(points_base, points_tip, span):

    # Create base section of the wing.
    polygon_base = Part.makePolygon(points_base)

    # Create tip section of the wing.
    polygon_tip = Part.makePolygon(points_tip)

    loft = Part.makeLoft([polygon_base, polygon_tip], True)

    return loft


doc = FreeCAD.newDocument('newdoc')

# Parameters
chord = 805.9 # mm
z_base = 0 # z coordinate of airfoil at base section. 
xl_base = 0 # x coordinate of leading edge at base section.
xt_base = xl_base + chord # x coordinate of trailing edge at base section.
y_base = 0 # y coordinate of airfoil at base section.
span = 1196.3 # mm
le_sweep = 30 # degrees
te_sweep = 15.8 # degrees
# A box is used to model farfield and symmetry boundaries.
# See https://su2code.github.io/tutorials/Inviscid_ONERAM6 for reference.
box_dx = 20 * chord
box_dy = 20 * chord
box_dz = 10 * span

# Get the distance between leading edges at the base and the tip sections
# and chord of the airfoil at the tip section.
dxl, chord_tip = compute_tip_section(xl_base, le_sweep, te_sweep, span)

# Airfoil coordinates for the base section for chord = 805.9 mm is generated in airfoiltools.com and stored in oa209-il-805.9.csv.
# With the given parameters, chord at tip section is computed as chord_tip = 453.7 mm.
# Airfoil coordinates are generated in airfoiltools.com for the given chord_tip and stored in oa209-il-453.7.csv.

points_base = []
with open("oa209-il-805.9.csv") as fp:
    lines = fp.readlines()
    for line in lines:
        x = line.split(",")[0]
        y = line.split(",")[1]
        points_base.append(FreeCAD.Vector(xl_base + float(x), y_base + float(y), z_base))

points_tip = []
with open("oa209-il-453.7.csv") as fp:
    lines = fp.readlines()
    for line in lines:
        x = line.split(",")[0]
        y = line.split(",")[1]
        points_tip.append(FreeCAD.Vector(xl_base + float(x) + dxl, y_base + float(y), z_base - span))

# Make a wing.
wing = make_wing(points_base, points_tip, span)
Part.show(wing)

# Make a box for outer and symmetry boundaries.
box = Part.makeBox(box_dx, box_dy, box_dz, FreeCAD.Vector(-box_dx/2,-box_dy/2,-box_dz))
Part.show(box)

# Cut the wing from the box.
cut = box.cut(wing)
Part.show(cut)

# Define the cut as FreeCAD object.
cut_object = doc.addObject("Part::Feature","Cut")
cut_object.Shape = cut

# Define a mesh.
mesh = ObjectsFem.makeMeshGmsh(doc, 'FEMMeshGmsh')
mesh.ElementDimension = 3 # mesh is three-dimensional.
mesh.Part = cut_object;

# Define mesh groups.
mg_farfield = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, mesh, False, 'mg_farfield')
mg_symmetry = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, mesh, False, 'mg_symmetry')
mg_wall = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, mesh, False, 'mg_wall')
mg_volume = ObjectsFem.makeMeshGroup(FreeCAD.ActiveDocument, mesh, False, 'mg_volume')

# The farfield faces.
farfield = [
    (cut_object, 'Face' + str(1)),
    (cut_object, 'Face' + str(2)),
    (cut_object, 'Face' + str(4)),
    (cut_object, 'Face' + str(5)),
    (cut_object, 'Face' + str(6))
        ]

# The symmetry faces.
symmetry = [cut_object, 'Face' + str(3)]

# The wall faces.
wall = []
for i in range(7, len(cut_object.Shape.Faces)+1):
    wall.append((cut_object, 'Face' + str(i)))

# Set mesh groups.
mg_farfield.References = farfield
mg_symmetry.References = symmetry
mg_wall.References = wall
mg_volume.References = (cut_object, 'Solid1')

# Create a mesh.
gmsh_mesh = femmesh.gmshtools.GmshTools(mesh)
gmsh_mesh.create_mesh()

# After create_mesh(), two files with .geo and .brep extensions are generated in /tmp such as /tmp/.
# The name of those files are shape2mesh.geo and xxx_Geometry.brep where xxx is the name of the meshed object. 
# In my case, the meshed object is named as 'Cut'.
# The geo and brep files will be read by Gmsh.
# I modify the generated geo file according to my needs.
# This function generates a file named oneram6.geo.
modify_geo("oneram6", 'Cut')
