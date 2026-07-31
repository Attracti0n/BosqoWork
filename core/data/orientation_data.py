import FreeCAD


class OrientationData:

    def __init__(self):

        #
        # Local coordinate system
        #

        self.XAxis = FreeCAD.Vector(1, 0, 0)
        self.YAxis = FreeCAD.Vector(0, 1, 0)
        self.ZAxis = FreeCAD.Vector(0, 0, 1)

        #
        # Center of the object
        #

        self.Center = FreeCAD.Vector(0, 0, 0)

        #
        # Bounding box dimensions
        #

        self.Length = 0.0
        self.Width = 0.0
        self.Thickness = 0.0

        #
        # Main axes
        #

        self.LengthAxis = None
        self.WidthAxis = None
        self.ThicknessAxis = None

        #
        # Validation
        #

        self.IsValid = False