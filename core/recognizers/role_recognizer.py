class RoleRecognizer:

    @staticmethod
    def recognize(part):

        #
        # Default
        #

        if not hasattr(part, "Role"):

            return ""

        part.Role = "Unknown"

        #
        # Dimensions
        #

        length = float(part.Length)
        width = float(part.Width)
        thickness = float(part.Thickness)

        #
        # Ignore invalid parts
        #

        if (
            length <= 0
            or width <= 0
            or thickness <= 0
        ):

            return part.Role

        #
        # Vertical panel
        #

        if part.LengthAxis == "Z":

            part.Role = "Vertical"

            return part.Role

        #
        # Horizontal panel
        #

        if part.ThicknessAxis == "Z":

            part.Role = "Horizontal"

            return part.Role

        #
        # Default
        #

        return part.Role