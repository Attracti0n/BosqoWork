from core.data.part_data import PartData


class ModuleData:


    def __init__(self):


        #
        # Identification
        #

        self.Name = ""

        self.Code = ""

        self.Type = ""


        #
        # Dimensions
        #

        self.Width = 0

        self.Height = 0

        self.Depth = 0


        #
        # Parts
        #

        self.Parts = []


        #
        # Status
        #

        self.Status = "Created"


    #
    # Add part
    #

    def addPart(
        self,
        part_data
    ):

        self.Parts.append(
            part_data
        )


    #
    # Load from FreeCAD module
    #

    def fromObject(
        self,
        obj
    ):


        self.Parts = []


        #
        # Identification
        #

        if hasattr(obj, "Label"):

            self.Name = obj.Label


        if hasattr(obj, "Code"):

            self.Code = obj.Code


        if hasattr(obj, "Type"):

            self.Type = obj.Type


        #
        # Dimensions
        #

        if hasattr(obj, "Width"):

            self.Width = obj.Width


        if hasattr(obj, "Height"):

            self.Height = obj.Height


        if hasattr(obj, "Depth"):

            self.Depth = obj.Depth


        #
        # Parts
        #

        if hasattr(obj, "Group"):

            for child in obj.Group:

                #
                # Only BosqoPart objects
                #

                if not hasattr(
                    child,
                    "Length"
                ):
                    continue


                part = PartData()

                part.fromObject(
                    child
                )

                self.addPart(
                    part
                )


        return self


    #
    # Export dictionary
    #

    def toDict(self):

        return {

            "Name": self.Name,

            "Code": self.Code,

            "Type": self.Type,

            "Width": self.Width,

            "Height": self.Height,

            "Depth": self.Depth,

            "Status": self.Status,

            "Parts": [

                part.toDict()

                for part in self.Parts

            ]

        }