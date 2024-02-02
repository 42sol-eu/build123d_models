# %%
"""

"""
from build123d import *
import ocp_vscode

Yes = True
No = False
from math import sqrt, acos


a = 10
alpha = 60
# %%
b = sqrt( a ** 2 - ((a/2) ** 2) )
h = a * ( sqrt(6) / 3)

with BuildLine(Plane.XY ) as model:
    l1 = PolarLine((-a/2,-b/2), a, alpha)
    l2 = PolarLine(l1@1, a,  -alpha)
    l3 = Line(l2@1, l1@0)
    l4 = Line(l1@0,(0,0,h))
    l5 = Line(l2@0,(0,0,h))
    l6 = Line(l3@0,(0,0,h))

points = []
for vertex in model.vertices():
    points.append(vertex.to_vector())
ic(points)
surface = Face.make_surface_from_array_of_points(points)
bbox = surface.bounding_box()

for vector in model.vertices():
    ic(vector)

for vector in model.wires():
    ic(vector)

if False:
    wires = Wire.make_wire(model.edges())
    faces = Face.sew_faces(wires)
    shell = Shell.make_shell(faces)
    D4 = Solid.make_solid(shell)


    ic(D4.part)

ocp_vscode.show_object(bbox)
# %%