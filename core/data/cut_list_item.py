class CutListItem:


    def __init__(self):


        #
        # Identification
        #

        self.Code = ""

        self.PartNumber = ""

        self.Name = ""

        self.Description = ""

        self.Role = ""


        #
        # Dimensions
        #

        self.Length = 0

        self.Width = 0

        self.Thickness = 0


        #
        # Material
        #

        self.Material = ""

        self.MaterialCode = ""

        self.Finish = ""

        self.GrainDirection = ""


        #
        # Quantity
        #

        self.Quantity = 1


        #
        # Edgebanding
        #

        self.EdgeTop = ""

        self.EdgeBottom = ""

        self.EdgeLeft = ""

        self.EdgeRight = ""


        #
        # Manufacturing
        #

        self.Operations = []

        self.Status = "Ready"



    #
    # Create from ManufacturingData
    #

    def fromManufacturingData(
        self,
        manufacturing
    ):


        self.Code = manufacturing.Code

        self.PartNumber = manufacturing.PartNumber

        self.Name = manufacturing.Name

        self.Description = manufacturing.Description

        self.Role = manufacturing.Role


        self.Length = manufacturing.Length

        self.Width = manufacturing.Width

        self.Thickness = manufacturing.Thickness


        self.Material = manufacturing.Material

        self.MaterialCode = manufacturing.MaterialCode

        self.Finish = manufacturing.Finish

        self.GrainDirection = manufacturing.GrainDirection


        self.Quantity = manufacturing.Quantity


        self.EdgeTop = manufacturing.Edges["Top"]

        self.EdgeBottom = manufacturing.Edges["Bottom"]

        self.EdgeLeft = manufacturing.Edges["Left"]

        self.EdgeRight = manufacturing.Edges["Right"]


        self.Operations = list(
            manufacturing.Operations
        )

        self.Status = manufacturing.Status


        return self



    #
    # Clone
    #

    def clone(self):

        item = CutListItem()

        item.fromDict(
            self.toDict()
        )

        return item



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

            "Code": self.Code,

            "PartNumber": self.PartNumber,

            "Name": self.Name,

            "Description": self.Description,

            "Role": self.Role,


            "Length": self.Length,

            "Width": self.Width,

            "Thickness": self.Thickness,


            "Material": self.Material,

            "MaterialCode": self.MaterialCode,

            "Finish": self.Finish,

            "GrainDirection": self.GrainDirection,


            "Quantity": self.Quantity,


            "EdgeTop": self.EdgeTop,

            "EdgeBottom": self.EdgeBottom,

            "EdgeLeft": self.EdgeLeft,

            "EdgeRight": self.EdgeRight,


            "Operations": self.Operations,


            "Status": self.Status

        }



    def __repr__(self):

        return (

            f"CutListItem("
            f"{self.Code}, "
            f"{self.Length} x "
            f"{self.Width} x "
            f"{self.Thickness}, "
            f"Qty={self.Quantity})"

        )