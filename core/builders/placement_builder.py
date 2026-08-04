import FreeCAD


class PlacementBuilder:


    @staticmethod
    def update(
        part
    ):

        #
        # Imported geometry
        #
        # ImportBuilder restores the original
        # placement of imported objects.
        #

        if getattr(
            part,
            "Source",
            ""
        ) == "Imported":

            return


        #
        # Generated geometry
        #
        # The Placement is calculated by the
        # generator/calculator and stored directly
        # in the BosqoPart.
        #
        # Do NOT rebuild the placement from
        # baseX/baseY/baseZ here.
        #

        if hasattr(
            part,
            "Placement"
        ):

            return