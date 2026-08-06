class BaseGenerator:

    @staticmethod
    def generate(
        module
    ):

        parts = []

        #
        # =====================================================
        # LATERALS
        # =====================================================
        #

        parts.append(
            {
                "Code": "LS",
                "Role": "Side"
            }
        )

        parts.append(
            {
                "Code": "RS",
                "Role": "Side"
            }
        )

        #
        # =====================================================
        # BOTTOM
        # =====================================================
        #

        parts.append(
            {
                "Code": "BT",
                "Role": "Bottom"
            }
        )

        #
        # =====================================================
        # TOP SYSTEM
        # =====================================================
        #

        top_type = getattr(
            module,
            "TopType",
            "Tapa completa"
        )

        #
        # COMPLETE TOP
        #

        if top_type == "Tapa completa":

            parts.append(
                {
                    "Code": "TP",
                    "Role": "Top",
                    "TopSystem": "Panel"
                }
            )

        #
        # TWO RAILS
        #

        elif top_type == "2 travesaños":

            parts.append(
                {
                    "Code": "TR1",
                    "Role": "Top",
                    "TopSystem": "Rail",
                    "RailCount": 2,
                    "RailIndex": 0,
                    "Label": "Travesaño superior 1"
                }
            )

            parts.append(
                {
                    "Code": "TR2",
                    "Role": "Top",
                    "TopSystem": "Rail",
                    "RailCount": 2,
                    "RailIndex": 1,
                    "Label": "Travesaño superior 2"
                }
            )

        #
        # THREE RAILS
        #

        elif top_type == "3 travesaños":

            parts.append(
                {
                    "Code": "TR1",
                    "Role": "Top",
                    "TopSystem": "Rail",
                    "RailCount": 3,
                    "RailIndex": 0,
                    "Label": "Travesaño superior 1"
                }
            )

            parts.append(
                {
                    "Code": "TR2",
                    "Role": "Top",
                    "TopSystem": "Rail",
                    "RailCount": 3,
                    "RailIndex": 1,
                    "Label": "Travesaño superior 2"
                }
            )

            parts.append(
                {
                    "Code": "TR3",
                    "Role": "Top",
                    "TopSystem": "Rail",
                    "RailCount": 3,
                    "RailIndex": 2,
                    "Label": "Travesaño superior 3"
                }
            )

        #
        # =====================================================
        # BACK SYSTEM
        # =====================================================
        #

        back_type = getattr(
            module,
            "BackType",
            "Trasera sobrepuesta"
        )

        #
        # COMPLETE BACK
        #

        if back_type in (
            "Trasera sobrepuesta",
            "Trasera oculta"
        ):

            parts.append(
                {
                    "Code": "BK",
                    "Role": "Back",
                    "BackSystem": "Panel"
                }
            )

        #
        # TWO BACK RAILS
        #

        elif back_type == "2 travesaños":

            parts.append(
                {
                    "Code": "BK1",
                    "Role": "Back",
                    "BackSystem": "Rail",
                    "RailCount": 2,
                    "RailIndex": 0,
                    "Label": "Travesaño trasero 1"
                }
            )

            parts.append(
                {
                    "Code": "BK2",
                    "Role": "Back",
                    "BackSystem": "Rail",
                    "RailCount": 2,
                    "RailIndex": 1,
                    "Label": "Travesaño trasero 2"
                }
            )

        #
        # THREE BACK RAILS
        #

        elif back_type == "3 travesaños":

            parts.append(
                {
                    "Code": "BK1",
                    "Role": "Back",
                    "BackSystem": "Rail",
                    "RailCount": 3,
                    "RailIndex": 0,
                    "Label": "Travesaño trasero 1"
                }
            )

            parts.append(
                {
                    "Code": "BK2",
                    "Role": "Back",
                    "BackSystem": "Rail",
                    "RailCount": 3,
                    "RailIndex": 1,
                    "Label": "Travesaño trasero 2"
                }
            )

            parts.append(
                {
                    "Code": "BK3",
                    "Role": "Back",
                    "BackSystem": "Rail",
                    "RailCount": 3,
                    "RailIndex": 2,
                    "Label": "Travesaño trasero 3"
                }
            )

        #
        # NO BACK
        #

        elif back_type == "Sin trasera":

            pass

        #
        # =====================================================
        # RETURN
        # =====================================================
        #

        return parts