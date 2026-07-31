import FreeCAD
import FreeCADGui
import os

from constants import ICONS_DIR

from core.recognizers.panel_recognizer import PanelRecognizer


class AnalyzePanelCommand:

    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "analyze.svg"
            ),

            "MenuText": "Analyze Panel",

            "ToolTip": "Recognize panel"

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

            panel = PanelRecognizer.recognize(obj)

        except Exception as error:

            FreeCAD.Console.PrintError(
                f"{error}\n"
            )

            return

        FreeCAD.Console.PrintMessage(
            "\n===== PANEL =====\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Is Panel : {panel.IsPanel}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Message  : {panel.Message}\n"
        )

        if not panel.IsPanel:

            return

        FreeCAD.Console.PrintMessage("\nGeometry\n")
        FreeCAD.Console.PrintMessage(
            f"Length    : {panel.Length}\n"
        )
        FreeCAD.Console.PrintMessage(
            f"Width     : {panel.Width}\n"
        )
        FreeCAD.Console.PrintMessage(
            f"Thickness : {panel.Thickness}\n"
        )

        if panel.Center is not None:

            FreeCAD.Console.PrintMessage(
                f"Center    : {panel.Center}\n"
            )

        #
        # Only Shape objects have BRep planes
        #

        if panel.FrontPlane is not None:

            FreeCAD.Console.PrintMessage(
                "\nFront Plane\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Area   : {panel.FrontPlane.Area}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Center : {panel.FrontPlane.Center}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Normal : {panel.FrontPlane.Normal}\n"
            )

        if panel.BackPlane is not None:

            FreeCAD.Console.PrintMessage(
                "\nBack Plane\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Area   : {panel.BackPlane.Area}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Center : {panel.BackPlane.Center}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Normal : {panel.BackPlane.Normal}\n"
            )

    def IsActive(self):

        return FreeCAD.ActiveDocument is not None


FreeCADGui.addCommand(
    "Bosqo_AnalyzePanel",
    AnalyzePanelCommand()
)