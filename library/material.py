class Material:


    def __init__(self):


        #
        # Identification
        #

        self.Code = ""

        self.Name = ""

        self.Category = "Panel"


        #
        # Technical
        #

        self.Thickness = 0.0

        self.Density = 0.0

        self.Core = ""

        self.Finish = ""

        self.Color = ""

        self.Texture = ""

        self.GrainDirection = True


        #
        # Commercial
        #

        self.Supplier = ""

        self.Manufacturer = ""

        self.Reference = ""


        #
        # Stock
        #

        self.SheetLength = 2440.0

        self.SheetWidth = 1220.0

        self.Unit = "m²"

        self.Price = 0.0

        self.Currency = "EUR"

        self.Active = True


        #
        # Extra
        #

        self.Notes = ""


    #
    # Clone
    #

    def clone(self):

        material = Material()

        material.fromDict(
            self.toDict()
        )

        return material


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

            #
            # Identification
            #

            "Code":
                self.Code,

            "Name":
                self.Name,

            "Category":
                self.Category,


            #
            # Technical
            #

            "Thickness":
                self.Thickness,

            "Density":
                self.Density,

            "Core":
                self.Core,

            "Finish":
                self.Finish,

            "Color":
                self.Color,

            "Texture":
                self.Texture,

            "GrainDirection":
                self.GrainDirection,


            #
            # Commercial
            #

            "Supplier":
                self.Supplier,

            "Manufacturer":
                self.Manufacturer,

            "Reference":
                self.Reference,


            #
            # Stock
            #

            "SheetLength":
                self.SheetLength,

            "SheetWidth":
                self.SheetWidth,

            "Unit":
                self.Unit,

            "Price":
                self.Price,

            "Currency":
                self.Currency,

            "Active":
                self.Active,


            #
            # Extra
            #

            "Notes":
                self.Notes

        }


    def __repr__(self):

        return (

            f"Material("
            f"{self.Code}, "
            f"{self.Name}, "
            f"{self.Thickness} mm)"

        )