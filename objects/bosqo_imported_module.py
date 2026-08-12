import FreeCAD
import json
import os

from app_paths import ICONS_DIR


# =============================================================
# STRUCTURAL PART IDENTIFICATION
# =============================================================

STRUCTURAL_CODES = {
    "LS",
    "RS",
    "BT",
    "TP",
    "BK"
}


STRUCTURAL_ROLES = {
    "LS",
    "RS",
    "BT",
    "TP",
    "BK",

    "LeftSide",
    "RightSide",
    "Bottom",
    "Top",
    "Back",

    "Lateral izquierdo",
    "Lateral derecho",
    "Base",
    "Tapa",
    "Trasera"
}


def _normalize_part_text(
    value
):

    try:

        return str(
            value
        ).strip().lower()

    except Exception:

        return ""


def is_structural_part(
    part
):

    """
    Determina si una pieza pertenece a la estructura
    principal del módulo.

    Las piezas estructurales NO deben aparecer en
    PartsJSON porque ya existen físicamente dentro
    del módulo importado.

    Se detectan principalmente mediante:

        Code
        Role
        PartType
        Name
        Label

    """

    if part is None:

        return False


    values = []


    # ---------------------------------------------------------
    # CODE
    # ---------------------------------------------------------

    for property_name in (
        "Code",
        "PartCode"
    ):

        try:

            if hasattr(
                part,
                property_name
            ):

                value = getattr(
                    part,
                    property_name
                )

                if value is not None:

                    values.append(
                        _normalize_part_text(
                            value
                        )
                    )

        except Exception:

            pass


    # ---------------------------------------------------------
    # ROLE
    # ---------------------------------------------------------

    for property_name in (
        "Role",
        "PartRole"
    ):

        try:

            if hasattr(
                part,
                property_name
            ):

                value = getattr(
                    part,
                    property_name
                )

                if value is not None:

                    values.append(
                        _normalize_part_text(
                            value
                        )
                    )

        except Exception:

            pass


    # ---------------------------------------------------------
    # PART TYPE
    # ---------------------------------------------------------

    for property_name in (
        "PartType",
        "Type"
    ):

        try:

            if hasattr(
                part,
                property_name
            ):

                value = getattr(
                    part,
                    property_name
                )

                if value is not None:

                    values.append(
                        _normalize_part_text(
                            value
                        )
                    )

        except Exception:

            pass


    # ---------------------------------------------------------
    # OBJECT NAME
    # ---------------------------------------------------------

    try:

        values.append(
            _normalize_part_text(
                getattr(
                    part,
                    "Name",
                    ""
                )
            )
        )

    except Exception:

        pass


    # ---------------------------------------------------------
    # LABEL
    # ---------------------------------------------------------

    try:

        values.append(
            _normalize_part_text(
                getattr(
                    part,
                    "Label",
                    ""
                )
            )
        )

    except Exception:

        pass


    # ---------------------------------------------------------
    # EXACT STRUCTURAL CODE MATCH
    # ---------------------------------------------------------

    for value in values:

        if value.upper() in STRUCTURAL_CODES:

            return True


    # ---------------------------------------------------------
    # STRUCTURAL ROLE MATCH
    # ---------------------------------------------------------

    normalized_roles = {

        _normalize_part_text(
            value
        )

        for value in STRUCTURAL_ROLES

    }


    for value in values:

        if value in normalized_roles:

            return True


    # ---------------------------------------------------------
    # COMMON BOSQO PART LABELS
    #
    # We only accept exact/simple structural identifiers.
    # We intentionally do NOT use words such as "estante"
    # or "divisor", because those are custom parts.
    # ---------------------------------------------------------

    structural_names = {

        "ls",
        "rs",
        "bt",
        "tp",
        "bk",

        "leftside",
        "rightside",
        "bottom",
        "top",
        "back",

        "lateralderecho",
        "lateralizquierdo",
        "base",
        "tapa",
        "trasera"

    }


    for value in values:

        compact = (
            value
            .replace(
                " ",
                ""
            )
            .replace(
                "_",
                ""
            )
            .replace(
                "-",
                ""
            )
        )

        if compact in structural_names:

            return True


    return False


# =============================================================
# VIEW PROVIDER
# =============================================================

class ViewProviderBosqoImportedModule:

    def __init__(
        self,
        view_object
    ):

        self.Object = (
            view_object.Object
        )

        view_object.Proxy = self

        try:

            view_object.Selectable = True

        except Exception:

            pass


    # =========================================================
    # CHILDREN
    # =========================================================

    def claimChildren(
        self
    ):

        try:

            return list(
                getattr(
                    self.Object,
                    "Group",
                    []
                )
            )

        except Exception:

            return []


    # =========================================================
    # ICON
    # =========================================================

    def getIcon(
        self
    ):

        return os.path.join(
            ICONS_DIR,
            "module.svg"
        )


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
# BOSQO IMPORTED MODULE
# =============================================================

class BosqoImportedModule:

    def __init__(
        self,
        obj
    ):

        # -----------------------------------------------------
        # INTERNAL TYPE
        # -----------------------------------------------------

        self.ObjectType = (
            "BosqoImportedModule"
        )

        self._applying_module_placement = False

        # -----------------------------------------------------
        # PROXY
        # -----------------------------------------------------

        obj.Proxy = self

        # -----------------------------------------------------
        # PROPERTIES
        # -----------------------------------------------------

        self.initProperties(
            obj
        )

        # -----------------------------------------------------
        # VIEW PROVIDER
        # -----------------------------------------------------

        try:

            if (
                getattr(
                    obj,
                    "ViewObject",
                    None
                )
                is not None
            ):

                ViewProviderBosqoImportedModule(
                    obj.ViewObject
                )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando ViewProvider "
                "del módulo importado: "
                +
                str(error)
                +
                "\n"
            )


    # =========================================================
    # PROPERTIES
    # =========================================================

    def initProperties(
        self,
        obj
    ):

        # =====================================================
        # MODULE NAME
        # =====================================================

        self.addString(
            obj,
            "ModuleName",
            "Módulo",
            "Nombre del módulo",
            "Nuevo módulo"
        )


        # =====================================================
        # DIMENSIONS
        #
        # Same public interface as BosqoModule.
        # =====================================================

        self.addLength(
            obj,
            "Width",
            "Dimensiones",
            "Ancho",
            600
        )

        self.addLength(
            obj,
            "Height",
            "Dimensiones",
            "Alto",
            720
        )

        self.addLength(
            obj,
            "Depth",
            "Dimensiones",
            "Profundidad",
            560
        )


        # =====================================================
        # THICKNESSES
        # =====================================================

        self.addLength(
            obj,
            "PanelThickness",
            "Espesores",
            "Espesor panel",
            19
        )

        self.addLength(
            obj,
            "BackThickness",
            "Espesores",
            "Espesor fondo",
            10
        )


        # =====================================================
        # BACK INSET
        # =====================================================

        self.addLength(
            obj,
            "BackInset",
            "Fondo",
            "Retranqueo fondo",
            0
        )


        # =====================================================
        # MODULE PLACEMENT
        # =====================================================

        self.addPlacement(
            obj
        )


        # =====================================================
        # LAST APPLIED PLACEMENT
        # =====================================================

        self.addString(
            obj,
            "AppliedModulePlacement",
            "Interno",
            "Última posición aplicada",
            ""
        )

        try:

            obj.setEditorMode(
                "AppliedModulePlacement",
                2
            )

        except Exception:

            pass


        # =====================================================
        # TOP TYPE
        # =====================================================

        self.addEnumeration(
            obj,
            "TopType",
            "Estructura",
            "Tipo de tapa",
            [
                "Tapa completa",
                "2 travesaños",
                "3 travesaños"
            ],
            "Tapa completa"
        )


        # =====================================================
        # BACK TYPE
        # =====================================================

        self.addEnumeration(
            obj,
            "BackType",
            "Estructura",
            "Tipo de trasera",
            [
                "Trasera sobrepuesta",
                "Trasera oculta",
                "2 travesaños",
                "3 travesaños",
                "Sin trasera"
            ],
            "Trasera sobrepuesta"
        )


        # =====================================================
        # USER PARTS
        #
        # IMPORTANT:
        #
        # This JSON contains ONLY loose/custom parts.
        #
        # Structural parts already exist as children and
        # must NEVER be duplicated from this list.
        # =====================================================

        self.addString(
            obj,
            "PartsJSON",
            "Interno",
            "Piezas personalizadas",
            "[]"
        )

        try:

            obj.setEditorMode(
                "PartsJSON",
                2
            )

        except Exception:

            pass


        # =====================================================
        # STRUCTURAL PLACEMENTS
        # =====================================================

        self.addString(
            obj,
            "StructuralPlacementsJSON",
            "Interno",
            "Posiciones manuales de estructura",
            "{}"
        )

        try:

            obj.setEditorMode(
                "StructuralPlacementsJSON",
                2
            )

        except Exception:

            pass


        # =====================================================
        # INITIAL LABEL
        # =====================================================

        try:

            if not str(
                getattr(
                    obj,
                    "Label",
                    ""
                )
            ).strip():

                obj.Label = (
                    "Nuevo módulo"
                )

        except Exception:

            pass


    # =========================================================
    # ADD STRING
    # =========================================================

    def addString(
        self,
        obj,
        name,
        group,
        label,
        value
    ):

        if hasattr(
            obj,
            name
        ):

            return

        obj.addProperty(
            "App::PropertyString",
            name,
            group,
            label
        )

        setattr(
            obj,
            name,
            str(value)
        )


    # =========================================================
    # ADD LENGTH
    # =========================================================

    def addLength(
        self,
        obj,
        name,
        group,
        label,
        value
    ):

        if hasattr(
            obj,
            name
        ):

            return

        obj.addProperty(
            "App::PropertyLength",
            name,
            group,
            label
        )

        try:

            setattr(
                obj,
                name,
                float(value)
            )

        except Exception:

            try:

                setattr(
                    obj,
                    name,
                    FreeCAD.Units.Quantity(
                        str(value)
                        +
                        " mm"
                    )
                )

            except Exception:

                setattr(
                    obj,
                    name,
                    0.0
                )


    # =========================================================
    # ADD PLACEMENT
    # =========================================================

    def addPlacement(
        self,
        obj
    ):

        if hasattr(
            obj,
            "Placement"
        ):

            return

        try:

            obj.addProperty(
                "App::PropertyPlacement",
                "Placement",
                "Posición",
                "Posición y orientación del módulo"
            )

            obj.Placement = (
                FreeCAD.Placement()
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando Placement "
                "del módulo importado: "
                +
                str(error)
                +
                "\n"
            )


    # =========================================================
    # ADD ENUMERATION
    # =========================================================

    def addEnumeration(
        self,
        obj,
        name,
        group,
        label,
        values,
        default
    ):

        if hasattr(
            obj,
            name
        ):

            return

        obj.addProperty(
            "App::PropertyEnumeration",
            name,
            group,
            label
        )

        setattr(
            obj,
            name,
            values
        )

        try:

            setattr(
                obj,
                name,
                default
            )

        except Exception:

            pass


    # =========================================================
    # GET PARTS
    # =========================================================

    def getParts(
        self,
        obj
    ):

        parts = []

        try:

            for child in getattr(
                obj,
                "Group",
                []
            ):

                if child is None:

                    continue

                if child is obj:

                    continue

                parts.append(
                    child
                )

        except Exception:

            pass

        return parts


    # =========================================================
    # GET STRUCTURAL PARTS
    # =========================================================

    def getStructuralParts(
        self,
        obj
    ):

        structural = []

        for part in self.getParts(
            obj
        ):

            try:

                if is_structural_part(
                    part
                ):

                    structural.append(
                        part
                    )

            except Exception:

                pass

        return structural


    # =========================================================
    # GET LOOSE PARTS
    # =========================================================

    def getLooseParts(
        self,
        obj
    ):

        loose = []

        for part in self.getParts(
            obj
        ):

            try:

                if not is_structural_part(
                    part
                ):

                    loose.append(
                        part
                    )

            except Exception:

                loose.append(
                    part
                )

        return loose


    # =========================================================
    # PART DICTIONARY
    # =========================================================

    def partToDictionary(
        self,
        part
    ):

        if part is None:

            return None

        try:

            objectName = str(
                getattr(
                    part,
                    "Name",
                    ""
                )
            )

            label = str(
                getattr(
                    part,
                    "Label",
                    objectName
                )
            )

            role = ""

            try:

                role = str(
                    getattr(
                        part,
                        "Role",
                        ""
                    )
                )

            except Exception:

                pass


            partType = ""

            try:

                if hasattr(
                    part,
                    "PartType"
                ):

                    partType = str(
                        part.PartType
                    )

                elif hasattr(
                    part,
                    "Type"
                ):

                    partType = str(
                        part.Type
                    )

            except Exception:

                pass


            code = ""

            try:

                code = str(
                    getattr(
                        part,
                        "Code",
                        ""
                    )
                )

            except Exception:

                pass


            length = 0.0
            width = 0.0
            thickness = 0.0
            quantity = 1
            materialCode = ""


            # -------------------------------------------------
            # LENGTH
            # -------------------------------------------------

            try:

                if hasattr(
                    part,
                    "Length"
                ):

                    value = part.Length

                    if hasattr(
                        value,
                        "Value"
                    ):

                        length = float(
                            value.Value
                        )

                    else:

                        length = float(
                            value
                        )

            except Exception:

                pass


            # -------------------------------------------------
            # WIDTH
            # -------------------------------------------------

            try:

                if hasattr(
                    part,
                    "Width"
                ):

                    value = part.Width

                    if hasattr(
                        value,
                        "Value"
                    ):

                        width = float(
                            value.Value
                        )

                    else:

                        width = float(
                            value
                        )

            except Exception:

                pass


            # -------------------------------------------------
            # THICKNESS
            # -------------------------------------------------

            try:

                if hasattr(
                    part,
                    "Thickness"
                ):

                    value = part.Thickness

                    if hasattr(
                        value,
                        "Value"
                    ):

                        thickness = float(
                            value.Value
                        )

                    else:

                        thickness = float(
                            value
                        )

            except Exception:

                pass


            # -------------------------------------------------
            # QUANTITY
            # -------------------------------------------------

            try:

                if hasattr(
                    part,
                    "Quantity"
                ):

                    quantity = int(
                        part.Quantity
                    )

            except Exception:

                pass


            # -------------------------------------------------
            # MATERIAL
            # -------------------------------------------------

            try:

                if hasattr(
                    part,
                    "MaterialCode"
                ):

                    materialCode = str(
                        part.MaterialCode
                    )

                elif hasattr(
                    part,
                    "MaterialName"
                ):

                    materialCode = str(
                        part.MaterialName
                    )

            except Exception:

                pass


            return {

                "ObjectName":
                    objectName,

                "Label":
                    label,

                "Name":
                    label,

                "Code":
                    code,

                "Role":
                    role,

                "PartType":
                    partType,

                "Length":
                    length,

                "Width":
                    width,

                "Thickness":
                    thickness,

                "Quantity":
                    quantity,

                "MaterialCode":
                    materialCode

            }

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "No se pudo obtener información "
                "de la pieza: "
                +
                str(error)
                +
                "\n"
            )

            return None


    # =========================================================
    # GET USER PARTS
    #
    # IMPORTANT:
    #
    # Structural entries are filtered out even if an old
    # PartsJSON still contains them.
    # =========================================================

    def getUserParts(
        self,
        obj
    ):

        result = []

        try:

            raw = str(
                getattr(
                    obj,
                    "PartsJSON",
                    "[]"
                )
            )

            data = json.loads(
                raw
            )

            if not isinstance(
                data,
                list
            ):

                return []


            for item in data:

                if not isinstance(
                    item,
                    dict
                ):

                    continue


                # -------------------------------------------------
                # CHECK IF JSON ENTRY REPRESENTS STRUCTURAL PART
                # -------------------------------------------------

                structural = False


                for key in (
                    "Code",
                    "Role",
                    "PartType",
                    "Name",
                    "Label",
                    "ObjectName"
                ):

                    try:

                        value = _normalize_part_text(
                            item.get(
                                key,
                                ""
                            )
                        )

                        if (
                            value.upper()
                            in STRUCTURAL_CODES
                        ):

                            structural = True

                            break


                        compact = (
                            value
                            .replace(
                                " ",
                                ""
                            )
                            .replace(
                                "_",
                                ""
                            )
                            .replace(
                                "-",
                                ""
                            )
                        )


                        if compact in {

                            "ls",
                            "rs",
                            "bt",
                            "tp",
                            "bk",

                            "leftside",
                            "rightside",
                            "bottom",
                            "top",
                            "back",

                            "base",
                            "tapa",
                            "trasera",
                            "lateralizquierdo",
                            "lateralderecho"

                        }:

                            structural = True

                            break

                    except Exception:

                        pass


                if structural:

                    continue


                result.append(
                    dict(item)
                )


        except Exception:

            pass


        return result


    # =========================================================
    # SET USER PARTS
    # =========================================================

    def setUserParts(
        self,
        obj,
        parts
    ):

        if parts is None:

            parts = []


        # -----------------------------------------------------
        # NEVER STORE STRUCTURAL PARTS
        # -----------------------------------------------------

        filteredParts = []


        for item in parts:

            if not isinstance(
                item,
                dict
            ):

                continue


            structural = False


            for key in (
                "Code",
                "Role",
                "PartType",
                "Name",
                "Label",
                "ObjectName"
            ):

                try:

                    value = _normalize_part_text(
                        item.get(
                            key,
                            ""
                        )
                    )

                    compact = (
                        value
                        .replace(
                            " ",
                            ""
                        )
                        .replace(
                            "_",
                            ""
                        )
                        .replace(
                            "-",
                            ""
                        )
                    )


                    if (
                        value.upper()
                        in STRUCTURAL_CODES
                        or
                        compact in {

                            "ls",
                            "rs",
                            "bt",
                            "tp",
                            "bk",

                            "leftside",
                            "rightside",
                            "bottom",
                            "top",
                            "back",

                            "base",
                            "tapa",
                            "trasera",
                            "lateralizquierdo",
                            "lateralderecho"

                        }
                    ):

                        structural = True

                        break

                except Exception:

                    pass


            if not structural:

                filteredParts.append(
                    dict(item)
                )


        try:

            obj.PartsJSON = json.dumps(
                filteredParts,
                ensure_ascii=False
            )

            obj.touch()

            return True

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error guardando piezas "
                "del módulo importado: "
                +
                str(error)
                +
                "\n"
            )

            return False


    # =========================================================
    # GET STRUCTURAL PLACEMENTS
    # =========================================================

    def getStructuralPlacements(
        self,
        obj
    ):

        try:

            raw = str(
                getattr(
                    obj,
                    "StructuralPlacementsJSON",
                    "{}"
                )
            )

            data = json.loads(
                raw
            )

            if isinstance(
                data,
                dict
            ):

                return data

        except Exception:

            pass

        return {}


    # =========================================================
    # SET STRUCTURAL PLACEMENTS
    # =========================================================

    def setStructuralPlacements(
        self,
        obj,
        data
    ):

        try:

            obj.StructuralPlacementsJSON = (
                json.dumps(
                    data,
                    ensure_ascii=False
                )
            )

            obj.touch()

            return True

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error guardando posiciones "
                "estructurales del módulo importado: "
                +
                str(error)
                +
                "\n"
            )

            return False


    # =========================================================
    # DATA
    # =========================================================

    def getData(
        self,
        obj
    ):

        return {

            "ModuleName":
                str(
                    getattr(
                        obj,
                        "ModuleName",
                        ""
                    )
                ),

            "Label":
                str(
                    getattr(
                        obj,
                        "Label",
                        ""
                    )
                ),

            "Width":
                float(
                    getattr(
                        obj,
                        "Width",
                        0
                    )
                ),

            "Height":
                float(
                    getattr(
                        obj,
                        "Height",
                        0
                    )
                ),

            "Depth":
                float(
                    getattr(
                        obj,
                        "Depth",
                        0
                    )
                ),

            "PanelThickness":
                float(
                    getattr(
                        obj,
                        "PanelThickness",
                        19
                    )
                ),

            "BackThickness":
                float(
                    getattr(
                        obj,
                        "BackThickness",
                        10
                    )
                ),

            "BackInset":
                float(
                    getattr(
                        obj,
                        "BackInset",
                        0
                    )
                ),

            "TopType":
                str(
                    getattr(
                        obj,
                        "TopType",
                        "Tapa completa"
                    )
                ),

            "BackType":
                str(
                    getattr(
                        obj,
                        "BackType",
                        "Trasera sobrepuesta"
                    )
                )

        }


    # =========================================================
    # SET DATA
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
    # PARTS
    # =========================================================

    def addPart(
        self,
        obj,
        part
    ):

        if part is None:

            return


        try:

            if part not in getattr(
                obj,
                "Group",
                []
            ):

                obj.addObject(
                    part
                )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error añadiendo pieza al "
                "módulo importado: "
                +
                str(error)
                +
                "\n"
            )


    def removePart(
        self,
        obj,
        part
    ):

        try:

            if part in getattr(
                obj,
                "Group",
                []
            ):

                obj.removeObject(
                    part
                )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error eliminando pieza del "
                "módulo importado: "
                +
                str(error)
                +
                "\n"
            )


    def getPartsList(
        self,
        obj
    ):

        return self.getParts(
            obj
        )


    # =========================================================
    # MODULE DATA
    # =========================================================

    def getModuleData(
        self,
        obj
    ):

        try:

            from core.data.module_data import ModuleData

            data = ModuleData()

            return data.fromObject(
                obj
            )

        except Exception:

            return self.getData(
                obj
            )


    # =========================================================
    # PLACEMENT TO DATA
    # =========================================================

    def placementToData(
        self,
        placement
    ):

        try:

            base = placement.Base
            rotation = placement.Rotation

            return {

                "x":
                    float(
                        base.x
                    ),

                "y":
                    float(
                        base.y
                    ),

                "z":
                    float(
                        base.z
                    ),

                "qx":
                    float(
                        rotation.Q[0]
                    ),

                "qy":
                    float(
                        rotation.Q[1]
                    ),

                "qz":
                    float(
                        rotation.Q[2]
                    ),

                "qw":
                    float(
                        rotation.Q[3]
                    )

            }

        except Exception:

            return {

                "x": 0.0,
                "y": 0.0,
                "z": 0.0,

                "qx": 0.0,
                "qy": 0.0,
                "qz": 0.0,
                "qw": 1.0

            }


    # =========================================================
    # DATA TO PLACEMENT
    # =========================================================

    def dataToPlacement(
        self,
        data
    ):

        try:

            if not isinstance(
                data,
                dict
            ):

                return FreeCAD.Placement()


            x = float(
                data.get(
                    "x",
                    0
                )
            )

            y = float(
                data.get(
                    "y",
                    0
                )
            )

            z = float(
                data.get(
                    "z",
                    0
                )
            )

            qx = float(
                data.get(
                    "qx",
                    0
                )
            )

            qy = float(
                data.get(
                    "qy",
                    0
                )
            )

            qz = float(
                data.get(
                    "qz",
                    0
                )
            )

            qw = float(
                data.get(
                    "qw",
                    1
                )
            )


            rotation = FreeCAD.Rotation(
                qx,
                qy,
                qz,
                qw
            )


            return FreeCAD.Placement(
                FreeCAD.Vector(
                    x,
                    y,
                    z
                ),
                rotation
            )

        except Exception:

            return FreeCAD.Placement()


    # =========================================================
    # GET LAST APPLIED PLACEMENT
    # =========================================================

    def getLastAppliedPlacement(
        self,
        obj
    ):

        try:

            raw = str(
                getattr(
                    obj,
                    "AppliedModulePlacement",
                    ""
                )
            ).strip()


            if not raw:

                return None


            data = json.loads(
                raw
            )


            return self.dataToPlacement(
                data
            )

        except Exception:

            return None


    # =========================================================
    # SAVE LAST APPLIED PLACEMENT
    # =========================================================

    def saveLastAppliedPlacement(
        self,
        obj,
        placement
    ):

        try:

            data = self.placementToData(
                placement
            )


            obj.AppliedModulePlacement = (
                json.dumps(
                    data,
                    ensure_ascii=False
                )
            )

        except Exception:

            pass


    # =========================================================
    # APPLY MODULE PLACEMENT
    # =========================================================

    def applyModulePlacement(
        self,
        obj
    ):

        if self._applying_module_placement:

            return


        self._applying_module_placement = True


        try:

            modulePlacement = getattr(
                obj,
                "Placement",
                FreeCAD.Placement()
            )


            parts = self.getParts(
                obj
            )


            if not parts:

                self.saveLastAppliedPlacement(
                    obj,
                    modulePlacement
                )

                return


            oldPlacement = (
                self.getLastAppliedPlacement(
                    obj
                )
            )


            # -------------------------------------------------
            # FIRST APPLICATION
            # -------------------------------------------------

            if oldPlacement is None:

                for part in parts:

                    if not hasattr(
                        part,
                        "Placement"
                    ):

                        continue


                    try:

                        localPlacement = (
                            part.Placement
                        )


                        part.Placement = (
                            modulePlacement.multiply(
                                localPlacement
                            )
                        )


                        part.touch()


                    except Exception:

                        pass


            # -------------------------------------------------
            # MODULE ALREADY HAS PLACEMENT
            # -------------------------------------------------

            else:

                inverseOld = (
                    oldPlacement.inverse()
                )


                for part in parts:

                    if not hasattr(
                        part,
                        "Placement"
                    ):

                        continue


                    try:

                        currentGlobal = (
                            part.Placement
                        )


                        localPlacement = (
                            inverseOld.multiply(
                                currentGlobal
                            )
                        )


                        newGlobal = (
                            modulePlacement.multiply(
                                localPlacement
                            )
                        )


                        part.Placement = (
                            newGlobal
                        )


                        part.touch()


                    except Exception as error:

                        FreeCAD.Console.PrintError(
                            "Error moviendo pieza "
                            +
                            str(
                                getattr(
                                    part,
                                    "Name",
                                    "part"
                                )
                            )
                            +
                            ": "
                            +
                            str(error)
                            +
                            "\n"
                        )


            # -------------------------------------------------
            # SAVE CURRENT MODULE PLACEMENT
            # -------------------------------------------------

            self.saveLastAppliedPlacement(
                obj,
                modulePlacement
            )


        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error aplicando posición del "
                "módulo importado: "
                +
                str(error)
                +
                "\n"
            )


        finally:

            self._applying_module_placement = False


    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(
        self,
        obj
    ):

        return


    # =========================================================
    # ON CHANGED
    # =========================================================

    def onChanged(
        self,
        obj,
        property
    ):

        # -----------------------------------------------------
        # MODULE NAME
        # -----------------------------------------------------

        if property == "ModuleName":

            try:

                name = str(
                    obj.ModuleName
                ).strip()


                if name:

                    obj.Label = name

            except Exception:

                pass


            return


        # -----------------------------------------------------
        # MODULE PLACEMENT
        # -----------------------------------------------------

        if property == "Placement":

            self.applyModulePlacement(
                obj
            )

            return


        # -----------------------------------------------------
        # DIMENSIONS / STRUCTURE
        #
        # Informational for imported modules.
        #
        # They do not rebuild geometry.
        # -----------------------------------------------------

        if property in (

            "Width",
            "Height",
            "Depth",

            "PanelThickness",
            "BackThickness",
            "BackInset",

            "TopType",
            "BackType",

            "PartsJSON",
            "StructuralPlacementsJSON"

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
# CALCULATE REAL IMPORTED DIMENSIONS
# =============================================================

def calculate_imported_dimensions(
    parts
):

    if not parts:

        return None


    minX = None
    maxX = None

    minY = None
    maxY = None

    minZ = None
    maxZ = None


    # =========================================================
    # ANALYSE ALL PARTS
    # =========================================================

    for part in parts:

        if part is None:

            continue


        try:

            shape = getattr(
                part,
                "Shape",
                None
            )


            if shape is None:

                continue


            if shape.isNull():

                continue


            placement = getattr(
                part,
                "Placement",
                FreeCAD.Placement()
            )


            transformedShape = (
                shape.copy()
            )


            transformedShape.Placement = (
                placement
            )


            box = (
                transformedShape.BoundBox
            )


            if box is None:

                continue


            if (
                minX is None
                or
                box.XMin < minX
            ):

                minX = box.XMin


            if (
                maxX is None
                or
                box.XMax > maxX
            ):

                maxX = box.XMax


            if (
                minY is None
                or
                box.YMin < minY
            ):

                minY = box.YMin


            if (
                maxY is None
                or
                box.YMax > maxY
            ):

                maxY = box.YMax


            if (
                minZ is None
                or
                box.ZMin < minZ
            ):

                minZ = box.ZMin


            if (
                maxZ is None
                or
                box.ZMax > maxZ
            ):

                maxZ = box.ZMax


        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "No se pudo analizar la pieza "
                +
                str(
                    getattr(
                        part,
                        "Name",
                        "desconocida"
                    )
                )
                +
                ": "
                +
                str(error)
                +
                "\n"
            )


    # =========================================================
    # NO VALID GEOMETRY
    # =========================================================

    if (
        minX is None
        or
        maxX is None
        or
        minY is None
        or
        maxY is None
        or
        minZ is None
        or
        maxZ is None
    ):

        return None


    # =========================================================
    # REAL EXTERNAL DIMENSIONS
    # =========================================================

    width = max(
        0.0,
        float(
            maxX - minX
        )
    )


    depth = max(
        0.0,
        float(
            maxY - minY
        )
    )


    height = max(
        0.0,
        float(
            maxZ - minZ
        )
    )


    return {

        "Width":
            width,

        "Height":
            height,

        "Depth":
            depth

    }


# =============================================================
# CREATE IMPORTED MODULE
# =============================================================

def create_imported_module(
    document,
    parts
):

    if document is None:

        raise RuntimeError(
            "No hay documento activo."
        )


    # =========================================================
    # NORMALIZE PART LIST
    # =========================================================

    if parts is None:

        parts = []


    try:

        parts = list(
            parts
        )

    except Exception:

        parts = []


    # =========================================================
    # CREATE MODULE
    # =========================================================

    module = document.addObject(
        "App::DocumentObjectGroupPython",
        "BosqoImportedModule"
    )


    # =========================================================
    # CREATE PROXY
    # =========================================================

    BosqoImportedModule(
        module
    )


    # =========================================================
    # INITIAL MODULE NAME
    # =========================================================

    try:

        module.ModuleName = (
            "Módulo importado"
        )

        module.Label = (
            module.ModuleName
        )

    except Exception:

        pass


    # =========================================================
    # INITIAL MODULE PLACEMENT
    # =========================================================

    try:

        module.Placement = (
            FreeCAD.Placement()
        )


        module.Proxy.saveLastAppliedPlacement(
            module,
            module.Placement
        )

    except Exception:

        pass


    # =========================================================
    # ADD EXISTING PARTS
    #
    # IMPORTANT:
    #
    # Existing objects are reused.
    # Nothing is copied or recreated.
    # =========================================================

    validParts = []


    for part in parts:

        if part is None:

            continue


        try:

            if part not in getattr(
                module,
                "Group",
                []
            ):

                module.addObject(
                    part
                )


            validParts.append(
                part
            )


        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error añadiendo pieza "
                +
                str(
                    getattr(
                        part,
                        "Name",
                        "desconocida"
                    )
                )
                +
                ": "
                +
                str(error)
                +
                "\n"
            )


    # =========================================================
    # CLASSIFY PARTS
    # =========================================================

    structuralParts = []
    looseParts = []


    for part in validParts:

        try:

            if is_structural_part(
                part
            ):

                structuralParts.append(
                    part
                )

            else:

                looseParts.append(
                    part
                )

        except Exception:

            looseParts.append(
                part
            )


    # =========================================================
    # DEBUG CLASSIFICATION
    # =========================================================

    try:

        FreeCAD.Console.PrintMessage(
            "\n"
            "========================================\n"
        )

        FreeCAD.Console.PrintMessage(
            "CLASIFICACIÓN MÓDULO IMPORTADO\n"
        )

        FreeCAD.Console.PrintMessage(
            "Estructurales: "
            +
            str(
                len(
                    structuralParts
                )
            )
            +
            "\n"
        )

        for part in structuralParts:

            FreeCAD.Console.PrintMessage(
                "  [ESTRUCTURAL] "
                +
                str(
                    getattr(
                        part,
                        "Name",
                        "?"
                    )
                )
                +
                " / "
                +
                str(
                    getattr(
                        part,
                        "Label",
                        "?"
                    )
                )
                +
                "\n"
            )


        FreeCAD.Console.PrintMessage(
            "Sueltas: "
            +
            str(
                len(
                    looseParts
                )
            )
            +
            "\n"
        )

        for part in looseParts:

            FreeCAD.Console.PrintMessage(
                "  [SUELTA] "
                +
                str(
                    getattr(
                        part,
                        "Name",
                        "?"
                    )
                )
                +
                " / "
                +
                str(
                    getattr(
                        part,
                        "Label",
                        "?"
                    )
                )
                +
                "\n"
            )

        FreeCAD.Console.PrintMessage(
            "========================================\n"
        )

    except Exception:

        pass


    # =========================================================
    # INITIAL PARTS JSON
    #
    # VERY IMPORTANT:
    #
    # ONLY LOOSE PARTS GO HERE.
    #
    # Structural pieces stay as real children of the module
    # and are NOT represented in PartsJSON.
    # =========================================================

    try:

        initialParts = []


        for part in looseParts:

            data = (
                BosqoImportedModule.partToDictionary(
                    module.Proxy,
                    part
                )
            )


            if data is None:

                continue


            initialParts.append(
                data
            )


        module.Proxy.setUserParts(
            module,
            initialParts
        )


    except Exception as error:

        FreeCAD.Console.PrintWarning(
            "No se pudieron guardar los datos "
            "iniciales de las piezas sueltas: "
            +
            str(error)
            +
            "\n"
        )


    # =========================================================
    # FIRST RECOMPUTE
    # =========================================================

    try:

        document.recompute()

    except Exception:

        pass


    # =========================================================
    # CALCULATE REAL MODULE DIMENSIONS
    #
    # IMPORTANT:
    #
    # ALL REAL PARTS participate in the external dimensions,
    # including structural parts.
    #
    # The exclusion above only affects PartsJSON.
    # =========================================================

    dimensions = (
        calculate_imported_dimensions(
            validParts
        )
    )


    if dimensions is not None:

        try:

            module.Width = (
                dimensions["Width"]
            )

            module.Height = (
                dimensions["Height"]
            )

            module.Depth = (
                dimensions["Depth"]
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error asignando dimensiones "
                "reales del módulo importado: "
                +
                str(error)
                +
                "\n"
            )

    else:

        FreeCAD.Console.PrintWarning(
            "No se pudieron calcular las "
            "dimensiones reales del módulo importado.\n"
        )


    # =========================================================
    # SECOND RECOMPUTE
    # =========================================================

    try:

        document.recompute()

    except Exception:

        pass


    # =========================================================
    # FINAL DEBUG
    # =========================================================

    try:

        FreeCAD.Console.PrintMessage(
            "\n"
            "========================================\n"
        )

        FreeCAD.Console.PrintMessage(
            "MÓDULO IMPORTADO CREADO\n"
        )

        FreeCAD.Console.PrintMessage(
            "Name: "
            +
            str(
                module.Name
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "Label: "
            +
            str(
                module.Label
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "ModuleName: "
            +
            str(
                module.ModuleName
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "Width: "
            +
            "%.2f" % float(
                module.Width
            )
            +
            " mm\n"
        )

        FreeCAD.Console.PrintMessage(
            "Height: "
            +
            "%.2f" % float(
                module.Height
            )
            +
            " mm\n"
        )

        FreeCAD.Console.PrintMessage(
            "Depth: "
            +
            "%.2f" % float(
                module.Depth
            )
            +
            " mm\n"
        )

        FreeCAD.Console.PrintMessage(
            "PanelThickness: "
            +
            "%.2f" % float(
                module.PanelThickness
            )
            +
            " mm\n"
        )

        FreeCAD.Console.PrintMessage(
            "BackThickness: "
            +
            "%.2f" % float(
                module.BackThickness
            )
            +
            " mm\n"
        )

        FreeCAD.Console.PrintMessage(
            "BackInset: "
            +
            "%.2f" % float(
                module.BackInset
            )
            +
            " mm\n"
        )

        FreeCAD.Console.PrintMessage(
            "TopType: "
            +
            str(
                module.TopType
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "BackType: "
            +
            str(
                module.BackType
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "Piezas totales: "
            +
            str(
                len(
                    validParts
                )
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "Piezas estructurales: "
            +
            str(
                len(
                    structuralParts
                )
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "Piezas sueltas: "
            +
            str(
                len(
                    looseParts
                )
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "Piezas en PartsJSON: "
            +
            str(
                len(
                    module.Proxy.getUserParts(
                        module
                    )
                )
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "Piezas en Group: "
            +
            str(
                len(
                    getattr(
                        module,
                        "Group",
                        []
                    )
                )
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "========================================\n"
        )

    except Exception:

        pass


    return module