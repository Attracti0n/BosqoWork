import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from objects.bosqo_part import create_part

from dialogs.part_dialog import PartDialog



class AddPartCommand:


    def GetResources(self):

        return {

            "Pixmap":
                os.path.join(
                    ICONS_DIR,
                    "part.svg"
                ),

            "MenuText":
                "Nueva pieza",

            "ToolTip":
                "Crear una nueva pieza"

        }


    def Activated(self):

        doc = FreeCAD.ActiveDocument


        if doc is None:

            doc = FreeCAD.newDocument(
                "Bosqo"
            )


        dialog = PartDialog()


        result = dialog.exec_()


        if result != 1:

            return


        data = dialog.getData()


        part = create_part(
            doc
        )


        #
        # Apply data
        #

        for key, value in data.items():

            if hasattr(
                part,
                key
            ):

                setattr(
                    part,
                    key,
                    value
                )


        #
        # Update
        #

        doc.recompute()


        FreeCADGui.activeDocument().activeView().fitAll()



    def IsActive(self):

        return FreeCAD.ActiveDocument is not None



FreeCADGui.addCommand(
    "Bosqo_AddPart",
    AddPartCommand()
)