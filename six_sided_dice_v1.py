from build123d import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
# Create a six sided dice (W6) with correct orientation
# of the numbers

size = 6 * MM

a = size
b = a / 4    
r = b / 2
matrix = GridLocations(b,b,3,3)
dot = [
    (5,),
    (1,3,7,9),
    (1,5,9),
    (1,9),
    (1,3,5,7,9),
    (1,3,4,6,7,9),
]
with BuildPart() as diceW6:
    Box(size,size,size)
    print(f'faces: {len(diceW6.faces().sort_by(Axis.Z))}')
    
    for j in range(6):
        with BuildSketch(diceW6.faces().sort_by(Axis.Z)[j]) as plane:
            # Rectangle(a,a)
            for i in dot[j]:
                print(f'face: {j}, dot: {i} ', matrix.locations[i-1])
                with Locations(matrix.locations[i-1]):
                    Circle(r/2)
    extrude(amount=-a/10,mode=Mode.SUBTRACT)
final = fillet(diceW6.edges().filter_by(GeomType.LINE), radius=a/20)
show(final)