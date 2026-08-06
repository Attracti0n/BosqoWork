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
    # =========================================================
    # PROPERTIES
    # =========================================================
    #

    def initProperties(
        self,
        obj
    ):

        #
        # NAME
        #

        if not obj.Label:

            obj.Label = "Módulo"


        #
        # TYPE
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
        # TOP TYPE
        #

        if not hasattr(
            obj,
            "TopType"
        ):

            obj.addProperty(
                "App::PropertyEnumeration",
                "TopType",
                "Module",
                "Sistema superior del módulo"
            )

            obj.TopType = [

                "Tapa completa",
                "2 travesaños",
                "3 travesaños"

            ]

            obj.TopType = "Tapa completa"


        #
        # BACK TYPE
        #

        if not hasattr(
            obj,
            "BackType"
        ):

            obj.addProperty(
                "App::PropertyEnumeration",
                "BackType",
                "Module",
                "Sistema trasero del módulo"
            )

            obj.BackType = [

                "Trasera sobrepuesta",
                "Trasera oculta",
                "2 travesaños",
                "3 travesaños",
                "Sin trasera"

            ]

            obj.BackType = "Trasera sobrepuesta"


        #
        # DIMENSIONS
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
        # PANEL THICKNESS
        #

        self.addLength(
            obj,
            "PanelThickness",
            19,
            "Parameters"
        )


        #
        # BACK THICKNESS
        #

        self.addLength(
            obj,
            "BackThickness",
            10,
            "Parameters"
        )


        #
        # BACK INSET
        #

        self.addLength(
            obj,
            "BackInset",
            0,
            "Parameters"
        )


    #
    # =========================================================
    # HELPERS
    # =========================================================
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
    # =========================================================
    # DATA
    # =========================================================
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

            "TopType":
                obj.TopType,

            "BackType":
                obj.BackType,

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
    # =========================================================
    # PARTS
    # =========================================================
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
    # =========================================================
    # MODULE DATA
    # =========================================================
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
    # =========================================================
    # FREECAD
    # =========================================================
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

        rebuild_properties = {

            "Type",
            "TopType",
            "BackType",

            "Width",
            "Height",
            "Depth",

            "PanelThickness",
            "BackThickness",
            "BackInset"

        }

        if prop not in rebuild_properties:

            return

        required_properties = [

            "Type",
            "TopType",
            "BackType",

            "Width",
            "Height",
            "Depth",

            "PanelThickness",
            "BackThickness",
            "BackInset"

        ]

        for property_name in required_properties:

            if not hasattr(
                obj,
                property_name
            ):

                return

        try:

            ModuleBuilder.build(
                obj
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "BosqoModule rebuild error: "
                +
                str(error)
                +
                "\n"
            )


    #
    # =========================================================
    # ICON
    # =========================================================
    #

    def getIcon(
        self
    ):

        return os.path.join(
            ICONS_DIR,
            "module.svg"
        )


    #
    # =========================================================
    # SERIALIZATION
    # =========================================================
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
# =========================================================
# FACTORY
# =========================================================
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