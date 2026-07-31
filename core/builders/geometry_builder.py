import FreeCAD
import Part


class GeometryBuilder:


    @staticmethod
    def createBox(obj):


        #
        # Validate dimensions
        #

        if (
            obj.Length <= 0
            or obj.Width <= 0
            or obj.Thickness <= 0
        ):

            return None



        #
        # Global axis dimensions
        #

        size = {

            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0

        }



        #
        # Assign dimensions according to detected orientation
        #

        size[obj.LengthAxis] = abs(float(obj.Length))

        size[obj.WidthAxis] = abs(float(obj.Width))

        size[obj.ThicknessAxis] = abs(float(obj.Thickness))



        #
        # Create local box
        #

        shape = Part.makeBox(

            size["X"],
            size["Y"],
            size["Z"]

        )



        #
        # Restore imported position
        #

        if hasattr(obj, "OriginalObject") and obj.OriginalObject:


            source = obj.OriginalObject


            bound = None



            #
            # Mesh objects
            #

            if hasattr(source, "Mesh"):


                bound = source.Mesh.BoundBox



            #
            # Part objects
            #

            elif hasattr(source, "Shape"):


                bound = source.Shape.BoundBox



            #
            # Move geometry to original coordinates
            #

            if bound:


                shape.translate(

                    FreeCAD.Vector(

                        bound.XMin,
                        bound.YMin,
                        bound.ZMin

                    )

                )



            #
            # Restore original rotation
            #

            if hasattr(source, "Placement"):


                rotation = source.Placement.Rotation


                shape.rotate(

                    FreeCAD.Vector(0,0,0),

                    rotation.Axis,

                    rotation.Angle

                )



        return shape