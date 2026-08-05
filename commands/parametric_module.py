import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from PySide import QtWidgets

from objects.bosqo_module import BosqoModule
from objects.bosqo_module_parameters import BosqoModuleParameters

from dialogs.parametric_module_dialog import (
    ParametricModuleDialog
)

from core.builders.module_builder import ModuleBuilder


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


    def Activated(
        self
    ):

        document = (
            FreeCAD.ActiveDocument
        )


        if document is None:

            return


        #
        # Create real module container
        #

        module = document.addObject(
            "App::DocumentObjectGroupPython",
            "BosqoModule"
        )


        BosqoModule(
            module
        )


        #
        # Make sure module has the
        # parametric properties.
        #

        self.ensureModuleProperties(
            module
        )


        #
        # Create parameter object
        #

        parameters = document.addObject(
            "App::FeaturePython",
            "BosqoModuleParameters"
        )


        BosqoModuleParameters(
            parameters
        )


        #
        # Add parameters object to module
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


        #
        # Open dialog
        #

        dialog = ParametricModuleDialog(
            parameters
        )


        result = dialog.exec_()


        #
        # Cancel
        #

        if result != QtWidgets.QDialog.Accepted:

            document.removeObject(
                module.Name
            )

            document.recompute()

            return


        #
        # Copy parameters
        # to the real module.
        #

        self.copyParameters(
            parameters,
            module
        )


        #
        # Remove parameter object
        # from the module tree.
        #
        # We keep the parameters object
        # because it can be useful for
        # editing later.
        #

        parameters.Label = (
            "Parámetros"
        )


        #
        # Recompute module properties
        #

        document.recompute()


        #
        # Build module parts
        #

        try:

            ModuleBuilder.build(
                module
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error building parametric module: "
                + str(error)
                + "\n"
            )

            raise


        #
        # Final recompute
        #

        document.recompute()


        #
        # Fit view
        #

        try:

            FreeCADGui.activeDocument().activeView().fitAll()

        except Exception:

            pass


    #
    # Ensure module properties
    #

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
                "Thickness of structural panels"
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
                "Thickness of back panel"
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
                "Rear panel inset"
            )

            module.BackInset = (
                FreeCAD.Units.Quantity(
                    "0 mm"
                )
            )


    #
    # Copy parameters
    #

    def copyParameters(
        self,
        parameters,
        module
    ):

        #
        # Name
        #

        if hasattr(
            parameters,
            "ModuleName"
        ):

            name = str(
                parameters.ModuleName
            ).strip()


            if name:

                module.Label = name


        #
        # Type
        #

        if hasattr(
            parameters,
            "ModuleType"
        ):

            if hasattr(
                module,
                "Type"
            ):

                module.Type = (
                    parameters.ModuleType
                )


        #
        # Width
        #

        if hasattr(
            parameters,
            "ModuleWidth"
        ):

            if hasattr(
                module,
                "Width"
            ):

                module.Width = (
                    parameters.ModuleWidth
                )


        #
        # Height
        #

        if hasattr(
            parameters,
            "ModuleHeight"
        ):

            if hasattr(
                module,
                "Height"
            ):

                module.Height = (
                    parameters.ModuleHeight
                )


        #
        # Depth
        #

        if hasattr(
            parameters,
            "ModuleDepth"
        ):

            if hasattr(
                module,
                "Depth"
            ):

                module.Depth = (
                    parameters.ModuleDepth
                )


        #
        # Panel thickness
        #

        if hasattr(
            parameters,
            "PanelThickness"
        ):

            if hasattr(
                module,
                "PanelThickness"
            ):

                module.PanelThickness = (
                    parameters.PanelThickness
                )


        #
        # Back thickness
        #

        if hasattr(
            parameters,
            "BackThickness"
        ):

            if hasattr(
                module,
                "BackThickness"
            ):

                module.BackThickness = (
                    parameters.BackThickness
                )


        #
        # Back inset
        #

        if hasattr(
            parameters,
            "BackInset"
        ):

            if hasattr(
                module,
                "BackInset"
            ):

                module.BackInset = (
                    parameters.BackInset
                )


#
# Register command
#

FreeCADGui.addCommand(
    "Bosqo_ParametricModule",
    ParametricModuleCommand()
)