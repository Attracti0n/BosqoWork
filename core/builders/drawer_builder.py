import FreeCAD

from objects.bosqo_part import (
    create_part
)


# =============================================================
# DRAWER BUILDER
# =============================================================

class DrawerBuilder:

    STRUCTURAL_PREFIXES = (
        "LS_",
        "RS_",
        "BT_",
        "BK_",
        "FR_"
    )

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

            return float(
                value
            )

        except Exception:

            return default

    # =========================================================
    # MODULE
    # =========================================================

    @staticmethod
    def getModule(
        drawer
    ):

        if drawer is None:

            return None

        document = getattr(
            drawer,
            "Document",
            None
        )

        if document is None:

            return None

        # -----------------------------------------------------
        # PRIMARY METHOD:
        # Find the real group containing the drawer.
        # -----------------------------------------------------

        try:

            for obj in document.Objects:

                try:

                    group = getattr(
                        obj,
                        "Group",
                        None
                    )

                    if group is None:

                        continue

                    if drawer not in group:

                        continue

                    if not (
                        hasattr(
                            obj,
                            "Width"
                        )
                        and
                        hasattr(
                            obj,
                            "Height"
                        )
                        and
                        hasattr(
                            obj,
                            "Depth"
                        )
                    ):

                        continue

                    return obj

                except Exception:

                    continue

        except Exception:

            pass

        # -----------------------------------------------------
        # OLD DOCUMENT FALLBACK
        # -----------------------------------------------------

        try:

            module_name = str(
                getattr(
                    drawer,
                    "ModuleName",
                    ""
                )
            ).strip()

        except Exception:

            module_name = ""

        if module_name:

            try:

                return document.getObject(
                    module_name
                )

            except Exception:

                pass

        return None

    # =========================================================
    # MODULE PLACEMENT
    # =========================================================

    @staticmethod
    def transformPoint(
        module,
        x,
        y,
        z
    ):

        local = FreeCAD.Vector(
            float(x),
            float(y),
            float(z)
        )

        if module is None:

            return local

        try:

            return module.Placement.multVec(
                local
            )

        except Exception:

            return local

    # =========================================================
    # ROTATION
    # =========================================================

    @staticmethod
    def rotation(
        rx,
        ry,
        rz
    ):

        return (

            FreeCAD.Rotation(
                FreeCAD.Vector(
                    1,
                    0,
                    0
                ),
                rx
            )

            *

            FreeCAD.Rotation(
                FreeCAD.Vector(
                    0,
                    1,
                    0
                ),
                ry
            )

            *

            FreeCAD.Rotation(
                FreeCAD.Vector(
                    0,
                    0,
                    1
                ),
                rz
            )

        )

    # =========================================================
    # PLACEMENT
    # =========================================================

    @staticmethod
    def makePlacement(
        module,
        x,
        y,
        z,
        rx=0,
        ry=0,
        rz=0
    ):

        position = (
            DrawerBuilder.transformPoint(
                module,
                x,
                y,
                z
            )
        )

        local_rotation = (
            DrawerBuilder.rotation(
                float(rx),
                float(ry),
                float(rz)
            )
        )

        if module is not None:

            try:

                rotation = (
                    module.Placement.Rotation
                    *
                    local_rotation
                )

            except Exception:

                rotation = local_rotation

        else:

            rotation = local_rotation

        return FreeCAD.Placement(
            position,
            rotation
        )

    # =========================================================
    # PART DATA
    # =========================================================

    @staticmethod
    def makeData(
        module,
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
        quantity=1
    ):

        placement = (
            DrawerBuilder.makePlacement(
                module,
                x,
                y,
                z
            )
        )

        global_position = (
            DrawerBuilder.transformPoint(
                module,
                x,
                y,
                z
            )
        )

        return {

            "Code":
                code,

            "Label":
                label,

            "Role":
                role,

            "PartType":
                part_type,

            "Length":
                length,

            "Width":
                width,

            "Thickness":
                thickness,

            "Quantity":
                quantity,

            "MaterialCode":
                "",

            "PositionX":
                global_position.x,

            "PositionY":
                global_position.y,

            "PositionZ":
                global_position.z,

            "PositionMode":
                "Automatic",

            "PositionType":
                "Automatic",

            "LengthAxis":
                length_axis,

            "WidthAxis":
                width_axis,

            "ThicknessAxis":
                thickness_axis,

            "Placement":
                placement
        }

    # =========================================================
    # BUILD
    # =========================================================

    @staticmethod
    def build(
        drawer
    ):

        if drawer is None:

            return False

        # =====================================================
        # MODULE
        # =====================================================

        module = (
            DrawerBuilder.getModule(
                drawer
            )
        )

        if module is None:

            FreeCAD.Console.PrintWarning(
                "El cajón no está contenido "
                "en un módulo válido.\n"
            )

            return False

        # =====================================================
        # MODULE DIMENSIONS
        # =====================================================

        module_width = (
            DrawerBuilder.toFloat(
                getattr(
                    module,
                    "Width",
                    0
                )
            )
        )

        module_height = (
            DrawerBuilder.toFloat(
                getattr(
                    module,
                    "Height",
                    0
                )
            )
        )

        module_depth = (
            DrawerBuilder.toFloat(
                getattr(
                    module,
                    "Depth",
                    0
                )
            )
        )

        module_thickness = (
            DrawerBuilder.toFloat(
                getattr(
                    module,
                    "PanelThickness",
                    19
                ),
                19
            )
        )

        # =====================================================
        # DRAWER DIMENSIONS
        # =====================================================

        width = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "Width",
                    0
                )
            )
        )

        height = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "Height",
                    0
                )
            )
        )

        depth = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "Depth",
                    0
                )
            )
        )

        # =====================================================
        # DRAWER PARAMETERS
        # =====================================================

        bottom_thickness = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "BottomThickness",
                    10
                ),
                10
            )
        )

        side_thickness = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "SideThickness",
                    16
                ),
                16
            )
        )

        back_thickness = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "BackThickness",
                    16
                ),
                16
            )
        )

        front_thickness = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "FrontThickness",
                    19
                ),
                19
            )
        )

        drawer_gap = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "DrawerGap",
                    3
                ),
                3
            )
        )

        # =====================================================
        # QUANTITY
        # =====================================================

        quantity = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "Quantity",
                    1
                ),
                1
            )
        )

        quantity = max(
            1,
            int(
                round(
                    quantity
                )
            )
        )

        # =====================================================
        # POSITION
        # =====================================================

        position_x = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "PositionX",
                    0
                )
            )
        )

        position_y = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "PositionY",
                    0
                )
            )
        )

        position_z = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "PositionZ",
                    0
                )
            )
        )

        # =====================================================
        # VALIDATION
        # =====================================================

        if (
            module_width <= 0
            or
            module_height <= 0
            or
            module_depth <= 0
        ):

            FreeCAD.Console.PrintWarning(
                "Dimensiones del módulo no válidas.\n"
            )

            return False

        if (
            width <= 0
            or
            height <= 0
            or
            depth <= 0
        ):

            FreeCAD.Console.PrintWarning(
                "Dimensiones del cajón no válidas.\n"
            )

            return False

        if (
            bottom_thickness <= 0
            or
            side_thickness <= 0
            or
            back_thickness <= 0
            or
            front_thickness <= 0
        ):

            FreeCAD.Console.PrintWarning(
                "Espesores del cajón no válidos.\n"
            )

            return False

        if drawer_gap < 0:

            FreeCAD.Console.PrintWarning(
                "La separación entre cajones "
                "no puede ser negativa.\n"
            )

            return False

        # =====================================================
        # INTERNAL WIDTH
        # =====================================================

        internal_width = (
            width
            -
            side_thickness * 2
        )

        if internal_width <= 0:

            FreeCAD.Console.PrintWarning(
                "La anchura del cajón no permite crear "
                "los laterales.\n"
            )

            return False

        # =====================================================
        # INTERNAL DEPTH
        # =====================================================

        internal_depth = (
            depth
            -
            back_thickness
        )

        if internal_depth <= 0:

            FreeCAD.Console.PrintWarning(
                "La profundidad del cajón no permite crear "
                "la trasera.\n"
            )

            return False

        # =====================================================
        # POSITION
        # =====================================================

        if position_x < 0:

            FreeCAD.Console.PrintWarning(
                "La posición X del cajón no puede ser negativa.\n"
            )

            return False

        if position_y < 0:

            FreeCAD.Console.PrintWarning(
                "La posición Y del cajón no puede ser negativa.\n"
            )

            return False

        if position_z < 0:

            FreeCAD.Console.PrintWarning(
                "La posición Z del cajón no puede ser negativa.\n"
            )

            return False

        # =====================================================
        # MODULE INTERNAL LIMITS
        # =====================================================

        internal_module_width = (
            module_width
            -
            module_thickness * 2
        )

        if (
            position_x
            +
            width
            >
            internal_module_width
        ):

            FreeCAD.Console.PrintWarning(
                "El cajón supera el ancho interior "
                "del módulo.\n"
            )

            return False

        if (
            position_y
            +
            depth
            >
            module_depth
        ):

            FreeCAD.Console.PrintWarning(
                "El cajón supera la profundidad "
                "del módulo.\n"
            )

            return False

        # =====================================================
        # TOTAL HEIGHT
        # =====================================================

        total_height = (
            height * quantity
            +
            drawer_gap * (quantity - 1)
        )

        internal_module_height = (
            module_height
            -
            module_thickness * 2
        )

        if (
            position_z
            +
            total_height
            >
            internal_module_height
        ):

            FreeCAD.Console.PrintWarning(
                "Los cajones superan la altura interior "
                "del módulo.\n"
            )

            return False

        # =====================================================
        # DEFINITIONS
        # =====================================================

        definitions = []

        # =====================================================
        # CREATE DRAWERS
        # =====================================================

        for index in range(
            quantity
        ):

            drawer_number = (
                index
                +
                1
            )

            # -------------------------------------------------
            # Vertical position
            # -------------------------------------------------

            base_z = (
                position_z
                +
                index
                *
                (
                    height
                    +
                    drawer_gap
                )
            )

            # -------------------------------------------------
            # LEFT SIDE
            # -------------------------------------------------

            definitions.append(

                DrawerBuilder.makeData(

                    module,

                    "LS_"
                    +
                    str(
                        drawer_number
                    ),

                    "Lateral izquierdo "
                    +
                    str(
                        drawer_number
                    ),

                    "Side",

                    "Estructural",

                    height,

                    depth,

                    side_thickness,

                    position_x,

                    position_y,

                    base_z,

                    "Z",

                    "Y",

                    "X"

                )

            )

            # -------------------------------------------------
            # RIGHT SIDE
            # -------------------------------------------------

            definitions.append(

                DrawerBuilder.makeData(

                    module,

                    "RS_"
                    +
                    str(
                        drawer_number
                    ),

                    "Lateral derecho "
                    +
                    str(
                        drawer_number
                    ),

                    "Side",

                    "Estructural",

                    height,

                    depth,

                    side_thickness,

                    position_x
                    +
                    width
                    -
                    side_thickness,

                    position_y,

                    base_z,

                    "Z",

                    "Y",

                    "X"

                )

            )

            # -------------------------------------------------
            # BOTTOM
            # -------------------------------------------------

            definitions.append(

                DrawerBuilder.makeData(

                    module,

                    "BT_"
                    +
                    str(
                        drawer_number
                    ),

                    "Fondo "
                    +
                    str(
                        drawer_number
                    ),

                    "Bottom",

                    "Estructural",

                    internal_width,

                    internal_depth,

                    bottom_thickness,

                    position_x
                    +
                    side_thickness,

                    position_y,

                    base_z,

                    "X",

                    "Y",

                    "Z"

                )

            )

            # -------------------------------------------------
            # BACK
            # -------------------------------------------------

            definitions.append(

                DrawerBuilder.makeData(

                    module,

                    "BK_"
                    +
                    str(
                        drawer_number
                    ),

                    "Trasera "
                    +
                    str(
                        drawer_number
                    ),

                    "Back",

                    "Estructural",

                    height,

                    internal_width,

                    back_thickness,

                    position_x
                    +
                    side_thickness,

                    position_y
                    +
                    depth
                    -
                    back_thickness,

                    base_z,

                    "Z",

                    "X",

                    "Y"

                )

            )

            # -------------------------------------------------
            # FRONT
            # -------------------------------------------------

            definitions.append(

                DrawerBuilder.makeData(

                    module,

                    "FR_"
                    +
                    str(
                        drawer_number
                    ),

                    "Frente "
                    +
                    str(
                        drawer_number
                    ),

                    "Front",

                    "Estructural",

                    height,

                    width,

                    front_thickness,

                    position_x,

                    position_y
                    -
                    front_thickness,

                    base_z,

                    "Z",

                    "X",

                    "Y"

                )

            )

        # =====================================================
        # EXISTING PARTS
        # =====================================================

        existing = {}

        try:

            children = list(
                drawer.Group
            )

        except Exception:

            children = []

        for child in children:

            code = str(
                getattr(
                    child,
                    "Code",
                    ""
                )
            ).strip()

            if code:

                existing[
                    code
                ] = child

        # =====================================================
        # WANTED CODES
        # =====================================================

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
        # REMOVE OLD STRUCTURAL PARTS
        # =====================================================

        for code, old in list(
            existing.items()
        ):

            is_structural = any(

                code.startswith(
                    prefix
                )

                for prefix in
                DrawerBuilder.STRUCTURAL_PREFIXES

            )

            if not is_structural:

                continue

            if code in wanted_codes:

                continue

            try:

                drawer.removeObject(
                    old
                )

            except Exception:

                pass

            try:

                drawer.Document.removeObject(
                    old.Name
                )

            except Exception:

                pass

        # =====================================================
        # CREATE / UPDATE PARTS
        # =====================================================

        for data in definitions:

            code = str(
                data.get(
                    "Code",
                    ""
                )
            ).strip()

            if not code:

                continue

            part = existing.get(
                code
            )

            # -------------------------------------------------
            # CREATE
            # -------------------------------------------------

            if part is None:

                try:

                    part = create_part(
                        drawer.Document
                    )

                    drawer.addObject(
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

            # -------------------------------------------------
            # PART PROXY
            # -------------------------------------------------

            part_proxy = getattr(
                part,
                "Proxy",
                None
            )

            # -------------------------------------------------
            # SET DATA
            # -------------------------------------------------

            try:

                set_data = getattr(
                    part_proxy,
                    "setData",
                    None
                )

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

                continue

            # -------------------------------------------------
            # PLACEMENT
            # -------------------------------------------------

            try:

                placement = data.get(
                    "Placement"
                )

                if placement is not None:

                    part.Placement = (
                        placement
                    )

            except Exception:

                pass

            # -------------------------------------------------
            # LABEL
            # -------------------------------------------------

            try:

                part.Label = data.get(
                    "Label",
                    part.Label
                )

            except Exception:

                pass

            # -------------------------------------------------
            # SOURCE
            # -------------------------------------------------

            try:

                part.Source = "Parametric"

            except Exception:

                pass

            # -------------------------------------------------
            # EXECUTE
            # -------------------------------------------------

            try:

                execute = getattr(
                    part_proxy,
                    "execute",
                    None
                )

                if callable(
                    execute
                ):

                    execute(
                        part
                    )

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error generando geometría de "
                    +
                    code
                    +
                    ": "
                    +
                    str(error)
                    +
                    "\n"
                )

            # -------------------------------------------------
            # RESTORE PLACEMENT
            # -------------------------------------------------

            try:

                placement = data.get(
                    "Placement"
                )

                if placement is not None:

                    part.Placement = (
                        placement
                    )

            except Exception:

                pass

            # -------------------------------------------------
            # VISIBILITY
            # -------------------------------------------------

            try:

                part.ViewObject.Visibility = True

            except Exception:

                pass

        # =====================================================
        # STATUS
        # =====================================================

        try:

            drawer.Status = "Generated"

        except Exception:

            pass

        try:

            drawer.GeometryStatus = "Generated"

        except Exception:

            pass

        try:

            drawer.ViewObject.Visibility = True

        except Exception:

            pass

        return True

    # =========================================================
    # CLEAR
    # =========================================================

    @staticmethod
    def clear(
        drawer
    ):

        if drawer is None:

            return

        try:

            children = list(
                drawer.Group
            )

        except Exception:

            children = []

        for child in children:

            try:

                drawer.removeObject(
                    child
                )

            except Exception:

                pass

            try:

                drawer.Document.removeObject(
                    child.Name
                )

            except Exception:

                pass

        try:

            drawer.Status = "Defined"

        except Exception:

            pass

        try:

            drawer.GeometryStatus = (
                "Not generated"
            )

        except Exception:

            pass

    # =========================================================
    # VALIDATE
    # =========================================================

    @staticmethod
    def validate(
        drawer
    ):

        if drawer is None:

            return False

        module = (
            DrawerBuilder.getModule(
                drawer
            )
        )

        if module is None:

            return False

        module_width = (
            DrawerBuilder.toFloat(
                getattr(
                    module,
                    "Width",
                    0
                )
            )
        )

        module_height = (
            DrawerBuilder.toFloat(
                getattr(
                    module,
                    "Height",
                    0
                )
            )
        )

        module_depth = (
            DrawerBuilder.toFloat(
                getattr(
                    module,
                    "Depth",
                    0
                )
            )
        )

        width = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "Width",
                    0
                )
            )
        )

        height = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "Height",
                    0
                )
            )
        )

        depth = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "Depth",
                    0
                )
            )
        )

        bottom_thickness = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "BottomThickness",
                    0
                )
            )
        )

        side_thickness = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "SideThickness",
                    0
                )
            )
        )

        back_thickness = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "BackThickness",
                    0
                )
            )
        )

        front_thickness = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "FrontThickness",
                    0
                )
            )

        )

        drawer_gap = (
            DrawerBuilder.toFloat(
                getattr(
                    drawer,
                    "DrawerGap",
                    0
                )
            )
        )

        if (
            module_width <= 0
            or
            module_height <= 0
            or
            module_depth <= 0
        ):

            return False

        if (
            width <= 0
            or
            height <= 0
            or
            depth <= 0
        ):

            return False

        if (
            bottom_thickness <= 0
            or
            side_thickness <= 0
            or
            back_thickness <= 0
            or
            front_thickness <= 0
        ):

            return False

        if drawer_gap < 0:

            return False

        if (
            width
            <=
            side_thickness * 2
        ):

            return False

        if (
            depth
            <=
            back_thickness
        ):

            return False

        return True