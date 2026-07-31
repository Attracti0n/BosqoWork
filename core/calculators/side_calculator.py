class SideCalculator:

    PART_NAMES = {

        "LS": "Lateral izquierdo",
        "RS": "Lateral derecho"

    }

    @staticmethod
    def update(part, module, code):

        #
        # Dimensions
        #

        part.Length = module.Height
        part.Width = module.Depth
        part.Thickness = 19

        #
        # Orientation
        #

        part.LengthAxis = "Z"
        part.WidthAxis = "Y"
        part.ThicknessAxis = "X"

        #
        # Position
        #

        if code == "LS":

            part.baseX = 0
            part.baseY = 0
            part.baseZ = 0

        elif code == "RS":

            part.baseX = module.Width - part.Thickness
            part.baseY = 0
            part.baseZ = 0

        #
        # BOSQO data
        #

        part.Code = code

        part.Role = "Side"

        part.Source = "Module"

        #
        # Visible name
        #

        name = SideCalculator.PART_NAMES.get(
            code,
            "Lateral"
        )

        part.Label = (
            f"{name} "
            f"{part.Length}x"
            f"{part.Width}x"
            f"{part.Thickness}"
        )

        #
        # Internal name
        #

        part.PartName = (
            f"{code}_"
            f"{part.Length}x"
            f"{part.Width}x"
            f"{part.Thickness}"
        )