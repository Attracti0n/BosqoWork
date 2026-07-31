import FreeCAD
import FreeCADGui
import os

from constants import ICONS_DIR

from dialogs.module_dialog import ModuleDialog

from objects.bosqo_module import create_module



class AddModuleCommand:


    def GetResources(self):

        return {

            "Pixmap": os.path.join(
                ICONS_DIR,
                "module.svg"
            ),

            "MenuText": "Añadir módulo",

            "ToolTip": "Crear un nuevo módulo"

        }


    def Activated(self):

        doc = FreeCAD.ActiveDocument


        if doc is None:

            FreeCAD.Console.PrintError(
                "No active document.\n"
            )

            return


        dialog = ModuleDialog()


        if dialog.exec_():


            data = dialog.getData()


            create_module(
                doc,
                data
            )


            doc.recompute()


            FreeCADGui.activeDocument().activeView().fitAll()



    def IsActive(self):

        return FreeCAD.ActiveDocument is not None



FreeCADGui.addCommand(
    "Bosqo_AddModule",
    AddModuleCommand()
)