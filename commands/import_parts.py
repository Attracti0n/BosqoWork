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




        #
        # Convert selected objects
        #

        parts = ImportBuilder.build(
            document,
            selection
        )



        #
        # Remove original objects
        # only if converted successfully
        #

        removed = 0



        for part in parts:


            if hasattr(part, "OriginalObject"):


                original = part.OriginalObject



                if original:


                    try:


                        document.removeObject(
                            original.Name
                        )


                        removed += 1



                    except Exception as error:


                        FreeCAD.Console.PrintWarning(
                            f"Cannot remove {original.Label}: {error}\n"
                        )



        document.recompute()



        FreeCAD.Console.PrintMessage(
            "\n===== IMPORT COMMAND =====\n"
        )


        FreeCAD.Console.PrintMessage(
            f"Created Bosqo Parts: {len(parts)}\n"
        )


        FreeCAD.Console.PrintMessage(
            f"Original objects removed: {removed}\n"
        )



    def IsActive(self):

        return FreeCAD.ActiveDocument is not None




FreeCADGui.addCommand(
    "Bosqo_ImportParts",
    ImportPartsCommand()
)