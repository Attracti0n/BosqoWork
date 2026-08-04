import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from dialogs.material_library_dialog import MaterialLibraryDialog


class MaterialsCommand:

    def GetResources(
        self
    ):

        return {
            "Pixmap":
                os.path.join(
                    ICONS_DIR,
                    "material.svg"
                ),

            "MenuText":
                "Materiales",

            "ToolTip":
                "Abrir biblioteca de materiales",

            "Accel":
                ""
        }


    def IsActive(
        self
    ):

        return True


    def Activated(
        self
    ):

        dialog = MaterialLibraryDialog()

        dialog.exec_()


FreeCADGui.addCommand(
    "Bosqo_Materials",
    MaterialsCommand()
)