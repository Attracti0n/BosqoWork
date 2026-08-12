import FreeCAD
import FreeCADGui
import os

from PySide import QtWidgets

from app_paths import ICONS_DIR
from dialogs.module_dialog import ModuleDialog
from objects.bosqo_imported_module import create_imported_module


# =============================================================
# CREATE MODULE FROM SELECTION
# =============================================================

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

            "MenuText": (
                "Crear módulo importado"
            ),

            "ToolTip": (
                "Crear un módulo importado "
                "a partir de la selección"
            )
        }

    # =========================================================
    # ACTIVATED
    # =========================================================

    def Activated(self):

        document = FreeCAD.ActiveDocument

        if document is None:

            QtWidgets.QMessageBox.warning(
                FreeCADGui.getMainWindow(),
                "Crear módulo importado",
                "No hay ningún documento activo."
            )

            return

        # =====================================================
        # SELECTION
        # =====================================================

        selection = (
            FreeCADGui.Selection.getSelection()
        )

        if not selection:

            QtWidgets.QMessageBox.information(
                FreeCADGui.getMainWindow(),
                "Crear módulo importado",
                "Selecciona primero las piezas "
                "que formarán el módulo."
            )

            return

        # =====================================================
        # VALID PARTS
        # =====================================================

        parts = []

        for obj in selection:

            if obj is None:
                continue

            if getattr(
                obj,
                "Document",
                None
            ) is None:

                continue

            # -------------------------------------------------
            # DO NOT ALLOW ANOTHER IMPORTED MODULE
            # -------------------------------------------------

            proxy = getattr(
                obj,
                "Proxy",
                None
            )

            if proxy is not None:

                try:

                    if proxy.__class__.__name__ == (
                        "BosqoImportedModule"
                    ):

                        continue

                except Exception:

                    pass

            parts.append(
                obj
            )

        # =====================================================
        # VALIDATION
        # =====================================================

        if not parts:

            QtWidgets.QMessageBox.information(
                FreeCADGui.getMainWindow(),
                "Crear módulo importado",
                "La selección no contiene piezas válidas."
            )

            return

        # =====================================================
        # DEBUG
        # =====================================================

        FreeCAD.Console.PrintMessage(
            "\n"
            "========================================\n"
        )

        FreeCAD.Console.PrintMessage(
            "CREAR MÓDULO IMPORTADO\n"
        )

        FreeCAD.Console.PrintMessage(
            "Piezas seleccionadas: "
            +
            str(len(parts))
            +
            "\n"
        )

        for part in parts:

            FreeCAD.Console.PrintMessage(
                "  - "
                +
                str(
                    getattr(
                        part,
                        "Name",
                        ""
                    )
                )
                +
                " / "
                +
                str(
                    getattr(
                        part,
                        "Label",
                        ""
                    )
                )
                +
                "\n"
            )

        FreeCAD.Console.PrintMessage(
            "========================================\n"
        )

        # =====================================================
        # CREATE MODULE FIRST
        #
        # IMPORTANT:
        #
        # The module must exist before opening ModuleDialog.
        # This allows ModuleDialog.saveToModule() to write
        # the changes directly to the real FreeCAD object.
        # =====================================================

        module = None

        try:

            module = create_imported_module(
                document,
                parts
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando módulo importado: "
                +
                str(error)
                +
                "\n"
            )

            QtWidgets.QMessageBox.critical(
                FreeCADGui.getMainWindow(),
                "Crear módulo importado",
                "No se pudo crear el módulo importado.\n\n"
                +
                str(error)
            )

            return

        if module is None:

            QtWidgets.QMessageBox.critical(
                FreeCADGui.getMainWindow(),
                "Crear módulo importado",
                "La creación del módulo no devolvió "
                "ningún objeto."
            )

            return

        # =====================================================
        # INITIAL NAME
        # =====================================================

        try:

            module.ModuleName = (
                "Módulo importado"
            )

            module.Label = (
                "Módulo importado"
            )

        except Exception:

            pass

        # =====================================================
        # MODULE SOURCE
        # =====================================================

        try:

            if hasattr(
                module,
                "ModuleSource"
            ):

                module.ModuleSource = (
                    "Imported"
                )

        except Exception:

            pass

        # =====================================================
        # RECOMPUTE
        # =====================================================

        try:

            document.recompute()

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "Error recomputando módulo antes "
                "del diálogo: "
                +
                str(error)
                +
                "\n"
            )

        # =====================================================
        # MODULE DATA
        #
        # Read the actual module data.
        # =====================================================

        moduleData = {

            "Label": (
                getattr(
                    module,
                    "Label",
                    "Módulo importado"
                )
            ),

            "Parts": []
        }

        # =====================================================
        # OPEN MODULE DIALOG
        #
        # IMPORTANT:
        #
        # module=module is essential.
        # =====================================================

        try:

            dialog = ModuleDialog(
                data=moduleData,
                parts=parts,
                parent=FreeCADGui.getMainWindow(),
                module=module
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando ModuleDialog: "
                +
                str(error)
                +
                "\n"
            )

            # -------------------------------------------------
            # Remove temporary module
            # -------------------------------------------------

            try:

                document.removeObject(
                    module.Name
                )

                document.recompute()

            except Exception:

                pass

            QtWidgets.QMessageBox.critical(
                FreeCADGui.getMainWindow(),
                "Crear módulo importado",
                "No se pudo abrir el diálogo del módulo.\n\n"
                +
                str(error)
            )

            return

        # =====================================================
        # EXECUTE DIALOG
        # =====================================================

        try:

            result = dialog.exec()

        except AttributeError:

            try:

                result = dialog.exec_()

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error ejecutando ModuleDialog: "
                    +
                    str(error)
                    +
                    "\n"
                )

                result = (
                    QtWidgets.QDialog.Rejected
                )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error ejecutando ModuleDialog: "
                +
                str(error)
                +
                "\n"
            )

            result = (
                QtWidgets.QDialog.Rejected
            )

        # =====================================================
        # CANCEL
        # =====================================================

        if result != QtWidgets.QDialog.Accepted:

            try:

                document.removeObject(
                    module.Name
                )

                document.recompute()

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error eliminando módulo cancelado: "
                    +
                    str(error)
                    +
                    "\n"
                )

            return

        # =====================================================
        # MODULE DIALOG HAS SAVED THE DATA
        #
        # At this point ModuleDialog.saveToModule()
        # has already saved:
        #
        #   module.ModuleName
        #   module.PartsJSON
        #   part.PartType
        #   part.Material
        #
        # We only recompute and verify.
        # =====================================================

        try:

            document.recompute()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error recomputando módulo importado: "
                +
                str(error)
                +
                "\n"
            )

        # =====================================================
        # SELECT MODULE
        # =====================================================

        try:

            FreeCADGui.Selection.clearSelection()

            FreeCADGui.Selection.addSelection(
                module
            )

        except Exception:

            pass

        # =====================================================
        # DEBUG
        # =====================================================

        FreeCAD.Console.PrintMessage(
            "\n"
            "========================================\n"
        )

        FreeCAD.Console.PrintMessage(
            "MÓDULO IMPORTADO CREADO\n"
        )

        FreeCAD.Console.PrintMessage(
            "Name: "
            +
            str(
                getattr(
                    module,
                    "Name",
                    ""
                )
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "Label: "
            +
            str(
                getattr(
                    module,
                    "Label",
                    ""
                )
            )
            +
            "\n"
        )

        FreeCAD.Console.PrintMessage(
            "Piezas: "
            +
            str(
                len(parts)
            )
            +
            "\n"
        )

        # -----------------------------------------------------
        # GROUP
        # -----------------------------------------------------

        try:

            groupParts = list(
                getattr(
                    module,
                    "Group",
                    []
                )
            )

            FreeCAD.Console.PrintMessage(
                "Piezas en Group: "
                +
                str(
                    len(groupParts)
                )
                +
                "\n"
            )

        except Exception:

            pass

        # -----------------------------------------------------
        # PARTS JSON
        # -----------------------------------------------------

        try:

            FreeCAD.Console.PrintMessage(
                "PartsJSON:\n"
            )

            FreeCAD.Console.PrintMessage(
                str(
                    getattr(
                        module,
                        "PartsJSON",
                        ""
                    )
                )
                +
                "\n"
            )

        except Exception:

            pass

        # -----------------------------------------------------
        # REAL PART ATTRIBUTES
        # -----------------------------------------------------

        for part in parts:

            try:

                partName = str(
                    getattr(
                        part,
                        "Name",
                        ""
                    )
                )

                partType = str(
                    getattr(
                        part,
                        "PartType",
                        ""
                    )
                )

                material = str(
                    getattr(
                        part,
                        "Material",
                        ""
                    )
                )

                FreeCAD.Console.PrintMessage(
                    "PIEZA: "
                    +
                    partName
                    +
                    " | Tipo: "
                    +
                    partType
                    +
                    " | Material: "
                    +
                    material
                    +
                    "\n"
                )

            except Exception:

                pass

        FreeCAD.Console.PrintMessage(
            "========================================\n"
        )


# =============================================================
# COMMAND REGISTRATION
# =============================================================

FreeCADGui.addCommand(
    "Bosqo_CreateModuleFromSelection",
    CreateModuleFromSelectionCommand()
)