import FreeCAD
import os

from app_paths import ICONS_DIR

from library.material_library import MaterialLibrary

from core.builders.geometry_builder import GeometryBuilder
from core.builders.placement_builder import PlacementBuilder


class BosqoPart:

    def __init__(self, obj):

        obj.Proxy = self

        self.initProperties(obj)

        ViewProviderBosqoPart(
            obj.ViewObject
        )


    # =========================================================
    # PROPERTIES
    # =========================================================

    def initProperties(self, obj):

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
        # Position
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

        self.addLength(
            obj,
            "PositionX",
            0,
            "Position"
        )

        self.addLength(
            obj,
            "PositionY",
            0,
            "Position"
        )

        self.addLength(
            obj,
            "PositionZ",
            0,
            "Position"
        )

        #
        # Rotation
        #

        self.addFloat(
            obj,
            "RotationX",
            0,
            "Position"
        )

        self.addFloat(
            obj,
            "RotationY",
            0,
            "Position"
        )

        self.addFloat(
            obj,
            "RotationZ",
            0,
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
    # PROPERTY HELPERS
    # =========================================================

    def addString(
        self,
        obj,
        name,
        value,
        group
    ):

        if hasattr(
            obj,
            name
        ):
            return

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

        if hasattr(
            obj,
            name
        ):
            return

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

        if hasattr(
            obj,
            name
        ):
            return

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
    # VALUE
    # =========================================================

    def toFloat(
        self,
        value,
        default=0.0
    ):

        try:

            if hasattr(
                value,
                "Value"
            ):

                return float(
                    value.Value
                )

            return float(
                value
            )

        except Exception:

            return default


    # =========================================================
    # ROTATION
    # =========================================================

    def createRotation(
        self,
        rx,
        ry,
        rz
    ):

        rx = self.toFloat(
            rx
        )

        ry = self.toFloat(
            ry
        )

        rz = self.toFloat(
            rz
        )

        rotation_x = FreeCAD.Rotation(
            FreeCAD.Vector(
                1,
                0,
                0
            ),
            rx
        )

        rotation_y = FreeCAD.Rotation(
            FreeCAD.Vector(
                0,
                1,
                0
            ),
            ry
        )

        rotation_z = FreeCAD.Rotation(
            FreeCAD.Vector(
                0,
                0,
                1
            ),
            rz
        )

        return (
            rotation_x
            *
            rotation_y
            *
            rotation_z
        )


    # =========================================================
    # MANUAL PLACEMENT
    # =========================================================

    def applyManualPlacement(
        self,
        obj
    ):

        if obj is None:
            return

        if not hasattr(
            obj,
            "Placement"
        ):
            return

        x = self.toFloat(
            getattr(
                obj,
                "PositionX",
                0
            )
        )

        y = self.toFloat(
            getattr(
                obj,
                "PositionY",
                0
            )
        )

        z = self.toFloat(
            getattr(
                obj,
                "PositionZ",
                0
            )
        )

        rx = self.toFloat(
            getattr(
                obj,
                "RotationX",
                0
            )
        )

        ry = self.toFloat(
            getattr(
                obj,
                "RotationY",
                0
            )
        )

        rz = self.toFloat(
            getattr(
                obj,
                "RotationZ",
                0
            )
        )

        rotation = self.createRotation(
            rx,
            ry,
            rz
        )

        obj.Placement = FreeCAD.Placement(
            FreeCAD.Vector(
                x,
                y,
                z
            ),
            rotation
        )


    # =========================================================
    # AUTOMATIC PLACEMENT
    # =========================================================

    def applyAutomaticPlacement(
        self,
        obj
    ):

        try:

            PlacementBuilder.update(
                obj
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error aplicando posicionamiento automático: "
                +
                str(error)
                +
                "\n"
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

        try:

            obj.MaterialCode = values

        except Exception:

            pass


    def updateMaterial(
        self,
        obj
    ):

        if not hasattr(
            obj,
            "MaterialCode"
        ):
            return

        code = str(
            getattr(
                obj,
                "MaterialCode",
                ""
            )
        )

        if not code:
            return

        try:

            material = MaterialLibrary.get(
                code
            )

        except Exception:

            material = None

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

        if not isinstance(
            data,
            dict
        ):
            return

        #
        # Store normal data first.
        #

        for key, value in data.items():

            if not hasattr(
                obj,
                key
            ):
                continue

            #
            # Length properties.
            #

            if key in (
                "Length",
                "Width",
                "Thickness",
                "Position",
                "PositionX",
                "PositionY",
                "PositionZ"
            ):

                try:

                    value = abs(
                        float(value)
                    )

                except Exception:

                    pass

            #
            # Rotation must keep
            # its original sign.
            #

            try:

                setattr(
                    obj,
                    key,
                    value
                )

            except Exception:

                pass

        #
        # Refresh material information
        # if a material was supplied.
        #

        try:

            self.refreshMaterialList(
                obj
            )

        except Exception:

            pass

        try:

            self.updateMaterial(
                obj
            )

        except Exception:

            pass

        #
        # Placement is handled LAST.
        #

        try:

            mode = str(
                getattr(
                    obj,
                    "PositionMode",
                    "Automatic"
                )
            )

            position_type = str(
                getattr(
                    obj,
                    "PositionType",
                    "Automatic"
                )
            )

            if (
                mode == "Manual"
                or
                position_type == "Manual"
            ):

                self.applyManualPlacement(
                    obj
                )

            else:

                self.applyAutomaticPlacement(
                    obj
                )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error aplicando posición de pieza: "
                +
                str(error)
                +
                "\n"
            )

        obj.touch()


    # =========================================================
    # PART DATA
    # =========================================================

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
    # CHANGED
    # =========================================================

    def onChanged(
        self,
        obj,
        prop
    ):

        #
        # Material changed.
        #

        if prop == "MaterialCode":

            try:

                self.updateMaterial(
                    obj
                )

            except Exception:

                pass

        #
        # Manual position changed.
        #

        if prop in (
            "PositionX",
            "PositionY",
            "PositionZ",
            "RotationX",
            "RotationY",
            "RotationZ"
        ):

            try:

                mode = str(
                    getattr(
                        obj,
                        "PositionMode",
                        "Automatic"
                    )
                )

                position_type = str(
                    getattr(
                        obj,
                        "PositionType",
                        "Automatic"
                    )
                )

                if (
                    mode == "Manual"
                    or
                    position_type == "Manual"
                ):

                    self.applyManualPlacement(
                        obj
                    )

            except Exception:

                pass


    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(
        self,
        obj
    ):

        #
        # Create local geometry.
        #

        try:

            shape = GeometryBuilder.createBox(
                obj
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando geometría de pieza: "
                +
                str(error)
                +
                "\n"
            )

            return

        if shape is None:
            return

        obj.Shape = shape

        #
        # Decide placement mode.
        #
        # IMPORTANT:
        # Manual placement is authoritative.
        # PlacementBuilder is ONLY used for
        # automatic pieces.
        #

        try:

            mode = str(
                getattr(
                    obj,
                    "PositionMode",
                    "Automatic"
                )
            )

            position_type = str(
                getattr(
                    obj,
                    "PositionType",
                    "Automatic"
                )
            )

            manual = (
                mode == "Manual"
                or
                position_type == "Manual"
            )

        except Exception:

            manual = False

        #
        # Automatic
        #

        if not manual:

            self.applyAutomaticPlacement(
                obj
            )

        #
        # Manual
        #
        # Do NOT call PlacementBuilder here.
        #

        else:

            self.applyManualPlacement(
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

    return part