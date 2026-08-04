import FreeCAD
import os

from app_paths import ICONS_DIR

from dialogs.module_dialog import ModuleDialog
from core.builders.module_builder import ModuleBuilder


class BosqoModule:

    def __init__(
        self,
        obj
    ):

        obj.Proxy = self

        self.initProperties(
            obj
        )

        ViewProviderBosqoModule(
            obj.ViewObject
        )


    #
    # Properties
    #

    def initProperties(
        self,
        obj
    ):

        #
        # Name
        #

        if not obj.Label:

            obj.Label = "Módulo"


        #
        # Type
        #

        if not hasattr(
            obj,
            "Type"
        ):

            obj.addProperty(
                "App::PropertyEnumeration",
                "Type",
                "Module",
                "Tipo de módulo"
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
        # Dimensions
        #

        self.addLength(
            obj,
            "Width",
            600,
            "Parameters"
        )

        self.addLength(
            obj,
            "Height",
            720,
            "Parameters"
        )

        self.addLength(
            obj,
            "Depth",
            560,
            "Parameters"
        )


        #
        # Panel thickness
        #

        self.addLength(
            obj,
            "PanelThickness",
            19,
            "Parameters"
        )


        #
        # Back thickness
        #

        self.addLength(
            obj,
            "BackThickness",
            10,
            "Parameters"
        )


        #
        # Back inset
        #

        self.addLength(
            obj,
            "BackInset",
            0,
            "Parameters"
        )


    #
    # Helpers
    #

    def addLength(
        self,
        obj,
        name,
        value,
        group
    ):

        if not hasattr(
            obj,
            name
        ):

            obj.addProperty(
                "App::PropertyLength",
                name,
                group
            )

            setattr(
                obj,
                name,
                FreeCAD.Units.Quantity(
                    f"{value} mm"
                )
            )


    #
    # Data
    #

    def getData(
        self,
        obj
    ):

        return {

            "Label":
                obj.Label,

            "Type":
                obj.Type,

            "Width":
                obj.Width,

            "Height":
                obj.Height,

            "Depth":
                obj.Depth,

            "PanelThickness":
                obj.PanelThickness,

            "BackThickness":
                obj.BackThickness,

            "BackInset":
                obj.BackInset

        }


    def setData(
        self,
        obj,
        data
    ):

        for key, value in data.items():

            if hasattr(
                obj,
                key
            ):

                setattr(
                    obj,
                    key,
                    value
                )


    #
    # Parts
    #

    def addPart(
        self,
        obj,
        part
    ):

        if part not in obj.Group:

            obj.addObject(
                part
            )


    def removePart(
        self,
        obj,
        part
    ):

        if part in obj.Group:

            obj.removeObject(
                part
            )


    def getParts(
        self,
        obj
    ):

        return list(
            obj.Group
        )


    #
    # Module Data
    #

    def getModuleData(
        self,
        obj
    ):

        from core.data.module_data import ModuleData

        data = ModuleData()

        return data.fromObject(
            obj
        )


    #
    # FreeCAD
    #

    def execute(
        self,
        obj
    ):

        pass


    def onChanged(
        self,
        obj,
        prop
    ):

        pass


    #
    # Icon
    #

    def getIcon(
        self
    ):

        return os.path.join(
            ICONS_DIR,
            "module.svg"
        )


    #
    # Serialization
    #

    def __getstate__(
        self
    ):

        return None


    def __setstate__(
        self,
        state
    ):

        return None


class ViewProviderBosqoModule:

    def __init__(
        self,
        view_object
    ):

        view_object.Proxy = self


    def attach(
        self,
        view_object
    ):

        pass


    def updateData(
        self,
        obj,
        prop
    ):

        pass


    def onChanged(
        self,
        view_object,
        prop
    ):

        pass


    def doubleClicked(
        self,
        view_object
    ):

        obj = view_object.Object

        dialog = ModuleDialog(
            obj.Proxy.getData(
                obj
            )
        )

        if dialog.exec():

            obj.Proxy.setData(
                obj,
                dialog.getData()
            )

            ModuleBuilder.build(
                obj
            )

            obj.Document.recompute()

        return True


    def getIcon(
        self
    ):

        return os.path.join(
            ICONS_DIR,
            "module.svg"
        )


#
# Factory
#

def create_module(
    doc,
    data=None
):

    module = doc.addObject(
        "App::DocumentObjectGroupPython",
        "BosqoModule"
    )

    BosqoModule(
        module
    )

    if data:

        module.Proxy.setData(
            module,
            data
        )

    return module