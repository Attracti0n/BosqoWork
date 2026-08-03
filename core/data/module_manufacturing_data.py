class ModuleManufacturingData:


    def __init__(self):


        #
        # Identification
        #

        self.Name = ""

        self.Type = ""



        #
        # Dimensions
        #

        self.Width = 0

        self.Height = 0

        self.Depth = 0



        #
        # Manufacturing parts
        #

        self.Parts = []



        #
        # Status
        #

        self.Status = "Ready"



    #
    # Load from ModuleData
    #

    def fromModuleData(
        self,
        module_data
    ):


        from core.data.manufacturing_data import ManufacturingData



        #
        # Module information
        #

        self.Name = module_data.Name

        self.Type = module_data.Type


        self.Width = module_data.Width

        self.Height = module_data.Height

        self.Depth = module_data.Depth



        #
        # Convert parts
        #

        for part in module_data.Parts:


            manufacturing = ManufacturingData()


            manufacturing.fromPartData(
                part
            )


            self.Parts.append(
                manufacturing
            )



        return self



    #
    # Add operation to a part
    #

    def addPartOperation(
        self,
        code,
        operation
    ):


        for part in self.Parts:


            if part.Code == code:


                part.addOperation(
                    operation
                )



    #
    # Export
    #

    def toDict(self):


        return {


            "Name": self.Name,

            "Type": self.Type,


            "Dimensions":
            {

                "Width": self.Width,

                "Height": self.Height,

                "Depth": self.Depth

            },


            "Parts":
            [

                part.toDict()

                for part in self.Parts

            ],


            "Status": self.Status

        }