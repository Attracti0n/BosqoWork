import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from core.data.module_data import ModuleData
from core.data.module_manufacturing_data import ModuleManufacturingData

from core.reports.bom_generator import BOMGenerator

from dialogs.bom_dialog import BOMDialog


class BOMCommand:


    def GetResources(self):

        return {

            "Pixmap":                 
                os.path.join(
                ICONS_DIR,
                "bom.svg"
            ),

            "MenuText": "Bill of Materials",

            "ToolTip": "Generate Bill of Materials"

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
        # Manufacturing -> BOM
        #

        generator = BOMGenerator()

        bom = generator.generate(
            manufacturing
        )


        #
        # Show dialog
        #

        dialog = BOMDialog(
            bom
        )

        dialog.exec_()


    def IsActive(self):

        return FreeCAD.ActiveDocument is not None


FreeCADGui.addCommand(

    "Bosqo_BOM",

    BOMCommand()

)