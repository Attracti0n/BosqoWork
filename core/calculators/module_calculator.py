import FreeCAD


class ModuleCalculator:

    @staticmethod
    def value(
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


    @staticmethod
    def calculate(
        module,
        definition,
        position_index=0,
        automatic_count=1,
        automatic_space=None
    ):

        code = str(
            definition.get(
                "Code",
                ""
            )
        )

        role = str(
            definition.get(
                "Role",
                "Structural"
            )
        )

        panel = ModuleCalculator.value(
            module.PanelThickness
        )

        back = ModuleCalculator.value(
            module.BackThickness
        )

        back_inset = ModuleCalculator.value(
            module.BackInset
        )

        module_width = ModuleCalculator.value(
            module.Width
        )

        module_height = ModuleCalculator.value(
            module.Height
        )

        module_depth = ModuleCalculator.value(
            module.Depth
        )

        data = {

            "Code":
                code,

            "Label":
                definition.get(
                    "Label",
                    "Pieza"
                ),

            "Role":
                role,

            "PartType":
                definition.get(
                    "PartType",
                    "Estructural"
                ),

            "Quantity":
                definition.get(
                    "Quantity",
                    1
                ),

            "MaterialCode":
                definition.get(
                    "MaterialCode",
                    ""
                ),

            "Position":
                definition.get(
                    "Position",
                    0
                ),

            "PositionMode":
                definition.get(
                    "PositionMode",
                    "Automatic"
                ),

            "PositionType":
                definition.get(
                    "PositionType",
                    "Automatic"
                ),

            "Source":
                "Module",

            "LengthAxis":
                "Z",

            "WidthAxis":
                "Y",

            "ThicknessAxis":
                "X",

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
                panel
            )

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
                    panel
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

            return data


        #
        # =====================================================
        # TOP
        # =====================================================
        #

        if role == "Top":

            data["Length"] = (
                module_width
                -
                panel * 2
            )

            data["Width"] = (
                module_depth
            )

            data["Thickness"] = (
                panel
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
                        panel,
                        0,
                        module_height - panel
                    ),
                    FreeCAD.Rotation()
                )
            )

            return data


        #
        # =====================================================
        # BOTTOM
        # =====================================================
        #

        if role == "Bottom":

            data["Length"] = (
                module_width
                -
                panel * 2
            )

            data["Width"] = (
                module_depth
            )

            data["Thickness"] = (
                panel
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
                        panel,
                        0,
                        0
                    ),
                    FreeCAD.Rotation()
                )
            )

            return data


        #
        # =====================================================
        # BACK
        # =====================================================
        #
        # TRASERA SOBREPUESTA
        #

        if role == "Back":

            data["Length"] = (
                module_height
                +
                panel * 2
            )

            data["Width"] = (
                module_width
                +
                panel * 2
            )

            data["Thickness"] = (
                back
            )

            data["Label"] = (
                "Trasera"
            )

            #
            # X = ancho
            # Y = espesor
            # Z = alto
            #

            data["LengthAxis"] = "Z"

            data["WidthAxis"] = "X"

            data["ThicknessAxis"] = "Y"


            #
            # Trasera situada en la parte posterior.
            #
            # Ejemplo:
            #
            # Depth = 560
            # BackThickness = 10
            #
            # Y = 550
            #

            y = (
                module_depth
                -
                back
            )


            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        -panel,
                        y,
                        -panel
                    ),
                    FreeCAD.Rotation()
                )
            )

            return data


        #
        # =====================================================
        # SHELF
        # =====================================================
        #

        if role == "Shelf":

            data["Length"] = (
                module_width
                -
                panel * 2
            )

            #
            # La balda termina en la cara interior
            # de la trasera.
            #

            data["Width"] = (
                module_depth
                -
                back
            )

            data["Thickness"] = (
                panel
            )

            data["LengthAxis"] = "X"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "Z"


            position_mode = (
                definition.get(
                    "PositionMode",
                    "Automatic"
                )
            )

            position_type = (
                definition.get(
                    "PositionType",
                    "Automatic"
                )
            )


            if position_mode == "Manual":

                z = ModuleCalculator.value(
                    definition.get(
                        "Position",
                        panel
                    )
                )

            elif position_type == "Bottom":

                z = panel

            elif position_type == "Center":

                z = (
                    module_height
                    / 2
                )

            elif position_type == "Top":

                z = (
                    module_height
                    - panel
                )

            else:

                if automatic_space is not None:

                    z = (
                        panel
                        +
                        automatic_space
                        *
                        (
                            position_index
                            +
                            1
                        )
                    )

                else:

                    usable = (
                        module_height
                        -
                        panel * 2
                    )

                    z = (
                        panel
                        +
                        (
                            usable
                            /
                            (
                                automatic_count
                                +
                                1
                            )
                        )
                        *
                        (
                            position_index
                            +
                            1
                        )
                    )


            data["Position"] = z


            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        panel,
                        0,
                        z
                    ),
                    FreeCAD.Rotation()
                )
            )

            return data


        #
        # =====================================================
        # DIVIDER
        # =====================================================
        #

        if role == "Divider":

            data["Length"] = (
                module_height
                -
                panel * 2
            )

            data["Width"] = (
                module_depth
                -
                back
            )

            data["Thickness"] = (
                panel
            )

            data["LengthAxis"] = "Z"

            data["WidthAxis"] = "Y"

            data["ThicknessAxis"] = "X"


            position_mode = (
                definition.get(
                    "PositionMode",
                    "Automatic"
                )
            )

            position_type = (
                definition.get(
                    "PositionType",
                    "Automatic"
                )
            )


            if position_mode == "Manual":

                x = ModuleCalculator.value(
                    definition.get(
                        "Position",
                        panel
                    )
                )

            elif position_type == "Bottom":

                x = panel

            elif position_type == "Center":

                x = (
                    module_width
                    / 2
                )

            elif position_type == "Top":

                x = (
                    module_width
                    -
                    panel
                )

            else:

                if automatic_space is not None:

                    x = (
                        panel
                        +
                        automatic_space
                        *
                        (
                            position_index
                            +
                            1
                        )
                    )

                else:

                    usable = (
                        module_width
                        -
                        panel * 2
                    )

                    x = (
                        panel
                        +
                        (
                            usable
                            /
                            (
                                automatic_count
                                +
                                1
                            )
                        )
                        *
                        (
                            position_index
                            +
                            1
                        )
                    )


            data["Position"] = x


            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        x,
                        0,
                        panel
                    ),
                    FreeCAD.Rotation()
                )
            )

            return data


        #
        # =====================================================
        # CUSTOM / USER STRUCTURAL
        # =====================================================
        #

        length = ModuleCalculator.value(
            definition.get(
                "Length",
                0
            )
        )

        width = ModuleCalculator.value(
            definition.get(
                "Width",
                0
            )
        )

        thickness = ModuleCalculator.value(
            definition.get(
                "Thickness",
                panel
            )
        )


        data["Length"] = length

        data["Width"] = width

        data["Thickness"] = thickness


        data["LengthAxis"] = (
            definition.get(
                "LengthAxis",
                "X"
            )
        )

        data["WidthAxis"] = (
            definition.get(
                "WidthAxis",
                "Y"
            )
        )

        data["ThicknessAxis"] = (
            definition.get(
                "ThicknessAxis",
                "Z"
            )
        )


        position_mode = (
            definition.get(
                "PositionMode",
                "Manual"
            )
        )

        position_type = (
            definition.get(
                "PositionType",
                "Manual"
            )
        )


        if position_mode == "Manual":

            position = ModuleCalculator.value(
                definition.get(
                    "Position",
                    0
                )
            )

        elif position_type == "Bottom":

            position = panel

        elif position_type == "Center":

            position = (
                module_height
                / 2
            )

        elif position_type == "Top":

            position = (
                module_height
                -
                thickness
            )

        else:

            position = ModuleCalculator.value(
                definition.get(
                    "Position",
                    0
                )
            )


        data["Position"] = position


        data["Placement"] = (
            FreeCAD.Placement(
                FreeCAD.Vector(
                    0,
                    0,
                    position
                ),
                FreeCAD.Rotation()
            )
        )

        return data