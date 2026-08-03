import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from core.analyzers.panel_geometry_analyzer import PanelGeometryAnalyzer


class AnalyzeGeometryCommand:


    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "analyze.svg"
            ),

            "MenuText": "Analyze Geometry",

            "ToolTip": "Analyze complete panel geometry"

        }



    def Activated(self):


        selection = FreeCADGui.Selection.getSelection()


        if not selection:

            FreeCAD.Console.PrintError(
                "No object selected.\n"
            )

            return



        obj = selection[0]


        geometry = PanelGeometryAnalyzer.analyze(
            obj
        )



        FreeCAD.Console.PrintMessage(
            "\n===== PANEL GEOMETRY =====\n"
        )


        #
        # Dimensions
        #

        FreeCAD.Console.PrintMessage(
            "\n--- Dimensions ---\n"
        )


        FreeCAD.Console.PrintMessage(
            f"Length    : {geometry.Length}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Width     : {geometry.Width}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Thickness : {geometry.Thickness}\n"
        )



        #
        # Axis
        #

        FreeCAD.Console.PrintMessage(
            "\n--- Axis ---\n"
        )


        FreeCAD.Console.PrintMessage(
            f"Length Axis    : {geometry.LengthAxis}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Width Axis     : {geometry.WidthAxis}\n"
        )

        FreeCAD.Console.PrintMessage(
            f"Thickness Axis : {geometry.ThicknessAxis}\n"
        )



        #
        # Faces
        #

        FreeCAD.Console.PrintMessage(
            "\n--- Faces ---\n"
        )


        for face in geometry.Faces:


            FreeCAD.Console.PrintMessage(
                f"\n{face.Name}\n"
            )


            if face.Face is None:

                FreeCAD.Console.PrintMessage(
                    "Not detected\n"
                )

                continue


            FreeCAD.Console.PrintMessage(
                f"Area   : {face.Area}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Center : {face.Center}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Normal : {face.Normal}\n"
            )



        #
        # Edges
        #

        FreeCAD.Console.PrintMessage(
            "\n--- Edges ---\n"
        )


        for edge in geometry.Edges:


            FreeCAD.Console.PrintMessage(
                f"\n{edge.Name}\n"
            )


            if edge.Edge is None:

                FreeCAD.Console.PrintMessage(
                    "Not detected\n"
                )

                continue


            FreeCAD.Console.PrintMessage(
                f"Length : {edge.Length}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Axis   : {edge.Axis}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Center : {edge.Center}\n"
            )



        FreeCAD.Console.PrintMessage(
            "\n===== ANALYSIS FINISHED =====\n"
        )



    def IsActive(self):

        return FreeCAD.ActiveDocument is not None




FreeCADGui.addCommand(
    "Bosqo_AnalyzeGeometry",
    AnalyzeGeometryCommand()
)