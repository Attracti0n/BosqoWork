import FreeCAD
import json


class BosqoModule:

    def __init__(self, obj):

        self.ObjectType = "BosqoModule"

        obj.Proxy = self

        self.initProperties(obj)


    # =========================================================
    # PROPERTIES
    # =========================================================

    def initProperties(self, obj):

        self.addString(
            obj,
            "ModuleName",
            "Módulo",
            "Nombre del módulo",
            "Nuevo módulo"
        )

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

        self.addLength(
            obj,
            "BackInset",
            "Fondo",
            "Retranqueo fondo",
            0
        )

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

        self.addString(
            obj,
            "PartsJSON",
            "Interno",
            "Piezas personalizadas",
            "[]"
        )

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

        if hasattr(obj, name):
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

        if hasattr(obj, name):
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

        if hasattr(obj, name):
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
                    dict(item)
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
        # DEBUG
        # -----------------------------------------------------

        try:

            FreeCAD.Console.PrintMessage(
                "\n"
                "=== BOSQO MODULE ONCHANGED ===\n"
            )

            FreeCAD.Console.PrintMessage(
                "obj.Name = "
                +
                str(
                    getattr(
                        obj,
                        "Name",
                        "SIN NAME"
                    )
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "obj.Label = "
                +
                str(
                    getattr(
                        obj,
                        "Label",
                        "SIN LABEL"
                    )
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "obj.TypeId = "
                +
                str(
                    getattr(
                        obj,
                        "TypeId",
                        "SIN TYPEID"
                    )
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "property = "
                +
                str(
                    property
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "Has Width = "
                +
                str(
                    hasattr(
                        obj,
                        "Width"
                    )
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "Has Height = "
                +
                str(
                    hasattr(
                        obj,
                        "Height"
                    )
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "Has Depth = "
                +
                str(
                    hasattr(
                        obj,
                        "Depth"
                    )
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "Has PanelThickness = "
                +
                str(
                    hasattr(
                        obj,
                        "PanelThickness"
                    )
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "Has BackThickness = "
                +
                str(
                    hasattr(
                        obj,
                        "BackThickness"
                    )
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "Has BackInset = "
                +
                str(
                    hasattr(
                        obj,
                        "BackInset"
                    )
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "Proxy = "
                +
                str(
                    type(
                        getattr(
                            obj,
                            "Proxy",
                            None
                        )
                    )
                )
                +
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "================================\n"
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error en diagnóstico onChanged: "
                +
                str(error)
                +
                "\n"
            )


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
        # RECALCULATE MODULE
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

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error recalculando módulo: "
                    +
                    str(error)
                    +
                    "\n"
                )


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