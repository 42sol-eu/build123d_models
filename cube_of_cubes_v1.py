# the goal of this script is to test the functions `top()`, `bottom()`, `left()`, `right()`, `back()` `front()` in `find_side.py`
# other names:
# -  U = top = up = upper
# -  D = bottom = down = lower
# -  L = left = west = W 
# -  R = right = east = E
# -  B = back = north = N
# -  F = front = south = S

from build123d import *
from ocp_vscode import *
set_port(3939)
x, y, z = 12, 12, 12
r = min(x,y,z)/3

with BuildPart() as box:
    a = Box(x,y,z)
    Cylinder(r, 2*z, mode=Mode.SUBTRACT)
    Cylinder(r, 2*x, mode=Mode.SUBTRACT,rotation=(90,0,0))
    Cylinder(r, 2*y, mode=Mode.SUBTRACT,rotation=(0,90,0))

    b = 5
    Cylinder(r, b*z, )
    Cylinder(r, b*x, rotation=(90,0,0))
    Cylinder(r, b*y, rotation=(0,90,0))

faces = box.part.faces()
U = faces.sort_by(Axis.Z)[-1]
D = faces.sort_by(Axis.Z)[0]
L = faces.sort_by(Axis.X)[0]
R = faces.sort_by(Axis.X)[-1]
B = faces.sort_by(Axis.Y)[-1]
F = faces.sort_by(Axis.Y)[0]

box.label = "core box"

U.label = "U rot"
U.color = Color("red")
F.label = "F grün"
F.color = Color("green")
B.label = "B weiß"
B.color = Color("white")
D.label = "D blau"
D.color = Color("blue")
L.label = "L schwarz"
L.color = Color("black")
R.label = "R gelb"
R.color = Color("yellow")

bounding = box.part.bounding_box()
next_plane = Plane.XY.offset(bounding.max.Z)

with BuildPart(next_plane) as sketch_on_plane1:
    with GridLocations(x,y,3,3):
        Box(x-0.1,y-0.1,z+0.1,align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(r, 2.2*z, mode=Mode.SUBTRACT)
sketch_on_plane1.label="on top"
sketch_on_plane1.color = U.color


next_plane = Plane.XZ.offset(bounding.max.Y)

with BuildPart(next_plane) as sketch_on_plane2:
    with GridLocations(x,y,3,3):
        Box(x-0.1,y-0.1,z+0.1,align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(r, 2.2*z, mode=Mode.SUBTRACT)
sketch_on_plane2.label="on front"
sketch_on_plane2.color = F.color


next_plane = Plane.YZ.offset(bounding.max.X)

with BuildPart(next_plane) as sketch_on_plane3:
    with GridLocations(x,y,3,3):
        Box(x-0.1,y-0.1,z+0.1,align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(r, 2.2*z, mode=Mode.SUBTRACT)
sketch_on_plane3.label="on right"
sketch_on_plane3.color = R.color


next_plane = Plane.XY.offset(-bounding.max.Z)
    
with BuildPart(next_plane) as sketch_on_plane4:
    with GridLocations(x,y,3,3):
        Box(x-0.1,y-0.1,z+0.1,align=(Align.CENTER, Align.CENTER, Align.MAX))
    Cylinder(r, 2.2*z, mode=Mode.SUBTRACT)
sketch_on_plane4.label="on bottom"
sketch_on_plane4.color = D.color


next_plane = Plane.XZ.offset(-bounding.max.Y)

with BuildPart(next_plane) as sketch_on_plane5:
    with GridLocations(x,y,3,3):
        Box(x-0.1,y-0.1,z+0.1,align=(Align.CENTER, Align.CENTER, Align.MAX))
    Cylinder(r, 2.2*z, mode=Mode.SUBTRACT)
sketch_on_plane5.label="on back"
sketch_on_plane5.color = B.color


next_plane = Plane.YZ.offset(-bounding.max.X)

with BuildPart(next_plane) as sketch_on_plane6:
    with GridLocations(x,y,3,3):
        Box(x-0.1,y-0.1,z+0.1,align=(Align.CENTER, Align.CENTER, Align.MAX))
    Cylinder(r, 2.2*z, mode=Mode.SUBTRACT)
sketch_on_plane6.label="on left"
sketch_on_plane6.color = L.color


faces = [sketch_on_plane1, sketch_on_plane2, sketch_on_plane3,
     sketch_on_plane4, sketch_on_plane5, sketch_on_plane6,]

bbox = box.part.bounding_box()
print(bbox)
show(box, *faces,
     U, D, L, R, B, F)