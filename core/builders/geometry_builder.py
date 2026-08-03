import FreeCAD
import Part


class GeometryBuilder:


    @staticmethod
    def createBox(obj):


        #
        # Validate dimensions
        #

        if (
            obj.Length <= 0
            or obj.Width <= 0
            or obj.Thickness <= 0
        ):

            return None


        #
        # Assign dimensions to global axes
        #

        size = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }


        size[obj.LengthAxis] = abs(float(obj.Length))
        size[obj.WidthAxis] = abs(float(obj.Width))
        size[obj.ThicknessAxis] = abs(float(obj.Thickness))


        #
        # Geometry is ALWAYS local.
        #
        # Position is handled only by PlacementBuilder.
        #

        shape = Part.makeBox(
            size["X"],
            size["Y"],
            size["Z"],
            FreeCAD.Vector(0, 0, 0)
        )


        return shape