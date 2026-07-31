import FreeCAD


class ModuleCalculator:


    THICKNESS = FreeCAD.Units.Quantity("19 mm")


    @staticmethod
    def calculate(module, definition):


        code = definition["Code"]

        role = definition["Role"]


        thickness = ModuleCalculator.THICKNESS



        data = {


            "Code": code,

            "Role": role,

            "Source": "Module",

            "Material": "",



            #
            # Default orientation
            #

            "LengthAxis": "Z",

            "WidthAxis": "Y",

            "ThicknessAxis": "X",



            #
            # Default placement
            #

            "Placement": FreeCAD.Placement(

                FreeCAD.Vector(0,0,0),

                FreeCAD.Rotation()

            )

        }



        #
        # Side panels
        #

        if role == "Side":


            data["Length"] = module.Height

            data["Width"] = module.Depth

            data["Thickness"] = thickness



            data["LengthAxis"] = "Z"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "X"



            if code == "LS":


                data["Label"] = "Lateral izquierdo"


                position = FreeCAD.Vector(

                    0,

                    0,

                    0

                )


            else:


                data["Label"] = "Lateral derecho"



                position = FreeCAD.Vector(

                    module.Width - thickness,

                    0,

                    0

                )



            data["Placement"] = FreeCAD.Placement(

                position,

                FreeCAD.Rotation()

            )




        #
        # Top panel
        #

        elif role == "Top":



            data["Length"] = module.Width - (thickness * 2)

            data["Width"] = module.Depth

            data["Thickness"] = thickness



            data["Label"] = "Tapa"



            data["LengthAxis"] = "X"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "Z"



            data["Placement"] = FreeCAD.Placement(

                FreeCAD.Vector(

                    thickness,

                    0,

                    module.Height - thickness

                ),

                FreeCAD.Rotation()

            )




        #
        # Bottom panel
        #

        elif role == "Bottom":



            data["Length"] = module.Width - (thickness * 2)

            data["Width"] = module.Depth

            data["Thickness"] = thickness



            data["Label"] = "Base"



            data["LengthAxis"] = "X"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "Z"



            data["Placement"] = FreeCAD.Placement(

                FreeCAD.Vector(

                    thickness,

                    0,

                    0

                ),

                FreeCAD.Rotation()

            )




        #
        # Back panel
        #

        elif role == "Back":



            back_thickness = FreeCAD.Units.Quantity("3 mm")



            data["Length"] = module.Height

            data["Width"] = module.Width

            data["Thickness"] = back_thickness



            data["Label"] = "Trasera"



            #
            # Vertical rear panel
            #

            data["LengthAxis"] = "Z"

            data["WidthAxis"] = "X"

            data["ThicknessAxis"] = "Y"



            data["Placement"] = FreeCAD.Placement(

                FreeCAD.Vector(

                    0,

                    module.Depth - back_thickness,

                    0

                ),

                FreeCAD.Rotation()

            )



        return data