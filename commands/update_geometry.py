import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from core.analyzers.panel_geometry_analyzer import PanelGeometryAnalyzer
from core.storage.geometry_storage import GeometryStorage



class UpdateGeometryCommand:


    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "analyze.svg"
            ),

            "MenuText": "Actualizar geometría",

            "ToolTip": "Analiza la geometría de la pieza seleccionada"

        }



    def Activated(self):


        selection = FreeCADGui.Selection.getSelection()


        if not selection:

            FreeCAD.Console.PrintError(
                "No hay ninguna pieza seleccionada.\n"
            )

            return



        obj = selection[0]



        FreeCAD.Console.PrintMessage(
            "Analizando: "
            + obj.Label
            + "\n"
        )



        try:

            geometry = PanelGeometryAnalyzer.analyze(
                obj
            )


            obj.GeometryData = (
                GeometryStorage.serialize(
                    geometry
                )
            )


            obj.GeometryStatus = "Analyzed"


            obj.Document.recompute()



            FreeCAD.Console.PrintMessage(
                "\n===== GEOMETRY UPDATED =====\n"
            )


            FreeCAD.Console.PrintMessage(
                "Length: "
                + str(geometry.Length)
                + "\n"
            )


            FreeCAD.Console.PrintMessage(
                "Width: "
                + str(geometry.Width)
                + "\n"
            )


            FreeCAD.Console.PrintMessage(
                "Thickness: "
                + str(geometry.Thickness)
                + "\n"
            )


            FreeCAD.Console.PrintMessage(
                "============================\n"
            )


        except Exception as error:


            FreeCAD.Console.PrintError(
                "Geometry update error: "
                + str(error)
                + "\n"
            )



    def IsActive(self):

        return FreeCAD.ActiveDocument is not None





FreeCADGui.addCommand(
    "Bosqo_UpdateGeometry",
    UpdateGeometryCommand()
)