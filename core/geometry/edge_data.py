class EdgeData:

    def __init__(self):

        #
        # Identification
        #

        self.Name = ""

        #
        # Geometry
        #

        self.Edge = None
        self.Start = None
        self.End = None
        self.Center = None

        self.Length = 0.0

        #
        # Orientation
        #

        self.Axis = ""

        #
        # Adjacent faces
        #

        self.Face1 = ""
        self.Face2 = ""

        #
        # Manufacturing
        #

        self.Visible = True

        self.GrainDirection = ""

        #
        # Edgebanding
        #

        self.HasEdgeband = False

        self.EdgebandMaterial = ""

        self.EdgebandThickness = 0.0

        #
        # Machining
        #

        self.Machinings = []

    def addMachining(self, machining):

        self.Machinings.append(machining)

    @property
    def IsEdgebanded(self):

        return self.HasEdgeband

    def __repr__(self):

        return (
            f"EdgeData("
            f"Name='{self.Name}', "
            f"Length={self.Length}, "
            f"Axis='{self.Axis}')"
        )