from objects.bosqo_part import create_part

from core.generators.generator_factory import GeneratorFactory
from core.calculators.module_calculator import ModuleCalculator


class ModuleBuilder:

    @staticmethod
    def build(
        module,
        user_parts=None
    ):

        if user_parts is None:

            user_parts = []

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
        # STRUCTURAL CODES
        # =====================================================

        structural_codes = {
            "LS",
            "RS",
            "BT",
            "TP",
            "BK"
        }

        # =====================================================
        # USER PARTS
        # =====================================================

        for definition in user_parts:

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

            #
            # Never duplicate structural parts.
            #

            if code in structural_codes:

                continue

            if role in (
                "Side",
                "Top",
                "Bottom",
                "Back"
            ):

                continue

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

            #
            # Use the actual thickness of the shelves.
            #

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
            # STRUCTURAL / CUSTOM
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

        for part in list(
            module.Group
        ):

            if not hasattr(
                part,
                "Code"
            ):

                continue

            if part.Code not in valid_codes:

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