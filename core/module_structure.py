class ModuleStructure:

    TOP_TYPES = [
        "Tapa",
        "Encimera",
        "2 travesaños",
        "3 travesaños"
    ]

    BACK_TYPES = [
        "Trasera sobrepuesta",
        "Trasera oculta",
        "2 travesaños",
        "3 travesaños"
    ]

    @staticmethod
    def getTopParts(top_type):

        if top_type == "Tapa":

            return [
                {
                    "Code": "TP",
                    "Role": "Top"
                }
            ]

        if top_type == "Encimera":

            return []

        if top_type == "2 travesaños":

            return [
                {
                    "Code": "TT1",
                    "Role": "TopCrossbar"
                },
                {
                    "Code": "TT2",
                    "Role": "TopCrossbar"
                }
            ]

        if top_type == "3 travesaños":

            return [
                {
                    "Code": "TT1",
                    "Role": "TopCrossbar"
                },
                {
                    "Code": "TT2",
                    "Role": "TopCrossbar"
                },
                {
                    "Code": "TT3",
                    "Role": "TopCrossbar"
                }
            ]

        return []


    @staticmethod
    def getBackParts(back_type):

        if back_type == "Trasera sobrepuesta":

            return [
                {
                    "Code": "BK",
                    "Role": "Back"
                }
            ]

        if back_type == "Trasera oculta":

            return [
                {
                    "Code": "BK",
                    "Role": "Back"
                }
            ]

        if back_type == "2 travesaños":

            return [
                {
                    "Code": "BT1",
                    "Role": "BackCrossbar"
                },
                {
                    "Code": "BT2",
                    "Role": "BackCrossbar"
                }
            ]

        if back_type == "3 travesaños":

            return [
                {
                    "Code": "BT1",
                    "Role": "BackCrossbar"
                },
                {
                    "Code": "BT2",
                    "Role": "BackCrossbar"
                },
                {
                    "Code": "BT3",
                    "Role": "BackCrossbar"
                }
            ]

        return []