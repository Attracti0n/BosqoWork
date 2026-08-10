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
        # User parts
        #

        if not hasattr(
            obj,
            "Parts"
        ):

            obj.addProperty(
                "App::PropertyPythonObject",
                "Parts",
                "Piezas",
                "Piezas añadidas al módulo"
            )

            obj.Parts = []


        #
        # Structural placements
        #

        if not hasattr(
            obj,
            "StructuralPlacements"
        ):

            obj.addProperty(
                "App::PropertyPythonObject",
                "StructuralPlacements",
                "Piezas",
                "Posiciones manuales de piezas estructurales"
            )

            obj.StructuralPlacements = {}


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
    # User parts
    #

    def getUserParts(
        self,
        obj
    ):

        try:

            parts = getattr(
                obj,
                "Parts",
                []
            )

            if isinstance(
                parts,
                list
            ):

                return [
                    dict(part)
                    for part in parts
                    if isinstance(
                        part,
                        dict
                    )
                ]

        except Exception:

            pass

        return []


    def setUserParts(
        self,
        obj,
        parts
    ):

        try:

            obj.Parts = [
                dict(part)
                for part in parts
                if isinstance(
                    part,
                    dict
                )
            ]

        except Exception:

            obj.Parts = []


    #
    # Structural placements
    #

    def getStructuralPlacements(
        self,
        obj
    ):

        try:

            placements = getattr(
                obj,
                "StructuralPlacements",
                {}
            )

            if isinstance(
                placements,
                dict
            ):

                return dict(
                    placements
                )

        except Exception:

            pass

        return {}


    def setStructuralPlacements(
        self,
        obj,
        placements
    ):

        try:

            if isinstance(
                placements,
                dict
            ):

                obj.StructuralPlacements = dict(
                    placements
                )

            else:

                obj.StructuralPlacements = {}

        except Exception:

            obj.StructuralPlacements = {}


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

            if topWidth < 0:

                topWidth = 0


            parts.append(
                {
                    "Label":
                        "Tapa",

                    "PartType":
                        "Balda",

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

            if bottomWidth < 0:

                bottomWidth = 0


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

            if backWidth < 0:

                backWidth = 0


            backHeight = (
                height
                - (2 * thickness)
            )

            if backHeight < 0:

                backHeight = 0


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

                    "BackInset":
                        backInset,

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