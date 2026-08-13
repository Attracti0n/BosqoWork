import FreeCAD
from PySide import QtWidgets, QtCore

from library.material_library import MaterialLibrary


class FinishDialog(QtWidgets.QDialog):

    # =========================================================
    # INIT
    # =========================================================

    def __init__(
        self,
        parts,
        parent=None
    ):

        super().__init__(parent)

        self.parts = []

        for part in parts:

            if part is None:
                continue

            if part not in self.parts:
                self.parts.append(part)

        self.setWindowTitle(
            "Acabado de pieza"
        )

        self.setMinimumWidth(
            500
        )

        self.setModal(
            True
        )

        self.buildUI()

        self.loadValues()

    # =========================================================
    # UI
    # =========================================================

    def buildUI(
        self
    ):

        layout = QtWidgets.QVBoxLayout(
            self
        )

        # =====================================================
        # PIEZAS
        # =====================================================

        partsGroup = QtWidgets.QGroupBox(
            "Piezas seleccionadas"
        )

        partsLayout = QtWidgets.QVBoxLayout(
            partsGroup
        )

        self.partsLabel = QtWidgets.QLabel()

        partsLayout.addWidget(
            self.partsLabel
        )

        layout.addWidget(
            partsGroup
        )

        # =====================================================
        # CARAS
        # =====================================================

        faceGroup = QtWidgets.QGroupBox(
            "Acabado de caras"
        )

        faceLayout = QtWidgets.QFormLayout(
            faceGroup
        )

        self.faceTopCombo = (
            QtWidgets.QComboBox()
        )

        self.faceBottomCombo = (
            QtWidgets.QComboBox()
        )

        self.loadFaceMaterials(
            self.faceTopCombo
        )

        self.loadFaceMaterials(
            self.faceBottomCombo
        )

        faceLayout.addRow(
            "Cara superior:",
            self.faceTopCombo
        )

        faceLayout.addRow(
            "Cara inferior:",
            self.faceBottomCombo
        )

        layout.addWidget(
            faceGroup
        )

        # =====================================================
        # CANTOS
        # =====================================================

        edgeGroup = QtWidgets.QGroupBox(
            "Cantos"
        )

        edgeLayout = QtWidgets.QFormLayout(
            edgeGroup
        )

        self.edgeTopCombo = (
            QtWidgets.QComboBox()
        )

        self.edgeBottomCombo = (
            QtWidgets.QComboBox()
        )

        self.edgeLeftCombo = (
            QtWidgets.QComboBox()
        )

        self.edgeRightCombo = (
            QtWidgets.QComboBox()
        )

        self.loadEdgeMaterials(
            self.edgeTopCombo
        )

        self.loadEdgeMaterials(
            self.edgeBottomCombo
        )

        self.loadEdgeMaterials(
            self.edgeLeftCombo
        )

        self.loadEdgeMaterials(
            self.edgeRightCombo
        )

        edgeLayout.addRow(
            "Canto superior:",
            self.edgeTopCombo
        )

        edgeLayout.addRow(
            "Canto inferior:",
            self.edgeBottomCombo
        )

        edgeLayout.addRow(
            "Canto izquierdo:",
            self.edgeLeftCombo
        )

        edgeLayout.addRow(
            "Canto derecho:",
            self.edgeRightCombo
        )

        layout.addWidget(
            edgeGroup
        )

        # =====================================================
        # LACADO
        # =====================================================

        lacquerGroup = QtWidgets.QGroupBox(
            "Lacado"
        )

        lacquerLayout = QtWidgets.QFormLayout(
            lacquerGroup
        )

        self.lacquerCheck = (
            QtWidgets.QCheckBox(
                "Pieza lacada"
            )
        )

        self.ralEdit = (
            QtWidgets.QLineEdit()
        )

        self.ralEdit.setPlaceholderText(
            "Ejemplo: RAL 9016"
        )

        self.lacquerFinishEdit = (
            QtWidgets.QLineEdit()
        )

        self.lacquerFinishEdit.setPlaceholderText(
            "Ejemplo: Mate, satinado..."
        )

        lacquerLayout.addRow(
            "",
            self.lacquerCheck
        )

        lacquerLayout.addRow(
            "RAL:",
            self.ralEdit
        )

        lacquerLayout.addRow(
            "Acabado:",
            self.lacquerFinishEdit
        )

        layout.addWidget(
            lacquerGroup
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
            |
            QtWidgets.QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(
            buttons
        )

        # =====================================================
        # LACQUER ENABLE
        # =====================================================

        self.lacquerCheck.toggled.connect(
            self.updateLacquerState
        )

        self.updateLacquerState(
            self.lacquerCheck.isChecked()
        )

    # =========================================================
    # LOAD FACE MATERIALS
    # =========================================================

    def loadFaceMaterials(
        self,
        combo
    ):

        combo.clear()

        combo.addItem(
            "",
            ""
        )

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

            # -------------------------------------------------
            # CARA = MATERIALTYPE "CHAPA"
            # -------------------------------------------------

            materialType = str(
                material.get(
                    "MaterialType",
                    ""
                )
            ).strip()

            if materialType.lower() != "chapa":

                continue

            code = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()

            if not code:

                continue

            name = str(
                material.get(
                    "MaterialName",
                    ""
                )
            ).strip()

            if name:

                text = (
                    code
                    +
                    " - "
                    +
                    name
                )

            else:

                text = code

            combo.addItem(
                text,
                code
            )

    # =========================================================
    # LOAD EDGE MATERIALS
    # =========================================================

    def loadEdgeMaterials(
        self,
        combo
    ):

        combo.clear()

        combo.addItem(
            "",
            ""
        )

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

            # -------------------------------------------------
            # CANTO = MATERIALTYPE "Canto"
            # -------------------------------------------------

            materialType = str(
                material.get(
                    "MaterialType",
                    ""
                )
            ).strip()

            if materialType.lower() != "canto":

                continue

            code = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()

            if not code:

                continue

            name = str(
                material.get(
                    "MaterialName",
                    ""
                )
            ).strip()

            if name:

                text = (
                    code
                    +
                    " - "
                    +
                    name
                )

            else:

                text = code

            combo.addItem(
                text,
                code
            )

    # =========================================================
    # LOAD CURRENT VALUES
    # =========================================================

    def loadValues(
        self
    ):

        self.partsLabel.setText(
            str(
                len(
                    self.parts
                )
            )
            +
            " pieza(s) seleccionada(s)"
        )

        if not self.parts:

            return

        # -----------------------------------------------------
        # FACE FINISH
        # -----------------------------------------------------

        self.setComboFromParts(
            self.faceTopCombo,
            "FaceTopCode"
        )

        self.setComboFromParts(
            self.faceBottomCombo,
            "FaceBottomCode"
        )

        # -----------------------------------------------------
        # EDGE FINISH
        # -----------------------------------------------------

        self.setComboFromParts(
            self.edgeTopCombo,
            "EdgeTopCode"
        )

        self.setComboFromParts(
            self.edgeBottomCombo,
            "EdgeBottomCode"
        )

        self.setComboFromParts(
            self.edgeLeftCombo,
            "EdgeLeftCode"
        )

        self.setComboFromParts(
            self.edgeRightCombo,
            "EdgeRightCode"
        )

        # -----------------------------------------------------
        # LACADO
        # -----------------------------------------------------

        lacquerValues = []

        for part in self.parts:

            value = str(
                getattr(
                    part,
                    "Lacquer",
                    ""
                )
            )

            lacquerValues.append(
                value
            )

        if lacquerValues:

            first = lacquerValues[0]

            if all(
                value == first
                for value in lacquerValues
            ):

                self.lacquerCheck.setChecked(
                    first.lower()
                    in (
                        "yes",
                        "true",
                        "1",
                        "si",
                        "sí"
                    )
                )

        # -----------------------------------------------------
        # RAL
        # -----------------------------------------------------

        ralValues = []

        for part in self.parts:

            value = str(
                getattr(
                    part,
                    "RAL",
                    ""
                )
            )

            ralValues.append(
                value
            )

        if ralValues:

            first = ralValues[0]

            if all(
                value == first
                for value in ralValues
            ):

                self.ralEdit.setText(
                    first
                )

        # -----------------------------------------------------
        # LACQUER FINISH
        # -----------------------------------------------------

        finishValues = []

        for part in self.parts:

            value = str(
                getattr(
                    part,
                    "LacquerFinish",
                    ""
                )
            )

            finishValues.append(
                value
            )

        if finishValues:

            first = finishValues[0]

            if all(
                value == first
                for value in finishValues
            ):

                self.lacquerFinishEdit.setText(
                    first
                )

    # =========================================================
    # SET COMBO FROM PARTS
    # =========================================================

    def setComboFromParts(
        self,
        combo,
        propertyName
    ):

        values = []

        for part in self.parts:

            value = str(
                getattr(
                    part,
                    propertyName,
                    ""
                )
            )

            values.append(
                value
            )

        if not values:

            return

        first = values[0]

        if not all(
            value == first
            for value in values
        ):

            return

        index = combo.findData(
            first
        )

        if index >= 0:

            combo.setCurrentIndex(
                index
            )

    # =========================================================
    # LACQUER STATE
    # =========================================================

    def updateLacquerState(
        self,
        enabled
    ):

        self.ralEdit.setEnabled(
            enabled
        )

        self.lacquerFinishEdit.setEnabled(
            enabled
        )

    # =========================================================
    # VALUES
    # =========================================================

    def values(
        self
    ):

        return {

            "FaceTopCode":
                self.faceTopCombo.currentData(),

            "FaceBottomCode":
                self.faceBottomCombo.currentData(),

            "EdgeTopCode":
                self.edgeTopCombo.currentData(),

            "EdgeBottomCode":
                self.edgeBottomCombo.currentData(),

            "EdgeLeftCode":
                self.edgeLeftCombo.currentData(),

            "EdgeRightCode":
                self.edgeRightCombo.currentData(),

            "Lacquer":
                (
                    "Yes"
                    if self.lacquerCheck.isChecked()
                    else
                    "No"
                ),

            "RAL":
                self.ralEdit.text().strip(),

            "LacquerFinish":
                self.lacquerFinishEdit.text().strip()
        }

    # =========================================================
    # ACCEPT
    # =========================================================

    def accept(
        self
    ):

        data = self.values()

        # -----------------------------------------------------
        # APPLY TO SELECTED PARTS
        # -----------------------------------------------------

        for part in self.parts:

            self.applyToPart(
                part,
                data
            )

        # -----------------------------------------------------
        # RECOMPUTE
        # -----------------------------------------------------

        try:

            if FreeCAD.ActiveDocument:

                FreeCAD.ActiveDocument.recompute()

        except Exception:

            pass

        super().accept()

    # =========================================================
    # APPLY
    # =========================================================

    def applyToPart(
        self,
        part,
        data
    ):

        if part is None:

            return

        # =====================================================
        # FACE FINISH
        # =====================================================

        self.setProperty(
            part,
            "FaceTopCode",
            data["FaceTopCode"]
        )

        self.setProperty(
            part,
            "FaceBottomCode",
            data["FaceBottomCode"]
        )

        # =====================================================
        # EDGEBANDING
        # =====================================================

        self.setProperty(
            part,
            "EdgeTopCode",
            data["EdgeTopCode"]
        )

        self.setProperty(
            part,
            "EdgeBottomCode",
            data["EdgeBottomCode"]
        )

        self.setProperty(
            part,
            "EdgeLeftCode",
            data["EdgeLeftCode"]
        )

        self.setProperty(
            part,
            "EdgeRightCode",
            data["EdgeRightCode"]
        )

        # =====================================================
        # LACQUER
        # =====================================================

        self.ensureStringProperty(
            part,
            "Lacquer",
            "Finish"
        )

        self.ensureStringProperty(
            part,
            "RAL",
            "Finish"
        )

        self.ensureStringProperty(
            part,
            "LacquerFinish",
            "Finish"
        )

        self.setProperty(
            part,
            "Lacquer",
            data["Lacquer"]
        )

        self.setProperty(
            part,
            "RAL",
            data["RAL"]
        )

        self.setProperty(
            part,
            "LacquerFinish",
            data["LacquerFinish"]
        )

        # =====================================================
        # INFORMATIONAL FIELDS
        # =====================================================

        self.updateFaceInfo(
            part,
            "FaceTopCode",
            "FaceTop"
        )

        self.updateFaceInfo(
            part,
            "FaceBottomCode",
            "FaceBottom"
        )

        self.updateEdgeInfo(
            part,
            "EdgeTopCode",
            "EdgeTop"
        )

        self.updateEdgeInfo(
            part,
            "EdgeBottomCode",
            "EdgeBottom"
        )

        self.updateEdgeInfo(
            part,
            "EdgeLeftCode",
            "EdgeLeft"
        )

        self.updateEdgeInfo(
            part,
            "EdgeRightCode",
            "EdgeRight"
        )

        try:

            part.touch()

        except Exception:

            pass

    # =========================================================
    # SET PROPERTY
    # =========================================================

    def setProperty(
        self,
        obj,
        name,
        value
    ):

        if not hasattr(
            obj,
            name
        ):

            return

        try:

            setattr(
                obj,
                name,
                value
            )

        except Exception:

            pass

    # =========================================================
    # ENSURE STRING PROPERTY
    # =========================================================

    def ensureStringProperty(
        self,
        obj,
        name,
        group
    ):

        if hasattr(
            obj,
            name
        ):

            return

        try:

            obj.addProperty(
                "App::PropertyString",
                name,
                group
            )

            setattr(
                obj,
                name,
                ""
            )

        except Exception:

            pass

    # =========================================================
    # FACE INFORMATION
    # =========================================================

    def updateFaceInfo(
        self,
        part,
        codeProperty,
        infoProperty
    ):

        code = str(
            getattr(
                part,
                codeProperty,
                ""
            )
        ).strip()

        if not code:

            self.setProperty(
                part,
                infoProperty,
                ""
            )

            return

        material = self.getMaterial(
            code
        )

        if material is None:

            self.setProperty(
                part,
                infoProperty,
                code
            )

            return

        name = str(
            material.get(
                "MaterialName",
                ""
            )
        ).strip()

        self.setProperty(
            part,
            infoProperty,
            name if name else code
        )

    # =========================================================
    # EDGE INFORMATION
    # =========================================================

    def updateEdgeInfo(
        self,
        part,
        codeProperty,
        infoProperty
    ):

        code = str(
            getattr(
                part,
                codeProperty,
                ""
            )
        ).strip()

        if not code:

            self.setProperty(
                part,
                infoProperty,
                ""
            )

            return

        material = self.getMaterial(
            code
        )

        if material is None:

            self.setProperty(
                part,
                infoProperty,
                code
            )

            return

        name = str(
            material.get(
                "MaterialName",
                ""
            )
        ).strip()

        self.setProperty(
            part,
            infoProperty,
            name if name else code
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

            data = MaterialLibrary.get(
                code
            )

        except Exception:

            return None

        # -----------------------------------------------------
        # PERSISTENT LIBRARY
        # -----------------------------------------------------

        if isinstance(
            data,
            dict
        ):

            return data

        # -----------------------------------------------------
        # BOSQOMATERIAL OBJECT
        # -----------------------------------------------------

        if data is not None:

            result = {}

            for key in (
                "Code",
                "MaterialName",
                "MaterialType",
                "Category",
                "Thickness",
                "SheetLength",
                "SheetWidth",
                "Supplier",
                "Finish",
                "GrainDirection",
                "Price",
                "PriceUnit"
            ):

                if hasattr(
                    data,
                    key
                ):

                    try:

                        result[key] = getattr(
                            data,
                            key
                        )

                    except Exception:

                        pass

            return result

        return None


# =============================================================
# FACTORY
# =============================================================

def create_finish_dialog(
    parts,
    parent=None
):

    return FinishDialog(
        parts,
        parent
    )