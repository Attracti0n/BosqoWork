import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from PySide import QtWidgets

from dialogs.finish_dialog import FinishDialog


class BosqoFinishCommand:

    # =========================================================
    # RESOURCES
    # =========================================================

    def GetResources(
        self
    ):

        return {
            "Pixmap": os.path.join(
                ICONS_DIR,
                "texture.svg"
            ),

            "MenuText":
                "Acabado",

            "ToolTip":
                "Aplicar acabado a las piezas seleccionadas"
        }


    # =========================================================
    # ACTIVATED
    # =========================================================

    def Activated(
        self
    ):

        # -----------------------------------------------------
        # CURRENT SELECTION
        # -----------------------------------------------------

        selection = (
            FreeCADGui.Selection.getSelection()
        )


        if not selection:

            FreeCAD.Console.PrintWarning(
                "Bosqo: selecciona al menos una pieza.\n"
            )

            return


        # -----------------------------------------------------
        # FILTER BOSQOPART
        # -----------------------------------------------------

        parts = []


        for obj in selection:

            if obj is None:

                continue


            if not hasattr(
                obj,
                "Proxy"
            ):

                continue


            proxy = obj.Proxy


            if proxy is None:

                continue


            if type(proxy).__name__ != "BosqoPart":

                continue


            if obj not in parts:

                parts.append(
                    obj
                )


        # -----------------------------------------------------
        # NOTHING VALID SELECTED
        # -----------------------------------------------------

        if not parts:

            FreeCAD.Console.PrintWarning(
                "Bosqo: la selección no contiene "
                "piezas BosqoPart.\n"
            )

            return


        # -----------------------------------------------------
        # PARENT
        # -----------------------------------------------------

        parent = None


        try:

            parent = (
                FreeCADGui.getMainWindow()
            )

        except Exception:

            pass


        # -----------------------------------------------------
        # DIALOG
        # -----------------------------------------------------

        dialog = FinishDialog(
            parts,
            parent
        )


        result = dialog.exec_()


        # -----------------------------------------------------
        # ACCEPTED
        # -----------------------------------------------------

        if result == QtWidgets.QDialog.Accepted:

            try:

                if FreeCAD.ActiveDocument:

                    FreeCAD.ActiveDocument.recompute()

            except Exception as error:

                FreeCAD.Console.PrintWarning(
                    "Bosqo Finish recompute error: "
                    +
                    str(error)
                    +
                    "\n"
                )


# =============================================================
# REGISTER
# =============================================================

def register():

    commandName = (
        "Bosqo_Finish"
    )


    #
    # Prevent duplicate registration.
    #

    try:

        if commandName in FreeCADGui.listCommands():

            return

    except Exception:

        pass


    FreeCADGui.addCommand(
        commandName,
        BosqoFinishCommand()
    )