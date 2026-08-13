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
        # POSITION DEFINITION
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

        #
        # This is the REAL material of the part.
        #
        # Example:
        #
        # MaterialCode = MDF19_WHITE
        #
        # The base board remains independent from
        # face finishes and lacquering.
        #

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
        # FACE FINISH
        # =====================================================

        #
        # These are additions to the base material.
        #
        # Example:
        #
        # MaterialCode    -> MDF19
        # FaceTopCode     -> CHAPA_ROBLE
        # FaceBottomCode  -> CHAPA_ROBLE
        #

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

        #
        # Lacquer is NOT a material and NOT an edgebanding.
        #
        # It is informational finishing applied to the part.
        #
        # Example:
        #
        # Lacquered   = Sí
        # LacquerRAL  = RAL 9016
        # LacquerFinish = Mate
        #
        # It does not modify the base material,
        # thickness or geometry.
        #

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
        # EDGEBANDING
        # =====================================================

        #
        # These are additions to the base material.
        #
        # Example:
        #
        # MaterialCode -> MDF19
        # EdgeTopCode  -> CANTO_ABS_1
        #

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

        #
        # Face finish is identified by:
        #
        # Category = "Chapa"
        #

        return self.materialCodesByCategory(
            "Chapa"
        )


    def edgeFinishCodes(
        self
    ):

        #
        # Edgebanding is identified by:
        #
        # MaterialType = "Canto"
        #

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

        #
        # Creates an enumeration for an added finish.
        #
        # FaceTopCode / FaceBottomCode:
        #     Category = Chapa
        #
        # Edge...Code:
        #     MaterialType = Canto
        #

        if not hasattr(
            obj,
            name
        ):

            obj.addProperty(
                "App::PropertyEnumeration",
                name,
                self._finishGroup(
                    name
                ),
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


        #
        # Preserve previous selection.
        #

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


        current = ""


        try:

            current = str(
                obj.MaterialCode
            )

        except Exception:

            pass


        try:

            obj.MaterialCode = values

        except Exception:

            return


        #
        # Preserve selected base material.
        #

        if current and current in values:

            try:

                obj.MaterialCode = current

            except Exception:

                pass


        #
        # Refresh added finishes.
        #

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

        if not obj.MaterialCode:

            return


        material = self.getMaterial(
            obj.MaterialCode
        )


        if material is None:

            return


        # =====================================================
        # NAME
        # =====================================================

        if hasattr(
            material,
            "MaterialName"
        ):

            obj.Material = (
                material.MaterialName
            )


        # =====================================================
        # THICKNESS
        # =====================================================

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


        # =====================================================
        # SUPPLIER
        # =====================================================

        if hasattr(
            material,
            "Supplier"
        ):

            obj.MaterialSupplier = (
                material.Supplier
            )


        # =====================================================
        # PRICE
        # =====================================================

        if hasattr(
            material,
            "Price"
        ):

            obj.MaterialPrice = (
                material.Price
            )


        # =====================================================
        # GRAIN
        # =====================================================

        if hasattr(
            material,
            "GrainDirection"
        ):

            obj.GrainDirection = (
                material.GrainDirection
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

        if not code:

            setattr(
                obj,
                propertyName,
                ""
            )

            return


        material = self.getMaterial(
            code
        )


        if material is None:

            return


        if hasattr(
            material,
            "MaterialName"
        ):

            setattr(
                obj,
                propertyName,
                material.MaterialName
            )

        else:

            setattr(
                obj,
                propertyName,
                code
            )


    # =========================================================
    # UPDATE EDGE FINISH
    # =========================================================

    def updateEdgeFinish(
        self,
        obj,
        code,
        propertyName
    ):

        if not code:

            setattr(
                obj,
                propertyName,
                ""
            )

            return


        material = self.getMaterial(
            code
        )


        if material is None:

            return


        if hasattr(
            material,
            "MaterialName"
        ):

            setattr(
                obj,
                propertyName,
                material.MaterialName
            )

        else:

            setattr(
                obj,
                propertyName,
                code
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


        #
        # Refresh material information.
        #

        try:

            self.updateMaterial(
                obj
            )

        except Exception:

            pass


        #
        # Refresh face finish information.
        #

        try:

            self.updateFaceFinish(
                obj,
                getattr(
                    obj,
                    "FaceTopCode",
                    ""
                ),
                "FaceTop"
            )

        except Exception:

            pass


        try:

            self.updateFaceFinish(
                obj,
                getattr(
                    obj,
                    "FaceBottomCode",
                    ""
                ),
                "FaceBottom"
            )

        except Exception:

            pass


        #
        # Refresh edge information.
        #

        try:

            self.updateEdgeFinish(
                obj,
                getattr(
                    obj,
                    "EdgeTopCode",
                    ""
                ),
                "EdgeTop"
            )

        except Exception:

            pass


        try:

            self.updateEdgeFinish(
                obj,
                getattr(
                    obj,
                    "EdgeBottomCode",
                    ""
                ),
                "EdgeBottom"
            )

        except Exception:

            pass


        try:

            self.updateEdgeFinish(
                obj,
                getattr(
                    obj,
                    "EdgeLeftCode",
                    ""
                ),
                "EdgeLeft"
            )

        except Exception:

            pass


        try:

            self.updateEdgeFinish(
                obj,
                getattr(
                    obj,
                    "EdgeRightCode",
                    ""
                ),
                "EdgeRight"
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

        The imported Shape remains local and
        the original Placement is assigned to
        the BosqoPart.
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
        # KEEP REFERENCE
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
        # COPY GEOMETRY
        # =====================================================

        try:

            localShape = (
                shape.copy()
            )

        except Exception:

            return False


        # =====================================================
        # RESET SHAPE PLACEMENT
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
        # ASSIGN ORIGINAL PLACEMENT
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
        # VISIBILITY
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
        # REAL DIMENSIONS
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
        # GEOMETRY STATUS
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

        # =====================================================
        # BASE MATERIAL
        # =====================================================

        if prop == "MaterialCode":

            self.updateMaterial(
                obj
            )


        # =====================================================
        # FACE TOP
        # =====================================================

        elif prop == "FaceTopCode":

            self.updateFaceFinish(
                obj,
                obj.FaceTopCode,
                "FaceTop"
            )


        # =====================================================
        # FACE BOTTOM
        # =====================================================

        elif prop == "FaceBottomCode":

            self.updateFaceFinish(
                obj,
                obj.FaceBottomCode,
                "FaceBottom"
            )


        # =====================================================
        # EDGES
        # =====================================================

        elif prop == "EdgeTopCode":

            self.updateEdgeFinish(
                obj,
                obj.EdgeTopCode,
                "EdgeTop"
            )


        elif prop == "EdgeBottomCode":

            self.updateEdgeFinish(
                obj,
                obj.EdgeBottomCode,
                "EdgeBottom"
            )


        elif prop == "EdgeLeftCode":

            self.updateEdgeFinish(
                obj,
                obj.EdgeLeftCode,
                "EdgeLeft"
            )


        elif prop == "EdgeRightCode":

            self.updateEdgeFinish(
                obj,
                obj.EdgeRightCode,
                "EdgeRight"
            )


        # =====================================================
        # LACQUER
        # =====================================================

        elif prop == "Lacquered":

            #
            # If lacquering is disabled,
            # clear the informational RAL and finish.
            #

            if str(
                obj.Lacquered
            ) == "No":

                try:

                    obj.LacquerRAL = ""

                except Exception:

                    pass

                try:

                    obj.LacquerFinish = ""

                except Exception:

                    pass


    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(
        self,
        obj
    ):

        # =====================================================
        # IMPORTED PART
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
                # RECOVER ORIGINAL
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
                # RECOVER PLACEMENT
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