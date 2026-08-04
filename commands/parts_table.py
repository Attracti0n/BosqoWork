import FreeCAD
import FreeCADGui

from PySide import QtWidgets

from dialogs.part_table_dialog import PartTableDialog


class PartsTableCommand:

    def GetResources(
        self
    ):

        return {
            "Pixmap":
                "parts",

            "MenuText":
                "Tabla de piezas",

            "ToolTip":
                "Editar piezas del módulo",

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


    def Activated(
        self
    ):

        document = FreeCAD.ActiveDocument


        if document is None:

            return


        #
        # Selected object
        #

        selection = (
            FreeCADGui.Selection.getSelection()
        )


        module = None


        #
        # Find BosqoModule
        #

        for obj in selection:

            if not hasattr(
                obj,
                "Proxy"
            ):

                continue


            proxy = obj.Proxy


            if proxy is None:

                continue


            if type(proxy).__name__ == (
                "BosqoModule"
            ):

                module = obj

                break


        #
        # No module selected
        #

        if module is None:

            FreeCAD.Console.PrintMessage(
                "Selecciona primero un módulo.\n"
            )

            return


        #
        # Get real BosqoPart objects
        #

        parts = (
            module.Proxy.getParts(
                module
            )
        )


        #
        # Open table
        #

        dialog = PartTableDialog(
            parts=parts
        )


        result = dialog.exec_()


        if result != QtWidgets.QDialog.Accepted:

            return


        #
        # Save changes
        #

        try:

            dialog.applyChanges()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error guardando piezas: "
                + str(error)
                + "\n"
            )

            return


        #
        # Recompute
        #

        document.recompute()


        #
        # Update view
        #

        Gui = FreeCADGui

        Gui.updateGui()


FreeCADGui.addCommand(
    "Bosqo_PartsTable",
    PartsTableCommand()
)