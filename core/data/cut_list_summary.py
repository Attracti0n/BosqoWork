class CutListSummary:


    def __init__(self):


        #
        # Parts
        #

        self.TotalParts = 0

        self.TotalUniqueParts = 0


        #
        # Materials
        #

        self.TotalMaterials = 0

        self.Materials = {}


        #
        # Dimensions
        #

        self.TotalArea = 0.0

        self.TotalVolume = 0.0


        #
        # Boards
        #

        self.TotalBoards = 0

        self.BoardArea = 0.0

        self.UsedArea = 0.0

        self.WasteArea = 0.0

        self.WastePercent = 0.0


        #
        # Manufacturing
        #

        self.TotalOperations = 0

        self.TotalEdgeLength = 0.0



    #
    # Import
    #

    def fromDict(
        self,
        data
    ):


        for key, value in data.items():

            if hasattr(
                self,
                key
            ):

                setattr(
                    self,
                    key,
                    value
                )


        return self



    #
    # Export
    #

    def toDict(self):


        return {

            "TotalParts": self.TotalParts,

            "TotalUniqueParts": self.TotalUniqueParts,

            "TotalMaterials": self.TotalMaterials,

            "Materials": self.Materials,

            "TotalArea": self.TotalArea,

            "TotalVolume": self.TotalVolume,

            "TotalBoards": self.TotalBoards,

            "BoardArea": self.BoardArea,

            "UsedArea": self.UsedArea,

            "WasteArea": self.WasteArea,

            "WastePercent": self.WastePercent,

            "TotalOperations": self.TotalOperations,

            "TotalEdgeLength": self.TotalEdgeLength

        }



    def clear(self):


        self.__init__()



    def __repr__(self):


        return (

            "CutListSummary("

            f"Parts={self.TotalParts}, "

            f"Materials={self.TotalMaterials}, "

            f"Waste={self.WastePercent:.2f}%)"

        )