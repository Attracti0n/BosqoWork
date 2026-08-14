import FreeCAD
import os

from app_paths import ICONS_DIR

from library.material_library import MaterialLibrary

from core.builders.geometry_builder import GeometryBuilder
from core.builders.placement_builder import PlacementBuilder


# =============================================================
# BOSQO PART
# =============================================================

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


        # =====================================================
        # IDENTIFICATION
        # =====================================================

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


        # =====================================================
        # DIMENSIONS
        # =====================================================

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


        # =====================================================
        # POSITION
        # =====================================================

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


        # =====================================================
        # BASE POSITION
        # =====================================================

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


        # =====================================================
        # AXIS MAPPING
        # =====================================================

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


        # =====================================================
        # GEOMETRY ANALYSIS
        # =====================================================

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


        # =====================================================
        # BASE MATERIAL
        # =====================================================

        if not hasattr(
            obj,
            "MaterialCode"
        ):

            obj.addProperty(
                "App::PropertyEnumeration",
                "MaterialCode",
                "Material",
                "Base material of the part"
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


        # =====================================================
        # FACE FINISH CODES
        # =====================================================

        self.addFinishEnumeration(
            obj,
            "FaceTopCode"
        )

        self.addFinishEnumeration(
            obj,
            "FaceBottomCode"
        )


        # =====================================================
        # FACE FINISH INFORMATION
        # =====================================================

        self.addString(
            obj,
            "FaceTop",
            "",
            "Finish"
        )

        self.addString(
            obj,
            "FaceBottom",
            "",
            "Finish"
        )


        # =====================================================
        # LACQUER
        # =====================================================

        self.addEnumeration(
            obj,
            "Lacquered",
            [
                "No",
                "Sí"
            ],
            "No",
            "Finish"
        )

        self.addString(
            obj,
            "LacquerRAL",
            "",
            "Finish"
        )

        self.addString(
            obj,
            "LacquerFinish",
            "",
            "Finish"
        )


        # =====================================================
        # EDGE FINISH CODES
        # =====================================================

        self.addFinishEnumeration(
            obj,
            "EdgeTopCode"
        )

        self.addFinishEnumeration(
            obj,
            "EdgeBottomCode"
        )

        self.addFinishEnumeration(
            obj,
            "EdgeLeftCode"
        )

        self.addFinishEnumeration(
            obj,
            "EdgeRightCode"
        )


        # =====================================================
        # EDGE FINISH INFORMATION
        # =====================================================

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


        # =====================================================
        # ORIGINAL OBJECT
        # =====================================================

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


        # =====================================================
        # SOURCE
        # =====================================================

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
    # MATERIAL HELPERS
    # =========================================================

    def materialCodesByType(
        self,
        materialType
    ):

        codes = []

        try:

            materials = MaterialLibrary.all()

        except Exception:

            materials = []


        for material in materials:

            if not isinstance(
                material,
                dict
            ):

                continue


            currentType = str(
                material.get(
                    "MaterialType",
                    ""
                )
            ).strip()


            if currentType != materialType:

                continue


            code = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()


            if not code:

                continue


            if code not in codes:

                codes.append(
                    code
                )


        return codes


    def materialCodesByCategory(
        self,
        category
    ):

        codes = []

        try:

            materials = MaterialLibrary.all()

        except Exception:

            materials = []


        for material in materials:

            if not isinstance(
                material,
                dict
            ):

                continue


            currentCategory = str(
                material.get(
                    "Category",
                    ""
                )
            ).strip()


            if currentCategory.lower() != str(
                category
            ).strip().lower():

                continue


            code = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()


            if not code:

                continue


            if code not in codes:

                codes.append(
                    code
                )


        return codes


    # =========================================================
    # FINISH CODES
    # =========================================================

    def faceFinishCodes(
        self
    ):

        return self.materialCodesByCategory(
            "Chapa"
        )


    def edgeFinishCodes(
        self
    ):

        return self.materialCodesByType(
            "Canto"
        )


    # =========================================================
    # FINISH PROPERTY
    # =========================================================

    def addFinishEnumeration(
        self,
        obj,
        name
    ):

        group = self._finishGroup(
            name
        )


        if not hasattr(
            obj,
            name
        ):

            obj.addProperty(
                "App::PropertyEnumeration",
                name,
                group,
                "Added finish selection"
            )


        if name in (
            "FaceTopCode",
            "FaceBottomCode"
        ):

            values = (
                [""]
                +
                self.faceFinishCodes()
            )

        else:

            values = (
                [""]
                +
                self.edgeFinishCodes()
            )


        try:

            current = str(
                getattr(
                    obj,
                    name,
                    ""
                )
            )

        except Exception:

            current = ""


        try:

            setattr(
                obj,
                name,
                values
            )

        except Exception:

            return


        if current and current in values:

            try:

                setattr(
                    obj,
                    name,
                    current
                )

            except Exception:

                pass


    def _finishGroup(
        self,
        name
    ):

        if name in (
            "FaceTopCode",
            "FaceBottomCode"
        ):

            return "Finish"

        return "Edgebanding"


    # =========================================================
    # REFRESH MATERIAL LIST
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

            current = str(
                obj.MaterialCode
            )

        except Exception:

            current = ""


        try:

            obj.MaterialCode = values

        except Exception:

            return


        if current and current in values:

            try:

                obj.MaterialCode = current

            except Exception:

                pass


        self.refreshFinishLists(
            obj
        )


    # =========================================================
    # REFRESH FINISH LISTS
    # =========================================================

    def refreshFinishLists(
        self,
        obj
    ):

        self.addFinishEnumeration(
            obj,
            "FaceTopCode"
        )

        self.addFinishEnumeration(
            obj,
            "FaceBottomCode"
        )

        self.addFinishEnumeration(
            obj,
            "EdgeTopCode"
        )

        self.addFinishEnumeration(
            obj,
            "EdgeBottomCode"
        )

        self.addFinishEnumeration(
            obj,
            "EdgeLeftCode"
        )

        self.addFinishEnumeration(
            obj,
            "EdgeRightCode"
        )


    # =========================================================
    # GET MATERIAL
    # =========================================================

    def getMaterial(
        self,
        code
    ):

        if not code:

            return None


        try:

            return MaterialLibrary.get(
                code
            )

        except Exception:

            return None


    # =========================================================
    # UPDATE BASE MATERIAL
    # =========================================================

    def updateMaterial(
        self,
        obj
    ):

        if not hasattr(
            obj,
            "MaterialCode"
        ):

            return


        if not obj.MaterialCode:

            return


        material = self.getMaterial(
            obj.MaterialCode
        )


        if material is None:

            return


        if isinstance(
            material,
            dict
        ):

            materialName = material.get(
                "MaterialName",
                material.get(
                    "Name",
                    ""
                )
            )

            materialThickness = material.get(
                "Thickness",
                0
            )

            supplier = material.get(
                "Supplier",
                ""
            )

            price = material.get(
                "Price",
                0
            )

            grain = material.get(
                "GrainDirection",
                ""
            )

        else:

            materialName = getattr(
                material,
                "MaterialName",
                ""
            )

            materialThickness = getattr(
                material,
                "Thickness",
                0
            )

            supplier = getattr(
                material,
                "Supplier",
                ""
            )

            price = getattr(
                material,
                "Price",
                0
            )

            grain = getattr(
                material,
                "GrainDirection",
                ""
            )


        if hasattr(
            obj,
            "Material"
        ):

            obj.Material = str(
                materialName
            )


        if hasattr(
            obj,
            "MaterialThickness"
        ):

            try:

                obj.MaterialThickness = (
                    materialThickness
                )

            except Exception:

                pass


        #
        # Do not overwrite the real thickness
        # of imported geometry.
        #

        if (
            hasattr(obj, "Thickness")
            and
            str(
                getattr(
                    obj,
                    "Source",
                    ""
                )
            ) != "Imported"
        ):

            try:

                obj.Thickness = (
                    materialThickness
                )

            except Exception:

                pass


        if hasattr(
            obj,
            "MaterialSupplier"
        ):

            obj.MaterialSupplier = str(
                supplier
            )


        if hasattr(
            obj,
            "MaterialPrice"
        ):

            try:

                obj.MaterialPrice = float(
                    price
                )

            except Exception:

                pass


        if hasattr(
            obj,
            "GrainDirection"
        ):

            obj.GrainDirection = str(
                grain
            )


    # =========================================================
    # UPDATE FACE FINISH
    # =========================================================

    def updateFaceFinish(
        self,
        obj,
        code,
        propertyName
    ):

        #
        # IMPORTANT:
        # onChanged can be called while BosqoPart
        # is still being initialized.
        #

        if not hasattr(
            obj,
            propertyName
        ):

            return


        if not code:

            try:

                setattr(
                    obj,
                    propertyName,
                    ""
                )

            except Exception:

                pass

            return


        material = self.getMaterial(
            code
        )


        if material is None:

            return


        if isinstance(
            material,
            dict
        ):

            value = material.get(
                "MaterialName",
                material.get(
                    "Name",
                    code
                )
            )

        else:

            value = getattr(
                material,
                "MaterialName",
                code
            )


        try:

            setattr(
                obj,
                propertyName,
                str(value)
            )

        except Exception:

            pass


    # =========================================================
    # UPDATE EDGE FINISH
    # =========================================================

    def updateEdgeFinish(
        self,
        obj,
        code,
        propertyName
    ):

        #
        # IMPORTANT:
        # protect against onChanged during initialization.
        #

        if not hasattr(
            obj,
            propertyName
        ):

            return


        if not code:

            try:

                setattr(
                    obj,
                    propertyName,
                    ""
                )

            except Exception:

                pass

            return


        material = self.getMaterial(
            code
        )


        if material is None:

            return


        if isinstance(
            material,
            dict
        ):

            value = material.get(
                "MaterialName",
                material.get(
                    "Name",
                    code
                )
            )

        else:

            value = getattr(
                material,
                "MaterialName",
                code
            )


        try:

            setattr(
                obj,
                propertyName,
                str(value)
            )

        except Exception:

            pass


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


        #
        # MATERIAL
        #

        try:

            self.updateMaterial(
                obj
            )

        except Exception:

            pass


        #
        # FACE FINISH
        #

        try:

            if (
                hasattr(obj, "FaceTopCode")
                and
                hasattr(obj, "FaceTop")
            ):

                self.updateFaceFinish(
                    obj,
                    obj.FaceTopCode,
                    "FaceTop"
                )

        except Exception:

            pass


        try:

            if (
                hasattr(obj, "FaceBottomCode")
                and
                hasattr(obj, "FaceBottom")
            ):

                self.updateFaceFinish(
                    obj,
                    obj.FaceBottomCode,
                    "FaceBottom"
                )

        except Exception:

            pass


        #
        # EDGE FINISH
        #

        edgePairs = (
            (
                "EdgeTopCode",
                "EdgeTop"
            ),
            (
                "EdgeBottomCode",
                "EdgeBottom"
            ),
            (
                "EdgeLeftCode",
                "EdgeLeft"
            ),
            (
                "EdgeRightCode",
                "EdgeRight"
            )
        )


        for codeProperty, valueProperty in edgePairs:

            try:

                if (
                    hasattr(obj, codeProperty)
                    and
                    hasattr(obj, valueProperty)
                ):

                    self.updateEdgeFinish(
                        obj,
                        getattr(
                            obj,
                            codeProperty
                        ),
                        valueProperty
                    )

            except Exception:

                pass


        try:

            obj.touch()

        except Exception:

            pass


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
    # IMPORTED GEOMETRY
    # =========================================================

    def setImportedShape(
        self,
        obj,
        original
    ):

        if original is None:

            return False


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


        #
        # ORIGINAL PLACEMENT
        #

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


        #
        # REFERENCE
        #

        try:

            obj.OriginalObject = original

        except Exception:

            pass


        #
        # SOURCE
        #

        try:

            obj.Source = "Imported"

        except Exception:

            pass


        #
        # COPY SHAPE
        #

        try:

            localShape = shape.copy()

        except Exception:

            return False


        try:

            localShape.Placement = (
                FreeCAD.Placement()
            )

        except Exception:

            pass


        try:

            obj.Shape = localShape

        except Exception:

            return False


        #
        # ORIGINAL PLACEMENT
        #

        try:

            obj.Placement = (
                originalPlacement
            )

        except Exception:

            try:

                obj.Placement = (
                    FreeCAD.Placement()
                )

            except Exception:

                pass


        #
        # VISIBILITY
        #

        try:

            obj.ViewObject.Visibility = True

        except Exception:

            pass


        #
        # LABEL
        #

        try:

            if original.Label:

                obj.Label = original.Label

        except Exception:

            pass


        #
        # REAL DIMENSIONS
        #

        try:

            box = localShape.BoundBox

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


        #
        # STATUS
        #

        try:

            obj.GeometryStatus = (
                "Imported"
            )

        except Exception:

            pass


        try:

            obj.touch()

        except Exception:

            pass


        return True


    # =========================================================
    # FREECAD ON CHANGED
    # =========================================================

    def onChanged(
        self,
        obj,
        prop
    ):

        #
        # During creation/loading FreeCAD may call onChanged
        # before all properties exist.
        #

        try:

            if prop == "MaterialCode":

                self.updateMaterial(
                    obj
                )


            elif prop == "FaceTopCode":

                if (
                    hasattr(obj, "FaceTopCode")
                    and
                    hasattr(obj, "FaceTop")
                ):

                    self.updateFaceFinish(
                        obj,
                        obj.FaceTopCode,
                        "FaceTop"
                    )


            elif prop == "FaceBottomCode":

                if (
                    hasattr(obj, "FaceBottomCode")
                    and
                    hasattr(obj, "FaceBottom")
                ):

                    self.updateFaceFinish(
                        obj,
                        obj.FaceBottomCode,
                        "FaceBottom"
                    )


            elif prop == "EdgeTopCode":

                if (
                    hasattr(obj, "EdgeTopCode")
                    and
                    hasattr(obj, "EdgeTop")
                ):

                    self.updateEdgeFinish(
                        obj,
                        obj.EdgeTopCode,
                        "EdgeTop"
                    )


            elif prop == "EdgeBottomCode":

                if (
                    hasattr(obj, "EdgeBottomCode")
                    and
                    hasattr(obj, "EdgeBottom")
                ):

                    self.updateEdgeFinish(
                        obj,
                        obj.EdgeBottomCode,
                        "EdgeBottom"
                    )


            elif prop == "EdgeLeftCode":

                if (
                    hasattr(obj, "EdgeLeftCode")
                    and
                    hasattr(obj, "EdgeLeft")
                ):

                    self.updateEdgeFinish(
                        obj,
                        obj.EdgeLeftCode,
                        "EdgeLeft"
                    )


            elif prop == "EdgeRightCode":

                if (
                    hasattr(obj, "EdgeRightCode")
                    and
                    hasattr(obj, "EdgeRight")
                ):

                    self.updateEdgeFinish(
                        obj,
                        obj.EdgeRightCode,
                        "EdgeRight"
                    )


            elif prop == "Lacquered":

                if (
                    hasattr(obj, "Lacquered")
                    and
                    str(obj.Lacquered) == "No"
                ):

                    if hasattr(
                        obj,
                        "LacquerRAL"
                    ):

                        obj.LacquerRAL = ""


                    if hasattr(
                        obj,
                        "LacquerFinish"
                    ):

                        obj.LacquerFinish = ""


        except Exception:

            #
            # Never allow initialization/load-time
            # onChanged errors to break the object.
            #

            pass


    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(
        self,
        obj
    ):

        #
        # IMPORTED PART
        #

        try:

            if str(
                getattr(
                    obj,
                    "Source",
                    ""
                )
            ) == "Imported":

                if (
                    obj.Shape is not None
                    and
                    not obj.Shape.isNull()
                ):

                    return


                original = (
                    getattr(
                        obj,
                        "OriginalObject",
                        None
                    )
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


                localShape = (
                    shape.copy()
                )


                try:

                    localShape.Placement = (
                        FreeCAD.Placement()
                    )

                except Exception:

                    pass


                obj.Shape = (
                    localShape
                )


                try:

                    obj.Placement = (
                        originalPlacement
                    )

                except Exception:

                    pass


                try:

                    obj.ViewObject.Visibility = True

                except Exception:

                    pass


                return

        except Exception:

            pass


        #
        # CREATED PART
        #

        try:

            shape = GeometryBuilder.createBox(
                obj
            )

        except Exception:

            return


        if shape is None:

            return


        obj.Shape = shape


        try:

            PlacementBuilder.update(
                obj
            )

        except Exception:

            pass


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
    # Normal manually created part.
    #

    part.Source = "Created"


    return part