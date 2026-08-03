class PartData:


    def __init__(self):


        #
        # Identification
        #

        self.Code = ""

        self.Name = ""

        self.PartType = ""

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
        # Edgebanding
        #

        self.EdgeTop = ""

        self.EdgeBottom = ""

        self.EdgeLeft = ""

        self.EdgeRight = ""



        #
        # Module relation
        #

        self.Module = None



        #
        # Source
        #

        self.Source = ""



        #
        # Geometry state
        #

        self.GeometryStatus = "Not analyzed"



    #
    # Convert from FreeCAD object
    #

    def fromObject(self, obj):


        if hasattr(obj, "Code"):

            self.Code = obj.Code


        if hasattr(obj, "Label"):

            self.Name = obj.Label


        if hasattr(obj, "PartType"):

            self.PartType = obj.PartType


        if hasattr(obj, "Role"):

            self.Role = obj.Role



        #
        # Dimensions
        #

        if hasattr(obj, "Length"):

            self.Length = obj.Length


        if hasattr(obj, "Width"):

            self.Width = obj.Width


        if hasattr(obj, "Thickness"):

            self.Thickness = obj.Thickness



        #
        # Material
        #

        if hasattr(obj, "Material"):

            self.Material = obj.Material


        if hasattr(obj, "MaterialCode"):

            self.MaterialCode = obj.MaterialCode


        if hasattr(obj, "GrainDirection"):

            self.GrainDirection = obj.GrainDirection



        #
        # Edges
        #

        if hasattr(obj, "EdgeTop"):

            self.EdgeTop = obj.EdgeTop


        if hasattr(obj, "EdgeBottom"):

            self.EdgeBottom = obj.EdgeBottom


        if hasattr(obj, "EdgeLeft"):

            self.EdgeLeft = obj.EdgeLeft


        if hasattr(obj, "EdgeRight"):

            self.EdgeRight = obj.EdgeRight



        #
        # Source
        #

        if hasattr(obj, "Source"):

            self.Source = obj.Source



        return self



    #
    # Export dictionary
    #

    def toDict(self):

        return {


            "Code": self.Code,

            "Name": self.Name,

            "PartType": self.PartType,

            "Role": self.Role,


            "Length": self.Length,

            "Width": self.Width,

            "Thickness": self.Thickness,


            "Material": self.Material,

            "MaterialCode": self.MaterialCode,

            "Finish": self.Finish,

            "GrainDirection": self.GrainDirection,


            "EdgeTop": self.EdgeTop,

            "EdgeBottom": self.EdgeBottom,

            "EdgeLeft": self.EdgeLeft,

            "EdgeRight": self.EdgeRight,


            "Source": self.Source,


            "GeometryStatus": self.GeometryStatus

        }