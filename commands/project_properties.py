import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR
from utils.document_properties import initialize_project_properties
from dialogs.project_properties_dialog import ProjectPropertiesDialog


class ProjectPropertiesCommand:

    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONS_DIR, "project.svg"),
            "MenuText": "Datos del proyecto",
            "ToolTip": "Redactar los datos del proyecto"
        }

    def Activated(self):

        doc = FreeCAD.ActiveDocument

        if doc is None:
            FreeCAD.Console.PrintError(
                "No active document.\n"
            )
            return

        initialize_project_properties(doc)

        dialog = ProjectPropertiesDialog(doc)
        dialog.exec_()

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None


FreeCADGui.addCommand(
    "Bosqo_ProjectProperties",
    ProjectPropertiesCommand()
)