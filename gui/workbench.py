import os

import FreeCADGui

import commands.add_module
import commands.add_part
import commands.project_properties

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

        self.appendToolbar(
            "Bosqo",
            [
                "Bosqo_AddModule",
                "Bosqo_ProjectProperties",
                "Bosqo_AddPart",
                "Bosqo_AnalyzeGeometry",
                "Bosqo_ImportParts",
                "Bosqo_AnalyzeOrientation",
                "Bosqo_AnalyzePlanes",
                "Bosqo_AnalyzePanel",
            ]
    )
        self.appendMenu(
            "BosqoWork",
            [
                "Bosqo_AddModule",
                "Bosqo_ProjectProperties",
                "Bosqo_AddPart",
                "Bosqo_AnalyzeGeometry",
                "Bosqo_ImportParts",
                "Bosqo_AnalyzeOrientation",
                "Bosqo_AnalyzePlanes",
                "Bosqo_AnalyzePanel",
            ]
        )

    def Activated(self):
        """Called when the workbench becomes active."""
        pass

    def Deactivated(self):
        """Called when the workbench is deactivated."""
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"

