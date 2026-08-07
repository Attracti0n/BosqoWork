import FreeCAD
import json


# =============================================================
# VIEW PROVIDER
# =============================================================

class ViewProviderBosqoModule:

    def __init__(
        self,
        viewObject
    ):

        self.Object = (
            viewObject.Object
        )

        viewObject.Proxy = self

        #
        # Make the module selectable.
        #

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
# BOSQO MODULE
# =============================================================

class BosqoModule:

    def __init__(
        self,
        obj
    ):

        self.ObjectType = "BosqoModule"

        obj.Proxy = self

        self._applying_module_placement = False

        self.initProperties(
            obj
        )

        #
        # Create our own ViewProvider.
        #
        # This is important because the module is an
        # App::DocumentObjectGroupPython and must be
        # selectable by the FreeCAD GUI.
        #

        try:

            if (
                getattr(
                    obj,
                    "ViewObject",
                    None
                )
                is not None
            ):

                ViewProviderBosqoModule(
                    obj.ViewObject
                )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando ViewProvider del módulo: "
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
            "Nuevo módulo"
        )


        # -----------------------------------------------------
        # MODULE TYPE
        # -----------------------------------------------------

        self.addEnumeration(
            obj,
            "Type",
            "Módulo",
            "Tipo de módulo",
            [
                "Módulo bajo"
            ],
            "Módulo bajo"
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
        # INTERNAL / LAST APPLIED PLACEMENT
        # -----------------------------------------------------

        self.addString(
            obj,
            "AppliedModulePlacement",
            "Interno",
            "Última posición aplicada",
            ""
        )

        obj.setEditorMode(
            "AppliedModulePlacement",
            2
        )


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
        # USER PARTS
        # -----------------------------------------------------

        self.addString(
            obj,
            "PartsJSON",
            "Interno",
            "Piezas personalizadas",
            "[]"
        )


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


        obj.setEditorMode(
            "PartsJSON",
            2
        )

        obj.setEditorMode(
            "StructuralPlacementsJSON",
            2
        )


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
                "Error creando Placement del módulo: "
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
    # GET USER PARTS
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

                    dict(
                        item
                    )

                    for item in data

                    if isinstance(
                        item,
                        dict
                    )

                ]

        except Exception:

            pass

        return []


    # =========================================================
    # SET USER PARTS
    # =========================================================

    def setUserParts(
        self,
        obj,
        parts
    ):

        try:

            obj.PartsJSON = json.dumps(
                parts,
                ensure_ascii=False
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error guardando piezas personalizadas: "
                +
                str(error)
                +
                "\n"
            )


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

            obj.StructuralPlacementsJSON = json.dumps(
                data,
                ensure_ascii=False
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
    # PLACEMENT SERIALIZATION
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
    # PLACEMENT DESERIALIZATION
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
            # CASE 1: REBUILT
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
                            "Error aplicando Placement al "
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
            # CASE 2: EXISTING MODULE MOVED
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
                "Error aplicando posición del módulo: "
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
        # MODULE DIMENSIONS / STRUCTURE
        # -----------------------------------------------------

        if property in (
            "Width",
            "Height",
            "Depth",
            "PanelThickness",
            "BackThickness",
            "BackInset",
            "TopType",
            "BackType"
        ):

            try:

                from core.builders.module_builder import (
                    ModuleBuilder
                )

                ModuleBuilder.build(
                    obj
                )

                self.applyModulePlacement(
                    obj,
                    rebuilt=True
                )

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error recalculando módulo: "
                    +
                    str(error)
                    +
                    "\n"
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
# CREATE MODULE
# =============================================================

def create_module(
    document
):

    module = document.addObject(
        "App::DocumentObjectGroupPython",
        "BosqoModule"
    )

    BosqoModule(
        module
    )

    return module