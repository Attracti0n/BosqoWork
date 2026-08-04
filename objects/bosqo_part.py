import FreeCAD
import os

from app_paths import ICONS_DIR

from library.material_library import MaterialLibrary

from core.builders.geometry_builder import GeometryBuilder
from core.builders.placement_builder import PlacementBuilder



class BosqoPart:


    def __init__(
        self,
        obj
    ):

        obj.Proxy = self

        self.initProperties(
            obj
        )

        ViewProviderBosqoPart(
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

            obj.Label = "Part"



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
            "PartType",
            "",
            "Identification"
        )


        self.addString(
            obj,
            "Role",
            "",
            "Identification"
        )



        #
        # Dimensions
        #

        self.addLength(
            obj,
            "Length",
            0,
            "Dimensions"
        )


        self.addLength(
            obj,
            "Width",
            0,
            "Dimensions"
        )


        self.addLength(
            obj,
            "Thickness",
            0,
            "Dimensions"
        )



        #
        # Position
        #

        self.addLength(
            obj,
            "baseX",
            0,
            "Geometry"
        )


        self.addLength(
            obj,
            "baseY",
            0,
            "Geometry"
        )


        self.addLength(
            obj,
            "baseZ",
            0,
            "Geometry"
        )



        #
        # Axis mapping
        #

        self.addString(
            obj,
            "LengthAxis",
            "Z",
            "Geometry"
        )


        self.addString(
            obj,
            "WidthAxis",
            "X",
            "Geometry"
        )


        self.addString(
            obj,
            "ThicknessAxis",
            "Y",
            "Geometry"
        )



        #
        # Geometry analysis
        #

        self.addString(
            obj,
            "GeometryStatus",
            "Not analyzed",
            "Geometry"
        )


        self.addString(
            obj,
            "GeometryData",
            "",
            "Geometry"
        )



        #
        # Material
        #

        if not hasattr(
            obj,
            "MaterialCode"
        ):


            obj.addProperty(
                "App::PropertyEnumeration",
                "MaterialCode",
                "Material",
                "Material selection"
            )


            obj.MaterialCode = [
                ""
            ] + MaterialLibrary.codes()



        self.addString(
            obj,
            "Material",
            "",
            "Material"
        )


        self.addLength(
            obj,
            "MaterialThickness",
            0,
            "Material"
        )


        self.addString(
            obj,
            "MaterialSupplier",
            "",
            "Material"
        )


        self.addFloat(
            obj,
            "MaterialPrice",
            0,
            "Material"
        )


        self.addString(
            obj,
            "GrainDirection",
            "",
            "Material"
        )



        #
        # Edgebanding
        #

        self.addString(
            obj,
            "EdgeTop",
            "",
            "Edgebanding"
        )


        self.addString(
            obj,
            "EdgeBottom",
            "",
            "Edgebanding"
        )


        self.addString(
            obj,
            "EdgeLeft",
            "",
            "Edgebanding"
        )


        self.addString(
            obj,
            "EdgeRight",
            "",
            "Edgebanding"
        )



        #
        # Original object
        #

        if not hasattr(
            obj,
            "OriginalObject"
        ):


            obj.addProperty(
                "App::PropertyLink",
                "OriginalObject",
                "Bosqo",
                "Original imported object"
            )



        #
        # Source
        #

        self.addString(
            obj,
            "Source",
            "",
            "Bosqo"
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
                    f"{abs(value)} mm"
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
    # Material management
    #

    def refreshMaterialList(
        self,
        obj
    ):


        if not hasattr(
            obj,
            "MaterialCode"
        ):

            return



        values = [

            ""

        ] + MaterialLibrary.codes()



        obj.MaterialCode = values



    def updateMaterial(
        self,
        obj
    ):


        if not obj.MaterialCode:

            return



        material = MaterialLibrary.get(
            obj.MaterialCode
        )



        if material is None:

            return



        #
        # Basic data
        #

        obj.Material = material.MaterialName



        #
        # Thickness
        #

        if hasattr(
            material,
            "Thickness"
        ):


            obj.MaterialThickness = material.Thickness


            obj.Thickness = material.Thickness



        #
        # Supplier
        #

        if hasattr(
            material,
            "Supplier"
        ):


            obj.MaterialSupplier = material.Supplier



        #
        # Price
        #

        if hasattr(
            material,
            "Price"
        ):


            obj.MaterialPrice = material.Price



        #
        # Grain
        #

        if hasattr(
            material,
            "GrainDirection"
        ):


            obj.GrainDirection = material.GrainDirection



    #
    # Data
    #

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


                if key in (

                    "Length",
                    "Width",
                    "Thickness"

                ):

                    value = abs(value)


                setattr(
                    obj,
                    key,
                    value
                )



        #
        # Part Data
        #

    def getPartData(
        self,
        obj
    ):


        from core.data.part_data import PartData


        data = PartData()


        return data.fromObject(
            obj
        )



    #
    # FreeCAD
    #

    def onChanged(
        self,
        obj,
        prop
    ):


        if prop == "MaterialCode":


            self.updateMaterial(
                obj
            )

    def execute(
        self,
        obj
    ):


        shape = GeometryBuilder.createBox(
            obj
        )


        if shape is None:

            return



        #
        # Geometry stays local
        #

        obj.Shape = shape



        #
        # Apply placement
        #

        PlacementBuilder.update(
            obj
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





class ViewProviderBosqoPart:


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
            "part.svg"
        )





#
# Factory
#

def create_part(
    doc
):


    part = doc.addObject(
        "Part::FeaturePython",
        "BosqoPart"
    )


    BosqoPart(
        part
    )


    return part