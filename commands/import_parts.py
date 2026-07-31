import FreeCAD
import FreeCADGui
import os

from constants import ICONS_DIR

from core.builders.import_builder import ImportBuilder


class ImportPartsCommand:

    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "import_parts.svg"
            ),

            "MenuText": "Convert to Bosqo Parts",

            "ToolTip": "Convert selected objects to Bosqo Parts"

        }


    def Activated(self):

        document = FreeCAD.ActiveDocument

        if document is None:

            FreeCAD.Console.PrintError(
                "No active document.\n"
            )

            return

        selection = FreeCADGui.Selection.getSelection()

        if not selection:

            FreeCAD.Console.PrintError(
                "No objects selected.\n"
            )

            return

        parts = ImportBuilder.build(
            document,
            selection
        )

        document.recompute()

        FreeCAD.Console.PrintMessage(
            f"{len(parts)} Bosqo Parts created.\n"
        )


    def IsActive(self):

        return FreeCAD.ActiveDocument is not None


FreeCADGui.addCommand(
    "Bosqo_ImportParts",
    ImportPartsCommand()
)