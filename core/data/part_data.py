from library.material_library import MaterialLibrary



class PartData:


    def __init__(self):


        #
        # Identification
        #

        self.Code = ""

        self.Name = ""

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
        # Manufacturing
        #

        self.Quantity = 1

        self.Operations = []



        #
        # Status
        #

        self.Status = "Ready"



    #
    # Material object
    #

    def getMaterial(
        self
    ):


        if not self.MaterialCode:

            return None


        return MaterialLibrary.get(
            self.MaterialCode
        )



    #
    # Apply material data
    #

    def applyMaterial(
        self
    ):


        material = self.getMaterial()


        if material is None:

            return



        self.Material = material.Name



        if not self.Thickness:

            self.Thickness = material.Thickness



        if not self.Finish:

            self.Finish = material.Finish



    #
    # Load from FreeCAD object
    #

    def fromObject(
        self,
        obj
    ):


        if hasattr(
            obj,
            "Code"
        ):

            self.Code = obj.Code



        if hasattr(
            obj,
            "Label"
        ):

            self.Name = obj.Label



        if hasattr(
            obj,
            "Role"
        ):

            self.Role = obj.Role



        #
        # Dimensions
        #

        if hasattr(
            obj,
            "Length"
        ):

            self.Length = obj.Length



        if hasattr(
            obj,
            "Width"
        ):

            self.Width = obj.Width



        if hasattr(
            obj,
            "Thickness"
        ):

            self.Thickness = obj.Thickness



        #
        # Material
        #

        if hasattr(
            obj,
            "Material"
        ):

            self.Material = obj.Material



        if hasattr(
            obj,
            "MaterialCode"
        ):

            self.MaterialCode = obj.MaterialCode



        if hasattr(
            obj,
            "Finish"
        ):

            self.Finish = obj.Finish



        if hasattr(
            obj,
            "GrainDirection"
        ):

            self.GrainDirection = obj.GrainDirection



        #
        # Edges
        #

        for edge in [

            "EdgeTop",
            "EdgeBottom",
            "EdgeLeft",
            "EdgeRight"

        ]:


            if hasattr(
                obj,
                edge
            ):

                setattr(
                    self,
                    edge,
                    getattr(
                        obj,
                        edge
                    )
                )



        self.applyMaterial()


        return self



    #
    # Export
    #

    def toDict(
        self
    ):


        return {


            "Code":
                self.Code,


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


            "Material":
                self.Material,


            "MaterialCode":
                self.MaterialCode,


            "Finish":
                self.Finish,


            "GrainDirection":
                self.GrainDirection,


            "EdgeTop":
                self.EdgeTop,


            "EdgeBottom":
                self.EdgeBottom,


            "EdgeLeft":
                self.EdgeLeft,


            "EdgeRight":
                self.EdgeRight,


            "Quantity":
                self.Quantity,


            "Operations":
                self.Operations,


            "Status":
                self.Status

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



    def __repr__(
        self
    ):


        return (

            f"PartData("
            f"{self.Code}, "
            f"{self.Length}x"
            f"{self.Width}x"
            f"{self.Thickness}, "
            f"{self.Material})"

        )