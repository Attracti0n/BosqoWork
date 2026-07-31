import FreeCAD
import os

from constants import ICONS_DIR
from dialogs.module_dialog import ModuleDialog
from core.builders.module_builder import ModuleBuilder


class BosqoModule:

    def __init__(self, obj):

        obj.Proxy = self

        self.initProperties(obj)

        ViewProviderBosqoModule(obj.ViewObject)

    #
    # Properties
    #

    def initProperties(self, obj):

        if not obj.Label:
            obj.Label = "Module"

        #
        # Type
        #

        if not hasattr(obj, "Type"):

            obj.addProperty(
                "App::PropertyEnumeration",
                "Type",
                "Bosqo",
                "Module type"
            )

            obj.Type = [
                "Módulo bajo",
                "Módulo alto",
                "Columna",
                "Armario",
                "Personalizado"
            ]

            obj.Type = "Módulo bajo"

        #
        # Width
        #

        if not hasattr(obj, "Width"):

            obj.addProperty(
                "App::PropertyLength",
                "Width",
                "Bosqo",
                "Module width"
            )

            obj.Width = 600

        #
        # Height
        #

        if not hasattr(obj, "Height"):

            obj.addProperty(
                "App::PropertyLength",
                "Height",
                "Bosqo",
                "Module height"
            )

            obj.Height = 720

        #
        # Depth
        #

        if not hasattr(obj, "Depth"):

            obj.addProperty(
                "App::PropertyLength",
                "Depth",
                "Bosqo",
                "Module depth"
            )

            obj.Depth = 560

    #
    # Data
    #

    def getData(self, obj):

        return {

            "Label": obj.Label,
            "Type": obj.Type,
            "Width": obj.Width,
            "Height": obj.Height,
            "Depth": obj.Depth

        }

    def setData(self, obj, data):

        if "Label" in data:
            obj.Label = data["Label"]

        if "Type" in data:
            obj.Type = data["Type"]

        if "Width" in data:
            obj.Width = data["Width"]

        if "Height" in data:
            obj.Height = data["Height"]

        if "Depth" in data:
            obj.Depth = data["Depth"]

    #
    # FreeCAD
    #

    def execute(self, obj):

        #
        # The module itself has no geometry.
        #

        pass

    def onChanged(self, obj, prop):

        #
        # Nothing here.
        # Rebuild is performed only after editing
        # or module creation.
        #

        pass

    def getIcon(self):

        return os.path.join(
            ICONS_DIR,
            "module.svg"
        )

    def __getstate__(self):

        return None

    def __setstate__(self, state):

        return None


class ViewProviderBosqoModule:

    def __init__(self, view_object):

        view_object.Proxy = self

    def attach(self, view_object):

        pass

    def updateData(self, obj, prop):

        pass

    def onChanged(self, view_object, prop):

        pass

    def doubleClicked(self, view_object):

        obj = view_object.Object

        dialog = ModuleDialog(
            obj.Proxy.getData(obj)
        )

        if dialog.exec():

            obj.Proxy.setData(
                obj,
                dialog.getData()
            )

            ModuleBuilder.build(obj)

            obj.Document.recompute()

        return True

    def getIcon(self):

        return os.path.join(
            ICONS_DIR,
            "module.svg"
        )


#
# Factory
#

def create_module(doc, data):

    module = doc.addObject(
        "App::DocumentObjectGroupPython",
        "Module"
    )

    BosqoModule(module)

    module.Proxy.setData(
        module,
        data
    )

    ModuleBuilder.build(module)

    doc.recompute()

    return module