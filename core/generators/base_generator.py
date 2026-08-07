class BaseGenerator:

    @staticmethod
    def generate(
        module
    ):

        parts = []

        # =====================================================
        # STRUCTURAL SIDES
        # =====================================================

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

        # =====================================================
        # TOP SYSTEM
        # =====================================================

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
                    "Role": "Top"
                }
            )

        #
        # TWO TOP BEAMS
        #

        elif top_type == "2 travesaños":

            parts.append(
                {
                    "Code": "TT1",
                    "Role": "TopBeam",
                    "BeamIndex": 1,
                    "BeamCount": 2
                }
            )

            parts.append(
                {
                    "Code": "TT2",
                    "Role": "TopBeam",
                    "BeamIndex": 2,
                    "BeamCount": 2
                }
            )

        #
        # THREE TOP BEAMS
        #

        elif top_type == "3 travesaños":

            parts.append(
                {
                    "Code": "TT1",
                    "Role": "TopBeam",
                    "BeamIndex": 1,
                    "BeamCount": 3
                }
            )

            parts.append(
                {
                    "Code": "TT2",
                    "Role": "TopBeam",
                    "BeamIndex": 2,
                    "BeamCount": 3
                }
            )

            parts.append(
                {
                    "Code": "TT3",
                    "Role": "TopBeam",
                    "BeamIndex": 3,
                    "BeamCount": 3
                }
            )

        #
        # SAFETY FALLBACK
        #

        else:

            parts.append(
                {
                    "Code": "TP",
                    "Role": "Top"
                }
            )

        # =====================================================
        # BOTTOM
        # =====================================================

        parts.append(
            {
                "Code": "BT",
                "Role": "Bottom"
            }
        )

        # =====================================================
        # BACK SYSTEM
        # =====================================================

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
                    "BackType": back_type
                }
            )

        #
        # TWO BACK BEAMS
        #

        elif back_type == "2 travesaños":

            parts.append(
                {
                    "Code": "TB1",
                    "Role": "BackBeam",
                    "BeamIndex": 1,
                    "BeamCount": 2
                }
            )

            parts.append(
                {
                    "Code": "TB2",
                    "Role": "BackBeam",
                    "BeamIndex": 2,
                    "BeamCount": 2
                }
            )

        #
        # THREE BACK BEAMS
        #

        elif back_type == "3 travesaños":

            parts.append(
                {
                    "Code": "TB1",
                    "Role": "BackBeam",
                    "BeamIndex": 1,
                    "BeamCount": 3
                }
            )

            parts.append(
                {
                    "Code": "TB2",
                    "Role": "BackBeam",
                    "BeamIndex": 2,
                    "BeamCount": 3
                }
            )

            parts.append(
                {
                    "Code": "TB3",
                    "Role": "BackBeam",
                    "BeamIndex": 3,
                    "BeamCount": 3
                }
            )

        #
        # NO BACK
        #

        elif back_type == "Sin trasera":

            pass

        #
        # SAFETY FALLBACK
        #

        else:

            parts.append(
                {
                    "Code": "BK",
                    "Role": "Back",
                    "BackType": "Trasera sobrepuesta"
                }
            )

        return parts