class FaceData:

    def __init__(self):

        #
        # Identification
        #

        self.Name = ""


        #
        # FreeCAD geometry
        #

        self.Face = None

        self.Edges = []

        self.Vertexes = []


        #
        # Geometry information
        #

        self.Area = 0.0

        self.Center = None

        self.Normal = None


        #
        # Manufacturing
        #

        self.Visible = True

        self.Material = ""

        self.Finish = ""


        #
        # Machining
        #

        self.Machinings = []


    def addMachining(self, machining):

        self.Machinings.append(
            machining
        )


    def __repr__(self):

        return (
            f"FaceData("
            f"Name='{self.Name}', "
            f"Area={self.Area})"
        )