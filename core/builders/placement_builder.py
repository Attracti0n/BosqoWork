import FreeCAD


class PlacementBuilder:


    @staticmethod
    def update(part):


        #
        # Imported geometry
        #
        # ImportBuilder has already restored the original
        # Placement from the imported object.
        #

        if part.Source == "Imported":

            return


        #
        # Generated geometry
        #

        placement = FreeCAD.Placement()

        placement.Base = FreeCAD.Vector(
            float(part.baseX),
            float(part.baseY),
            float(part.baseZ)
        )

        #
        # Default rotation
        #

        placement.Rotation = FreeCAD.Rotation()

        part.Placement = placement