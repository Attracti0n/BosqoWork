from PySide import QtWidgets, QtCore


# =============================================================
# MODULE DIALOG
# =============================================================

class ModuleDialog(QtWidgets.QDialog):

    # =========================================================
    # INIT
    # =========================================================

    def __init__(
        self,
        data=None,
        parts=None,
        parent=None
    ):

        super().__init__(parent)

        self.data = data or {}

        self.parts = list(
            parts or []
        )

        self.setWindowTitle(
            "Módulo"
        )

        self.resize(
            900,
            560
        )

        self.createUI()

        self.loadData()

    # =========================================================
    # UI
    # =========================================================

    def createUI(self):

        mainLayout = QtWidgets.QVBoxLayout(
            self
        )

        # =====================================================
        # MODULE NAME
        # =====================================================

        nameLayout = QtWidgets.QHBoxLayout()

        nameLayout.addWidget(
            QtWidgets.QLabel(
                "Nombre:"
            )
        )

        self.nameEdit = QtWidgets.QLineEdit()

        nameLayout.addWidget(
            self.nameEdit
        )

        mainLayout.addLayout(
            nameLayout
        )

        # =====================================================
        # PARTS TABLE
        # =====================================================

        self.partsTable = QtWidgets.QTableWidget()

        self.partsTable.setColumnCount(
            7
        )

        self.partsTable.setHorizontalHeaderLabels(
            [
                "Pieza",
                "Tipo",
                "Largo",
                "Ancho",
                "Espesor",
                "Cantidad",
                "Material"
            ]
        )

        self.partsTable.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )

        self.partsTable.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )

        # -----------------------------------------------------
        # NO DIRECT CELL EDITING
        #
        # Type and Material are edited through their combos.
        # -----------------------------------------------------

        self.partsTable.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        self.partsTable.horizontalHeader().setStretchLastSection(
            True
        )

        mainLayout.addWidget(
            self.partsTable
        )

        # =====================================================
        # INFO
        # =====================================================

        self.infoLabel = QtWidgets.QLabel(
            "Las dimensiones de las piezas importadas no se pueden modificar."
        )

        mainLayout.addWidget(
            self.infoLabel
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        mainLayout.addWidget(
            buttons
        )

    # =========================================================
    # LOAD DATA
    # =========================================================

    def loadData(self):

        self.nameEdit.setText(
            str(
                self.data.get(
                    "Label",
                    "Módulo importado"
                )
            )
        )

        self.loadParts()

    # =========================================================
    # LOAD PARTS
    # =========================================================

    def loadParts(self):

        self.partsTable.setRowCount(
            0
        )

        for part in self.parts:

            if part is None:
                continue

            row = self.partsTable.rowCount()

            self.partsTable.insertRow(
                row
            )

            # =================================================
            # NAME
            # =================================================

            name = self.getPartName(
                part
            )

            self.setReadOnlyItem(
                row,
                0,
                name
            )

            # =================================================
            # TYPE
            # =================================================
            #
            # Imported parts are ALWAYS initially:
            #
            # Personalizado
            #
            # The user can change the type manually.
            # =================================================

            self.createTypeCombo(
                row
            )

            # =================================================
            # LENGTH
            # =================================================

            length = self.getDimension(
                part,
                (
                    "Length",
                    "Largo"
                ),
                "X"
            )

            self.setReadOnlyItem(
                row,
                2,
                self.formatValue(
                    length
                )
            )

            # =================================================
            # WIDTH
            # =================================================

            width = self.getDimension(
                part,
                (
                    "Width",
                    "Ancho"
                ),
                "Y"
            )

            self.setReadOnlyItem(
                row,
                3,
                self.formatValue(
                    width
                )
            )

            # =================================================
            # THICKNESS
            # =================================================

            thickness = self.getDimension(
                part,
                (
                    "Thickness",
                    "Espesor"
                ),
                "Z"
            )

            self.setReadOnlyItem(
                row,
                4,
                self.formatValue(
                    thickness
                )
            )

            # =================================================
            # QUANTITY
            # =================================================

            self.setReadOnlyItem(
                row,
                5,
                "1"
            )

            # =================================================
            # MATERIAL
            # =================================================

            self.createMaterialCombo(
                row,
                part
            )

        self.partsTable.resizeColumnsToContents()

    # =========================================================
    # PART NAME
    # =========================================================

    def getPartName(
        self,
        part
    ):

        for propertyName in (
            "Label",
            "PartName",
            "Name"
        ):

            try:

                if not hasattr(
                    part,
                    propertyName
                ):

                    continue

                value = getattr(
                    part,
                    propertyName
                )

                if value is None:
                    continue

                value = str(
                    value
                ).strip()

                if value:

                    return value

            except Exception:

                pass

        return "Pieza"

    # =========================================================
    # TYPE COMBO
    # =========================================================

    def createTypeCombo(
        self,
        row
    ):

        combo = QtWidgets.QComboBox()

        # -----------------------------------------------------
        # THESE ARE THE BOSQO PART TYPES.
        #
        # Keep these names synchronized with PartTableDialog.
        # -----------------------------------------------------

        types = [
            "Personalizado",
            "Lateral",
            "Base",
            "Superior",
            "Trasera",
            "Balda",
            "Separador",
            "Estructural"
        ]

        combo.addItems(
            types
        )

        # -----------------------------------------------------
        # DEFAULT
        #
        # Imported pieces start as Personalizado.
        # -----------------------------------------------------

        index = combo.findText(
            "Personalizado",
            QtCore.Qt.MatchFixedString
        )

        if index >= 0:

            combo.setCurrentIndex(
                index
            )

        self.partsTable.setCellWidget(
            row,
            1,
            combo
        )

    # =========================================================
    # MATERIAL COMBO
    # =========================================================

    def createMaterialCombo(
        self,
        row,
        part
    ):

        combo = QtWidgets.QComboBox()

        combo.setEditable(
            False
        )

        materials = self.getMaterials(
            part
        )

        for material in materials:

            combo.addItem(
                material
            )

        # -----------------------------------------------------
        # CURRENT MATERIAL OF THE PART
        # -----------------------------------------------------

        currentMaterial = self.getMaterial(
            part
        )

        if currentMaterial:

            index = combo.findText(
                currentMaterial,
                QtCore.Qt.MatchFixedString
            )

            if index >= 0:

                combo.setCurrentIndex(
                    index
                )

        # -----------------------------------------------------
        # IF THE LIBRARY IS EMPTY
        # -----------------------------------------------------
        #
        # Do NOT invent material names.
        #
        # -----------------------------------------------------

        if combo.count() == 0:

            combo.addItem(
                ""
            )

        self.partsTable.setCellWidget(
            row,
            6,
            combo
        )

    # =========================================================
    # GET MATERIALS
    # =========================================================

    def getMaterials(
        self,
        part
    ):

        materials = []

        try:

            from library.material_library import MaterialLibrary

            # -------------------------------------------------
            # USE THE REAL BOSQO MATERIAL LIBRARY
            #
            # all(document) returns the material objects
            # associated with the current document.
            # -------------------------------------------------

            document = None

            try:

                document = part.Document

            except Exception:

                pass

            result = MaterialLibrary.all(
                document
            )

            if result is None:

                return []

            # -------------------------------------------------
            # DICTIONARY
            # -------------------------------------------------

            if isinstance(
                result,
                dict
            ):

                for key, value in result.items():

                    name = self.extractMaterialName(
                        value
                    )

                    if not name:

                        name = str(
                            key
                        ).strip()

                    if name:

                        materials.append(
                            name
                        )

            # -------------------------------------------------
            # LIST / TUPLE / SET
            # -------------------------------------------------

            elif isinstance(
                result,
                (
                    list,
                    tuple,
                    set
                )
            ):

                for value in result:

                    name = self.extractMaterialName(
                        value
                    )

                    if name:

                        materials.append(
                            name
                        )

            # -------------------------------------------------
            # SINGLE OBJECT
            # -------------------------------------------------

            else:

                name = self.extractMaterialName(
                    result
                )

                if name:

                    materials.append(
                        name
                    )

        except Exception as error:

            # -------------------------------------------------
            # IMPORTANT:
            # Do not create fake materials.
            # -------------------------------------------------

            try:

                import FreeCAD

                FreeCAD.Console.PrintWarning(
                    "No se pudieron cargar los materiales: "
                    + str(error)
                    + "\n"
                )

            except Exception:

                pass

        # -----------------------------------------------------
        # REMOVE DUPLICATES
        # -----------------------------------------------------

        clean = []

        for material in materials:

            text = str(
                material
            ).strip()

            if not text:
                continue

            if text not in clean:

                clean.append(
                    text
                )

        return clean

    # =========================================================
    # EXTRACT MATERIAL NAME
    # =========================================================

    def extractMaterialName(
        self,
        material
    ):

        if material is None:

            return ""

        # -----------------------------------------------------
        # STRING
        # -----------------------------------------------------

        if isinstance(
            material,
            str
        ):

            return material.strip()

        # -----------------------------------------------------
        # BOSQO MATERIAL
        # -----------------------------------------------------

        for propertyName in (
            "Name",
            "name",
            "Label",
            "label",
            "MaterialName",
            "materialName",
            "Code",
            "code"
        ):

            try:

                value = getattr(
                    material,
                    propertyName
                )

                if value is None:
                    continue

                value = str(
                    value
                ).strip()

                if value:

                    return value

            except Exception:

                pass

        return ""

    # =========================================================
    # GET MATERIAL FROM PART
    # =========================================================

    def getMaterial(
        self,
        part
    ):

        for propertyName in (
            "Material",
            "MaterialName"
        ):

            try:

                if not hasattr(
                    part,
                    propertyName
                ):

                    continue

                value = getattr(
                    part,
                    propertyName
                )

                if value is None:
                    continue

                # -------------------------------------------------
                # FreeCAD / Bosqo material object
                # -------------------------------------------------

                for nameProperty in (
                    "Name",
                    "name",
                    "Label",
                    "label",
                    "MaterialName",
                    "materialName",
                    "Code",
                    "code"
                ):

                    try:

                        nested = getattr(
                            value,
                            nameProperty
                        )

                        if nested is not None:

                            nested = str(
                                nested
                            ).strip()

                            if nested:

                                return nested

                    except Exception:

                        pass

                # -------------------------------------------------
                # Plain value
                # -------------------------------------------------

                text = str(
                    value
                ).strip()

                if text:

                    return text

            except Exception:

                pass

        return ""

    # =========================================================
    # DIMENSION
    # =========================================================

    def getDimension(
        self,
        part,
        propertyNames,
        axis
    ):

        # -----------------------------------------------------
        # FIRST:
        # REAL BOSQO PART PROPERTY
        # -----------------------------------------------------

        for propertyName in propertyNames:

            try:

                if not hasattr(
                    part,
                    propertyName
                ):

                    continue

                value = getattr(
                    part,
                    propertyName
                )

                if value is not None:

                    return value

            except Exception:

                pass

        # -----------------------------------------------------
        # SECOND:
        # SHAPE BOUNDING BOX
        # -----------------------------------------------------

        try:

            shape = getattr(
                part,
                "Shape",
                None
            )

            if shape is None:
                return ""

            if shape.isNull():
                return ""

            box = shape.BoundBox

            if axis == "X":

                return box.XLength

            if axis == "Y":

                return box.YLength

            if axis == "Z":

                return box.ZLength

        except Exception:

            pass

        return ""

    # =========================================================
    # READ ONLY ITEM
    # =========================================================

    def setReadOnlyItem(
        self,
        row,
        column,
        text
    ):

        item = QtWidgets.QTableWidgetItem(
            str(text)
        )

        item.setFlags(
            item.flags()
            &
            ~QtCore.Qt.ItemIsEditable
        )

        self.partsTable.setItem(
            row,
            column,
            item
        )

    # =========================================================
    # FORMAT VALUE
    # =========================================================

    def formatValue(
        self,
        value
    ):

        if value is None:

            return ""

        # -----------------------------------------------------
        # FreeCAD Quantity
        # -----------------------------------------------------

        try:

            if hasattr(
                value,
                "Value"
            ):

                return "%.2f" % float(
                    value.Value
                )

        except Exception:

            pass

        # -----------------------------------------------------
        # Numeric
        # -----------------------------------------------------

        try:

            return "%.2f" % float(
                value
            )

        except Exception:

            pass

        return str(
            value
        )

    # =========================================================
    # GET DATA
    # =========================================================

    def getData(
        self
    ):

        partsData = []

        for row in range(
            self.partsTable.rowCount()
        ):

            # -------------------------------------------------
            # NAME
            # -------------------------------------------------

            nameItem = self.partsTable.item(
                row,
                0
            )

            if nameItem is None:

                continue

            # -------------------------------------------------
            # TYPE
            # -------------------------------------------------

            typeWidget = self.partsTable.cellWidget(
                row,
                1
            )

            if isinstance(
                typeWidget,
                QtWidgets.QComboBox
            ):

                partType = (
                    typeWidget.currentText()
                )

            else:

                partType = "Personalizado"

            # -------------------------------------------------
            # LENGTH
            # -------------------------------------------------

            lengthItem = self.partsTable.item(
                row,
                2
            )

            # -------------------------------------------------
            # WIDTH
            # -------------------------------------------------

            widthItem = self.partsTable.item(
                row,
                3
            )

            # -------------------------------------------------
            # THICKNESS
            # -------------------------------------------------

            thicknessItem = self.partsTable.item(
                row,
                4
            )

            # -------------------------------------------------
            # QUANTITY
            # -------------------------------------------------

            quantityItem = self.partsTable.item(
                row,
                5
            )

            # -------------------------------------------------
            # MATERIAL
            # -------------------------------------------------

            materialWidget = self.partsTable.cellWidget(
                row,
                6
            )

            if isinstance(
                materialWidget,
                QtWidgets.QComboBox
            ):

                material = (
                    materialWidget.currentText()
                )

            else:

                material = ""

            # -------------------------------------------------
            # PART DATA
            # -------------------------------------------------

            partsData.append(
                {

                    "Name":
                        nameItem.text(),

                    "Type":
                        partType,

                    "Length":
                        (
                            lengthItem.text()
                            if lengthItem
                            else ""
                        ),

                    "Width":
                        (
                            widthItem.text()
                            if widthItem
                            else ""
                        ),

                    "Thickness":
                        (
                            thicknessItem.text()
                            if thicknessItem
                            else ""
                        ),

                    "Quantity":
                        (
                            quantityItem.text()
                            if quantityItem
                            else "1"
                        ),

                    "Material":
                        material
                }
            )

        return {

            "Label":
                self.nameEdit.text(),

            "Parts":
                partsData
        }