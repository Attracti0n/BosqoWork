import json


class GeometryStorage:


    @staticmethod
    def serialize(geometry):

        if geometry is None:

            return "{}"


        data = {


            #
            # Dimensions
            #

            "Length": geometry.Length,

            "Width": geometry.Width,

            "Thickness": geometry.Thickness,


            #
            # Axis
            #

            "LengthAxis": geometry.LengthAxis,

            "WidthAxis": geometry.WidthAxis,

            "ThicknessAxis": geometry.ThicknessAxis,


            #
            # Status
            #

            "IsPanel": geometry.IsPanel,

            "Message": geometry.Message

        }


        return json.dumps(
            data
        )



    @staticmethod
    def deserialize(data):

        from core.geometry.panel_geometry import PanelGeometry


        geometry = PanelGeometry()


        if not data:

            return geometry


        try:

            values = json.loads(
                data
            )


        except Exception:

            return geometry



        #
        # Dimensions
        #

        geometry.Length = values.get(
            "Length",
            0
        )

        geometry.Width = values.get(
            "Width",
            0
        )

        geometry.Thickness = values.get(
            "Thickness",
            0
        )



        #
        # Axis
        #

        geometry.LengthAxis = values.get(
            "LengthAxis",
            "Z"
        )

        geometry.WidthAxis = values.get(
            "WidthAxis",
            "Y"
        )

        geometry.ThicknessAxis = values.get(
            "ThicknessAxis",
            "X"
        )



        #
        # Status
        #

        geometry.IsPanel = values.get(
            "IsPanel",
            False
        )

        geometry.Message = values.get(
            "Message",
            ""
        )


        return geometry