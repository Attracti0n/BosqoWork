import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from PySide import QtWidgets

from dialogs.part_table_dialog import PartTableDialog


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

        document = FreeCAD.ActiveDocument


        if document is None:

            return


        # =====================================================
        # OBJETO SELECCIONADO
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
        # NO HAY MÓDULO SELECCIONADO
        # =====================================================

        if module is None:

            FreeCAD.Console.PrintMessage(
                "Selecciona primero un módulo.\n"
            )

            return


        # =====================================================
        # OBTENER PIEZAS REALES
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
                + str(error)
                + "\n"
            )

            return


        if parts is None:

            parts = []


        # =====================================================
        # ABRIR EDITOR DEL MÓDULO
        # =====================================================

        dialog = PartTableDialog(
            module=module,
            parts=parts
        )


        result = dialog.exec_()


        if result != QtWidgets.QDialog.Accepted:

            return


        # =====================================================
        # GUARDAR CAMBIOS
        # =====================================================

        try:

            self.saveParts(
                parts,
                dialog.getData()
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error guardando piezas: "
                + str(error)
                + "\n"
            )

            return


        # =====================================================
        # RECOMPUTE
        # =====================================================

        document.recompute()


        # =====================================================
        # ACTUALIZAR VISTA
        # =====================================================

        FreeCADGui.updateGui()


    # =========================================================
    # GUARDAR DATOS DE LAS PIEZAS
    # =========================================================

    def saveParts(
        self,
        parts,
        tableData
    ):

        if parts is None:

            return


        if tableData is None:

            return


        # -----------------------------------------------------
        # Actualizar las piezas existentes
        # -----------------------------------------------------

        count = min(
            len(parts),
            len(tableData)
        )


        for index in range(
            count
        ):

            part = parts[
                index
            ]

            data = tableData[
                index
            ]


            if not hasattr(
                part,
                "Proxy"
            ):

                continue


            proxy = part.Proxy


            if proxy is None:

                continue


            if type(proxy).__name__ != (
                "BosqoPart"
            ):

                continue


            # -------------------------------------------------
            # Nombre
            # -------------------------------------------------

            if hasattr(
                part,
                "Label"
            ):

                label = data.get(
                    "Label",
                    ""
                )


                if label:

                    part.Label = label


            # -------------------------------------------------
            # Tipo
            # -------------------------------------------------

            if hasattr(
                part,
                "PartType"
            ):

                part.PartType = data.get(
                    "PartType",
                    ""
                )


            # -------------------------------------------------
            # Largo
            # -------------------------------------------------

            if hasattr(
                part,
                "Length"
            ):

                part.Length = data.get(
                    "Length",
                    0
                )


            # -------------------------------------------------
            # Ancho
            # -------------------------------------------------

            if hasattr(
                part,
                "Width"
            ):

                part.Width = data.get(
                    "Width",
                    0
                )


            # -------------------------------------------------
            # Espesor
            # -------------------------------------------------

            if hasattr(
                part,
                "Thickness"
            ):

                part.Thickness = data.get(
                    "Thickness",
                    0
                )


            # -------------------------------------------------
            # Cantidad
            # -------------------------------------------------

            if hasattr(
                part,
                "Quantity"
            ):

                part.Quantity = data.get(
                    "Quantity",
                    1
                )


            # -------------------------------------------------
            # Material
            # -------------------------------------------------

            if hasattr(
                part,
                "MaterialCode"
            ):

                part.MaterialCode = data.get(
                    "MaterialCode",
                    ""
                )


            # -------------------------------------------------
            # Actualizar objeto
            # -------------------------------------------------

            part.touch()


# =============================================================
# REGISTRAR COMANDO
# =============================================================

FreeCADGui.addCommand(
    "Bosqo_PartsTable",
    PartsTableCommand()
)