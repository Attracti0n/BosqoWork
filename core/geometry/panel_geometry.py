from core.geometry.face_collection import FaceCollection
from core.geometry.edge_collection import EdgeCollection


class PanelGeometry:

    def __init__(self):

        #
        # Basic dimensions
        #

        self.Length = 0.0

        self.Width = 0.0

        self.Thickness = 0.0


        #
        # Axis mapping
        #

        self.LengthAxis = "Z"

        self.WidthAxis = "Y"

        self.ThicknessAxis = "X"


        #
        # Position
        #

        self.Placement = None

        self.Center = None


        #
        # Bounding box
        #

        self.BoundBox = None


        #
        # Geometry collections
        #

        self.Faces = FaceCollection()

        self.Edges = EdgeCollection()


        #
        # Source
        #

        self.Shape = None


        #
        # Classification
        #

        self.IsPanel = False

        self.Message = ""


    def setDimensions(
        self,
        length,
        width,
        thickness
    ):

        self.Length = abs(length)

        self.Width = abs(width)

        self.Thickness = abs(thickness)


    def setAxes(
        self,
        lengthAxis,
        widthAxis,
        thicknessAxis
    ):

        self.LengthAxis = lengthAxis

        self.WidthAxis = widthAxis

        self.ThicknessAxis = thicknessAxis


    def setShape(self, shape):

        self.Shape = shape


    def setPlacement(self, placement):

        self.Placement = placement


    def __repr__(self):

        return (
            "PanelGeometry("
            f"Length={self.Length}, "
            f"Width={self.Width}, "
            f"Thickness={self.Thickness})"
        )