class BaseGenerator:

    @staticmethod
    def generate(
        module
    ):

        #
        # Part definitions
        #
        # The generator defines which parts
        # belong to the module.
        #
        # Dimensions and placement are
        # calculated by ModuleCalculator.
        #

        parts = [

            {
                "Code": "LS",
                "Role": "Side"
            },

            {
                "Code": "RS",
                "Role": "Side"
            },

            {
                "Code": "TP",
                "Role": "Top"
            },

            {
                "Code": "BT",
                "Role": "Bottom"
            },

            {
                "Code": "BK",
                "Role": "Back"
            }

        ]

        return parts