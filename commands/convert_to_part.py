import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR
from core.converters.part_converter import PartConverter


class ConvertToPartCommand:

    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "part.svg"
            ),

            "MenuText":
                "Convertir a Bosqo Part",

            "ToolTip":
                "Convert selected object to Bosqo Part"

        }

    def Activated(self):

        selection = FreeCADGui.Selection.getSelection()

        if len(selection) != 1:

            FreeCAD.Console.PrintError(
                "Select one object.\n"
            )

            return

        obj = selection[0]

        try:

            PartConverter.convert(obj)

            obj.Document.recompute()

        except Exception as e:

            FreeCAD.Console.PrintError(
                str(e) + "\n"
            )

    def IsActive(self):

        return (
            FreeCAD.ActiveDocument
            is not None
        )


FreeCADGui.addCommand(

    "Bosqo_ConvertPart",

    ConvertToPartCommand()

)