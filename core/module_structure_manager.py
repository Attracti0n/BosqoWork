from core.module_structure import ModuleStructure


class ModuleStructureManager:

    @staticmethod
    def getParts(module):

        parts = []

        #
        # Fixed structure
        #

        parts.append({
            "Code": "LS",
            "Role": "Side"
        })

        parts.append({
            "Code": "RS",
            "Role": "Side"
        })

        parts.append({
            "Code": "BT",
            "Role": "Bottom"
        })

        #
        # Top
        #

        top_type = getattr(
            module,
            "TopType",
            "Tapa"
        )

        parts.extend(
            ModuleStructure.getTopParts(
                top_type
            )
        )

        #
        # Back
        #

        back_type = getattr(
            module,
            "BackType",
            "Trasera sobrepuesta"
        )

        parts.extend(
            ModuleStructure.getBackParts(
                back_type
            )
        )

        return parts