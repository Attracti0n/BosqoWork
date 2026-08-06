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

        #
        # =====================================================
        # BASIC DEFINITION
        # =====================================================
        #

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
        # STRUCTURAL ROLES
        # =====================================================
        #

        fixed_roles = {

            "LS": "Side",
            "RS": "Side",
            "BT": "Bottom",
            "TP": "Top",
            "BK": "Back"

        }

        if code in fixed_roles:

            role = fixed_roles[code]

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
                10
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
        # USEFUL DEPTH
        # =====================================================
        #

        useful_depth = (
            module_depth
            -
            back_inset
            -
            back_thickness
        )

        if useful_depth < 0:

            useful_depth = 0

        #
        # =====================================================
        # POSITION MODE
        # =====================================================
        #

        position_mode = definition.get(
            "PositionMode",
            "Automatic"
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

            "PositionMode":
                position_mode,

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

            data["Length"] = module_height

            data["Width"] = module_depth

            data["Thickness"] = panel_thickness

            data["LengthAxis"] = "Z"
            data["WidthAxis"] = "Y"
            data["ThicknessAxis"] = "X"

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

            top_system = definition.get(
                "TopSystem",
                "Panel"
            )

            #
            # -------------------------------------------------
            # COMPLETE TOP
            # -------------------------------------------------
            #

            if top_system == "Panel":

                data["Length"] = (
                    module_width
                    -
                    panel_thickness * 2
                )

                data["Width"] = module_depth

                data["Thickness"] = panel_thickness

                data["Label"] = "Tapa"

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
            # -------------------------------------------------
            # TOP RAIL
            # -------------------------------------------------
            #

            elif top_system == "Rail":

                rail_count = int(
                    definition.get(
                        "RailCount",
                        2
                    )
                )

                rail_index = int(
                    definition.get(
                        "RailIndex",
                        0
                    )
                )

                #
                # Width of the rail.
                #
                # It fits between the two side panels.
                #

                rail_length = (
                    module_width
                    -
                    panel_thickness * 2
                )

                #
                # Depth of each rail.
                #
                # 100 mm is a practical initial value.
                # This can later become a module parameter.
                #

                rail_depth = 100.0

                if rail_depth > module_depth:

                    rail_depth = module_depth

                #
                # Thickness.
                #

                rail_thickness = panel_thickness

                #
                # Position along depth.
                #
                # The rails are distributed evenly between
                # the front and rear of the module.
                #

                available_depth = (
                    module_depth
                    -
                    rail_depth
                )

                if rail_count <= 1:

                    y = 0

                else:

                    spacing = (
                        available_depth
                        /
                        (
                            rail_count - 1
                        )
                    )

                    y = (
                        spacing
                        *
                        rail_index
                    )

                #
                # Dimensions.
                #

                data["Length"] = rail_length

                data["Width"] = rail_depth

                data["Thickness"] = rail_thickness

                data["Label"] = (
                    definition.get(
                        "Label",
                        "Travesaño superior"
                    )
                )

                data["LengthAxis"] = "X"
                data["WidthAxis"] = "Y"
                data["ThicknessAxis"] = "Z"

                #
                # Top position.
                #

                z = (
                    module_height
                    -
                    rail_thickness
                )

                x = panel_thickness

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
        # BOTTOM
        # =====================================================
        #

        elif role == "Bottom":

            data["Length"] = (
                module_width
                -
                panel_thickness * 2
            )

            data["Width"] = module_depth

            data["Thickness"] = panel_thickness

            data["Label"] = "Base"

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

            back_system = definition.get(
                "BackSystem",
                "Panel"
            )

            #
            # -------------------------------------------------
            # COMPLETE BACK
            # -------------------------------------------------
            #

            if back_system == "Panel":

                data["Length"] = module_height

                data["Width"] = module_width

                data["Thickness"] = back_thickness

                data["Label"] = (
                    definition.get(
                        "Label",
                        "Trasera"
                    )
                )

                data["LengthAxis"] = "Z"
                data["WidthAxis"] = "X"
                data["ThicknessAxis"] = "Y"

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
            # -------------------------------------------------
            # BACK RAIL
            # -------------------------------------------------
            #

            elif back_system == "Rail":

                rail_count = int(
                    definition.get(
                        "RailCount",
                        2
                    )
                )

                rail_index = int(
                    definition.get(
                        "RailIndex",
                        0
                    )
                )

                #
                # Rail width across the module.
                #

                rail_width = (
                    module_width
                    -
                    panel_thickness * 2
                )

                #
                # Height of the rear rail.
                #

                rail_height = 100.0

                if rail_height > module_height:

                    rail_height = module_height

                #
                # Thickness.
                #

                rail_thickness = back_thickness

                #
                # Available vertical space.
                #

                available_height = (
                    module_height
                    -
                    rail_height
                )

                if rail_count <= 1:

                    z = 0

                else:

                    spacing = (
                        available_height
                        /
                        (
                            rail_count - 1
                        )
                    )

                    z = (
                        spacing
                        *
                        rail_index
                    )

                #
                # Dimensions.
                #

                data["Length"] = rail_height

                data["Width"] = rail_width

                data["Thickness"] = rail_thickness

                data["Label"] = (
                    definition.get(
                        "Label",
                        "Travesaño trasero"
                    )
                )

                data["LengthAxis"] = "Z"
                data["WidthAxis"] = "X"
                data["ThicknessAxis"] = "Y"

                #
                # Rear position.
                #

                y = (
                    module_depth
                    -
                    back_inset
                    -
                    rail_thickness
                )

                x = panel_thickness

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
        # SHELF
        # =====================================================
        #

        elif role == "Shelf":

            if position_mode == "Automatic":

                data["Length"] = (
                    module_width
                    -
                    panel_thickness * 2
                )

                data["Width"] = useful_depth

                data["Thickness"] = panel_thickness

            else:

                data["Length"] = (
                    ModuleCalculator.toFloat(
                        definition.get(
                            "Length",
                            module_width
                            -
                            panel_thickness * 2
                        )
                    )
                )

                data["Width"] = (
                    ModuleCalculator.toFloat(
                        definition.get(
                            "Width",
                            module_depth
                        )
                    )
                )

                data["Thickness"] = (
                    ModuleCalculator.toFloat(
                        definition.get(
                            "Thickness",
                            panel_thickness
                        )
                    )
                )

            data["Label"] = (
                definition.get(
                    "Label",
                    "Balda"
                )
            )

            data["LengthAxis"] = "X"
            data["WidthAxis"] = "Y"
            data["ThicknessAxis"] = "Z"

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

            else:

                if automatic_space is not None:

                    z = (
                        panel_thickness
                        +
                        ModuleCalculator.toFloat(
                            automatic_space
                        )
                        *
                        (
                            position_index + 1
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
                            automatic_count + 1
                        )
                    )

                    z = (
                        panel_thickness
                        +
                        spacing
                        *
                        (
                            position_index + 1
                        )
                        +
                        panel_thickness
                        *
                        position_index
                    )

                x = panel_thickness

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

            if position_mode == "Automatic":

                data["Length"] = (
                    module_height
                    -
                    panel_thickness * 2
                )

                data["Width"] = useful_depth

                data["Thickness"] = panel_thickness

            else:

                data["Length"] = (
                    ModuleCalculator.toFloat(
                        definition.get(
                            "Length",
                            module_height
                            -
                            panel_thickness * 2
                        )
                    )
                )

                data["Width"] = (
                    ModuleCalculator.toFloat(
                        definition.get(
                            "Width",
                            module_depth
                        )
                    )
                )

                data["Thickness"] = (
                    ModuleCalculator.toFloat(
                        definition.get(
                            "Thickness",
                            panel_thickness
                        )
                    )
                )

            data["Label"] = (
                definition.get(
                    "Label",
                    "Separador"
                )
            )

            data["LengthAxis"] = "Z"
            data["WidthAxis"] = "Y"
            data["ThicknessAxis"] = "X"

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
                            position_index + 1
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
                            automatic_count + 1
                        )
                    )

                    x = (
                        panel_thickness
                        +
                        spacing
                        *
                        (
                            position_index + 1
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

            data["Length"] = (
                ModuleCalculator.toFloat(
                    definition.get(
                        "Length",
                        100
                    )
                )
            )

            data["Width"] = (
                ModuleCalculator.toFloat(
                    definition.get(
                        "Width",
                        100
                    )
                )
            )

            data["Thickness"] = (
                ModuleCalculator.toFloat(
                    definition.get(
                        "Thickness",
                        panel_thickness
                    )
                )
            )

            data["Label"] = (
                definition.get(
                    "Label",
                    "Pieza personalizada"
                )
            )

            data["PartType"] = (
                "Personalizado"
            )

            data["LengthAxis"] = "X"
            data["WidthAxis"] = "Y"
            data["ThicknessAxis"] = "Z"

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

            data["Length"] = (
                ModuleCalculator.toFloat(
                    definition.get(
                        "Length",
                        100
                    )
                )
            )

            data["Width"] = (
                ModuleCalculator.toFloat(
                    definition.get(
                        "Width",
                        100
                    )
                )
            )

            data["Thickness"] = (
                ModuleCalculator.toFloat(
                    definition.get(
                        "Thickness",
                        panel_thickness
                    )
                )
            )

            data["Label"] = (
                definition.get(
                    "Label",
                    "Pieza"
                )
            )

            data["PartType"] = (
                definition.get(
                    "PartType",
                    "Personalizado"
                )
            )

        return data


    #
    # =========================================================
    # TO FLOAT
    # =========================================================
    #

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