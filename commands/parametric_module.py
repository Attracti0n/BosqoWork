import FreeCAD
import FreeCADGui
import os

from PySide import QtWidgets

from app_paths import ICONS_DIR

from objects.bosqo_module import BosqoModule
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
            return


        #
        # Create temporary module group.
        #

        module = document.addObject(
            "App::DocumentObjectGroupPython",
            "BosqoModule"
        )

        BosqoModule(
            module
        )

        module.Label = (
            "Módulo paramétrico"
        )

        document.recompute()


        #
        # Open dialog.
        #

        try:

            dialog = ParametricModuleDialog(
                module
            )

            result = dialog.exec_()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error abriendo el diálogo: "
                +
                str(error)
                +
                "\n"
            )

            self.deleteObjectTree(
                module
            )

            document.recompute()

            raise


        #
        # CANCEL
        #

        if (
            result
            !=
            QtWidgets.QDialog.Accepted
        ):

            #
            # IMPORTANT:
            # remove the complete tree, not only
            # the module group.
            #

            self.deleteObjectTree(
                module
            )

            document.recompute()

            return


        #
        # ACCEPT
        #

        document.recompute()

        try:

            FreeCADGui.activeDocument() \
                .activeView() \
                .fitAll()

        except Exception:

            pass


FreeCADGui.addCommand(
    "Bosqo_ParametricModule",
    ParametricModuleCommand()
)