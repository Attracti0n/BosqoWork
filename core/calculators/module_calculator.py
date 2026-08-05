import FreeCAD


class ModuleCalculator:

    @staticmethod
    def calculate(
        module,
        definition,
        position_index=0,
        automatic_count=1,
        automatic_space=None
    ):

        code = definition.get(
            "Code",
            ""
        )

        role = definition.get(
            "Role",
            "Custom"
        )

        #
        # =====================================================
        # MODULE VALUES
        # =====================================================
        #

        panel_thickness = ModuleCalculator.toFloat(
            getattr(
                module,
                "PanelThickness",
                19
            )
        )

        back_thickness = ModuleCalculator.toFloat(
            getattr(
                module,
                "BackThickness",
                3
            )
        )

        back_inset = ModuleCalculator.toFloat(
            getattr(
                module,
                "BackInset",
                0
            )
        )

        module_width = ModuleCalculator.toFloat(
            getattr(
                module,
                "Width",
                600
            )
        )

        module_height = ModuleCalculator.toFloat(
            getattr(
                module,
                "Height",
                720
            )
        )

        module_depth = ModuleCalculator.toFloat(
            getattr(
                module,
                "Depth",
                560
            )
        )

        #
        # =====================================================
        # BASE DATA
        # =====================================================
        #

        data = {

            "Code":
                code,

            "Role":
                role,

            "PartType":
                definition.get(
                    "PartType",
                    ""
                ),

            "Label":
                definition.get(
                    "Label",
                    "Pieza"
                ),

            "Source":
                "Module",

            "Material":
                definition.get(
                    "Material",
                    ""
                ),

            "MaterialCode":
                definition.get(
                    "MaterialCode",
                    ""
                ),

            "Quantity":
                ModuleCalculator.toFloat(
                    definition.get(
                        "Quantity",
                        1
                    )
                ),

            "LengthAxis":
                "X",

            "WidthAxis":
                "Y",

            "ThicknessAxis":
                "Z",

            "Placement":
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        0,
                        0,
                        0
                    ),
                    FreeCAD.Rotation()
                )
        }

        #
        # =====================================================
        # SIDE
        # =====================================================
        #

        if role == "Side":

            data["Length"] = (
                module_height
            )

            data["Width"] = (
                module_depth
            )

            data["Thickness"] = (
                panel_thickness
            )

            #
            # Local dimensions:
            #
            # Length -> Z
            # Width  -> Y
            # Thickness -> X
            #

            data["LengthAxis"] = "Z"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "X"

            #
            # LEFT / RIGHT
            #

            if code == "LS":

                data["Label"] = (
                    "Lateral izquierdo"
                )

                x = 0

            else:

                data["Label"] = (
                    "Lateral derecho"
                )

                x = (
                    module_width
                    -
                    panel_thickness
                )

            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        x,
                        0,
                        0
                    ),
                    FreeCAD.Rotation()
                )
            )

        #
        # =====================================================
        # TOP
        # =====================================================
        #

        elif role == "Top":

            data["Length"] = (
                module_width
                -
                panel_thickness * 2
            )

            data["Width"] = (
                module_depth
            )

            data["Thickness"] = (
                panel_thickness
            )

            data["Label"] = (
                "Tapa"
            )

            data["LengthAxis"] = "X"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "Z"

            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        panel_thickness,
                        0,
                        module_height
                        -
                        panel_thickness
                    ),
                    FreeCAD.Rotation()
                )
            )

        #
        # =====================================================
        # BOTTOM
        # =====================================================
        #

        elif role == "Bottom":

            data["Length"] = (
                module_width
                -
                panel_thickness * 2
            )

            data["Width"] = (
                module_depth
            )

            data["Thickness"] = (
                panel_thickness
            )

            data["Label"] = (
                "Base"
            )

            data["LengthAxis"] = "X"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "Z"

            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        panel_thickness,
                        0,
                        0
                    ),
                    FreeCAD.Rotation()
                )
            )

        #
        # =====================================================
        # BACK
        # =====================================================
        #

        elif role == "Back":

            #
            # Physical dimensions:
            #
            # Width  -> module width
            # Height -> module height
            # Thickness -> back thickness
            #

            data["Length"] = (
                module_height
            )

            data["Width"] = (
                module_width
            )

            data["Thickness"] = (
                back_thickness
            )

            data["Label"] = (
                "Trasera"
            )

            #
            # Local axes:
            #
            # Length    -> Z
            # Width     -> X
            # Thickness -> Y
            #

            data["LengthAxis"] = "Z"

            data["WidthAxis"] = "X"

            data["ThicknessAxis"] = "Y"

            #
            # IMPORTANT
            #
            # The back must remain vertical.
            #
            # We rotate the local panel:
            #
            # local X -> global X
            # local Y -> global Y
            # local Z -> global Z
            #
            # No rotation of the panel itself is required.
            #
            # Instead, BosqoPart uses the axis information
            # to construct the geometry.
            #

            y = (
                module_depth
                -
                back_inset
                -
                back_thickness
            )

            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        0,
                        y,
                        0
                    ),
                    FreeCAD.Rotation()
                )
            )

        #
        # =====================================================
        # SHELF
        # =====================================================
        #

        elif role == "Shelf":

            position_mode = definition.get(
                "PositionMode",
                "Automatic"
            )

            #
            # =================================================
            # AUTOMATIC SHELF
            # =================================================
            #
            # IMPORTANT:
            #
            # When the shelf is automatic, its dimensions must
            # ALWAYS be calculated from the current module.
            #
            # We must NOT use old Length / Width values stored
            # in the dialog.
            #

            if position_mode == "Automatic":

                data["Length"] = (
                    module_width
                    -
                    panel_thickness * 2
                )

                data["Width"] = (
                    module_depth
                )

                data["Thickness"] = (
                    panel_thickness
                )

            #
            # =================================================
            # MANUAL SHELF
            # =================================================
            #

            else:

                data["Length"] = ModuleCalculator.toFloat(
                    definition.get(
                        "Length",
                        module_width
                        -
                        panel_thickness * 2
                    )
                )

                data["Width"] = ModuleCalculator.toFloat(
                    definition.get(
                        "Width",
                        module_depth
                    )
                )

                data["Thickness"] = ModuleCalculator.toFloat(
                    definition.get(
                        "Thickness",
                        panel_thickness
                    )
                )

            data["Label"] = definition.get(
                "Label",
                "Balda"
            )

            #
            # Shelf orientation.
            #

            data["LengthAxis"] = "X"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "Z"

            #
            # =================================================
            # MANUAL POSITION
            # =================================================
            #

            if position_mode == "Manual":

                x = ModuleCalculator.toFloat(
                    definition.get(
                        "PositionX",
                        panel_thickness
                    )
                )

                y = ModuleCalculator.toFloat(
                    definition.get(
                        "PositionY",
                        0
                    )
                )

                z = ModuleCalculator.toFloat(
                    definition.get(
                        "PositionZ",
                        definition.get(
                            "Position",
                            0
                        )
                    )
                )

            #
            # =================================================
            # AUTOMATIC POSITION
            # =================================================
            #

            else:

                #
                # automatic_space represents the free vertical
                # distance between shelves.
                #

                if automatic_space is not None:

                    z = (
                        panel_thickness
                        +
                        ModuleCalculator.toFloat(
                            automatic_space
                        )
                        *
                        (
                            position_index
                            +
                            1
                        )
                        +
                        panel_thickness
                        *
                        position_index
                    )

                else:

                    usable_height = (
                        module_height
                        -
                        panel_thickness * 2
                    )

                    total_shelf_thickness = (
                        panel_thickness
                        *
                        automatic_count
                    )

                    free_height = (
                        usable_height
                        -
                        total_shelf_thickness
                    )

                    spacing = (
                        free_height
                        /
                        (
                            automatic_count
                            +
                            1
                        )
                    )

                    z = (
                        panel_thickness
                        +
                        spacing
                        *
                        (
                            position_index
                            +
                            1
                        )
                        +
                        panel_thickness
                        *
                        position_index
                    )

                #
                # X:
                # start at the inside face of left side.
                #

                x = panel_thickness

                #
                # Y:
                # front of the module.
                #

                y = 0

            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        x,
                        y,
                        z
                    ),
                    FreeCAD.Rotation()
                )
            )

        #
        # =====================================================
        # DIVIDER
        # =====================================================
        #

        elif role == "Divider":

            position_mode = definition.get(
                "PositionMode",
                "Automatic"
            )

            #
            # =================================================
            # AUTOMATIC DIVIDER
            # =================================================
            #

            if position_mode == "Automatic":

                data["Length"] = (
                    module_height
                    -
                    panel_thickness * 2
                )

                data["Width"] = (
                    module_depth
                )

                data["Thickness"] = (
                    panel_thickness
                )

            #
            # =================================================
            # MANUAL DIVIDER
            # =================================================
            #

            else:

                data["Length"] = ModuleCalculator.toFloat(
                    definition.get(
                        "Length",
                        module_height
                        -
                        panel_thickness * 2
                    )
                )

                data["Width"] = ModuleCalculator.toFloat(
                    definition.get(
                        "Width",
                        module_depth
                    )
                )

                data["Thickness"] = ModuleCalculator.toFloat(
                    definition.get(
                        "Thickness",
                        panel_thickness
                    )
                )

            data["Label"] = definition.get(
                "Label",
                "Separador"
            )

            #
            # Divider orientation.
            #

            data["LengthAxis"] = "Z"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "X"

            #
            # =================================================
            # MANUAL POSITION
            # =================================================
            #

            if position_mode == "Manual":

                x = ModuleCalculator.toFloat(
                    definition.get(
                        "PositionX",
                        definition.get(
                            "Position",
                            0
                        )
                    )
                )

                y = ModuleCalculator.toFloat(
                    definition.get(
                        "PositionY",
                        0
                    )
                )

                z = ModuleCalculator.toFloat(
                    definition.get(
                        "PositionZ",
                        panel_thickness
                    )
                )

            #
            # =================================================
            # AUTOMATIC POSITION
            # =================================================
            #

            else:

                if automatic_space is not None:

                    x = (
                        panel_thickness
                        +
                        ModuleCalculator.toFloat(
                            automatic_space
                        )
                        *
                        (
                            position_index
                            +
                            1
                        )
                        +
                        panel_thickness
                        *
                        position_index
                    )

                else:

                    usable_width = (
                        module_width
                        -
                        panel_thickness * 2
                    )

                    total_divider_thickness = (
                        panel_thickness
                        *
                        automatic_count
                    )

                    free_width = (
                        usable_width
                        -
                        total_divider_thickness
                    )

                    spacing = (
                        free_width
                        /
                        (
                            automatic_count
                            +
                            1
                        )
                    )

                    x = (
                        panel_thickness
                        +
                        spacing
                        *
                        (
                            position_index
                            +
                            1
                        )
                        +
                        panel_thickness
                        *
                        position_index
                    )

                y = 0

                z = panel_thickness

            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        x,
                        y,
                        z
                    ),
                    FreeCAD.Rotation()
                )
            )

        #
        # =====================================================
        # CUSTOM
        # =====================================================
        #

        elif role == "Custom":

            #
            # Custom dimensions always come from the table.
            #

            data["Length"] = ModuleCalculator.toFloat(
                definition.get(
                    "Length",
                    100
                )
            )

            data["Width"] = ModuleCalculator.toFloat(
                definition.get(
                    "Width",
                    100
                )
            )

            data["Thickness"] = ModuleCalculator.toFloat(
                definition.get(
                    "Thickness",
                    panel_thickness
                )
            )

            data["Label"] = definition.get(
                "Label",
                "Pieza personalizada"
            )

            data["PartType"] = (
                "Personalizado"
            )

            data["LengthAxis"] = "X"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "Z"

            #
            # =================================================
            # POSITION
            # =================================================
            #

            x = ModuleCalculator.toFloat(
                definition.get(
                    "PositionX",
                    0
                )
            )

            y = ModuleCalculator.toFloat(
                definition.get(
                    "PositionY",
                    0
                )
            )

            z = ModuleCalculator.toFloat(
                definition.get(
                    "PositionZ",
                    0
                )
            )

            #
            # =================================================
            # ROTATION
            # =================================================
            #

            rotation_x = ModuleCalculator.toFloat(
                definition.get(
                    "RotationX",
                    0
                )
            )

            rotation_y = ModuleCalculator.toFloat(
                definition.get(
                    "RotationY",
                    0
                )
            )

            rotation_z = ModuleCalculator.toFloat(
                definition.get(
                    "RotationZ",
                    0
                )
            )

            rotation = (
                FreeCAD.Rotation(
                    FreeCAD.Vector(
                        1,
                        0,
                        0
                    ),
                    rotation_x
                )
                *
                FreeCAD.Rotation(
                    FreeCAD.Vector(
                        0,
                        1,
                        0
                    ),
                    rotation_y
                )
                *
                FreeCAD.Rotation(
                    FreeCAD.Vector(
                        0,
                        0,
                        1
                    ),
                    rotation_z
                )
            )

            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        x,
                        y,
                        z
                    ),
                    rotation
                )
            )

        #
        # =====================================================
        # UNKNOWN
        # =====================================================
        #

        else:

            data["Length"] = ModuleCalculator.toFloat(
                definition.get(
                    "Length",
                    100
                )
            )

            data["Width"] = ModuleCalculator.toFloat(
                definition.get(
                    "Width",
                    100
                )
            )

            data["Thickness"] = ModuleCalculator.toFloat(
                definition.get(
                    "Thickness",
                    panel_thickness
                )
            )

            data["Label"] = definition.get(
                "Label",
                "Pieza"
            )

            data["PartType"] = definition.get(
                "PartType",
                "Personalizado"
            )

        return data


    # =========================================================
    # TO FLOAT
    # =========================================================

    @staticmethod
    def toFloat(
        value
    ):

        try:

            if hasattr(
                value,
                "Value"
            ):

                return float(
                    value.Value
                )

            return float(
                value
            )

        except Exception:

            return 0.0