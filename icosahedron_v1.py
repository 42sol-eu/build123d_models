"""
 D20 (icosahedron) with Pips!

 name: icosahedron.py
 by:   Gumyr
 date: April 18th 2022

 An icosahedron is defined by 12 vertices:
   (0, ±1, ±φ)
   (±1, ±φ, 0)
   (±φ, 0, ±1)
 where φ = (1 + √5) / 2 - the golden ratio

 The length of each edge is 2.

 The radius of the circumscribed sphere (the sphere that contains the icosahedron
 and touches each of the icosahedron's vertices) is:
   R = (a/4)√(10+2√5)
where a is the edge length.

 license: Creative Commons Attribution-NonCommercial-ShareAlike 4.0
          International Public License see:
          https:#creativecommons.org/licenses/by-nc-sa/4.0/legalcode
"""
from math import sqrt, floor, ceil, sin, cos, radians
import cadquery as cq
from cadquery import (
    Vertex,
    Vector,
    Edge,
    Wire,
    Face,
    Shell,
    Solid,
    Plane,
    Workplane,
    Compound,
)
import ocp_vscode

#
# ------------------------ User Parameters ------------------------------------------

d20_diameter = 120  # Diameter of smallest sphere which contains D20
make_pips = True  # D20 should have pips not numerals

PHI = (1 + sqrt(5)) / 2  # The Golden Ratio


class Icosahedron:
    """Icosahedron

    Args:
        diameter (float): Diameter of smallest sphere which contains the icosahedron

    Attributes:
        cq_object (Solid): the icosahedron object
    """

    icosahedron_edge_length = 2
    icosahedron_radius = (icosahedron_edge_length / 4) * sqrt(10 + 2 * sqrt(5))
    icosahedron_scale_factor = d20_diameter / (2 * icosahedron_radius)
    icosahedron_vertices = (
        [Vector(0, i, j * PHI) for i in [-1, 1] for j in [-1, 1]]
        + [Vector(i, j * PHI, 0) for i in [-1, 1] for j in [-1, 1]]
        + [Vector(i * PHI, 0, j) for i in [-1, 1] for j in [-1, 1]]
    )

    # The faces are arranged such that opposing faces sum to 21 (when numbered 1 to 20)
    vertex_indices_per_face = [
        [0, 2, 8],  # 1
        [1, 9, 3],  # 2
        [0, 6, 10],  # 3
        [3, 5, 7],  # 4
        [5, 9, 8],  # 5
        [10, 11, 7],  # 6
        [0, 8, 4],  # 7
        [6, 1, 11],  # 8
        [10, 7, 2],  # 9
        [4, 1, 6],  # 10
        [5, 2, 7],  # 11
        [4, 9, 1],  # 12
        [5, 8, 2],  # 13
        [11, 3, 7],  # 14
        [4, 8, 9],  # 15
        [6, 11, 10],  # 16
        [0, 4, 6],  # 17
        [3, 9, 5],  # 18
        [0, 10, 2],  # 19
        [11, 1, 3],  # 20
    ]

    @property
    def cq_object(self) -> cq.Solid:
        return self.icosahedron_solid

    def __init__(self, diameter: float):
        self.target_diameter = diameter
        self.nominal_radius = (2 / 4) * sqrt(10 + 2 * sqrt(5))
        self.scale = self.target_diameter / (2 * self.nominal_radius)

        # To see the vertices they need to be of the Vertex class - only used for display
        self.icosahedron_vertices_as_vertex = [
            Vertex.makeVertex(*v.toTuple()) for v in self.icosahedron_vertices
        ]

        # Create a list of three edges for each face
        self.icosahedron_edges_per_face = [
            [
                Edge.makeLine(
                    self.icosahedron_vertices[vertices[i]],
                    self.icosahedron_vertices[vertices[(i + 1) % len(vertices)]],
                )
                for i in range(len(vertices))
            ]
            for vertices in self.vertex_indices_per_face
        ]
        self.icosahedron_wires = [
            Wire.assembleEdges(e) for e in self.icosahedron_edges_per_face
        ]
        self.icosahedron_faces = [
            Face.makeFromWires(w, []) for w in self.icosahedron_wires
        ]
        self.icosahedron_shell = Shell.makeShell(self.icosahedron_faces)
        self.icosahedron_solid = Solid.makeSolid(self.icosahedron_shell).scale(
            self.scale
        )


class D20:
    """D20

    An icosahedron with labelled faces.

    Args:
        diameter (float): Diameter of smallest sphere which contains the icosahedron
        pips (bool): label faces with pips or numerals. Defaults to True.

    Attributes:
        cq_object (Solid): the icosahedron object
    """

    @staticmethod
    def pip_rotation_angle(face_number: int) -> int:
        pip_count = face_number % 10
        return -30 if face_number < 10 else 0 + 60 if pip_count >= 7 else 0

    @staticmethod
    def pip_location_angle(face_number: int) -> int:
        pip_count = face_number % 10
        return (pip_count - 1) * 120 + 60 * floor(pip_count / 7)

    @staticmethod
    def pip_location_radius(face_number: int) -> float:
        ring_radius = [
            0,
            1.35 * sqrt(6) / 9,
            1.35 * 2 * sqrt(6) / 9,
            1.35 * sqrt(6) / 9,
        ]
        pip_count = face_number % 10
        pip_layer = floor((pip_count + 2) / 3)
        return ring_radius[pip_layer]

    @property
    def cq_object(self) -> cq.Solid:
        return self._cq_object

    def __init__(self, diameter: float, pips: bool = True):
        self.target_diameter = diameter
        self.pips = pips
        self.nominal_radius = (2 / 4) * sqrt(10 + 2 * sqrt(5))
        self.scale = self.target_diameter / (2 * self.nominal_radius)

        self.icosahedron = Icosahedron(sqrt(10 + 2 * sqrt(5)))

        # Using the predefined edges and faces, create numerical labels for each face
        d20_label_list = []
        d20_pips_list = []
        for i, face in enumerate(self.icosahedron.icosahedron_faces):
            face_center = face.Center()
            face_plane = Plane(
                origin=face_center,
                xDir=-self.icosahedron.icosahedron_edges_per_face[i][0].tangentAt(0),
                normal=face.normalAt(face_center) * -1,
            )
            if self.pips:
                pip_count = i % 10 + 1
                pip_locations = [
                    cq.Location(
                        cq.Vector(
                            D20.pip_location_radius(j)
                            * cos(radians(D20.pip_location_angle(j) + 90)),
                            D20.pip_location_radius(j)
                            * sin(radians(D20.pip_location_angle(j) + 90)),
                            0,
                        ),
                        cq.Vector(0, 0, 1),
                        D20.pip_rotation_angle(i),
                    )
                    for j in range(pip_count)
                ]
                d20_pips_list.append(
                    Workplane(face_plane)
                    .pushPoints(pip_locations)
                    .polygon(3 * ceil((i + 1) / 10), 0.35)
                    .extrude(-0.14)
                    .val()
                )
                d20_pips = Compound.makeCompound(d20_pips_list)
                self._cq_object = self.icosahedron.cq_object.cut(d20_pips).scale(
                    self.scale
                )
            else:
                d20_label_list.append(
                    Workplane(face_plane)
                    .text(str(i + 1), fontsize=0.75, distance=-0.14)
                    .val()
                )
                d20_labels = Compound.makeCompound(d20_label_list)
                self._cq_object = self.icosahedron.cq_object.cut(d20_labels).scale(
                    self.scale
                )


d20_pips = D20(diameter=d20_diameter, pips=make_pips)
d20_diameter = 130
d20_nums = D20(diameter=d20_diameter, pips=False)

ocp_vscode.show_objects(d20_pips.cq_object)