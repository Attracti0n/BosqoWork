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

            "Pixmap":
                os.path.join(
                    ICONS_DIR,
                    "select_to_group.svg"
                ),

            "MenuText":
                "Crear módulo importado",

            "ToolTip":
                "Crear un módulo importado a partir de la selección"

        }

    # =========================================================
    # ACTIVATED
    # =========================================================

    def Activated(self,):

        document = FreeCAD.ActiveDocument

        if document is None:

            QtWidgets.QMessageBox.warning(
                FreeCADGui.getMainWindow(),
                "Crear módulo importado",
                "No hay ningún documento activo."
            )

            return

        # -----------------------------------------------------
        # SELECTION
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # REMOVE INVALID OBJECTS
        # -----------------------------------------------------

        parts = []

        for obj in selection:

            if obj is None:
                continue

            # Object must belong to a document
            if getattr(
                obj,
                "Document",
                None
            ) is None:

                continue

            # Do not allow selecting the module itself
            proxy = getattr(
                obj,
                "Proxy",
                None
            )

            if proxy is not None:

                if proxy.__class__.__name__ == (
                    "BosqoImportedModule"
                ):

                    continue

            parts.append(
                obj
            )

        # -----------------------------------------------------
        # VALIDATION
        # -----------------------------------------------------

        if not parts:

            QtWidgets.QMessageBox.information(
                FreeCADGui.getMainWindow(),
                "Crear módulo importado",
                "La selección no contiene piezas válidas."
            )

            return

        # -----------------------------------------------------
        # DEBUG
        # -----------------------------------------------------

        FreeCAD.Console.PrintMessage(
            "========================================\n"
        )

        FreeCAD.Console.PrintMessage(
            "CREAR MÓDULO IMPORTADO\n"
        )

        FreeCAD.Console.PrintMessage(
            "Piezas seleccionadas: "
            + str(len(parts))
            + "\n"
        )

        for part in parts:

            FreeCAD.Console.PrintMessage(
                "  - "
                + str(
                    getattr(
                        part,
                        "Name",
                        ""
                    )
                )
                + " / "
                + str(
                    getattr(
                        part,
                        "Label",
                        ""
                    )
                )
                + "\n"
            )

        FreeCAD.Console.PrintMessage(
            "========================================\n"
        )

        # -----------------------------------------------------
        # MODULE DIALOG
        # -----------------------------------------------------

        module_name = "Módulo importado"

        try:

            # IMPORTANT:
            #
            # ModuleDialog expects:
            #
            #   data
            #   parts
            #   parent
            #
            # Previously the QMainWindow was passed as
            # "data", causing:
            #
            # QMainWindow object has no attribute 'get'
            #
            dialog = ModuleDialog(
                data={
                    "Label": "Módulo importado"
                },
                parts=parts,
                parent=FreeCADGui.getMainWindow()
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando ModuleDialog: "
                + str(error)
                + "\n"
            )

            return

        # -----------------------------------------------------
        # EXECUTE DIALOG
        # -----------------------------------------------------

        try:

            result = dialog.exec()

        except AttributeError:

            # Compatibility with older PySide versions
            try:

                result = dialog.exec_()

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error ejecutando ModuleDialog: "
                    + str(error)
                    + "\n"
                )

                return

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error ejecutando ModuleDialog: "
                + str(error)
                + "\n"
            )

            return

        # -----------------------------------------------------
        # CANCEL
        # -----------------------------------------------------

        if result != QtWidgets.QDialog.Accepted:

            return

        # -----------------------------------------------------
        # GET MODULE NAME
        # -----------------------------------------------------

        module_name = (
            self.getModuleName(
                dialog
            )
            or
            "Módulo importado"
        )

        # -----------------------------------------------------
        # CREATE IMPORTED MODULE
        # -----------------------------------------------------

        try:

            module = create_imported_module(
                document,
                parts
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando módulo importado: "
                + str(error)
                + "\n"
            )

            QtWidgets.QMessageBox.critical(
                FreeCADGui.getMainWindow(),
                "Crear módulo importado",
                "No se pudo crear el módulo importado.\n\n"
                + str(error)
            )

            return

        if module is None:

            QtWidgets.QMessageBox.critical(
                FreeCADGui.getMainWindow(),
                "Crear módulo importado",
                "La creación del módulo no devolvió ningún objeto."
            )

            return

        # -----------------------------------------------------
        # MODULE NAME
        # -----------------------------------------------------

        try:

            module.ModuleName = module_name

        except Exception:
            pass

        try:

            module.Label = module_name

        except Exception:
            pass

        # -----------------------------------------------------
        # MODULE SOURCE
        # -----------------------------------------------------
        #
        # Keep this if the property exists.
        #

        if hasattr(
            module,
            "ModuleSource"
        ):

            try:

                module.ModuleSource = "Imported"

            except Exception:

                pass

        # -----------------------------------------------------
        # RECOMPUTE
        # -----------------------------------------------------

        try:

            document.recompute()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error recomputando módulo importado: "
                + str(error)
                + "\n"
            )

        # -----------------------------------------------------
        # CLEAR SELECTION
        # -----------------------------------------------------

        try:

            FreeCADGui.Selection.clearSelection()

            FreeCADGui.Selection.addSelection(
                module
            )

        except Exception:

            pass

        # -----------------------------------------------------
        # MESSAGE
        # -----------------------------------------------------

        FreeCAD.Console.PrintMessage(
            "========================================\n"
        )

        FreeCAD.Console.PrintMessage(
            "MÓDULO IMPORTADO CREADO\n"
        )

        FreeCAD.Console.PrintMessage(
            "Nombre: "
            + str(
                getattr(
                    module,
                    "Label",
                    ""
                )
            )
            + "\n"
        )

        FreeCAD.Console.PrintMessage(
            "Piezas: "
            + str(
                len(parts)
            )
            + "\n"
        )

        # Also show the actual Group contents
        try:

            group_parts = list(
                getattr(
                    module,
                    "Group",
                    []
                )
            )

            FreeCAD.Console.PrintMessage(
                "Piezas en Group: "
                + str(
                    len(group_parts)
                )
                + "\n"
            )

        except Exception:

            pass

        FreeCAD.Console.PrintMessage(
            "========================================\n"
        )

    # =========================================================
    # GET MODULE NAME
    # =========================================================

    def getModuleName(
        self,
        dialog
    ):

        # -----------------------------------------------------
        # Current ModuleDialog
        # -----------------------------------------------------

        if hasattr(
            dialog,
            "nameEdit"
        ):

            try:

                value = (
                    dialog.nameEdit
                    .text()
                    .strip()
                )

                if value:

                    return value

            except Exception:

                pass

        # -----------------------------------------------------
        # Compatibility with possible names
        # -----------------------------------------------------

        for name in (
            "moduleNameEdit",
            "nameField",
            "moduleNameField"
        ):

            if not hasattr(
                dialog,
                name
            ):

                continue

            try:

                widget = getattr(
                    dialog,
                    name
                )

                if hasattr(
                    widget,
                    "text"
                ):

                    value = (
                        widget.text()
                        .strip()
                    )

                    if value:

                        return value

            except Exception:

                pass

        # -----------------------------------------------------
        # Possible getter methods
        # -----------------------------------------------------

        for method_name in (
            "getModuleName",
            "getName"
        ):

            if not hasattr(
                dialog,
                method_name
            ):

                continue

            try:

                value = getattr(
                    dialog,
                    method_name
                )()

                if value is not None:

                    value = str(
                        value
                    ).strip()

                    if value:

                        return value

            except Exception:

                pass

        return "Módulo importado"


# =============================================================
# COMMAND REGISTRATION
# =============================================================

FreeCADGui.addCommand(
    "Bosqo_CreateModuleFromSelection",
    CreateModuleFromSelectionCommand()
)