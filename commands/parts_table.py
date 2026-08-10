import FreeCAD
import FreeCADGui
import os

from PySide import QtWidgets

from app_paths import ICONS_DIR

from dialogs.part_table_dialog import (
    PartTableDialog
)


class PartsTableCommand:

    def GetResources(
        self
    ):

        return {

            "Pixmap":
                os.path.join(
                    ICONS_DIR,
                    "explode.svg"
                ),

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

        document = (
            FreeCAD.ActiveDocument
        )


        if document is None:

            return


        # =====================================================
        # SELECTION
        # =====================================================

        selection = (
            FreeCADGui.Selection.getSelection()
        )


        module = None


        for obj in selection:

            if not hasattr(
                obj,
                "Proxy"
            ):

                continue


            proxy = obj.Proxy


            if proxy is None:

                continue


            # =================================================
            # IMPORTANT:
            #
            # Accept both normal and imported modules.
            # =================================================

            proxyName = type(
                proxy
            ).__name__


            if proxyName in (
                "BosqoModule",
                "BosqoImportedModule"
            ):

                module = obj

                break


        # =====================================================
        # NO MODULE
        # =====================================================

        if module is None:

            QtWidgets.QMessageBox.information(
                None,
                "Tabla de piezas",
                "Selecciona primero un módulo."
            )

            return


        # =====================================================
        # GET REAL PARTS
        # =====================================================

        try:

            parts = (
                module.Proxy.getParts(
                    module
                )
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error obteniendo las piezas "
                "del módulo: "
                +
                str(
                    error
                )
                +
                "\n"
            )

            return


        if parts is None:

            parts = []


        # =====================================================
        # OPEN EDITOR
        # =====================================================

        dialog = PartTableDialog(

            module=module,

            parts=parts

        )


        result = dialog.exec_()


        if result != (
            QtWidgets.QDialog.Accepted
        ):

            return


        # =====================================================
        # IMPORTANT:
        #
        # The dialog itself has already saved
        # the real FreeCAD objects.
        #
        # We DO NOT call ModuleBuilder here.
        # =====================================================

        try:

            document.recompute()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error en recompute: "
                +
                str(
                    error
                )
                +
                "\n"
            )


        try:

            FreeCADGui.updateGui()

        except Exception:

            pass


# =============================================================
# REGISTER COMMAND
# =============================================================

FreeCADGui.addCommand(
    "Bosqo_PartsTable",
    PartsTableCommand()
)