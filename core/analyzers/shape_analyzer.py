from core.data.geometry_data import GeometryData


class ShapeAnalyzer:

    @staticmethod
    def analyze(obj):

        shape = obj.Shape

        if shape.isNull():

            raise Exception(
                "Empty Shape."
            )

        data = GeometryData()

        box = shape.BoundBox

        x = float(box.XLength)
        y = float(box.YLength)
        z = float(box.ZLength)

        dimensions = sorted([x, y, z])

        data.Thickness = dimensions[0]
        data.Width = dimensions[1]
        data.Length = dimensions[2]

        tolerance = 0.01

        if abs(x - data.Thickness) < tolerance:

            data.Orientation = "YZ"

        elif abs(y - data.Thickness) < tolerance:

            data.Orientation = "XZ"

        else:

            data.Orientation = "XY"

        data.Area = shape.Area
        data.Volume = shape.Volume

        data.Center = shape.CenterOfMass

        data.BoundingBox = box

        data.Faces = len(shape.Faces)
        data.Edges = len(shape.Edges)
        data.Vertices = len(shape.Vertexes)

        data.IsSolid = len(shape.Solids) > 0

        return data