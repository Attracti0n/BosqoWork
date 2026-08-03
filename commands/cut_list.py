import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR


from core.data.module_data import ModuleData
from core.data.module_manufacturing_data import ModuleManufacturingData

from core.data.project_data import ProjectData
from core.data.project_manufacturing_data import ProjectManufacturingData


from core.reports.cutlist_generator import CutListGenerator

from dialogs.cut_list_dialog import CutListDialog



class CutListCommand:


    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "cutting.svg"
            ),

            "MenuText": "Cut List",

            "ToolTip": "Crear cut list"

        }



    def Activated(self):


        selection = FreeCADGui.Selection.getSelection()


        if not selection:


            FreeCAD.Console.PrintError(
                "No object selected.\n"
            )

            return



        obj = selection[0]



        manufacturing = None



        #
        # Bosqo Module
        #

        if hasattr(obj, "Proxy") and obj.Proxy.__class__.__name__ == "BosqoModule":


            moduleData = ModuleData()


            moduleData.fromObject(
                obj
            )


            manufacturing = ModuleManufacturingData()


            manufacturing.fromModuleData(
                moduleData
            )



        #
        # Imported project / BosqoParts
        #

        else:


            project = ProjectData()


            project.fromDocument()



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
        # Dialog
        #

        dialog = CutListDialog(
            cutlist
        )


        dialog.exec_()



    def IsActive(self):

        return FreeCAD.ActiveDocument is not None





FreeCADGui.addCommand(
    "Bosqo_CutList",
    CutListCommand()
)