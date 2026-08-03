import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from core.analyzers.orientation_analyzer import OrientationAnalyzer


class AnalyzeOrientationCommand:

    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "analyze.svg"
            ),

            "MenuText": "Analyze Orientation",

            "ToolTip": "Analyze object orientation"

        }

    def Activated(self):

        selection = FreeCADGui.Selection.getSelection()

        if not selection:

            FreeCAD.Console.PrintError(
                "No object selected.\n"
            )

            return

        obj = selection[0]

        try:

            orientation = OrientationAnalyzer.analyze(
                obj
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                f"{error}\n"
            )

            return

        FreeCAD.Console.PrintMessage(
            "\n===== Orientation =====\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Length         : {orientation.Length}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Width          : {orientation.Width}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Thickness      : {orientation.Thickness}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Length Axis    : {orientation.LengthAxis}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Width Axis     : {orientation.WidthAxis}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Thickness Axis : {orientation.ThicknessAxis}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Center         : {orientation.Center}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Valid          : {orientation.IsValid}\n"
        )

    def IsActive(self):

        return FreeCAD.ActiveDocument is not None


FreeCADGui.addCommand(
    "Bosqo_AnalyzeOrientation",
    AnalyzeOrientationCommand()
)