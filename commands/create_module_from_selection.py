import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from dialogs.module_dialog import ModuleDialog
from objects.bosqo_imported_module import create_imported_module


class CreateModuleFromSelectionCommand:

    # =========================================================
    # RESOURCES
    # =========================================================

    def GetResources(self):

        return {
            "Pixmap": os.path.join(
                ICONS_DIR,
                "select_to_group.svg"
            ),

            "MenuText":
                "Crear módulo desde selección",

            "ToolTip":
                "Crear un módulo Bosqo con las piezas seleccionadas"
        }

    # =========================================================
    # ACTIVATED
    # =========================================================

    def Activated(self):

        # -----------------------------------------------------
        # GET SELECTION
        # -----------------------------------------------------

        selection = self.getSelectedParts()

        if not selection:

            FreeCAD.Console.PrintError(
                "Seleccione una o más BosqoPart.\n"
            )

            return

        # -----------------------------------------------------
        # DOCUMENT
        # -----------------------------------------------------

        doc = selection[0].Document

        # -----------------------------------------------------
        # GLOBAL BOUNDING BOX
        # -----------------------------------------------------

        bbox = self.getGlobalBoundingBox(
            selection
        )

        if bbox is None:

            FreeCAD.Console.PrintError(
                "No se pudo calcular el volumen "
                "de las piezas seleccionadas.\n"
            )

            return

        # -----------------------------------------------------
        # DEFAULT MODULE DATA
        # -----------------------------------------------------

        data = {

            "Label":
                "Nuevo módulo",

            "Width":
                bbox.XLength,

            "Height":
                bbox.ZLength,

            "Depth":
                bbox.YLength
        }

        # -----------------------------------------------------
        # DIALOG
        # -----------------------------------------------------

        dialog = ModuleDialog(
            data=data,
            parts=selection
        )

        if not dialog.exec():

            return

        # -----------------------------------------------------
        # GET DATA FROM DIALOG
        # -----------------------------------------------------

        data = dialog.getData()

        label = data.get(
            "Label",
            "Nuevo módulo"
        )

        # -----------------------------------------------------
        # CREATE IMPORTED MODULE
        # -----------------------------------------------------
        #
        # create_imported_module() already adds the selected
        # objects to the module Group.
        #
        # THEREFORE WE DO NOT CALL:
        #
        # module.Proxy.setParts(...)
        #
        # -----------------------------------------------------

        try:

            module = create_imported_module(
                doc,
                selection
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando el módulo importado: "
                + str(error)
                + "\n"
            )

            return

        # =====================================================
        # MODULE PROPERTIES
        # =====================================================

        try:

            # -------------------------------------------------
            # MODULE NAME
            # -------------------------------------------------

            if not hasattr(
                module,
                "ModuleName"
            ):

                module.addProperty(
                    "App::PropertyString",
                    "ModuleName",
                    "Módulo",
                    "Nombre del módulo"
                )

            module.ModuleName = label

            # -------------------------------------------------
            # WIDTH
            # -------------------------------------------------

            if not hasattr(
                module,
                "Width"
            ):

                module.addProperty(
                    "App::PropertyLength",
                    "Width",
                    "Dimensiones",
                    "Anchura del módulo"
                )

            module.Width = float(
                data.get(
                    "Width",
                    bbox.XLength
                )
            )

            # -------------------------------------------------
            # HEIGHT
            # -------------------------------------------------

            if not hasattr(
                module,
                "Height"
            ):

                module.addProperty(
                    "App::PropertyLength",
                    "Height",
                    "Dimensiones",
                    "Altura del módulo"
                )

            module.Height = float(
                data.get(
                    "Height",
                    bbox.ZLength
                )
            )

            # -------------------------------------------------
            # DEPTH
            # -------------------------------------------------

            if not hasattr(
                module,
                "Depth"
            ):

                module.addProperty(
                    "App::PropertyLength",
                    "Depth",
                    "Dimensiones",
                    "Profundidad del módulo"
                )

            module.Depth = float(
                data.get(
                    "Depth",
                    bbox.YLength
                )
            )

            # -------------------------------------------------
            # LABEL
            # -------------------------------------------------

            module.Label = label

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error configurando el módulo importado: "
                + str(error)
                + "\n"
            )

            try:

                doc.removeObject(
                    module.Name
                )

            except Exception:

                pass

            return

        # =====================================================
        # RECOMPUTE
        # =====================================================

        try:

            doc.recompute()

        except Exception:

            pass

        # =====================================================
        # VISIBILITY
        # =====================================================

        try:

            module.ViewObject.Visibility = True

        except Exception:

            pass

        # -----------------------------------------------------
        # ORIGINAL PARTS
        # -----------------------------------------------------

        for part in selection:

            try:

                part.ViewObject.Visibility = True

            except Exception:

                pass

        # =====================================================
        # GUI REDRAW
        # =====================================================

        try:

            FreeCADGui.activeDocument().activeView().redraw()

        except Exception:

            pass

        # =====================================================
        # DEBUG
        # =====================================================

        FreeCAD.Console.PrintMessage(
            "\n"
            "========================================\n"
            " IMPORTED MODULE CREATED\n"
            "========================================\n"
        )

        FreeCAD.Console.PrintMessage(
            "Module: "
            + str(module.Label)
            + "\n"
        )

        try:

            FreeCAD.Console.PrintMessage(
                "Width:  "
                + str(module.Width)
                + "\n"
            )

            FreeCAD.Console.PrintMessage(
                "Height: "
                + str(module.Height)
                + "\n"
            )

            FreeCAD.Console.PrintMessage(
                "Depth:  "
                + str(module.Depth)
                + "\n"
            )

        except Exception:

            pass

        FreeCAD.Console.PrintMessage(
            "\n--- ORIGINAL PARTS ---\n"
        )

        for part in selection:

            try:

                FreeCAD.Console.PrintMessage(
                    "\n"
                    + str(part.Label)
                    + "\n"
                )

                FreeCAD.Console.PrintMessage(
                    "Object = "
                    + str(part.Name)
                    + "\n"
                )

                FreeCAD.Console.PrintMessage(
                    "Placement = "
                    + str(part.Placement)
                    + "\n"
                )

                FreeCAD.Console.PrintMessage(
                    "Base = "
                    + str(part.Placement.Base)
                    + "\n"
                )

                FreeCAD.Console.PrintMessage(
                    "Rotation = "
                    + str(part.Placement.Rotation)
                    + "\n"
                )

            except Exception:

                pass

        FreeCAD.Console.PrintMessage(
            "\n"
            "========================================\n"
            + str(len(selection))
            + " piezas asociadas al módulo.\n"
            "========================================\n"
        )

    # =========================================================
    # GLOBAL BOUNDING BOX
    # =========================================================

    def getGlobalBoundingBox(
        self,
        parts
    ):

        result = None

        for part in parts:

            try:

                shape = part.Shape

                if shape is None:
                    continue

                if shape.isNull():
                    continue

                local_bbox = shape.BoundBox

                # -------------------------------------------------
                # LOCAL CORNERS
                # -------------------------------------------------

                corners = [

                    FreeCAD.Vector(
                        local_bbox.XMin,
                        local_bbox.YMin,
                        local_bbox.ZMin
                    ),

                    FreeCAD.Vector(
                        local_bbox.XMin,
                        local_bbox.YMin,
                        local_bbox.ZMax
                    ),

                    FreeCAD.Vector(
                        local_bbox.XMin,
                        local_bbox.YMax,
                        local_bbox.ZMin
                    ),

                    FreeCAD.Vector(
                        local_bbox.XMin,
                        local_bbox.YMax,
                        local_bbox.ZMax
                    ),

                    FreeCAD.Vector(
                        local_bbox.XMax,
                        local_bbox.YMin,
                        local_bbox.ZMin
                    ),

                    FreeCAD.Vector(
                        local_bbox.XMax,
                        local_bbox.YMin,
                        local_bbox.ZMax
                    ),

                    FreeCAD.Vector(
                        local_bbox.XMax,
                        local_bbox.YMax,
                        local_bbox.ZMin
                    ),

                    FreeCAD.Vector(
                        local_bbox.XMax,
                        local_bbox.YMax,
                        local_bbox.ZMax
                    )
                ]

                # -------------------------------------------------
                # APPLY PLACEMENT
                # -------------------------------------------------

                placement = part.Placement

                for point in corners:

                    global_point = placement.multVec(
                        point
                    )

                    if result is None:

                        result = FreeCAD.BoundBox()

                    result.add(
                        global_point
                    )

            except Exception as error:

                FreeCAD.Console.PrintWarning(
                    "No se pudo calcular el BoundingBox "
                    "global de "
                    + str(
                        getattr(
                            part,
                            "Label",
                            "pieza"
                        )
                    )
                    + ": "
                    + str(error)
                    + "\n"
                )

        return result

    # =========================================================
    # SELECTED PARTS
    # =========================================================

    def getSelectedParts(
        self
    ):

        result = []

        for obj in FreeCADGui.Selection.getSelection():

            if not hasattr(
                obj,
                "Proxy"
            ):

                continue

            if obj.Proxy is None:

                continue

            if type(
                obj.Proxy
            ).__name__ != "BosqoPart":

                continue

            result.append(
                obj
            )

        return result

    # =========================================================
    # IS ACTIVE
    # =========================================================

    def IsActive(
        self
    ):

        return (
            FreeCAD.ActiveDocument is not None
        )


# =============================================================
# REGISTER COMMAND
# =============================================================

FreeCADGui.addCommand(
    "Bosqo_CreateModuleFromSelection",
    CreateModuleFromSelectionCommand()
)