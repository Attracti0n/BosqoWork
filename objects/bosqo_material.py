import FreeCAD
import os

from app_paths import ICONS_DIR


class BosqoMaterial:

    def __init__(
        self,
        obj
    ):

        obj.Proxy = self

        self.initProperties(
            obj
        )

        ViewProviderBosqoMaterial(
            obj.ViewObject
        )


    #
    # Properties
    #

    def initProperties(
        self,
        obj
    ):

        if not obj.Label:

            obj.Label = "Material"


        #
        # Identification
        #

        self.addString(
            obj,
            "Code",
            "",
            "Identification"
        )

        self.addString(
            obj,
            "MaterialName",
            "",
            "Identification"
        )

        self.addEnumeration(
            obj,
            "MaterialType",
            [
                "Tablero",
                "Canto",
                "Herraje",
                "Consumible",
                "Embalaje",
                "Otro"
            ],
            "Tablero",
            "Identification"
        )

        self.addString(
            obj,
            "Category",
            "",
            "Identification"
        )


        #
        # Dimensions
        #

        self.addLength(
            obj,
            "Thickness",
            0,
            "Dimensions"
        )

        self.addLength(
            obj,
            "SheetLength",
            2800,
            "Dimensions"
        )

        self.addLength(
            obj,
            "SheetWidth",
            2070,
            "Dimensions"
        )


        #
        # Supplier
        #

        self.addString(
            obj,
            "Supplier",
            "",
            "Supplier"
        )


        #
        # Finish
        #

        self.addString(
            obj,
            "Finish",
            "",
            "Finish"
        )

        self.addString(
            obj,
            "GrainDirection",
            "",
            "Finish"
        )

        self.addString(
            obj,
            "ColorCode",
            "",
            "Finish"
        )

        self.addString(
            obj,
            "TexturePath",
            "",
            "Finish"
        )


        #
        # Cost
        #

        self.addFloat(
            obj,
            "Price",
            0.0,
            "Cost"
        )

        self.addEnumeration(
            obj,
            "PriceUnit",
            [
                "€/m²",
                "€/m",
                "€/ud"
            ],
            "€/m²",
            "Cost"
        )


        #
        # Helpers
        #


    def addString(
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
                "App::PropertyString",
                name,
                group
            )

            setattr(
                obj,
                name,
                value
            )


    def addEnumeration(
        self,
        obj,
        name,
        values,
        default,
        group
    ):

        if not hasattr(
            obj,
            name
        ):

            obj.addProperty(
                "App::PropertyEnumeration",
                name,
                group
            )

            setattr(
                obj,
                name,
                values
            )

            if default in values:

                setattr(
                    obj,
                    name,
                    default
                )


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


    def addFloat(
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
                "App::PropertyFloat",
                name,
                group
            )

            setattr(
                obj,
                name,
                value
            )


    #
    # Data
    #

    def getData(
        self,
        obj
    ):

        return {

            "Code":
                obj.Code,

            "MaterialName":
                obj.MaterialName,

            "MaterialType":
                obj.MaterialType,

            "Category":
                obj.Category,

            "Thickness":
                obj.Thickness,

            "SheetLength":
                obj.SheetLength,

            "SheetWidth":
                obj.SheetWidth,

            "Supplier":
                obj.Supplier,

            "Finish":
                obj.Finish,

            "GrainDirection":
                obj.GrainDirection,

            "ColorCode":
                obj.ColorCode,

            "TexturePath":
                obj.TexturePath,

            "Price":
                obj.Price,

            "PriceUnit":
                obj.PriceUnit

        }


    def setData(
        self,
        obj,
        data
    ):

        for key, value in data.items():

            if not hasattr(
                obj,
                key
            ):

                continue


            if key in (
                "Thickness",
                "SheetLength",
                "SheetWidth"
            ):

                value = abs(
                    value
                )


            setattr(
                obj,
                key,
                value
            )


    #
    # FreeCAD
    #

    def execute(
        self,
        obj
    ):

        pass


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


class ViewProviderBosqoMaterial:

    def __init__(
        self,
        view_object
    ):

        view_object.Proxy = self


    def getIcon(
        self
    ):

        return os.path.join(
            ICONS_DIR,
            "material.svg"
        )


#
# Factory
#

def create_material(
    doc
):

    material = doc.addObject(
        "App::FeaturePython",
        "BosqoMaterial"
    )

    BosqoMaterial(
        material
    )

    return material