from core.data.geometry_data import GeometryData


class MeshAnalyzer:

    #
    # Accepted panel thickness range (mm)
    #

    MIN_THICKNESS = 3.0
    MAX_THICKNESS = 60.0

    @staticmethod
    def analyze(obj):

        if obj is None:

            raise Exception(
                "Object is None."
            )

        if not hasattr(obj, "Mesh"):

            raise Exception(
                "Object has no Mesh."
            )

        mesh = obj.Mesh

        box = mesh.BoundBox

        data = GeometryData()

        #
        # Dimensions
        #

        x = float(box.XLength)
        y = float(box.YLength)
        z = float(box.ZLength)

        values = [
            ("X", x),
            ("Y", y),
            ("Z", z)
        ]

        values.sort(
            key=lambda item: item[1]
        )

        #
        # Dimensions
        #

        data.Thickness = round(values[0][1], 1)
        data.Width = round(values[1][1], 1)
        data.Length = round(values[2][1], 1)

        #
        # Axis mapping
        #

        data.ThicknessAxis = values[0][0]
        data.WidthAxis = values[1][0]
        data.LengthAxis = values[2][0]

        #
        # Orientation
        #

        if data.ThicknessAxis == "X":

            data.Orientation = "YZ"

        elif data.ThicknessAxis == "Y":

            data.Orientation = "XZ"

        else:

            data.Orientation = "XY"

        #
        # Geometry
        #

        data.Center = box.Center
        data.BoundingBox = box

        #
        # Mesh information
        #

        data.Area = 0.0
        data.Volume = 0.0

        data.Faces = mesh.CountFacets
        data.Edges = mesh.CountEdges
        data.Vertices = mesh.CountPoints

        #
        # Meshes are not BRep solids
        #

        data.IsSolid = False

        return data