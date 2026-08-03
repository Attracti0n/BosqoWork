import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from core.builders.edge_builder import EdgeBuilder


class AnalyzeEdgesCommand:


    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "analyze.svg"
            ),

            "MenuText": "Analyze Edges",

            "ToolTip": "Analyze panel edges"

        }


    def Activated(self):

        selection = FreeCADGui.Selection.getSelection()

        if not selection:

            FreeCAD.Console.PrintError(
                "No object selected.\n"
            )

            return


        obj = selection[0]


        edges = EdgeBuilder.build(obj)


        FreeCAD.Console.PrintMessage(
            "\n===== EDGE ANALYSIS =====\n"
        )


        for edge in edges:


            FreeCAD.Console.PrintMessage(
                f"\n{edge.Name}\n"
            )


            if edge.Edge is None:

                FreeCAD.Console.PrintWarning(
                    "Not found\n"
                )

                continue


            FreeCAD.Console.PrintMessage(
                f"Length : {edge.Length}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Center : {edge.Center}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Start  : {edge.Start}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"End    : {edge.End}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Axis   : {edge.Axis}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Visible: {edge.Visible}\n"
            )


    def IsActive(self):

        return FreeCAD.ActiveDocument is not None


FreeCADGui.addCommand(
    "Bosqo_AnalyzeEdges",
    AnalyzeEdgesCommand()
)