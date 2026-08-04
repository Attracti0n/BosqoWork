import FreeCAD


class ModuleCalculator:


    @staticmethod
    def calculate(
        module,
        definition
    ):

        code = definition["Code"]

        role = definition["Role"]


        #
        # Module parameters
        #

        panel_thickness = module.PanelThickness

        back_thickness = module.BackThickness

        back_inset = module.BackInset


        #
        # Base data
        #

        data = {

            "Code":
                code,

            "Role":
                role,

            "Source":
                "Module",

            "Material":
                "",

            "MaterialCode":
                "",


            #
            # Default orientation
            #

            "LengthAxis":
                "Z",

            "WidthAxis":
                "Y",

            "ThicknessAxis":
                "X",


            #
            # Default placement
            #

            "Placement":
                FreeCAD.Placement(

                    FreeCAD.Vector(
                        0,
                        0,
                        0
                    ),

                    FreeCAD.Rotation()

                )

        }


        #
        # Side panels
        #

        if role == "Side":

            data["Length"] = (
                module.Height
            )

            data["Width"] = (
                module.Depth
            )

            data["Thickness"] = (
                panel_thickness
            )


            data["LengthAxis"] = "Z"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "X"


            #
            # Left side
            #

            if code == "LS":

                data["Label"] = (
                    "Lateral izquierdo"
                )


                position = FreeCAD.Vector(

                    0,

                    0,

                    0

                )


            #
            # Right side
            #

            else:

                data["Label"] = (
                    "Lateral derecho"
                )


                position = FreeCAD.Vector(

                    module.Width
                    - panel_thickness,

                    0,

                    0

                )


            data["Placement"] = (
                FreeCAD.Placement(

                    position,

                    FreeCAD.Rotation()

                )
            )


        #
        # Top panel
        #

        elif role == "Top":

            data["Length"] = (

                module.Width

                - (
                    panel_thickness
                    * 2
                )

            )

            data["Width"] = (
                module.Depth
            )

            data["Thickness"] = (
                panel_thickness
            )


            data["Label"] = (
                "Tapa"
            )


            data["LengthAxis"] = "X"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "Z"


            data["Placement"] = (
                FreeCAD.Placement(

                    FreeCAD.Vector(

                        panel_thickness,

                        0,

                        module.Height
                        - panel_thickness

                    ),

                    FreeCAD.Rotation()

                )
            )


        #
        # Bottom panel
        #

        elif role == "Bottom":

            data["Length"] = (

                module.Width

                - (
                    panel_thickness
                    * 2
                )

            )

            data["Width"] = (
                module.Depth
            )

            data["Thickness"] = (
                panel_thickness
            )


            data["Label"] = (
                "Base"
            )


            data["LengthAxis"] = "X"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "Z"


            data["Placement"] = (
                FreeCAD.Placement(

                    FreeCAD.Vector(

                        panel_thickness,

                        0,

                        0

                    ),

                    FreeCAD.Rotation()

                )
            )


        #
        # Back panel
        #

        elif role == "Back":

            data["Length"] = (
                module.Height
            )

            data["Width"] = (
                module.Width
            )

            data["Thickness"] = (
                back_thickness
            )


            data["Label"] = (
                "Trasera"
            )


            #
            # Vertical rear panel
            #

            data["LengthAxis"] = "Z"

            data["WidthAxis"] = "X"

            data["ThicknessAxis"] = "Y"


            #
            # Back position
            #
            # The back is positioned from
            # the rear of the module using
            # BackInset.
            #

            position = FreeCAD.Vector(

                0,

                module.Depth
                - back_inset
                - back_thickness,

                0

            )


            data["Placement"] = (
                FreeCAD.Placement(

                    position,

                    FreeCAD.Rotation()

                )
            )


        return data