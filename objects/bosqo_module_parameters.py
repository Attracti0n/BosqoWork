import FreeCAD


class BosqoModuleParameters:

    def __init__(
        self,
        obj
    ):

        self.ObjectType = "BosqoModuleParameters"

        obj.Proxy = self

        self.initProperties(
            obj
        )


    #
    # Properties
    #

    def initProperties(
        self,
        obj
    ):

        #
        # Identification
        #

        self.addString(
            obj,
            "ModuleName",
            "Identificación",
            "Nombre del módulo",
            "Nuevo módulo"
        )


        #
        # Module dimensions
        #

        self.addLength(
            obj,
            "ModuleWidth",
            "Dimensiones",
            "Ancho",
            600
        )

        self.addLength(
            obj,
            "ModuleHeight",
            "Dimensiones",
            "Alto",
            720
        )

        self.addLength(
            obj,
            "ModuleDepth",
            "Dimensiones",
            "Profundidad",
            560
        )


        #
        # Material thickness
        #

        self.addLength(
            obj,
            "PanelThickness",
            "Espesores",
            "Espesor panel",
            19
        )

        self.addLength(
            obj,
            "BackThickness",
            "Espesores",
            "Espesor fondo",
            10
        )


        #
        # Back position
        #

        self.addLength(
            obj,
            "BackInset",
            "Fondo",
            "Retranqueo fondo",
            0
        )


        #
        # Automatic pieces
        #

        self.addBool(
            obj,
            "GenerateSides",
            "Piezas",
            "Generar laterales",
            True
        )

        self.addBool(
            obj,
            "GenerateTop",
            "Piezas",
            "Generar tapa",
            True
        )

        self.addBool(
            obj,
            "GenerateBottom",
            "Piezas",
            "Generar base",
            True
        )

        self.addBool(
            obj,
            "GenerateBack",
            "Piezas",
            "Generar fondo",
            True
        )


    #
    # Add String property
    #

    def addString(
        self,
        obj,
        name,
        group,
        label,
        value
    ):

        if hasattr(
            obj,
            name
        ):

            return

        obj.addProperty(
            "App::PropertyString",
            name,
            group,
            label
        )

        setattr(
            obj,
            name,
            value
        )


    #
    # Add Length property
    #

    def addLength(
        self,
        obj,
        name,
        group,
        label,
        value
    ):

        if hasattr(
            obj,
            name
        ):

            return

        obj.addProperty(
            "App::PropertyLength",
            name,
            group,
            label
        )

        setattr(
            obj,
            name,
            value
        )


    #
    # Add Bool property
    #

    def addBool(
        self,
        obj,
        name,
        group,
        label,
        value
    ):

        if hasattr(
            obj,
            name
        ):

            return

        obj.addProperty(
            "App::PropertyBool",
            name,
            group,
            label
        )

        setattr(
            obj,
            name,
            value
        )


    #
    # Calculate parts
    #

    def calculateParts(
        self,
        obj
    ):

        width = float(
            obj.ModuleWidth.Value
        )

        height = float(
            obj.ModuleHeight.Value
        )

        depth = float(
            obj.ModuleDepth.Value
        )

        thickness = float(
            obj.PanelThickness.Value
        )

        backThickness = float(
            obj.BackThickness.Value
        )

        backInset = float(
            obj.BackInset.Value
        )


        parts = []


        #
        # Sides
        #

        if obj.GenerateSides:

            parts.append(
                {
                    "Label":
                        "Lateral izquierdo",

                    "PartType":
                        "Panel lateral",

                    "Length":
                        height,

                    "Width":
                        depth,

                    "Thickness":
                        thickness,

                    "Quantity":
                        1,

                    "MaterialCode":
                        ""
                }
            )


            parts.append(
                {
                    "Label":
                        "Lateral derecho",

                    "PartType":
                        "Panel lateral",

                    "Length":
                        height,

                    "Width":
                        depth,

                    "Thickness":
                        thickness,

                    "Quantity":
                        1,

                    "MaterialCode":
                        ""
                }
            )


        #
        # Top
        #

        if obj.GenerateTop:

            topWidth = (
                width
                - (2 * thickness)
            )


            parts.append(
                {
                    "Label":
                        "Tapa",

                    "PartType":
                        "Estante",

                    "Length":
                        topWidth,

                    "Width":
                        depth,

                    "Thickness":
                        thickness,

                    "Quantity":
                        1,

                    "MaterialCode":
                        ""
                }
            )


        #
        # Bottom
        #

        if obj.GenerateBottom:

            bottomWidth = (
                width
                - (2 * thickness)
            )


            parts.append(
                {
                    "Label":
                        "Base",

                    "PartType":
                        "Base",

                    "Length":
                        bottomWidth,

                    "Width":
                        depth,

                    "Thickness":
                        thickness,

                    "Quantity":
                        1,

                    "MaterialCode":
                        ""
                }
            )


        #
        # Back
        #

        if obj.GenerateBack:

            backWidth = (
                width
                - (2 * thickness)
            )


            backHeight = (
                height
                - (2 * thickness)
            )


            parts.append(
                {
                    "Label":
                        "Fondo",

                    "PartType":
                        "Fondo",

                    "Length":
                        backWidth,

                    "Width":
                        backHeight,

                    "Thickness":
                        backThickness,

                    "Quantity":
                        1,

                    "MaterialCode":
                        ""
                }
            )


        return parts


    #
    # Execute
    #

    def execute(
        self,
        obj
    ):

        return


    #
    # Changed
    #

    def onChanged(
        self,
        obj,
        property
    ):

        #
        # Keep Label synchronized
        # with module name.
        #

        if property == "ModuleName":

            try:

                name = str(
                    obj.ModuleName
                ).strip()

                if name:

                    obj.Label = name

            except Exception:

                pass