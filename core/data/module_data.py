class ModuleData:

    def __init__(self):

        #
        # Recognition
        #

        self.IsModule = False
        self.Message = ""

        #
        # Parts
        #

        self.Parts = []

        #
        # Roles
        #

        self.LeftSide = None
        self.RightSide = None

        self.Top = None
        self.Bottom = None

        self.Back = None

        self.Shelves = []

        self.Doors = []
        self.Drawers = []

        #
        # Overall dimensions
        #

        self.Width = 0.0
        self.Height = 0.0
        self.Depth = 0.0