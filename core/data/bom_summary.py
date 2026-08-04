class BOMSummary:


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
        # Area
        #

        self.TotalArea = 0.0


        #
        # Volume
        #

        self.TotalVolume = 0.0


        #
        # Manufacturing
        #

        self.TotalOperations = 0

        self.TotalEdgeLength = 0.0


    #
    # Export
    #

    def toDict(self):

        return {

            "TotalParts":
                self.TotalParts,

            "TotalUniqueParts":
                self.TotalUniqueParts,

            "TotalMaterials":
                self.TotalMaterials,

            "Materials":
                self.Materials,

            "TotalArea":
                self.TotalArea,

            "TotalVolume":
                self.TotalVolume,

            "TotalOperations":
                self.TotalOperations,

            "TotalEdgeLength":
                self.TotalEdgeLength

        }


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