from library.material_library import MaterialLibrary



class ManufacturingData:


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

        self.MaterialCode = ""

        self.Material = ""

        self.MaterialData = None

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
        # Manufacturing
        #

        self.Operations = []

        self.Status = "Ready"



    #
    # Load from PartData
    #

    def fromPartData(
        self,
        part
    ):


        #
        # Identification
        #

        self.Code = part.Code

        self.PartNumber = part.Code

        self.Name = part.Name

        self.Role = part.Role



        #
        # Dimensions
        #

        self.Length = part.Length

        self.Width = part.Width

        self.Thickness = part.Thickness



        #
        # Material
        #

        self.MaterialCode = part.MaterialCode


        material = part.getMaterial()


        if material:


            self.MaterialData = material


            self.Material = material.Name


            if not self.Thickness:

                self.Thickness = material.Thickness


            if not self.Finish:

                self.Finish = material.Finish



        #
        # Other data
        #

        self.GrainDirection = part.GrainDirection



        #
        # Edges
        #

        self.Edges["Top"] = part.EdgeTop

        self.Edges["Bottom"] = part.EdgeBottom

        self.Edges["Left"] = part.EdgeLeft

        self.Edges["Right"] = part.EdgeRight



        #
        # Quantity
        #

        self.Quantity = part.Quantity



        #
        # Operations
        #

        self.Operations = list(
            part.Operations
        )


        return self



    #
    # Create from object
    #

    def fromObject(
        self,
        obj
    ):

        from core.data.part_data import PartData


        part = PartData()


        part.fromObject(
            obj
        )


        return self.fromPartData(
            part
        )



    #
    # Material price
    #

    def getMaterialPrice(
        self
    ):


        if self.MaterialData:

            return self.MaterialData.Price


        return 0.0



    #
    # Export
    #

    def toDict(
        self
    ):


        return {


            "Code":
                self.Code,


            "PartNumber":
                self.PartNumber,


            "Name":
                self.Name,


            "Role":
                self.Role,


            "Length":
                self.Length,


            "Width":
                self.Width,


            "Thickness":
                self.Thickness,


            "MaterialCode":
                self.MaterialCode,


            "Material":
                self.Material,


            "Finish":
                self.Finish,


            "Quantity":
                self.Quantity,


            "Edges":
                self.Edges,


            "Operations":
                self.Operations,


            "Status":
                self.Status

        }