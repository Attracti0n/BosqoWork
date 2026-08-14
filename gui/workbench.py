import os

import FreeCADGui

import commands.add_part
import commands.project_properties
from commands.bosqo_drawer import (
    BosqoDrawerCommand
)
from commands.bosqo_finish import register as register_finish

register_finish()


ICON_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "resources",
    "icons",
    "bosqo.svg"
)



class BosqoWorkbench(FreeCADGui.Workbench):
    """BosqoWork Workbench"""


    MenuText = "BosqoWork"

    ToolTip = "Proyectista de muebles"

    Icon = ICON_PATH



    def Initialize(self):
        """Called once when FreeCAD starts."""



        #
        # Main toolbar
        #

        self.appendToolbar(
            "Crear",
            [
                "Bosqo_AddPart",
                "Bosqo_ParametricModule",
                "Bosqo_Drawer",
                "Bosqo_ModulePlacement",
                "Bosqo_ProjectProperties",
                "Bosqo_PartsTable",
                "Bosqo_Materials",
                "Bosqo_Finish"
            ]
        )

        self.appendToolbar(
            "Fabricación",
            [
                "Bosqo_CutList",
                "Bosqo_CutListReport",
                "Bosqo_BOM"
            ]
        )


        #
        # Main menu
        #

        self.appendMenu(
            "Crear",
            [
                "Bosqo_AddPart",
                "Bosqo_ParametricModule",
                "Bosqo_Drawer",
                "Bosqo_ModulePlacement",
                "Bosqo_ProjectProperties",
                "Bosqo_PartsTable",
                "Bosqo_Materials",
                "Bosqo_Finish"
            ]
        )

        self.appendMenu(
            "Fabricación",
            [
                "Bosqo_CutList",
                "Bosqo_CutListReport",
                "Bosqo_BOM"
            ]
        )


    def Activated(self):

        pass



    def Deactivated(self):

        pass



    def GetClassName(self):

        return "Gui::PythonWorkbench"

