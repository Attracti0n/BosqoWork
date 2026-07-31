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
            # Default origin
            #

            "OriginX": 0,
            "OriginY": 0,
            "OriginZ": 0

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

                data["OriginX"] = 0

            else:

                data["Label"] = "Lateral derecho"

                data["OriginX"] = module.Width - thickness

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

            data["OriginX"] = thickness
            data["OriginY"] = 0
            data["OriginZ"] = module.Height - thickness

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

            data["OriginX"] = thickness
            data["OriginY"] = 0
            data["OriginZ"] = 0

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
            # Panel vertical
            #

            data["LengthAxis"] = "Z"
            data["WidthAxis"] = "X"
            data["ThicknessAxis"] = "Y"

            data["OriginX"] = 0
            data["OriginY"] = module.Depth - back_thickness
            data["OriginZ"] = 0

        return data