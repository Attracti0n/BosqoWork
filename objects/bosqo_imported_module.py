import FreeCAD
import json


# =============================================================
# VIEW PROVIDER
# =============================================================

class ViewProviderBosqoImportedModule:

    def __init__(
        self,
        viewObject
    ):

        self.Object = viewObject.Object

        viewObject.Proxy = self

        # -----------------------------------------------------
        # Make the module selectable.
        # -----------------------------------------------------

        try:

            viewObject.Selectable = True

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

        return ""

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
        # ASSIGN PROXY
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

            if getattr(
                obj,
                "ViewObject",
                None
            ) is not None:

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

        # -----------------------------------------------------
        # MODULE NAME
        # -----------------------------------------------------

        self.addString(
            obj,
            "ModuleName",
            "Módulo",
            "Nombre del módulo",
            "Módulo importado"
        )

        # -----------------------------------------------------
        # MODULE SOURCE
        # -----------------------------------------------------

        self.addString(
            obj,
            "ModuleSource",
            "Módulo",
            "Origen del módulo",
            "Imported"
        )

        try:

            obj.setEditorMode(
                "ModuleSource",
                2
            )

        except Exception:

            pass

        # -----------------------------------------------------
        # MODULE TYPE
        # -----------------------------------------------------

        self.addEnumeration(
            obj,
            "Type",
            "Módulo",
            "Tipo de módulo",
            [
                "Módulo importado"
            ],
            "Módulo importado"
        )

        # -----------------------------------------------------
        # DIMENSIONS
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # THICKNESSES
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # BACK INSET
        # -----------------------------------------------------

        self.addLength(
            obj,
            "BackInset",
            "Fondo",
            "Retranqueo fondo",
            0
        )

        # -----------------------------------------------------
        # MODULE PLACEMENT
        # -----------------------------------------------------

        self.addPlacement(
            obj
        )

        # -----------------------------------------------------
        # LAST APPLIED MODULE PLACEMENT
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # TOP TYPE
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # BACK TYPE
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # PARTS DATA
        #
        # This contains the information edited in ModuleDialog:
        #
        # ObjectName
        # Name
        # Type
        # Length
        # Width
        # Thickness
        # Quantity
        # Material
        #
        # -----------------------------------------------------

        self.addString(
            obj,
            "PartsJSON",
            "Interno",
            "Datos de las piezas",
            "[]"
        )

        try:

            obj.setEditorMode(
                "PartsJSON",
                2
            )

        except Exception:

            pass

        # -----------------------------------------------------
        # STRUCTURAL PLACEMENTS
        # -----------------------------------------------------

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
            value
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

        setattr(
            obj,
            name,
            value
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

        for child in getattr(
            obj,
            "Group",
            []
        ):

            if child is obj:

                continue

            parts.append(
                child
            )

        return parts

    # =========================================================
    # GET USER PARTS / SAVED PART DATA
    # =========================================================

    def getUserParts(
        self,
        obj
    ):

        try:

            data = json.loads(
                getattr(
                    obj,
                    "PartsJSON",
                    "[]"
                )
            )

            if isinstance(
                data,
                list
            ):

                return [

                    dict(item)

                    for item in data

                    if isinstance(
                        item,
                        dict
                    )

                ]

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "Error leyendo PartsJSON: "
                +
                str(error)
                +
                "\n"
            )

        return []

    # =========================================================
    # SET USER PARTS / SAVE MODULE DIALOG DATA
    # =========================================================

    def setUserParts(
        self,
        obj,
        parts
    ):

        if parts is None:

            parts = []

        try:

            data = []

            for item in parts:

                if not isinstance(
                    item,
                    dict
                ):

                    continue

                data.append(
                    dict(
                        item
                    )
                )

            obj.PartsJSON = json.dumps(
                data,
                ensure_ascii=False
            )

            obj.touch()

            return True

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error guardando piezas del módulo: "
                +
                str(error)
                +
                "\n"
            )

            return False

    # =========================================================
    # SAVE MODULE DIALOG DATA
    # =========================================================
    #
    # This is the method that ModuleDialog uses indirectly.
    #
    # It stores:
    #
    # Type
    # Material
    # Quantity
    # Dimensions
    # Name
    # ObjectName
    #
    # ---------------------------------------------------------

    def saveModuleDialogData(
        self,
        obj,
        data
    ):

        if not isinstance(
            data,
            dict
        ):

            return False

        try:

            # -------------------------------------------------
            # MODULE NAME
            # -------------------------------------------------

            label = str(
                data.get(
                    "Label",
                    ""
                )
            ).strip()

            if label:

                obj.ModuleName = label
                obj.Label = label

            # -------------------------------------------------
            # PARTS
            # -------------------------------------------------

            parts = data.get(
                "Parts",
                []
            )

            if not isinstance(
                parts,
                list
            ):

                parts = []

            return self.setUserParts(
                obj,
                parts
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error guardando datos de ModuleDialog: "
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

            data = json.loads(
                getattr(
                    obj,
                    "StructuralPlacementsJSON",
                    "{}"
                )
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

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error guardando posiciones estructurales: "
                +
                str(error)
                +
                "\n"
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

                "x": float(base.x),
                "y": float(base.y),
                "z": float(base.z),

                "qx": float(rotation.Q[0]),
                "qy": float(rotation.Q[1]),
                "qz": float(rotation.Q[2]),
                "qw": float(rotation.Q[3])

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
                    data
                )
            )

        except Exception:

            pass

    # =========================================================
    # APPLY MODULE PLACEMENT
    # =========================================================

    def applyModulePlacement(
        self,
        obj,
        rebuilt=False
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

            # -------------------------------------------------
            # FIRST APPLICATION / REBUILT
            # -------------------------------------------------

            if rebuilt:

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

                    except Exception as error:

                        FreeCAD.Console.PrintError(
                            "Error aplicando Placement "
                            "al objeto "
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
            # EXISTING MODULE MOVED
            # -------------------------------------------------

            else:

                oldPlacement = (
                    self.getLastAppliedPlacement(
                        obj
                    )
                )

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
                "Error aplicando posición "
                "del módulo importado: "
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

        # Imported modules NEVER rebuild geometry.

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

        # -----------------------------------------------------
        # MODULE PLACEMENT
        # -----------------------------------------------------

        if property == "Placement":

            self.applyModulePlacement(
                obj,
                rebuilt=False
            )

            return

        # -----------------------------------------------------
        # INFORMATIONAL PROPERTIES
        # -----------------------------------------------------

        if property in (

            "ModuleSource",
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

    if parts is None:

        parts = []

    try:

        parts = list(
            parts
        )

    except Exception:

        parts = []

    # ---------------------------------------------------------
    # CREATE GROUP
    # ---------------------------------------------------------

    module = document.addObject(
        "App::DocumentObjectGroupPython",
        "BosqoImportedModule"
    )

    # ---------------------------------------------------------
    # CREATE PROXY
    # ---------------------------------------------------------

    BosqoImportedModule(
        module
    )

    # ---------------------------------------------------------
    # ADD REAL OBJECTS TO GROUP
    # ---------------------------------------------------------

    validParts = []

    for part in parts:

        if part is None:

            continue

        try:

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

    # ---------------------------------------------------------
    # INITIAL NAME
    # ---------------------------------------------------------

    try:

        module.ModuleName = (
            "Módulo importado"
        )

        module.Label = (
            module.ModuleName
        )

    except Exception:

        pass

    # ---------------------------------------------------------
    # INITIAL MODULE SOURCE
    # ---------------------------------------------------------

    try:

        module.ModuleSource = (
            "Imported"
        )

    except Exception:

        pass

    # ---------------------------------------------------------
    # INITIAL PLACEMENT
    #
    # The selected pieces already have their correct
    # global placements.
    #
    # Therefore we DO NOT apply module placement here.
    # ---------------------------------------------------------

    try:

        proxy = module.Proxy

        proxy.saveLastAppliedPlacement(
            module,
            module.Placement
        )

    except Exception:

        pass

    # ---------------------------------------------------------
    # INITIAL PART DATA
    #
    # Save the selected objects immediately so that
    # ModuleDialog has persistent data to work with.
    # ---------------------------------------------------------

    try:

        initialParts = []

        for part in validParts:

            if part is None:

                continue

            objectName = str(
                getattr(
                    part,
                    "Name",
                    ""
                )
            )

            displayName = str(
                getattr(
                    part,
                    "Label",
                    objectName
                )
            )

            initialParts.append(
                {

                    "ObjectName":
                        objectName,

                    "Name":
                        displayName,

                    "Type":
                        "Personalizado",

                    "Length":
                        "",

                    "Width":
                        "",

                    "Thickness":
                        "",

                    "Quantity":
                        "1",

                    "Material":
                        ""

                }
            )

        proxy.setUserParts(
            module,
            initialParts
        )

    except Exception as error:

        FreeCAD.Console.PrintWarning(
            "No se pudieron guardar los datos "
            "iniciales de las piezas: "
            +
            str(error)
            +
            "\n"
        )

    # ---------------------------------------------------------
    # RECOMPUTE
    # ---------------------------------------------------------

    try:

        document.recompute()

    except Exception:

        pass

    return module