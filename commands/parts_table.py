import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from PySide import QtWidgets

from dialogs.part_table_dialog import PartTableDialog

from core.builders.module_builder import ModuleBuilder


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


    # =========================================================
    # ACTIVATED
    # =========================================================

    def Activated(
        self
    ):

        document = FreeCAD.ActiveDocument

        if document is None:

            return


        # =====================================================
        # SELECCIÓN
        # =====================================================

        selection = (
            FreeCADGui.Selection.getSelection()
        )

        module = None


        # =====================================================
        # BUSCAR BOSQOMODULE
        # =====================================================

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


        # =====================================================
        # NO HAY MÓDULO
        # =====================================================

        if module is None:

            QtWidgets.QMessageBox.information(
                None,
                "Tabla de piezas",
                "Selecciona primero un módulo."
            )

            return


        # =====================================================
        # OBTENER PIEZAS
        # =====================================================

        try:

            parts = (
                module.Proxy.getParts(
                    module
                )
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error obteniendo las piezas del módulo: "
                +
                str(error)
                +
                "\n"
            )

            return


        if parts is None:

            parts = []


        # =====================================================
        # ABRIR EDITOR
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
        # OBTENER DATOS
        # =====================================================

        try:

            tableData = dialog.getData()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error obteniendo datos de la tabla: "
                +
                str(error)
                +
                "\n"
            )

            return


        if tableData is None:

            return


        # =====================================================
        # GUARDAR / RECALCULAR
        # =====================================================

        try:

            self.rebuildModule(
                module,
                tableData
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error reconstruyendo módulo: "
                +
                str(error)
                +
                "\n"
            )

            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                "No se ha podido recalcular el módulo.\n\n"
                +
                str(error)
            )

            return


        # =====================================================
        # RECOMPUTE
        # =====================================================

        try:

            document.recompute()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error en recompute: "
                +
                str(error)
                +
                "\n"
            )


        # =====================================================
        # ACTUALIZAR VISTA
        # =====================================================

        try:

            FreeCADGui.updateGui()

        except Exception:

            pass


    # =========================================================
    # REBUILD MODULE
    # =========================================================

    def rebuildModule(
        self,
        module,
        tableData
    ):

        #
        # tableData puede venir en dos formatos:
        #
        # 1. lista de piezas
        #
        # 2. diccionario con "Parts"
        #
        #

        userParts = tableData


        if isinstance(
            tableData,
            dict
        ):

            userParts = tableData.get(
                "Parts",
                []
            )


        if userParts is None:

            userParts = []


        if not isinstance(
            userParts,
            list
        ):

            userParts = list(
                userParts
            )


        # =====================================================
        # LIMPIAR DATOS
        # =====================================================

        cleanParts = []


        for definition in userParts:

            if not isinstance(
                definition,
                dict
            ):

                continue


            cleanParts.append(
                dict(
                    definition
                )
            )


        # =====================================================
        # CONSTRUIR DE NUEVO
        # =====================================================

        ModuleBuilder.build(
            module,
            user_parts=cleanParts
        )


        # =====================================================
        # RECOMPUTE
        # =====================================================

        module.Document.recompute()


        # =====================================================
        # ACTUALIZAR VISTA
        # =====================================================

        try:

            FreeCADGui.updateGui()

        except Exception:

            pass


# =============================================================
# REGISTRAR COMANDO
# =============================================================

FreeCADGui.addCommand(
    "Bosqo_PartsTable",
    PartsTableCommand()
)