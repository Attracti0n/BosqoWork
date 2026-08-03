import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from core.analyzers.plane_analyzer import PlaneAnalyzer


class AnalyzePlanesCommand:

    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "analyze.svg"
            ),

            "MenuText": "Analyze Planes",

            "ToolTip": "Analyze planar faces"

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

            planes = PlaneAnalyzer.analyze(
                obj
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                f"{error}\n"
            )

            return

        FreeCAD.Console.PrintMessage(
            "\n===== PLANES =====\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Planes found : {len(planes)}\n\n"
        )

        for index, plane in enumerate(planes, start=1):

            FreeCAD.Console.PrintMessage(
                f"Plane {index}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Area        : {plane.Area}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Center      : {plane.Center}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Normal      : {plane.Normal}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"SurfaceType : {plane.SurfaceType}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"IsPlane     : {plane.IsPlane}\n"
            )

            FreeCAD.Console.PrintMessage(
                "-----------------------------\n"
            )

    def IsActive(self):

        return FreeCAD.ActiveDocument is not None


FreeCADGui.addCommand(
    "Bosqo_AnalyzePlanes",
    AnalyzePlanesCommand()
)