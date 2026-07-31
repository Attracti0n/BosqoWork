import FreeCAD

from core.data.orientation_data import OrientationData


class OrientationAnalyzer:

    @staticmethod
    def analyze(obj):

        data = OrientationData()

        #
        # Shape
        #

        if hasattr(obj, "Shape"):

            shape = obj.Shape

            if (
                shape is not None
                and not shape.isNull()
            ):

                box = shape.BoundBox

                OrientationAnalyzer.fromBoundingBox(
                    data,
                    box
                )

                data.Center = shape.CenterOfMass
                data.IsValid = True

                return data

        #
        # Mesh
        #

        if hasattr(obj, "Mesh"):

            mesh = obj.Mesh

            if mesh is not None:

                box = mesh.BoundBox

                OrientationAnalyzer.fromBoundingBox(
                    data,
                    box
                )

                data.Center = box.Center
                data.IsValid = True

                return data

        raise Exception(
            "Object has no supported geometry."
        )

    @staticmethod
    def fromBoundingBox(data, box):

        x = float(box.XLength)
        y = float(box.YLength)
        z = float(box.ZLength)

        axes = [

            ("X", x, FreeCAD.Vector(1, 0, 0)),
            ("Y", y, FreeCAD.Vector(0, 1, 0)),
            ("Z", z, FreeCAD.Vector(0, 0, 1))

        ]

        axes.sort(
            key=lambda item: item[1]
        )

        #
        # Thickness
        #

        data.Thickness = axes[0][1]
        data.ThicknessAxis = axes[0][2]

        #
        # Width
        #

        data.Width = axes[1][1]
        data.WidthAxis = axes[1][2]

        #
        # Length
        #

        data.Length = axes[2][1]
        data.LengthAxis = axes[2][2]

        #
        # Local coordinate system
        #

        data.XAxis = FreeCAD.Vector(1, 0, 0)
        data.YAxis = FreeCAD.Vector(0, 1, 0)
        data.ZAxis = FreeCAD.Vector(0, 0, 1)