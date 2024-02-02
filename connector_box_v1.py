# %%
"""
rebuild the catch all box from printables model https://www.printables.com/model/399667-catch-all-trays-desk-organizer-stackable-remix

"""
Yes = True
No = False

from build123d import *
from ocp_vscode import *
from copy import copy
# %%
Export_STL = Yes
Show = Yes

connector_1 = import_stl("./_inbox/Connector_fit.STL")

x = 17.0 * MM
x1 = 14.5 * MM
y = 2.0 * MM
diff = 1.0 * MM
conn_width = 18.0 * MM - diff
conn_length = 3.8 * MM
alpha = 55.0

with BuildPart() as connector:
    with BuildSketch(Plane.XY):
        with Locations((conn_width/2,conn_length/2,0)):
            Trapezoid(width=conn_width, height=conn_length, left_side_angle=alpha)
        with Locations((conn_width/2,conn_length/2,0)):
            Trapezoid(width=conn_width, height=conn_length, left_side_angle=alpha, rotation=180.0)

    extrude(amount=21)


# %%
if Show:
    show(connector, connector_1, reset_camera=Camera.KEEP)

if Export_STL:
    connector.part.export_stl(f"./_exports/Andor_connector.stl")

# %%