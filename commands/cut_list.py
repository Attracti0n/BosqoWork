import FreeCAD
import FreeCADGui

from core.data.module_data import ModuleData
from core.data.module_manufacturing_data import ModuleManufacturingData
from core.reports.cutlist_generator import CutListGenerator

from dialogs.cut_list_dialog import CutListDialog


class CutListCommand:


    def GetResources(self):

        return {

            "Pixmap": "",

            "MenuText": "Cut List",

            "ToolTip": "Generate cut list"

        }


    def Activated(self):

        selection = FreeCADGui.Selection.getSelection()

        if not selection:

            FreeCAD.Console.PrintError(
                "No module selected.\n"
            )

            return


        module = selection[0]


        #
        # Module -> ModuleData
        #

        moduleData = ModuleData()

        moduleData.fromObject(
            module
        )


        #
        # ModuleData -> Manufacturing
        #

        manufacturing = ModuleManufacturingData()

        manufacturing.fromModuleData(
            moduleData
        )


        #
        # Manufacturing -> CutList
        #

        generator = CutListGenerator()

        cutlist = generator.generate(
            manufacturing
        )


        #
        # Show dialog
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