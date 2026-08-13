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


    # =========================================================
    # PROPERTIES
    # =========================================================

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

        self.addFloat(
            obj,
            "Quantity",
            1,
            "Dimensions"
        )


        #
        # Position definition
        #

        self.addLength(
            obj,
            "Position",
            0,
            "Position"
        )

        self.addString(
            obj,
            "PositionMode",
            "Automatic",
            "Position"
        )

        self.addString(
            obj,
            "PositionType",
            "Automatic",
            "Position"
        )


        #
        # Base position
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

            obj.MaterialCode = (
                [""]
                +
                MaterialLibrary.codes()
            )

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


    # =========================================================
    # HELPERS
    # =========================================================

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


    # =========================================================
    # MATERIAL
    # =========================================================

    def refreshMaterialList(
        self,
        obj
    ):

        if not hasattr(
            obj,
            "MaterialCode"
        ):

            return


        values = (
            [""]
            +
            MaterialLibrary.codes()
        )


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


        if hasattr(
            material,
            "MaterialName"
        ):

            obj.Material = (
                material.MaterialName
            )


        if hasattr(
            material,
            "Thickness"
        ):

            obj.MaterialThickness = (
                material.Thickness
            )


            #
            # Do not overwrite the real thickness
            # of an imported part.
            #

            if str(
                obj.Source
            ) != "Imported":

                obj.Thickness = (
                    material.Thickness
                )


        if hasattr(
            material,
            "Supplier"
        ):

            obj.MaterialSupplier = (
                material.Supplier
            )


        if hasattr(
            material,
            "Price"
        ):

            obj.MaterialPrice = (
                material.Price
            )


        if hasattr(
            material,
            "GrainDirection"
        ):

            obj.GrainDirection = (
                material.GrainDirection
            )


    # =========================================================
    # DATA
    # =========================================================

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
                "Length",
                "Width",
                "Thickness",
                "Position"
            ):

                try:

                    value = abs(
                        float(value)
                    )

                except Exception:

                    pass


            try:

                setattr(
                    obj,
                    key,
                    value
                )

            except Exception:

                pass


        obj.touch()


    def getPartData(
        self,
        obj
    ):

        from core.data.part_data import PartData


        data = PartData()


        return data.fromObject(
            obj
        )


    # =========================================================
    # IMPORTED GEOMETRY
    # =========================================================

    def setImportedShape(
        self,
        obj,
        original
    ):
        """
        Assign an imported FreeCAD object as the
        geometry source of this BosqoPart.

        IMPORTANT:
        
        The imported object's Shape is kept in LOCAL
        coordinates and its Placement is copied to
        the BosqoPart object.

        Therefore:

            original.Shape
                -> local geometry

            original.Placement
                -> real position/orientation

            obj.Shape
                -> local geometry

            obj.Placement
                -> real position/orientation

        This is essential because the rest of Bosqo
        works with obj.Placement.
        """

        if original is None:

            return False


        # =====================================================
        # GET ORIGINAL SHAPE
        # =====================================================

        try:

            shape = original.Shape

        except Exception:

            return False


        if shape is None:

            return False


        try:

            if shape.isNull():

                return False

        except Exception:

            pass


        # =====================================================
        # GET ORIGINAL PLACEMENT
        #
        # THIS IS THE IMPORTANT PART.
        #
        # The original object's Placement must be preserved
        # separately from its Shape.
        # =====================================================

        try:

            originalPlacement = (
                original.Placement.copy()
            )

        except Exception:

            try:

                originalPlacement = (
                    FreeCAD.Placement(
                        original.Placement
                    )
                )

            except Exception:

                originalPlacement = (
                    FreeCAD.Placement()
                )


        # =====================================================
        # KEEP REFERENCE TO ORIGINAL OBJECT
        # =====================================================

        try:

            obj.OriginalObject = original

        except Exception:

            pass


        # =====================================================
        # MARK AS IMPORTED
        # =====================================================

        try:

            obj.Source = "Imported"

        except Exception:

            pass


        # =====================================================
        # COPY GEOMETRY AS LOCAL SHAPE
        #
        # DO NOT COPY THE OBJECT PLACEMENT INTO THE SHAPE.
        #
        # The Shape must remain local.
        # The Placement belongs to obj.Placement.
        # =====================================================

        try:

            localShape = (
                shape.copy()
            )

        except Exception:

            return False


        # =====================================================
        # RESET SHAPE PLACEMENT
        #
        # In case the source Shape itself contains a
        # Placement, remove it so that the position is not
        # applied twice.
        # =====================================================

        try:

            localShape.Placement = (
                FreeCAD.Placement()
            )

        except Exception:

            pass


        # =====================================================
        # ASSIGN LOCAL SHAPE
        # =====================================================

        try:

            obj.Shape = localShape

        except Exception:

            return False


        # =====================================================
        # ASSIGN ORIGINAL OBJECT PLACEMENT
        #
        # THIS IS THE ACTUAL FIX.
        # =====================================================

        try:

            obj.Placement = (
                originalPlacement
            )

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "No se pudo conservar el Placement "
                "de la pieza importada: "
                +
                str(error)
                +
                "\n"
            )

            try:

                obj.Placement = (
                    FreeCAD.Placement()
                )

            except Exception:

                pass


        # =====================================================
        # DEBUG PLACEMENT
        # =====================================================

        try:

            base = (
                obj.Placement.Base
            )

            FreeCAD.Console.PrintMessage(
                "BOSQO PART IMPORTADA | "
                +
                str(
                    getattr(
                        obj,
                        "Name",
                        "?"
                    )
                )
                +
                " | Placement = "
                +
                "X:"
                +
                "%.2f" % float(base.x)
                +
                " Y:"
                +
                "%.2f" % float(base.y)
                +
                " Z:"
                +
                "%.2f" % float(base.z)
                +
                "\n"
            )

        except Exception:

            pass


        # =====================================================
        # KEEP VISIBILITY EXPLICITLY ENABLED
        # =====================================================

        try:

            obj.ViewObject.Visibility = True

        except Exception:

            pass


        # =====================================================
        # COPY LABEL
        # =====================================================

        try:

            if original.Label:

                obj.Label = original.Label

        except Exception:

            pass


        # =====================================================
        # GET REAL DIMENSIONS FROM LOCAL SHAPE
        #
        # The dimensions are taken from the local geometry,
        # not from the object's Placement.
        # =====================================================

        try:

            box = (
                localShape.BoundBox
            )

            x = abs(
                float(
                    box.XLength
                )
            )

            y = abs(
                float(
                    box.YLength
                )
            )

            z = abs(
                float(
                    box.ZLength
                )
            )


            obj.Width = x
            obj.Thickness = y
            obj.Length = z

        except Exception:

            pass


        # =====================================================
        # MARK GEOMETRY
        # =====================================================

        try:

            obj.GeometryStatus = (
                "Imported"
            )

        except Exception:

            pass


        obj.touch()

        return True


    # =========================================================
    # FREECAD
    # =========================================================

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

        # =====================================================
        # IMPORTED PART
        # =====================================================
        #
        # The imported Shape already exists.
        #
        # NEVER replace it with createBox().
        #
        # IMPORTANT:
        #
        # If the Shape has to be recovered, the original
        # Placement must also be copied.
        # =====================================================

        try:

            if str(
                obj.Source
            ) == "Imported":

                # -------------------------------------------------
                # CURRENT IMPORTED SHAPE
                # -------------------------------------------------

                if (
                    obj.Shape is not None
                    and
                    not obj.Shape.isNull()
                ):

                    return


                # -------------------------------------------------
                # RECOVER FROM ORIGINAL OBJECT
                # -------------------------------------------------

                original = (
                    obj.OriginalObject
                )


                if original is None:

                    return


                shape = (
                    original.Shape
                )


                if (
                    shape is None
                    or
                    shape.isNull()
                ):

                    return


                # -------------------------------------------------
                # RECOVER ORIGINAL PLACEMENT
                # -------------------------------------------------

                try:

                    originalPlacement = (
                        original.Placement.copy()
                    )

                except Exception:

                    try:

                        originalPlacement = (
                            FreeCAD.Placement(
                                original.Placement
                            )
                        )

                    except Exception:

                        originalPlacement = (
                            FreeCAD.Placement()
                        )


                # -------------------------------------------------
                # COPY SHAPE
                # -------------------------------------------------

                localShape = (
                    shape.copy()
                )


                # -------------------------------------------------
                # ENSURE LOCAL SHAPE
                # -------------------------------------------------

                try:

                    localShape.Placement = (
                        FreeCAD.Placement()
                    )

                except Exception:

                    pass


                # -------------------------------------------------
                # ASSIGN GEOMETRY
                # -------------------------------------------------

                obj.Shape = (
                    localShape
                )


                # -------------------------------------------------
                # RESTORE PLACEMENT
                # -------------------------------------------------

                try:

                    obj.Placement = (
                        originalPlacement
                    )

                except Exception:

                    pass


                # -------------------------------------------------
                # VISIBILITY
                # -------------------------------------------------

                try:

                    obj.ViewObject.Visibility = True

                except Exception:

                    pass


                return

        except Exception:

            pass


        # =====================================================
        # CREATED PART
        # =====================================================

        shape = GeometryBuilder.createBox(
            obj
        )


        if shape is None:

            return


        obj.Shape = shape


        PlacementBuilder.update(
            obj
        )


    # =========================================================
    # SERIALIZATION
    # =========================================================

    def __getstate__(
        self
    ):

        return None


    def __setstate__(
        self,
        state
    ):

        return None


# =============================================================
# VIEW PROVIDER
# =============================================================

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


# =============================================================
# FACTORY
# =============================================================

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


    #
    # A normal new piece is created geometry.
    #

    part.Source = "Created"


    return part