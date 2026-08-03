import os

import FreeCADGui

import commands.add_module
import commands.add_part
import commands.project_properties
import commands.import_parts


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
            "Bosqo",
            [
                "Bosqo_AddModule",
                "Bosqo_AddPart",
                "Bosqo_ProjectProperties",
                "Bosqo_ImportParts",
                "Bosqo_CutList",
                "Bosqo_CutListReport",
                "Bosqo_CreateModuleFromSelection",
            ]
        )



        #
        # Main menu
        #

        self.appendMenu(
            "BosqoWork",
            [
                "Bosqo_AddModule",
                "Bosqo_AddPart",
                "Bosqo_ProjectProperties",
                "Bosqo_ImportParts",
                "Bosqo_CutList",
                "Bosqo_CutListReport",
                "Bosqo_CreateModuleFromSelection",
            ]
        )



        #
        # Development tools
        #
        # Later we can create:
        #
        # BosqoWork
        #   └── Tools
        #          ├── Analyze Geometry
        #          ├── Analyze Panel
        #          └── Diagnostics
        #
        # For now hidden from normal workflow.
        #



    def Activated(self):

        pass



    def Deactivated(self):

        pass



    def GetClassName(self):

        return "Gui::PythonWorkbench"

