class PanelData:

    def __init__(self):

        #
        # Recognition
        #

        self.IsPanel = False
        self.Reason = ""
        self.Message = ""

        #
        # Geometry
        #

        self.Length = 0
        self.Width = 0
        self.Thickness = 0

        self.LengthAxis = ""
        self.WidthAxis = ""
        self.ThicknessAxis = ""

        self.BoundBox = None

        #
        # Source object
        #

        self.Object = None