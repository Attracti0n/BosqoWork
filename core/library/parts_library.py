class PartsLibrary:

    PARTS_LIBRARY = {

        "KitchenBase": [

            {
                "Code": "LS",
                "Label": "Lateral izquierdo",
                "Role": "Side",
                "Side": "Left"
            },

            {
                "Code": "RS",
                "Label": "Lateral derecho",
                "Role": "Side",
                "Side": "Right"
            },

            {
                "Code": "TP",
                "Label": "Tapa",
                "Role": "Top"
            },

            {
                "Code": "BT",
                "Label": "Base",
                "Role": "Bottom"
            },

            {
                "Code": "BK",
                "Label": "Trasera",
                "Role": "Back"
            }

        ]

    }

    @staticmethod
    def getParts(moduleType):

        if moduleType not in PartsLibrary.PARTS_LIBRARY:

            raise ValueError(
                f"Unknown module type: {moduleType}"
            )

        return [
            part.copy()
            for part in PartsLibrary.PARTS_LIBRARY[moduleType]
        ]


PARTS_LIBRARY = PartsLibrary.PARTS_LIBRARY