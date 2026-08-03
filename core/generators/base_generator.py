import FreeCAD


class BaseGenerator:

    THICKNESS = FreeCAD.Units.Quantity("19 mm")
    BACK_THICKNESS = FreeCAD.Units.Quantity("3 mm")

    @staticmethod
    def generate(module):

        thickness = BaseGenerator.THICKNESS
        back = BaseGenerator.BACK_THICKNESS

        parts = []

        #
        # Left side
        #

        parts.append({

            "Code": "LS",
            "Role": "Side",
            "Label": "Lateral izquierdo",

            "Source": "Module",

            "Length": module.Height,
            "Width": module.Depth,
            "Thickness": thickness,

            "LengthAxis": "Z",
            "WidthAxis": "Y",
            "ThicknessAxis": "X",

            "baseX": 0,
            "baseY": 0,
            "baseZ": 0

        })

        #
        # Right side
        #

        parts.append({

            "Code": "RS",
            "Role": "Side",
            "Label": "Lateral derecho",

            "Source": "Module",

            "Length": module.Height,
            "Width": module.Depth,
            "Thickness": thickness,

            "LengthAxis": "Z",
            "WidthAxis": "Y",
            "ThicknessAxis": "X",

            "baseX": module.Width - thickness,
            "baseY": 0,
            "baseZ": 0

        })

        #
        # Top
        #

        parts.append({

            "Code": "TP",
            "Role": "Top",
            "Label": "Tapa",

            "Source": "Module",

            "Length": module.Width - (thickness * 2),
            "Width": module.Depth,
            "Thickness": thickness,

            "LengthAxis": "X",
            "WidthAxis": "Y",
            "ThicknessAxis": "Z",

            "baseX": thickness,
            "baseY": 0,
            "baseZ": module.Height - thickness

        })

        #
        # Bottom
        #

        parts.append({

            "Code": "BT",
            "Role": "Bottom",
            "Label": "Base",

            "Source": "Module",

            "Length": module.Width - (thickness * 2),
            "Width": module.Depth,
            "Thickness": thickness,

            "LengthAxis": "X",
            "WidthAxis": "Y",
            "ThicknessAxis": "Z",

            "baseX": thickness,
            "baseY": 0,
            "baseZ": 0

        })

        #
        # Back
        #

        parts.append({

            "Code": "BK",
            "Role": "Back",
            "Label": "Trasera",

            "Source": "Module",

            "Length": module.Height,
            "Width": module.Width,
            "Thickness": back,

            "LengthAxis": "Z",
            "WidthAxis": "X",
            "ThicknessAxis": "Y",

            "baseX": 0,
            "baseY": module.Depth - back,
            "baseZ": 0

        })

        return parts