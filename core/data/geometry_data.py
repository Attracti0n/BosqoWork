class GeometryData:

    def __init__(self):

        #
        # Main dimensions
        #

        self.Length = 0.0
        self.Width = 0.0
        self.Thickness = 0.0

        #
        # Axis mapping
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
        # Geometry
        #

        self.Center = None
        self.BoundingBox = None

        self.Faces = 0
        self.Edges = 0
        self.Vertices = 0

        #
        # Solid
        #

        self.IsSolid = False