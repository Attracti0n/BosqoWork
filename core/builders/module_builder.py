from objects.bosqo_part import create_part

from core.generators.generator_factory import GeneratorFactory
from core.calculators.module_calculator import ModuleCalculator


class ModuleBuilder:

    # =========================================================
    # STRUCTURAL CODES
    # =========================================================

    STRUCTURAL_CODES = {

        "LS",
        "RS",

        "BT",
        "TP",

        "BK",

        "TR1",
        "TR2",
        "TR3",

        "BK1",
        "BK2",
        "BK3"

    }

    # =========================================================
    # BUILD
    # =========================================================

    @staticmethod
    def build(
        module,
        user_parts=None
    ):

        if user_parts is None:

            user_parts = []

        # =====================================================
        # EXISTING USER PARTS
        # =====================================================
        #
        # IMPORTANT:
        #
        # We do NOT use Source to determine whether a part is
        # structural.
        #
        # ModuleCalculator currently assigns Source = "Module"
        # to calculated parts, including shelves added from the
        # table.
        #
        # Therefore the reliable distinction is the structural
        # code list.
        #

        existing_user_parts = (
            ModuleBuilder.getExistingUserParts(
                module
            )
        )

        # =====================================================
        # GENERATOR
        # =====================================================

        generator = GeneratorFactory.get(
            module.Type
        )

        definitions = generator.generate(
            module
        )

        # =====================================================
        # USER PARTS
        # =====================================================

        all_user_parts = []

        all_user_parts.extend(
            existing_user_parts
        )

        all_user_parts.extend(
            user_parts
        )

        added_user_codes = set()

        for definition in all_user_parts:

            if not isinstance(
                definition,
                dict
            ):

                continue

            code = str(
                definition.get(
                    "Code",
                    ""
                )
            )

            role = str(
                definition.get(
                    "Role",
                    ""
                )
            )

            if not code:

                continue

            #
            # Structural parts belong exclusively to the
            # generator.
            #

            if code in ModuleBuilder.STRUCTURAL_CODES:

                continue

            #
            # Structural roles also remain controlled by the
            # generator.
            #

            if role in (
                "Side",
                "Top",
                "Bottom",
                "Back"
            ):

                continue

            #
            # Avoid duplicates.
            #

            if code in added_user_codes:

                continue

            added_user_codes.add(
                code
            )

            definitions.append(
                dict(
                    definition
                )
            )

        # =====================================================
        # AUTOMATIC SHELVES
        # =====================================================

        shelves = [

            definition

            for definition in definitions

            if definition.get(
                "Role"
            ) == "Shelf"

            and
            definition.get(
                "PositionMode",
                "Automatic"
            ) == "Automatic"

        ]

        # =====================================================
        # AUTOMATIC DIVIDERS
        # =====================================================

        dividers = [

            definition

            for definition in definitions

            if definition.get(
                "Role"
            ) == "Divider"

            and
            definition.get(
                "PositionMode",
                "Automatic"
            ) == "Automatic"

        ]

        shelf_count = len(
            shelves
        )

        divider_count = len(
            dividers
        )

        # =====================================================
        # MODULE DIMENSIONS
        # =====================================================

        panel_thickness = (
            ModuleCalculator.toFloat(
                module.PanelThickness
            )
        )

        module_height = (
            ModuleCalculator.toFloat(
                module.Height
            )
        )

        module_width = (
            ModuleCalculator.toFloat(
                module.Width
            )
        )

        # =====================================================
        # SHELF SPACING
        # =====================================================

        shelf_space = None

        if shelf_count > 0:

            internal_height = (
                module_height
                -
                panel_thickness * 2
            )

            shelf_thicknesses = [

                ModuleCalculator.toFloat(
                    definition.get(
                        "Thickness",
                        panel_thickness
                    )
                )

                for definition in shelves

            ]

            total_shelf_thickness = sum(
                shelf_thicknesses
            )

            shelf_space = (
                internal_height
                -
                total_shelf_thickness
            ) / (
                shelf_count + 1
            )

        # =====================================================
        # DIVIDER SPACING
        # =====================================================

        divider_space = None

        if divider_count > 0:

            internal_width = (
                module_width
                -
                panel_thickness * 2
            )

            divider_thicknesses = [

                ModuleCalculator.toFloat(
                    definition.get(
                        "Thickness",
                        panel_thickness
                    )
                )

                for definition in dividers

            ]

            total_divider_thickness = sum(
                divider_thicknesses
            )

            divider_space = (
                internal_width
                -
                total_divider_thickness
            ) / (
                divider_count + 1
            )

        # =====================================================
        # CALCULATE
        # =====================================================

        parts_data = []

        shelf_index = 0

        divider_index = 0

        for definition in definitions:

            role = definition.get(
                "Role",
                ""
            )

            # =================================================
            # SHELF
            # =================================================

            if role == "Shelf":

                data = ModuleCalculator.calculate(

                    module,

                    definition,

                    position_index=shelf_index,

                    automatic_count=(
                        shelf_count
                        if shelf_count > 0
                        else 1
                    ),

                    automatic_space=shelf_space

                )

                if definition.get(
                    "PositionMode",
                    "Automatic"
                ) == "Automatic":

                    shelf_index += 1

            # =================================================
            # DIVIDER
            # =================================================

            elif role == "Divider":

                data = ModuleCalculator.calculate(

                    module,

                    definition,

                    position_index=divider_index,

                    automatic_count=(
                        divider_count
                        if divider_count > 0
                        else 1
                    ),

                    automatic_space=divider_space

                )

                if definition.get(
                    "PositionMode",
                    "Automatic"
                ) == "Automatic":

                    divider_index += 1

            # =================================================
            # EVERYTHING ELSE
            # =================================================

            else:

                data = ModuleCalculator.calculate(
                    module,
                    definition
                )

            parts_data.append(
                data
            )

        # =====================================================
        # CREATE / UPDATE
        # =====================================================

        for data in parts_data:

            code = data.get(
                "Code",
                ""
            )

            if not code:

                continue

            part = ModuleBuilder.find(
                module,
                code
            )

            if part is None:

                part = ModuleBuilder.create(
                    module
                )

            part.Proxy.setData(
                part,
                data
            )

            part.touch()

        # =====================================================
        # VALID CODES
        # =====================================================

        valid_codes = {

            data.get(
                "Code",
                ""
            )

            for data in parts_data

        }

        # =====================================================
        # REMOVE OBSOLETE
        # =====================================================
        #
        # ONLY STRUCTURAL PARTS MAY BE REMOVED AUTOMATICALLY.
        #
        # User-created parts such as shelves and custom parts
        # are preserved.
        #

        for part in list(
            module.Group
        ):

            if not hasattr(
                part,
                "Code"
            ):

                continue

            code = str(
                part.Code
            )

            #
            # User-created part:
            # preserve it.
            #

            if code not in ModuleBuilder.STRUCTURAL_CODES:

                continue

            #
            # Structural part:
            # remove if no longer generated.
            #

            if code not in valid_codes:

                try:

                    module.removeObject(
                        part
                    )

                except Exception:

                    pass

                try:

                    module.Document.removeObject(
                        part.Name
                    )

                except Exception:

                    pass

        # =====================================================
        # RECOMPUTE
        # =====================================================

        module.Document.recompute()

    # =========================================================
    # GET EXISTING USER PARTS
    # =========================================================

    @staticmethod
    def getExistingUserParts(
        module
    ):

        definitions = []

        for part in list(
            module.Group
        ):

            if not hasattr(
                part,
                "Code"
            ):

                continue

            code = str(
                getattr(
                    part,
                    "Code",
                    ""
                )
            )

            if not code:

                continue

            #
            # Structural parts are controlled by the generator.
            #

            if code in ModuleBuilder.STRUCTURAL_CODES:

                continue

            #
            # Everything else already present in the module is
            # considered a user part.
            #

            definition = {

                "Code":
                    code,

                "Role":
                    getattr(
                        part,
                        "Role",
                        "Custom"
                    ),

                "PartType":
                    getattr(
                        part,
                        "PartType",
                        ""
                    ),

                "Label":
                    getattr(
                        part,
                        "Label",
                        "Pieza"
                    ),

                "Material":
                    getattr(
                        part,
                        "Material",
                        ""
                    ),

                "MaterialCode":
                    getattr(
                        part,
                        "MaterialCode",
                        ""
                    ),

                "Quantity":
                    getattr(
                        part,
                        "Quantity",
                        1
                    ),

                "PositionMode":
                    getattr(
                        part,
                        "PositionMode",
                        "Automatic"
                    )

            }

            # =================================================
            # DIMENSIONS
            # =================================================

            if hasattr(
                part,
                "Length"
            ):

                definition["Length"] = (
                    part.Length
                )

            if hasattr(
                part,
                "Width"
            ):

                definition["Width"] = (
                    part.Width
                )

            if hasattr(
                part,
                "Thickness"
            ):

                definition["Thickness"] = (
                    part.Thickness
                )

            # =================================================
            # POSITION
            # =================================================

            if hasattr(
                part,
                "PositionX"
            ):

                definition["PositionX"] = (
                    part.PositionX
                )

            if hasattr(
                part,
                "PositionY"
            ):

                definition["PositionY"] = (
                    part.PositionY
                )

            if hasattr(
                part,
                "PositionZ"
            ):

                definition["PositionZ"] = (
                    part.PositionZ
                )

            # =================================================
            # ROTATION
            # =================================================

            if hasattr(
                part,
                "RotationX"
            ):

                definition["RotationX"] = (
                    part.RotationX
                )

            if hasattr(
                part,
                "RotationY"
            ):

                definition["RotationY"] = (
                    part.RotationY
                )

            if hasattr(
                part,
                "RotationZ"
            ):

                definition["RotationZ"] = (
                    part.RotationZ
                )

            definitions.append(
                definition
            )

        return definitions

    # =========================================================
    # FIND
    # =========================================================

    @staticmethod
    def find(
        module,
        code
    ):

        for part in module.Group:

            if not hasattr(
                part,
                "Code"
            ):

                continue

            if str(
                part.Code
            ) == str(
                code
            ):

                return part

        return None

    # =========================================================
    # CREATE
    # =========================================================

    @staticmethod
    def create(
        module
    ):

        part = create_part(
            module.Document
        )

        module.addObject(
            part
        )

        return part