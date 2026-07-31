import FreeCAD


class PlaneData:

    def __init__(self):

        #
        # Face
        #

        self.Face = None

        #
        # Geometry
        #

        self.Area = 0.0

        self.Center = FreeCAD.Vector()

        self.Normal = FreeCAD.Vector()

        #
        # Surface
        #

        self.SurfaceType = ""

        #
        # Recognition
        #

        self.IsPlane = False

        self.Reason = ""