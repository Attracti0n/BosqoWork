import FreeCAD


# =============================================================
# BOSQO DRAWER
# =============================================================

class BosqoDrawer:

    def __init__(
        self,
        obj
    ):

        obj.Proxy = self

        self.initProperties(
            obj
        )

    # =========================================================
    # PROPERTIES
    # =========================================================

    def initProperties(
        self,
        obj
    ):

        # =====================================================
        # IDENTIFICATION
        # =====================================================

        self.addString(
            obj,
            "DrawerType",
            "",
            "Cajón"
        )

        self.addString(
            obj,
            "System",
            "",
            "Cajón"
        )

        self.addString(
            obj,
            "Status",
            "Defined",
            "Cajón"
        )

        self.addString(
            obj,
            "Source",
            "Created",
            "Cajón"
        )

        # =====================================================
        # DIMENSIONS
        # =====================================================

        self.addLength(
            obj,
            "Width",
            540,
            "Dimensiones"
        )

        self.addLength(
            obj,
            "Height",
            150,
            "Dimensiones"
        )

        self.addLength(
            obj,
            "Depth",
            500,
            "Dimensiones"
        )

        # =====================================================
        # POSITION
        # =====================================================

        self.addLength(
            obj,
            "PositionX",
            0,
            "Posición"
        )

        self.addLength(
            obj,
            "PositionY",
            0,
            "Posición"
        )

        self.addLength(
            obj,
            "PositionZ",
            0,
            "Posición"
        )

        self.addString(
            obj,
            "PositionMode",
            "Automatic",
            "Posición"
        )

        # =====================================================
        # PARAMETERS
        # =====================================================

        self.addLength(
            obj,
            "BottomThickness",
            10,
            "Parámetros"
        )

        self.addLength(
            obj,
            "SideThickness",
            16,
            "Parámetros"
        )

        self.addLength(
            obj,
            "BackThickness",
            16,
            "Parámetros"
        )

        self.addLength(
            obj,
            "FrontThickness",
            19,
            "Parámetros"
        )

        self.addLength(
            obj,
            "DrawerGap",
            3,
            "Parámetros"
        )

        # =====================================================
        # QUANTITY
        # =====================================================

        if not hasattr(
            obj,
            "Quantity"
        ):

            obj.addProperty(
                "App::PropertyInteger",
                "Quantity",
                "Cajón",
                "Cantidad de cajones"
            )

            obj.Quantity = 1

        # =====================================================
        # GEOMETRY STATUS
        # =====================================================

        if not hasattr(
            obj,
            "GeometryStatus"
        ):

            obj.addProperty(
                "App::PropertyString",
                "GeometryStatus",
                "Geometry",
                "Estado de la geometría"
            )

            obj.GeometryStatus = (
                "Not generated"
            )

    # =========================================================
    # HELPERS
    # =========================================================

    def addString(
        self,
        obj,
        name,
        value,
        group
    ):

        if not hasattr(
            obj,
            name
        ):

            obj.addProperty(
                "App::PropertyString",
                name,
                group
            )

            setattr(
                obj,
                name,
                value
            )

    def addLength(
        self,
        obj,
        name,
        value,
        group
    ):

        if not hasattr(
            obj,
            name
        ):

            obj.addProperty(
                "App::PropertyLength",
                name,
                group
            )

            setattr(
                obj,
                name,
                FreeCAD.Units.Quantity(
                    str(value)
                    +
                    " mm"
                )
            )

    # =========================================================
    # DATA
    # =========================================================

    def setData(
        self,
        obj,
        data
    ):

        if not isinstance(
            data,
            dict
        ):

            return

        for key, value in data.items():

            if not hasattr(
                obj,
                key
            ):

                continue

            try:

                setattr(
                    obj,
                    key,
                    value
                )

            except Exception:

                pass

    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(
        self,
        obj
    ):

        try:

            if hasattr(
                obj,
                "GeometryStatus"
            ):

                if str(
                    getattr(
                        obj,
                        "Status",
                        ""
                    )
                ) == "Generated":

                    obj.GeometryStatus = (
                        "Generated"
                    )

        except Exception:

            pass

    # =========================================================
    # ON CHANGED
    # =========================================================

    def onChanged(
        self,
        obj,
        prop
    ):

        return

    # =========================================================
    # SERIALIZATION
    # =========================================================

    def __getstate__(
        self
    ):

        return None

    def __setstate__(
        self,
        state
    ):

        return None


# =============================================================
# VIEW PROVIDER
# =============================================================

class ViewProviderBosqoDrawer:

    def __init__(
        self,
        view_object
    ):

        view_object.Proxy = self

    def getIcon(
        self
    ):

        return ""


# =============================================================
# FACTORY
# =============================================================

def create_drawer(
    document
):

    drawer = document.addObject(
        "App::DocumentObjectGroupPython",
        "BosqoDrawer"
    )

    BosqoDrawer(
        drawer
    )

    ViewProviderBosqoDrawer(
        drawer.ViewObject
    )

    return drawer