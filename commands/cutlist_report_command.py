import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from core.data.project_data import ProjectData
from core.data.project_manufacturing_data import ProjectManufacturingData
from core.reports.cutlist_generator import CutListGenerator
from core.reports.cutlist_report import CutListReport



class CutListReportCommand:


    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "report_fabrication.svg"
            ),

            "MenuText": "Informe de fabricación",

            "ToolTip": "Genera informe de lista de corte"

        }



    def Activated(self):


        if FreeCAD.ActiveDocument is None:

            FreeCAD.Console.PrintError(
                "No hay documento abierto.\n"
            )

            return



        #
        # Project Data
        #

        project = ProjectData()

        project.fromDocument()



        #
        # Manufacturing Data
        #

        manufacturing = ProjectManufacturingData()

        manufacturing.fromProjectData(
            project
        )



        #
        # Generate CutList
        #

        generator = CutListGenerator()

        cutlist = generator.generate(
            manufacturing
        )



        #
        # Report
        #

        report = CutListReport()

        filename = report.generateHTML(
            cutlist
        )



        report.openHTML(
            filename
        )



        FreeCAD.Console.PrintMessage(

            "Informe generado:\n"

            + filename

            + "\n"

        )



    def IsActive(self):

        return FreeCAD.ActiveDocument is not None





FreeCADGui.addCommand(
    "Bosqo_CutListReport",
    CutListReportCommand()
)