class GeometryData:

    def __init__(self):

        #
        # Main dimensions
        #
        # Dimensions are always positive.
        # Position and orientation are handled separately.
        #

        self.Length = 0.0
        self.Width = 0.0
        self.Thickness = 0.0


        #
        # Axis mapping
        #
        # Defines which global axis contains each dimension.
        # It does not contain a sign.
        #

        self.LengthAxis = ""

        self.WidthAxis = ""

        self.ThicknessAxis = ""


        #
        # Orientation
        #

        self.Orientation = ""


        #
        # Physical properties
        #

        self.Area = 0.0

        self.Volume = 0.0


        #
        # Geometry position
        #
        # Center can contain negative coordinates.
        # Example:
        # Vector(-1500, 200, 0)
        #

        self.Center = None

        self.BoundingBox = None


        #
        # Mesh information
        #

        self.Faces = 0

        self.Edges = 0

        self.Vertices = 0


        #
        # Solid
        #

        self.IsSolid = False