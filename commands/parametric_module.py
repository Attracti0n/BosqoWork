import FreeCAD
import FreeCADGui
import os

from PySide import QtWidgets

from app_paths import ICONS_DIR

from objects.bosqo_module import BosqoModule
from objects.bosqo_module_parameters import (
    BosqoModuleParameters
)

from dialogs.parametric_module_dialog import (
    ParametricModuleDialog
)

from core.builders.module_builder import (
    ModuleBuilder
)


class ParametricModuleCommand:

    # =========================================================
    # RESOURCES
    # =========================================================

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


    # =========================================================
    # ACTIVE
    # =========================================================

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


        #
        # Create module container
        #

        module = document.addObject(
            "App::DocumentObjectGroupPython",
            "BosqoModule"
        )

        BosqoModule(
            module
        )


        #
        # Make sure required module
        # properties exist.
        #

        self.ensureModuleProperties(
            module
        )


        #
        # Create parameter object.
        #
        # This object stores the values used
        # by the dialog.
        #

        parameters = document.addObject(
            "App::FeaturePython",
            "BosqoModuleParameters"
        )

        BosqoModuleParameters(
            parameters
        )


        #
        # Put parameter object inside
        # the module.
        #

        module.addObject(
            parameters
        )


        #
        # Initial labels
        #

        module.Label = (
            "Módulo paramétrico"
        )

        parameters.Label = (
            "Parámetros"
        )


        document.recompute()


        # =====================================================
        # OPEN DIALOG
        # =====================================================

        dialog = ParametricModuleDialog(
            parameters
        )


        result = dialog.exec_()


        # =====================================================
        # CANCEL
        # =====================================================

        if (
            result
            !=
            QtWidgets.QDialog.Accepted
        ):

            try:

                document.removeObject(
                    module.Name
                )

            except Exception:

                pass


            document.recompute()

            return


        # =====================================================
        # GET DATA FROM DIALOG
        # =====================================================

        try:

            dialogData = dialog.getData()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error obteniendo datos del módulo: "
                +
                str(error)
                +
                "\n"
            )

            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                "No se pudieron obtener los datos "
                "del módulo:\n\n"
                +
                str(error)
            )

            try:

                document.removeObject(
                    module.Name
                )

            except Exception:

                pass

            document.recompute()

            return


        # =====================================================
        # COPY MODULE PARAMETERS
        # =====================================================

        self.copyParameters(
            parameters,
            module,
            dialogData
        )


        # =====================================================
        # USER PARTS
        # =====================================================

        userParts = dialogData.get(
            "Parts",
            []
        )


        #
        # Make an independent copy.
        #
        # This is important because the dialog
        # will be destroyed after this command.
        #

        parts = []

        for definition in userParts:

            if not isinstance(
                definition,
                dict
            ):

                continue


            parts.append(
                dict(
                    definition
                )
            )


        # =====================================================
        # BUILD MODULE
        # =====================================================

        try:

            #
            # IMPORTANT:
            #
            # ModuleBuilder must receive the
            # definitions coming from the dialog.
            #

            ModuleBuilder.build(
                module,
                parts
            )


        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error building parametric module: "
                +
                str(error)
                +
                "\n"
            )


            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                "Error creando el módulo:\n\n"
                +
                str(error)
            )


            try:

                document.removeObject(
                    module.Name
                )

            except Exception:

                pass


            document.recompute()

            return


        # =====================================================
        # FINAL RECOMPUTE
        # =====================================================

        document.recompute()


        # =====================================================
        # FIT VIEW
        # =====================================================

        try:

            FreeCADGui.activeDocument().activeView().fitAll()

        except Exception:

            pass


    # =========================================================
    # ENSURE MODULE PROPERTIES
    # =========================================================

    def ensureModuleProperties(
        self,
        module
    ):

        #
        # Panel thickness
        #

        if not hasattr(
            module,
            "PanelThickness"
        ):

            module.addProperty(
                "App::PropertyLength",
                "PanelThickness",
                "Parameters",
                "Espesor de los paneles"
            )

            module.PanelThickness = (
                FreeCAD.Units.Quantity(
                    "19 mm"
                )
            )


        #
        # Back thickness
        #

        if not hasattr(
            module,
            "BackThickness"
        ):

            module.addProperty(
                "App::PropertyLength",
                "BackThickness",
                "Parameters",
                "Espesor de la trasera"
            )

            module.BackThickness = (
                FreeCAD.Units.Quantity(
                    "3 mm"
                )
            )


        #
        # Back inset
        #

        if not hasattr(
            module,
            "BackInset"
        ):

            module.addProperty(
                "App::PropertyLength",
                "BackInset",
                "Parameters",
                "Retranqueo de la trasera"
            )

            module.BackInset = (
                FreeCAD.Units.Quantity(
                    "0 mm"
                )
            )


    # =========================================================
    # COPY PARAMETERS
    # =========================================================

    def copyParameters(
        self,
        parameters,
        module,
        data
    ):

        #
        # Name
        #

        name = data.get(
            "Label",
            "Módulo"
        )


        if not name:

            name = "Módulo"


        module.Label = (
            str(
                name
            )
        )


        #
        # Width
        #

        width = data.get(
            "Width",
            600
        )


        if hasattr(
            module,
            "Width"
        ):

            module.Width = width


        #
        # Height
        #

        height = data.get(
            "Height",
            720
        )


        if hasattr(
            module,
            "Height"
        ):

            module.Height = height


        #
        # Depth
        #

        depth = data.get(
            "Depth",
            560
        )


        if hasattr(
            module,
            "Depth"
        ):

            module.Depth = depth


        #
        # Panel thickness
        #

        panelThickness = data.get(
            "PanelThickness",
            19
        )


        if hasattr(
            module,
            "PanelThickness"
        ):

            module.PanelThickness = (
                panelThickness
            )


        #
        # Back thickness
        #

        backThickness = data.get(
            "BackThickness",
            3
        )


        if hasattr(
            module,
            "BackThickness"
        ):

            module.BackThickness = (
                backThickness
            )


        #
        # Back inset
        #

        backInset = data.get(
            "BackInset",
            0
        )


        if hasattr(
            module,
            "BackInset"
        ):

            module.BackInset = (
                backInset
            )


        # =====================================================
        # UPDATE PARAMETER OBJECT
        # =====================================================

        if parameters is None:

            return


        #
        # Name
        #

        if hasattr(
            parameters,
            "ModuleName"
        ):

            parameters.ModuleName = (
                str(
                    name
                )
            )


        #
        # Width
        #

        if hasattr(
            parameters,
            "ModuleWidth"
        ):

            parameters.ModuleWidth = (
                width
            )


        #
        # Height
        #

        if hasattr(
            parameters,
            "ModuleHeight"
        ):

            parameters.ModuleHeight = (
                height
            )


        #
        # Depth
        #

        if hasattr(
            parameters,
            "ModuleDepth"
        ):

            parameters.ModuleDepth = (
                depth
            )


        #
        # Panel thickness
        #

        if hasattr(
            parameters,
            "PanelThickness"
        ):

            parameters.PanelThickness = (
                panelThickness
            )


        #
        # Back thickness
        #

        if hasattr(
            parameters,
            "BackThickness"
        ):

            parameters.BackThickness = (
                backThickness
            )


        #
        # Back inset
        #

        if hasattr(
            parameters,
            "BackInset"
        ):

            parameters.BackInset = (
                backInset
            )


        #
        # Type
        #

        if (
            "ModuleType"
            in data
        ):

            if hasattr(
                parameters,
                "ModuleType"
            ):

                parameters.ModuleType = (
                    data[
                        "ModuleType"
                    ]
                )


            if hasattr(
                module,
                "Type"
            ):

                module.Type = (
                    data[
                        "ModuleType"
                    ]
                )


        #
        # Recompute
        #

        try:

            module.Document.recompute()

        except Exception:

            pass


# =============================================================
# REGISTER COMMAND
# =============================================================

FreeCADGui.addCommand(
    "Bosqo_ParametricModule",
    ParametricModuleCommand()
)