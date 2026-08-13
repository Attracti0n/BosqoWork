import FreeCAD

from objects.bosqo_part import create_part


class ModuleBuilder:

    STRUCTURAL_CODES = {
        "LS",
        "RS",
        "BT",
        "TP",
        "TT1",
        "TT2",
        "TT3",
        "BK",
        "TB1",
        "TB2",
        "TB3"
    }

    USER_CODE_PREFIX = "USER_"

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def toFloat(
        value,
        default=0.0
    ):

        try:

            if hasattr(
                value,
                "Value"
            ):

                return float(
                    value.Value
                )

            return float(value)

        except Exception:

            return default


    @staticmethod
    def rotation(
        rx,
        ry,
        rz
    ):

        return (
            FreeCAD.Rotation(
                FreeCAD.Vector(1, 0, 0),
                rx
            )
            *
            FreeCAD.Rotation(
                FreeCAD.Vector(0, 1, 0),
                ry
            )
            *
            FreeCAD.Rotation(
                FreeCAD.Vector(0, 0, 1),
                rz
            )
        )


    @staticmethod
    def makePlacement(
        x,
        y,
        z,
        rx=0,
        ry=0,
        rz=0
    ):

        return FreeCAD.Placement(
            FreeCAD.Vector(
                float(x),
                float(y),
                float(z)
            ),
            ModuleBuilder.rotation(
                float(rx),
                float(ry),
                float(rz)
            )
        )


    @staticmethod
    def makeData(
        code,
        label,
        role,
        part_type,
        length,
        width,
        thickness,
        x,
        y,
        z,
        length_axis,
        width_axis,
        thickness_axis,
        position_mode="Automatic",
        rx=0,
        ry=0,
        rz=0,
        material_code="",
        quantity=1
    ):

        return {

            "Code": code,

            "Label": label,

            "Role": role,

            "PartType": part_type,

            "Length": length,

            "Width": width,

            "Thickness": thickness,

            "Quantity": quantity,

            "MaterialCode": material_code,

            "LengthAxis": length_axis,

            "WidthAxis": width_axis,

            "ThicknessAxis": thickness_axis,

            "PositionX": x,

            "PositionY": y,

            "PositionZ": z,

            "RotationX": rx,

            "RotationY": ry,

            "RotationZ": rz,

            "PositionMode": position_mode,

            "PositionType": position_mode,

            "Placement": ModuleBuilder.makePlacement(
                x,
                y,
                z,
                rx,
                ry,
                rz
            )
        }


    # =========================================================
    # USER PART CODE
    # =========================================================

    @staticmethod
    def makeUserCode(
        index
    ):

        return (
            ModuleBuilder.USER_CODE_PREFIX
            +
            str(index)
        )


    # =========================================================
    # NORMALIZE USER ROLE
    # =========================================================

    @staticmethod
    def getUserRole(
        data
    ):

        role = str(
            data.get(
                "Role",
                ""
            )
        ).strip()


        if role:

            return role


        part_type = str(
            data.get(
                "PartType",
                ""
            )
        ).strip()


        mapping = {

            "Balda": "Shelf",

            "Estante": "Shelf",

            "Shelf": "Shelf",

            "Separador": "Divider",

            "Divisor": "Divider",

            "Divider": "Divider"

        }


        return mapping.get(
            part_type,
            "Custom"
        )


    # =========================================================
    # BUILD
    # =========================================================

    @staticmethod
    def build(
        module,
        user_parts=None
    ):

        if module is None:

            return


        proxy = getattr(
            module,
            "Proxy",
            None
        )

        if proxy is None:

            return


        # =====================================================
        # USER PARTS
        # =====================================================

        if user_parts is None:

            try:

                user_parts = proxy.getUserParts(
                    module
                )

            except Exception:

                user_parts = []


        if not isinstance(
            user_parts,
            list
        ):

            user_parts = []


        # =====================================================
        # STRUCTURAL MANUAL PLACEMENTS
        # =====================================================

        try:

            structural_placements = (
                proxy.getStructuralPlacements(
                    module
                )
            )

        except Exception:

            structural_placements = {}


        # =====================================================
        # MODULE DIMENSIONS
        # =====================================================

        width = ModuleBuilder.toFloat(
            getattr(
                module,
                "Width",
                600
            ),
            600
        )

        height = ModuleBuilder.toFloat(
            getattr(
                module,
                "Height",
                720
            ),
            720
        )

        depth = ModuleBuilder.toFloat(
            getattr(
                module,
                "Depth",
                560
            ),
            560
        )

        thickness = ModuleBuilder.toFloat(
            getattr(
                module,
                "PanelThickness",
                19
            ),
            19
        )

        back_thickness = ModuleBuilder.toFloat(
            getattr(
                module,
                "BackThickness",
                10
            ),
            10
        )

        back_inset = ModuleBuilder.toFloat(
            getattr(
                module,
                "BackInset",
                0
            ),
            0
        )


        top_type = str(
            getattr(
                module,
                "TopType",
                "Tapa completa"
            )
        )


        back_type = str(
            getattr(
                module,
                "BackType",
                "Trasera sobrepuesta"
            )
        )


        definitions = []


        # =====================================================
        # LATERAL IZQUIERDO
        # =====================================================

        definitions.append(
            ModuleBuilder.makeData(
                "LS",
                "Lateral izquierdo",
                "Side",
                "Estructural",
                height,
                depth,
                thickness,
                0,
                0,
                0,
                "Z",
                "Y",
                "X"
            )
        )


        # =====================================================
        # LATERAL DERECHO
        # =====================================================

        definitions.append(
            ModuleBuilder.makeData(
                "RS",
                "Lateral derecho",
                "Side",
                "Estructural",
                height,
                depth,
                thickness,
                width - thickness,
                0,
                0,
                "Z",
                "Y",
                "X"
            )
        )


        # =====================================================
        # BASE
        # =====================================================

        definitions.append(
            ModuleBuilder.makeData(
                "BT",
                "Base",
                "Bottom",
                "Estructural",
                width - thickness * 2,
                depth,
                thickness,
                thickness,
                0,
                0,
                "X",
                "Y",
                "Z"
            )
        )


        # =====================================================
        # TAPA
        # =====================================================

        if top_type == "Tapa completa":

            definitions.append(
                ModuleBuilder.makeData(
                    "TP",
                    "Tapa",
                    "Top",
                    "Estructural",
                    width - thickness * 2,
                    depth,
                    thickness,
                    thickness,
                    0,
                    height - thickness,
                    "X",
                    "Y",
                    "Z"
                )
            )

        elif top_type in (
            "2 travesaños",
            "3 travesaños"
        ):

            count = 2

            if top_type == "3 travesaños":

                count = 3


            beam_size = 80.0


            interior_width = max(
                0,
                width - thickness * 2
            )


            available_depth = max(
                0,
                depth - beam_size
            )


            spacing = 0


            if count > 1:

                spacing = (
                    available_depth
                    /
                    (count - 1)
                )


            for index in range(count):

                code = (
                    "TT"
                    +
                    str(index + 1)
                )


                y = (
                    spacing
                    *
                    index
                )


                definitions.append(
                    ModuleBuilder.makeData(
                        code,
                        "Travesaño superior "
                        +
                        str(index + 1),
                        "TopBeam",
                        "Estructural",
                        interior_width,
                        beam_size,
                        thickness,
                        thickness,
                        y,
                        height - thickness,
                        "X",
                        "Y",
                        "Z"
                    )
                )


        # =====================================================
        # TRASERA
        # =====================================================

        if back_type == "Trasera sobrepuesta":

            y = (
                depth
                -
                back_inset
            )


            definitions.append(
                ModuleBuilder.makeData(
                    "BK",
                    "Trasera sobrepuesta",
                    "Back",
                    "Estructural",
                    height,
                    width,
                    back_thickness,
                    0,
                    y,
                    0,
                    "Z",
                    "X",
                    "Y"
                )
            )


        elif back_type == "Trasera oculta":

            internal_width = max(
                0,
                width - thickness * 2
            )


            internal_height = max(
                0,
                height - thickness * 2
            )


            y = (
                depth
                -
                back_inset
                -
                back_thickness
            )


            definitions.append(
                ModuleBuilder.makeData(
                    "BK",
                    "Trasera oculta",
                    "Back",
                    "Estructural",
                    internal_height,
                    internal_width,
                    back_thickness,
                    thickness,
                    y,
                    thickness,
                    "Z",
                    "X",
                    "Y"
                )
            )


        elif back_type in (
            "2 travesaños",
            "3 travesaños"
        ):

            count = 2


            if back_type == "3 travesaños":

                count = 3


            beam_size = 80.0


            interior_width = max(
                0,
                width - thickness * 2
            )


            available_height = max(
                0,
                height
                -
                thickness * 2
                -
                beam_size
            )


            spacing = 0


            if count > 1:

                spacing = (
                    available_height
                    /
                    (count - 1)
                )


            y = (
                depth
                -
                back_inset
                -
                back_thickness
            )


            for index in range(count):

                code = (
                    "TB"
                    +
                    str(index + 1)
                )


                z = (
                    thickness
                    +
                    spacing * index
                )


                definitions.append(
                    ModuleBuilder.makeData(
                        code,
                        "Travesaño trasero "
                        +
                        str(index + 1),
                        "BackBeam",
                        "Estructural",
                        interior_width,
                        back_thickness,
                        beam_size,
                        thickness,
                        y,
                        z,
                        "X",
                        "Y",
                        "Z"
                    )
                )


        # =====================================================
        # USER PARTS
        # =====================================================

        user_index = 0


        for part in user_parts:

            if not isinstance(
                part,
                dict
            ):

                continue


            data = dict(part)


            user_index += 1


            # -------------------------------------------------
            # CODE
            # -------------------------------------------------

            code = str(
                data.get(
                    "Code",
                    ""
                )
            ).strip()


            if not code:

                code = ModuleBuilder.makeUserCode(
                    user_index
                )


            data["Code"] = code


            # -------------------------------------------------
            # ROLE
            # -------------------------------------------------

            role = ModuleBuilder.getUserRole(
                data
            )


            data["Role"] = role


            # -------------------------------------------------
            # PART TYPE
            # -------------------------------------------------

            if not data.get(
                "PartType"
            ):

                data["PartType"] = (
                    "Personalizada"
                )


            # -------------------------------------------------
            # POSITION MODE
            # -------------------------------------------------

            mode = str(
                data.get(
                    "PositionMode",
                    "Manual"
                )
            )


            data["PositionMode"] = mode

            data["PositionType"] = mode


            # -------------------------------------------------
            # AUTOMATIC SHELF
            # -------------------------------------------------

            if (
                role == "Shelf"
                and
                mode == "Automatic"
            ):

                data["Length"] = max(
                    0,
                    width
                    -
                    thickness * 2
                )


                data["Width"] = max(
                    0,
                    depth
                    -
                    back_inset
                    -
                    back_thickness
                )


                data["Thickness"] = thickness


                data["LengthAxis"] = "X"

                data["WidthAxis"] = "Y"

                data["ThicknessAxis"] = "Z"


            # -------------------------------------------------
            # AUTOMATIC DIVIDER
            # -------------------------------------------------

            elif (
                role == "Divider"
                and
                mode == "Automatic"
            ):

                data["Length"] = max(
                    0,
                    height
                    -
                    thickness * 2
                )


                data["Width"] = max(
                    0,
                    depth
                    -
                    back_inset
                    -
                    back_thickness
                )


                data["Thickness"] = thickness


                data["LengthAxis"] = "Z"

                data["WidthAxis"] = "Y"

                data["ThicknessAxis"] = "X"


            # -------------------------------------------------
            # DEFAULTS
            # -------------------------------------------------

            data.setdefault(
                "Length",
                0
            )

            data.setdefault(
                "Width",
                0
            )

            data.setdefault(
                "Thickness",
                thickness
            )

            data.setdefault(
                "Quantity",
                1
            )

            data.setdefault(
                "MaterialCode",
                ""
            )


            data.setdefault(
                "PositionX",
                0
            )

            data.setdefault(
                "PositionY",
                0
            )

            data.setdefault(
                "PositionZ",
                0
            )


            data.setdefault(
                "RotationX",
                0
            )

            data.setdefault(
                "RotationY",
                0
            )

            data.setdefault(
                "RotationZ",
                0
            )


            data.setdefault(
                "LengthAxis",
                "X"
            )

            data.setdefault(
                "WidthAxis",
                "Y"
            )

            data.setdefault(
                "ThicknessAxis",
                "Z"
            )


            # -------------------------------------------------
            # PLACEMENT
            # -------------------------------------------------

            data["Placement"] = (
                ModuleBuilder.makePlacement(
                    data["PositionX"],
                    data["PositionY"],
                    data["PositionZ"],
                    data["RotationX"],
                    data["RotationY"],
                    data["RotationZ"]
                )
            )


            definitions.append(
                data
            )


        # =====================================================
        # STRUCTURAL MANUAL PLACEMENTS
        # =====================================================

        for data in definitions:

            code = str(
                data.get(
                    "Code",
                    ""
                )
            )


            if code not in structural_placements:

                continue


            override = (
                structural_placements.get(
                    code
                )
            )


            if not isinstance(
                override,
                dict
            ):

                continue


            data["PositionMode"] = "Manual"

            data["PositionType"] = "Manual"


            for key in (
                "PositionX",
                "PositionY",
                "PositionZ",
                "RotationX",
                "RotationY",
                "RotationZ"
            ):

                if key in override:

                    data[key] = override[key]


            data["Placement"] = (
                ModuleBuilder.makePlacement(
                    data.get(
                        "PositionX",
                        0
                    ),
                    data.get(
                        "PositionY",
                        0
                    ),
                    data.get(
                        "PositionZ",
                        0
                    ),
                    data.get(
                        "RotationX",
                        0
                    ),
                    data.get(
                        "RotationY",
                        0
                    ),
                    data.get(
                        "RotationZ",
                        0
                    )
                )
            )


        # =====================================================
        # EXISTING OBJECTS
        # =====================================================

        existing = {}


        for child in list(
            getattr(
                module,
                "Group",
                []
            )
        ):

            code = str(
                getattr(
                    child,
                    "Code",
                    ""
                )
            )


            if code:

                existing[code] = child


        wanted_codes = {

            str(
                data.get(
                    "Code",
                    ""
                )
            )

            for data in definitions

        }


        # =====================================================
        # REMOVE OLD STRUCTURAL PIECES
        # =====================================================

        for code in ModuleBuilder.STRUCTURAL_CODES:

            if code in wanted_codes:

                continue


            old = existing.get(
                code
            )


            if old is not None:

                try:

                    module.removeObject(
                        old
                    )

                    module.Document.removeObject(
                        old.Name
                    )

                except Exception:

                    pass


        # =====================================================
        # REMOVE OLD USER PIECES
        # =====================================================

        for code, old in list(
            existing.items()
        ):

            if not code.startswith(
                ModuleBuilder.USER_CODE_PREFIX
            ):

                continue


            if code in wanted_codes:

                continue


            try:

                module.removeObject(
                    old
                )

                module.Document.removeObject(
                    old.Name
                )

            except Exception:

                pass


        # =====================================================
        # CREATE / UPDATE PIECES
        # =====================================================

        for data in definitions:

            code = str(
                data.get(
                    "Code",
                    ""
                )
            )


            if not code:

                continue


            part = existing.get(
                code
            )


            if part is None:

                try:

                    part = create_part(
                        module.Document
                    )


                    module.addObject(
                        part
                    )


                except Exception as error:

                    FreeCAD.Console.PrintError(
                        "Error creando pieza "
                        +
                        code
                        +
                        ": "
                        +
                        str(error)
                        +
                        "\n"
                    )


                    continue


            proxy = getattr(
                part,
                "Proxy",
                None
            )


            try:

                set_data = (

                    getattr(
                        proxy,
                        "setData",
                        None
                    )

                    if proxy is not None

                    else None

                )


                # -------------------------------------------------
                # SET DATA
                # -------------------------------------------------

                if callable(
                    set_data
                ):

                    set_data(
                        part,
                        data
                    )


                else:

                    for key, value in data.items():

                        if key == "Placement":

                            continue


                        if hasattr(
                            part,
                            key
                        ):

                            setattr(
                                part,
                                key,
                                value
                            )


                # -------------------------------------------------
                # FINAL PLACEMENT
                # -------------------------------------------------

                placement = data.get(
                    "Placement"
                )


                if placement is not None:

                    part.Placement = (
                        placement
                    )


                part.Label = data.get(
                    "Label",
                    part.Label
                )


                part.touch()


            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error actualizando pieza "
                    +
                    code
                    +
                    ": "
                    +
                    str(error)
                    +
                    "\n"
                )