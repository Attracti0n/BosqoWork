import FreeCAD
import FreeCADGui
import os

from constants import ICONS_DIR

from core.analyzers.geometry_analyzer import GeometryAnalyzer


class AnalyzeGeometryCommand:


    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "analyze.svg"
            ),

            "MenuText": "Analyze Geometry",

            "ToolTip": "Analyze selected geometry"

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

            data = GeometryAnalyzer.analyze(
                obj
            )

            FreeCAD.Console.PrintMessage(
                "\n"
            )

            FreeCAD.Console.PrintMessage(
                "===== Geometry =====\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Length      : {data.Length}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Width       : {data.Width}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Thickness   : {data.Thickness}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Orientation : {data.Orientation}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Area        : {data.Area}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Volume      : {data.Volume}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Faces       : {data.Faces}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Edges       : {data.Edges}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Vertices    : {data.Vertices}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Solid       : {data.IsSolid}\n"
            )

            FreeCAD.Console.PrintMessage(
                "====================\n"
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                str(error) + "\n"
            )


    def IsActive(self):

        return True


FreeCADGui.addCommand(
    "Bosqo_AnalyzeGeometry",
    AnalyzeGeometryCommand()
)