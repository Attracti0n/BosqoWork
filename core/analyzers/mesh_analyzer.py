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
        # IMPORTANT:
        # FreeCAD dimensions must always be positive.
        # Orientation is handled separately by Placement.
        #

        x = abs(float(box.XLength))
        y = abs(float(box.YLength))
        z = abs(float(box.ZLength))


        values = [
            ("X", x),
            ("Y", y),
            ("Z", z)
        ]


        #
        # Sort axes by size
        #
        # Smallest dimension = thickness
        # Middle dimension   = width
        # Largest dimension  = length
        #

        values.sort(
            key=lambda item: item[1]
        )


        #
        # Positive dimensions only
        #

        data.Thickness = round(values[0][1], 1)

        data.Width = round(values[1][1], 1)

        data.Length = round(values[2][1], 1)



        #
        # Axis mapping
        #
        # The axis name describes where the dimension comes from.
        # It does NOT change the dimension sign.
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
        # Position information
        #
        # Position and rotation are stored separately.
        # Never use negative dimensions for positioning.
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