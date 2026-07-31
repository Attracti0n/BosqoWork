import FreeCAD
import Part


class GeometryBuilder:

    @staticmethod
    def createBox(obj):

        if (
            obj.Length <= 0
            or obj.Width <= 0
            or obj.Thickness <= 0
        ):
            return None

        #
        # Assign size to each global axis
        #

        size = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }

        size[obj.LengthAxis] = float(obj.Length)
        size[obj.WidthAxis] = float(obj.Width)
        size[obj.ThicknessAxis] = float(obj.Thickness)

        #
        # Origin
        #

        if hasattr(obj, "OriginalObject") and obj.OriginalObject:

            source = obj.OriginalObject

            if hasattr(source, "Mesh"):

                box = source.Mesh.BoundBox

            elif hasattr(source, "Shape"):

                box = source.Shape.BoundBox

            else:

                box = None

            if box:

                origin = FreeCAD.Vector(
                    box.XMin,
                    box.YMin,
                    box.ZMin
                )

            else:

                origin = FreeCAD.Vector(
                    float(obj.OriginX),
                    float(obj.OriginY),
                    float(obj.OriginZ)
                )

        else:

            origin = FreeCAD.Vector(
                float(obj.OriginX),
                float(obj.OriginY),
                float(obj.OriginZ)
            )

        #
        # Create box
        #

        return Part.makeBox(
            size["X"],
            size["Y"],
            size["Z"],
            origin
        )