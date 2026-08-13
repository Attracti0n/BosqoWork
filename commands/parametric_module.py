import FreeCAD
import FreeCADGui
import os

from PySide import QtWidgets

from app_paths import ICONS_DIR

from objects.bosqo_module import create_module

from dialogs.parametric_module_dialog import (
    ParametricModuleDialog
)


class ParametricModuleCommand:

    def GetResources(
        self
    ):

        return {

            "Pixmap":
                os.path.join(
                    ICONS_DIR,
                    "module.svg"
                ),

            "MenuText":
                "Módulo paramétrico",

            "ToolTip":
                "Crear módulo paramétrico",

            "Accel":
                ""
        }


    def IsActive(
        self
    ):

        return (
            FreeCAD.ActiveDocument
            is not None
        )


    # =========================================================
    # DELETE OBJECT TREE
    # =========================================================

    def deleteObjectTree(
        self,
        obj
    ):

        if obj is None:
            return

        document = getattr(
            obj,
            "Document",
            None
        )

        if document is None:
            return

        #
        # First delete children.
        #

        children = list(
            getattr(
                obj,
                "Group",
                []
            )
        )

        for child in children:

            self.deleteObjectTree(
                child
            )

        #
        # Then delete the object itself.
        #

        try:

            document.removeObject(
                obj.Name
            )

        except Exception:

            pass


    # =========================================================
    # ACTIVATED
    # =========================================================

    def Activated(
        self
    ):

        document = (
            FreeCAD.ActiveDocument
        )

        if document is None:

            FreeCAD.Console.PrintError(
                "No hay ningún documento activo.\n"
            )

            return


        # =====================================================
        # CREATE INITIAL PARAMETRIC MODULE
        # =====================================================

        #
        # IMPORTANT:
        #
        # The dialog requires an existing module because
        # calculateParts() works with self.module.
        #
        # create_module() is the central creation function.
        #
        # It creates:
        #
        #   BosqoModule
        #   BosqoPart objects
        #   ModuleParameters Spreadsheet
        #   ParameterSheet link
        #
        # This replaces the old direct:
        #
        #   document.addObject(...)
        #   BosqoModule(module)
        #
        # =====================================================

        data = {

            "Label":
                "Nuevo módulo",

            "Width":
                600,

            "Height":
                720,

            "Depth":
                560,

            "PanelThickness":
                19,

            "BackThickness":
                10,

            "BackInset":
                0,

            "TopType":
                "Tapa completa",

            "BackType":
                "Trasera sobrepuesta",

            "Parts":
                [],

            "StructuralPlacements":
                {}

        }


        try:

            module = create_module(
                document,
                data
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando el módulo paramétrico: "
                +
                str(error)
                +
                "\n"
            )

            raise


        # =====================================================
        # VERIFY / UPDATE DOCUMENT
        # =====================================================

        try:

            document.recompute()

        except Exception:

            pass


        # =====================================================
        # OPEN PARAMETRIC MODULE DIALOG
        # =====================================================

        try:

            dialog = ParametricModuleDialog(
                module
            )

            result = dialog.exec_()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error abriendo el diálogo de módulo "
                "paramétrico: "
                +
                str(error)
                +
                "\n"
            )

            #
            # Remove complete temporary module tree.
            #

            self.deleteObjectTree(
                module
            )

            try:

                document.recompute()

            except Exception:

                pass

            raise


        # =====================================================
        # CANCEL
        # =====================================================

        if (
            result
            !=
            QtWidgets.QDialog.Accepted
        ):

            #
            # IMPORTANT:
            #
            # create_module() already created:
            #
            #   BosqoModule
            #   BosqoParts
            #   ModuleParameters
            #
            # Therefore cancel must remove the complete tree.
            #

            self.deleteObjectTree(
                module
            )

            try:

                document.recompute()

            except Exception:

                pass

            return


        # =====================================================
        # ACCEPT
        # =====================================================

        try:

            document.recompute()

        except Exception:

            pass


        # =====================================================
        # FIT VIEW
        # =====================================================

        try:

            FreeCADGui.activeDocument() \
                .activeView() \
                .fitAll()

        except Exception:

            pass


# =============================================================
# REGISTER COMMAND
# =============================================================

FreeCADGui.addCommand(
    "Bosqo_ParametricModule",
    ParametricModuleCommand()
)