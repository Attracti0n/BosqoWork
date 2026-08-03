import FreeCAD
import FreeCADGui

from dialogs.module_dialog import ModuleDialog
from objects.bosqo_module import create_module


class CreateModuleFromSelectionCommand:


    def GetResources(self):

        return {

            "Pixmap": "",

            "MenuText": "Crear módulo desde selección",

            "ToolTip": "Crear un módulo Bosqo con las piezas seleccionadas"

        }


    def Activated(self):

        selection = self.getSelectedParts()

        if not selection:

            FreeCAD.Console.PrintError(
                "Seleccione una o más BosqoPart.\n"
            )

            return


        #
        # Document
        #

        doc = selection[0].Document


        #
        # Calculate bounding box
        #

        bbox = None

        for part in selection:

            if bbox is None:

                bbox = part.Shape.BoundBox

            else:

                bbox.add(
                    part.Shape.BoundBox
                )


        #
        # Default values
        #

        data = {

            "Label": "Nuevo módulo",

            "Type": "Personalizado",

            "Width": bbox.XLength,

            "Height": bbox.ZLength,

            "Depth": bbox.YLength

        }


        #
        # Dialog
        #

        dialog = ModuleDialog(
            data
        )

        if not dialog.exec():

            return


        data = dialog.getData()


        #
        # Create module
        #

        module = create_module(
            doc,
            data
        )


        #
        # Add parts
        #

        for part in selection:

            module.Proxy.addPart(
                module,
                part
            )


        doc.recompute()

        FreeCAD.Console.PrintMessage(

            f"Module '{module.Label}' created with "
            f"{len(selection)} parts.\n"

        )


    def getSelectedParts(self):

        result = []

        for obj in FreeCADGui.Selection.getSelection():

            if not hasattr(obj, "Proxy"):

                continue

            if obj.Proxy is None:

                continue

            if type(obj.Proxy).__name__ != "BosqoPart":

                continue

            result.append(
                obj
            )

        return result


    def IsActive(self):

        return FreeCAD.ActiveDocument is not None


FreeCADGui.addCommand(

    "Bosqo_CreateModuleFromSelection",

    CreateModuleFromSelectionCommand()

)