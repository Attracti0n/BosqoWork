import FreeCAD
import FreeCADGui

from PySide import QtWidgets

from dialogs.drawer_dialog import (
    create_drawer_dialog
)

from objects.bosqo_drawer import (
    create_drawer
)

from core.builders.drawer_builder import (
    DrawerBuilder
)


# =============================================================
# COMMAND
# =============================================================

class BosqoDrawerCommand:

    def GetResources(
        self
    ):

        return {

            "MenuText":
                "Cajón",

            "ToolTip":
                "Crear un nuevo cajón",

            "Pixmap":
                "",

            "Accel":
                ""
        }

    # =========================================================
    # ACTIVATION
    # =========================================================

    def Activated(
        self
    ):

        # =====================================================
        # DOCUMENT
        # =====================================================

        document = (
            FreeCAD.ActiveDocument
        )

        if document is None:

            FreeCAD.Console.PrintError(
                "No hay ningún documento activo.\n"
            )

            return

        # =====================================================
        # MODULE
        # =====================================================

        module = None

        try:

            selection = (
                FreeCADGui.Selection.getSelection()
            )

            for selected in selection:

                if (
                    hasattr(
                        selected,
                        "Width"
                    )
                    and
                    hasattr(
                        selected,
                        "Height"
                    )
                    and
                    hasattr(
                        selected,
                        "Depth"
                    )
                    and
                    hasattr(
                        selected,
                        "Group"
                    )
                ):

                    module = selected
                    break

        except Exception:

            pass

        # -----------------------------------------------------
        # FALLBACK
        # -----------------------------------------------------

        if module is None:

            try:

                module = document.getObject(
                    "BosqoModule"
                )

            except Exception:

                module = None

        if module is None:

            FreeCAD.Console.PrintError(
                "No se encontró un módulo válido "
                "para crear el cajón.\n"
            )

            return

        # =====================================================
        # DIALOG
        # =====================================================

        dialog = (
            create_drawer_dialog()
        )

        result = (
            dialog.exec_()
        )

        if result != QtWidgets.QDialog.Accepted:

            return

        # =====================================================
        # DATA
        # =====================================================

        try:

            data = (
                dialog.getData()
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error obteniendo los datos "
                "del cajón: "
                +
                str(error)
                +
                "\n"
            )

            return

        # =====================================================
        # CREATE DRAWER
        # =====================================================

        try:

            drawer = create_drawer(
                document
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "No se pudo crear el objeto "
                "BosqoDrawer: "
                +
                str(error)
                +
                "\n"
            )

            return

        # =====================================================
        # ADD DRAWER TO MODULE
        # =====================================================

        try:

            module.addObject(
                drawer
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "No se pudo introducir el cajón "
                "dentro del módulo: "
                +
                str(error)
                +
                "\n"
            )

            try:

                document.removeObject(
                    drawer.Name
                )

            except Exception:

                pass

            return

        # =====================================================
        # APPLY DATA
        # =====================================================

        try:

            proxy = (
                getattr(
                    drawer,
                    "Proxy",
                    None
                )
            )

            if data.get(
                "Label"
            ):

                drawer.Label = (
                    data["Label"]
                )

            if proxy is not None:

                proxy.setData(
                    drawer,
                    data
                )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "No se pudieron aplicar "
                "los datos del cajón: "
                +
                str(error)
                +
                "\n"
            )

            try:

                module.removeObject(
                    drawer
                )

            except Exception:

                pass

            try:

                document.removeObject(
                    drawer.Name
                )

            except Exception:

                pass

            return

        # =====================================================
        # VALIDATE
        # =====================================================

        try:

            if not DrawerBuilder.validate(
                drawer
            ):

                FreeCAD.Console.PrintError(
                    "Los datos del cajón no son válidos.\n"
                )

                try:

                    module.removeObject(
                        drawer
                    )

                except Exception:

                    pass

                try:

                    document.removeObject(
                        drawer.Name
                    )

                except Exception:

                    pass

                return

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error validando el cajón: "
                +
                str(error)
                +
                "\n"
            )

            try:

                module.removeObject(
                    drawer
                )

            except Exception:

                pass

            try:

                document.removeObject(
                    drawer.Name
                )

            except Exception:

                pass

            return

        # =====================================================
        # BUILD
        # =====================================================

        try:

            success = (
                DrawerBuilder.build(
                    drawer
                )
            )

            if not success:

                FreeCAD.Console.PrintError(
                    "No se pudo construir el cajón.\n"
                )

                try:

                    DrawerBuilder.clear(
                        drawer
                    )

                except Exception:

                    pass

                try:

                    module.removeObject(
                        drawer
                    )

                except Exception:

                    pass

                try:

                    document.removeObject(
                        drawer.Name
                    )

                except Exception:

                    pass

                return

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error construyendo el cajón: "
                +
                str(error)
                +
                "\n"
            )

            try:

                DrawerBuilder.clear(
                    drawer
                )

            except Exception:

                pass

            try:

                module.removeObject(
                    drawer
                )

            except Exception:

                pass

            try:

                document.removeObject(
                    drawer.Name
                )

            except Exception:

                pass

            return

        # =====================================================
        # RECOMPUTE
        # =====================================================

        try:

            document.recompute()

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "No se pudo recalcular "
                "el documento: "
                +
                str(error)
                +
                "\n"
            )

        # =====================================================
        # VISIBILITY
        # =====================================================

        try:

            drawer.ViewObject.Visibility = True

        except Exception:

            pass

        try:

            for part in drawer.Group:

                part.ViewObject.Visibility = True

        except Exception:

            pass

        # =====================================================
        # SELECT
        # =====================================================

        try:

            FreeCADGui.Selection.clearSelection()

            FreeCADGui.Selection.addSelection(
                drawer
            )

        except Exception:

            pass


# =============================================================
# REGISTER COMMAND
# =============================================================

FreeCADGui.addCommand(
    "Bosqo_Drawer",
    BosqoDrawerCommand()
)