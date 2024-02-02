# %%
"""
rebuild the catch all box from printables model https://www.printables.com/model/399667-catch-all-trays-desk-organizer-stackable-remix

"""
Yes = True
No = False

from build123d import *
from ocp_vscode import *

# %%

title_text = "Andor Boks"
id_text = "AB"

unit = 50 * MM
wall = 3 * MM
n_width = 2
n_length = 2
box_width = unit * n_width
box_length = unit * n_length
box_height = 22.2 * MM
conn_length = 3.8 * MM
conn_width = 18.0 * MM
alpha = 45.0
r_outer = 5.0
r_inner = 1.0

#font_1 = "Hobbiton Brushhand Hobbiton brush"
#font_1 = "Ebrima"
font_1 = "Apple Chancery Chancery"
font_2 = "Futhark AOE"

foot_width = wall-0.9

x,y,z =-50.5,-50.5,-15.8
show_remix = No
if show_remix:
    remix_100x100 = import_stl("./remix/Container100x100_stack.STL")
    remix_100x100.move(Location((x,y,z)))

    remix_050x050 = import_stl("./remix/Container50x50_stack.STL")
    remix_050x050.move(Location((x/2+0.2,y/2,z)))

def add_text(workplane, text, x, y, depth=1, align=(Align.CENTER, Align.CENTER) ):
    pass

# %%
with BuildPart() as the_box:
    Box( box_width,box_length,box_height)
    with BuildSketch():
        RectangleRounded(box_width-2*wall,box_length-2*wall, radius=wall/3.0)
    extrude(amount=box_height, both=True, mode=Mode.SUBTRACT)

    edges = the_box.edges().filter_by(GeomType.LINE).filter_by(Axis.Z).sort_by(Axis.Z)[:4]
    fillet(edges, radius=r_outer)    
    top_edges = the_box.faces().filter_by(Axis.Z).sort_by(Axis.Z)[-1].edges()
    fillet(top_edges, radius=r_inner)
    with BuildSketch():
        with GridLocations(unit,-box_length,n_width,2):
            Trapezoid(width=conn_width, height=conn_length, left_side_angle=alpha)
            Trapezoid(width=conn_width, height=conn_length, left_side_angle=alpha, rotation=180.0)
    extrude(amount=box_height, both=True, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY):
        with GridLocations(-box_width, unit,2,n_length):
            Trapezoid(width=conn_width, height=conn_length, left_side_angle=alpha,rotation=90.0)
            Trapezoid(width=conn_width, height=conn_length, left_side_angle=alpha, rotation=270.0)
    extrude(amount=box_height, both=True, mode=Mode.SUBTRACT)

    box_faces = the_box.faces().sort_by(Axis.Z)
    bottom_face = box_faces[0]
    with BuildPart() as the_foot:
        with BuildSketch(bottom_face) as foot_print_1:
            RectangleRounded(box_width,box_length, radius=r_outer)
        with BuildSketch(bottom_face.offset(foot_width)) as foot_print_2:
            RectangleRounded(box_width-3*foot_width,box_length-3*foot_width, radius=2.0)
        with BuildSketch(bottom_face.offset(2*foot_width)) as foot_print_3:
            RectangleRounded(box_width-4*foot_width,box_length-4*foot_width, radius=0.5)
            #Rectangle(box_width-4*foot_width,box_length-4*foot_width)
        loft()

        
        foot_faces = the_foot.faces().sort_by(Axis.Z)
        feet_face = foot_faces[0]
        inner_face = foot_faces[-1]
        write_plane = Plane(face=bottom_face,z_dir=(0,0,1))
        print(write_plane.x_dir, write_plane.y_dir, write_plane.z_dir)

        x= -box_width/2+5
        y= box_length/2-12.5

        with BuildSketch(-write_plane) as foot_print_4:
            with Locations((x,y,0)):
                Text(title_text, 7, font_2, align=(Align.MIN,Align.MIN))            
            with Locations((-box_width/2+7.5,-box_length/2+5,0)):
                Text(id_text, 14, font_2, align=(Align.MIN,Align.MIN))
        extrude(amount=1,both=True,mode=Mode.SUBTRACT)

        print(feet_face.position, feet_face.location)
        # bottom_face 
        with BuildSketch(bottom_face.offset(2*foot_width)) as foot_print_3:
            with Locations((x,y,0)):
                Text(title_text, font_size=7, font=font_2, align=(Align.MIN,Align.MIN), font_path="/Users/felix/Library/Fonts/")
            with Locations((-box_width/2+5,-box_length/2+7.5,0)):
                Text(id_text, 14, font_2, align=(Align.MIN,Align.MIN))           
        extrude(amount=1,both=True,mode=Mode.SUBTRACT)        

if show_remix:
    show(remix_050x050, the_box)
else:
    show(the_box, the_foot, bottom_face, reset_camera=Camera.KEEP)

the_box.part.export_stl(f"./_exports/Andor_Box_100x100_{id_text}.stl")
