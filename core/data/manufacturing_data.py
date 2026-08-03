class ManufacturingData:


    def __init__(self):


        #
        # Identification
        #

        self.Code = ""

        self.Name = ""

        self.Description = ""

        self.PartNumber = ""

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

        self.Edges = {

            "Top": "",

            "Bottom": "",

            "Left": "",

            "Right": ""

        }



        #
        # Machining operations
        #

        self.Operations = []



        #
        # Status
        #

        self.Status = "Ready"



    #
    # Create from PartData
    #

    def fromPartData(
        self,
        part_data
    ):


        #
        # Identification
        #

        self.Code = part_data.Code

        self.Name = part_data.Name

        self.Description = part_data.Name

        self.Role = part_data.Role



        #
        # Dimensions
        #

        self.Length = part_data.Length

        self.Width = part_data.Width

        self.Thickness = part_data.Thickness



        #
        # Manufacturing number
        #

        self.PartNumber = (

            f"{self.Code}-"
            f"{int(self.Length)}-"
            f"{int(self.Width)}-"
            f"{int(self.Thickness)}"

        )



        #
        # Material
        #

        self.Material = part_data.Material

        self.MaterialCode = part_data.MaterialCode

        self.Finish = part_data.Finish

        self.GrainDirection = part_data.GrainDirection



        #
        # Edges
        #

        self.Edges["Top"] = part_data.EdgeTop

        self.Edges["Bottom"] = part_data.EdgeBottom

        self.Edges["Left"] = part_data.EdgeLeft

        self.Edges["Right"] = part_data.EdgeRight



        return self



    #
    # Add operation
    #

    def addOperation(
        self,
        operation
    ):

        self.Operations.append(
            operation
        )



    #
    # Export dictionary
    #

    def toDict(self):

        return {


            "Code": self.Code,

            "PartNumber": self.PartNumber,

            "Name": self.Name,

            "Description": self.Description,

            "Role": self.Role,


            "Dimensions":
            {

                "Length": self.Length,

                "Width": self.Width,

                "Thickness": self.Thickness

            },


            "Material":
            {

                "Name": self.Material,

                "Code": self.MaterialCode,

                "Finish": self.Finish,

                "Grain": self.GrainDirection

            },


            "Quantity": self.Quantity,


            "Edges": self.Edges,


            "Operations": self.Operations,


            "Status": self.Status

        }