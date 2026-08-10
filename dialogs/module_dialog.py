from PySide import QtWidgets, QtCore
import json
import FreeCAD


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
        parent=None,
        module=None
    ):

        super().__init__(parent)

        # -----------------------------------------------------
        # DATA
        # -----------------------------------------------------

        self.data = data or {}

        # -----------------------------------------------------
        # REAL FREECAD MODULE OBJECT
        # -----------------------------------------------------

        self.module = module

        # -----------------------------------------------------
        # PARTS
        # -----------------------------------------------------

        self.parts = list(
            parts or []
        )

        # -----------------------------------------------------
        # REAL FREECAD OBJECT ASSOCIATED WITH EACH ROW
        # -----------------------------------------------------

        self.rowParts = []

        # -----------------------------------------------------
        # WINDOW
        # -----------------------------------------------------

        self.setWindowTitle(
            "Módulo"
        )

        self.resize(
            900,
            560
        )

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        self.createUI()

        # -----------------------------------------------------
        # LOAD
        # -----------------------------------------------------

        self.loadData()

    # =========================================================
    # UI
    # =========================================================

    def createUI(
        self
    ):

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
            self.saveChanges
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

    def loadData(
        self
    ):

        # -----------------------------------------------------
        # NAME
        # -----------------------------------------------------

        name = ""

        # First try real module object.

        if self.module is not None:

            try:

                name = str(
                    getattr(
                        self.module,
                        "ModuleName",
                        ""
                    )
                ).strip()

            except Exception:

                name = ""

        # Fallback to Label from data.

        if not name:

            name = str(
                self.data.get(
                    "Label",
                    "Módulo importado"
                )
            )

        self.nameEdit.setText(
            name
        )

        # -----------------------------------------------------
        # PARTS
        # -----------------------------------------------------

        self.loadParts()

    # =========================================================
    # LOAD PARTS
    # =========================================================

    def loadParts(
        self
    ):

        self.partsTable.setRowCount(
            0
        )

        self.rowParts = []

        for part in self.parts:

            if part is None:

                continue

            row = self.partsTable.rowCount()

            self.partsTable.insertRow(
                row
            )

            # -------------------------------------------------
            # SAVE REAL FREECAD OBJECT
            # -------------------------------------------------

            self.rowParts.append(
                part
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

            self.createTypeCombo(
                row,
                part
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
    # SAVE CHANGES
    # =========================================================

    def saveChanges(
        self
    ):

        try:

            # -------------------------------------------------
            # COLLECT DATA FROM TABLE
            # -------------------------------------------------

            result = self.getData()

            # -------------------------------------------------
            # SAVE TO REAL FREECAD MODULE
            # -------------------------------------------------

            if self.module is not None:

                self.saveToModule(
                    result
                )

            # -------------------------------------------------
            # KEEP LOCAL DATA UPDATED
            # -------------------------------------------------

            self.data = result

            # -------------------------------------------------
            # ACCEPT
            # -------------------------------------------------

            self.accept()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error guardando cambios del módulo: "
                +
                str(error)
                +
                "\n"
            )

            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                "No se pudieron guardar los cambios:\n\n"
                +
                str(error)
            )

    # =========================================================
    # SAVE TO FREECAD MODULE
    # =========================================================

    def saveToModule(
        self,
        data
    ):

        module = self.module

        if module is None:

            return

        # =====================================================
        # MODULE NAME
        # =====================================================

        try:

            moduleName = str(
                data.get(
                    "Label",
                    "Módulo importado"
                )
            ).strip()

            if not moduleName:

                moduleName = "Módulo importado"

            if hasattr(
                module,
                "ModuleName"
            ):

                module.ModuleName = moduleName

            module.Label = moduleName

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "No se pudo guardar el nombre del módulo: "
                +
                str(error)
                +
                "\n"
            )

        # =====================================================
        # PARTS JSON
        # =====================================================

        try:

            partsData = data.get(
                "Parts",
                []
            )

            jsonData = json.dumps(
                partsData,
                ensure_ascii=False
            )

            if hasattr(
                module,
                "PartsJSON"
            ):

                module.PartsJSON = jsonData

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "No se pudo guardar PartsJSON: "
                +
                str(error)
                +
                "\n"
            )

        # =====================================================
        # SAVE TYPE + MATERIAL TO REAL PARTS
        # =====================================================

        for row in range(
            self.partsTable.rowCount()
        ):

            if row >= len(
                self.rowParts
            ):

                continue

            part = self.rowParts[
                row
            ]

            if part is None:

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

                partType = str(
                    typeWidget.currentText()
                ).strip()

            else:

                partType = "Personalizada"

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

                material = str(
                    materialWidget.currentText()
                ).strip()

            else:

                material = ""

            # -------------------------------------------------
            # WRITE TYPE
            # -------------------------------------------------

            self.setPartProperty(
                part,
                "PartType",
                partType
            )

            # -------------------------------------------------
            # WRITE MATERIAL
            # -------------------------------------------------

            self.setPartProperty(
                part,
                "Material",
                material
            )

            # -------------------------------------------------
            # ALSO TRY MaterialName
            # -------------------------------------------------

            if not self.hasProperty(
                part,
                "Material"
            ):

                self.setPartProperty(
                    part,
                    "MaterialName",
                    material
                )

            # -------------------------------------------------
            # TOUCH PART
            # -------------------------------------------------

            try:

                part.touch()

            except Exception:

                pass

        # =====================================================
        # TOUCH MODULE
        # =====================================================

        try:

            module.touch()

        except Exception:

            pass

        # =====================================================
        # RECOMPUTE DOCUMENT
        # =====================================================

        try:

            document = module.Document

            if document is not None:

                document.recompute()

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "Error recomputando documento: "
                +
                str(error)
                +
                "\n"
            )

    # =========================================================
    # SET PART PROPERTY
    # =========================================================

    def setPartProperty(
        self,
        part,
        propertyName,
        value
    ):

        try:

            if not self.hasProperty(
                part,
                propertyName
            ):

                return False

            current = getattr(
                part,
                propertyName
            )

            # -------------------------------------------------
            # ENUMERATION
            # -------------------------------------------------

            try:

                values = part.getEnumerationsOfProperty(
                    propertyName
                )

                if values:

                    if value in values:

                        setattr(
                            part,
                            propertyName,
                            value
                        )

                        return True

                    return False

            except Exception:

                pass

            # -------------------------------------------------
            # STRING / NORMAL PROPERTY
            # -------------------------------------------------

            setattr(
                part,
                propertyName,
                value
            )

            return True

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "No se pudo guardar "
                +
                propertyName
                +
                " en "
                +
                str(
                    getattr(
                        part,
                        "Name",
                        "pieza"
                    )
                )
                +
                ": "
                +
                str(error)
                +
                "\n"
            )

            return False

    # =========================================================
    # HAS PROPERTY
    # =========================================================

    def hasProperty(
        self,
        obj,
        propertyName
    ):

        try:

            return propertyName in obj.PropertiesList

        except Exception:

            try:

                return hasattr(
                    obj,
                    propertyName
                )

            except Exception:

                return False

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
        row,
        part
    ):

        combo = QtWidgets.QComboBox()

        types = [
            "Estructural",
            "Balda",
            "Separador",
            "Personalizada"
        ]

        combo.addItems(
            types
        )

        # -----------------------------------------------------
        # CURRENT TYPE
        # -----------------------------------------------------

        currentType = self.getExistingPartType(
            part
        )

        # -----------------------------------------------------
        # NORMALIZE OLD TYPES
        # -----------------------------------------------------

        typeMap = {

            "Personalizado":
                "Personalizada",

            "Personalizada":
                "Personalizada",

            "Lateral":
                "Estructural",

            "Base":
                "Estructural",

            "Superior":
                "Estructural",

            "Trasera":
                "Estructural",

            "Estructural":
                "Estructural",

            "Balda":
                "Balda",

            "Separador":
                "Separador"

        }

        currentType = typeMap.get(
            currentType,
            "Personalizada"
        )

        index = combo.findText(
            currentType,
            QtCore.Qt.MatchFixedString
        )

        if index < 0:

            index = combo.findText(
                "Personalizada",
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
    # GET EXISTING PART TYPE
    # =========================================================

    def getExistingPartType(
        self,
        part
    ):

        # -----------------------------------------------------
        # REAL BOSQO PROPERTY
        # -----------------------------------------------------

        for propertyName in (
            "PartType",
            "Type"
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

                text = str(
                    value
                ).strip()

                if text:

                    return text

            except Exception:

                pass

        # -----------------------------------------------------
        # STORED MODULE DATA
        # -----------------------------------------------------

        try:

            objectName = str(
                getattr(
                    part,
                    "Name",
                    ""
                )
            )

            for item in self.data.get(
                "Parts",
                []
            ):

                if not isinstance(
                    item,
                    dict
                ):

                    continue

                storedName = str(
                    item.get(
                        "ObjectName",
                        ""
                    )
                )

                if storedName == objectName:

                    storedType = str(
                        item.get(
                            "Type",
                            ""
                        )
                    ).strip()

                    if storedType:

                        return storedType

        except Exception:

            pass

        return ""

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

        # -----------------------------------------------------
        # LOAD MATERIAL LIBRARY
        # -----------------------------------------------------

        materials = self.getMaterials(
            part
        )

        for material in materials:

            combo.addItem(
                material
            )

        # -----------------------------------------------------
        # CURRENT MATERIAL
        # -----------------------------------------------------

        currentMaterial = self.getMaterial(
            part
        )

        # -----------------------------------------------------
        # CHECK STORED DATA
        # -----------------------------------------------------

        if not currentMaterial:

            try:

                objectName = str(
                    getattr(
                        part,
                        "Name",
                        ""
                    )
                )

                for item in self.data.get(
                    "Parts",
                    []
                ):

                    if not isinstance(
                        item,
                        dict
                    ):

                        continue

                    if str(
                        item.get(
                            "ObjectName",
                            ""
                        )
                    ) == objectName:

                        currentMaterial = str(
                            item.get(
                                "Material",
                                ""
                            )
                        ).strip()

                        if currentMaterial:

                            break

            except Exception:

                pass

        # -----------------------------------------------------
        # ADD CURRENT MATERIAL
        # -----------------------------------------------------

        if currentMaterial:

            index = combo.findText(
                currentMaterial,
                QtCore.Qt.MatchFixedString
            )

            if index < 0:

                combo.insertItem(
                    0,
                    currentMaterial
                )

                index = 0

            combo.setCurrentIndex(
                index
            )

        # -----------------------------------------------------
        # EMPTY LIBRARY
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

            result = MaterialLibrary.all()

            if result is None:

                return []

            # -------------------------------------------------
            # LIST
            # -------------------------------------------------

            if isinstance(
                result,
                list
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
            # DICT
            # -------------------------------------------------

            elif isinstance(
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

            try:

                FreeCAD.Console.PrintWarning(
                    "No se pudieron cargar los materiales: "
                    +
                    str(error)
                    +
                    "\n"
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
        # DICT
        # -----------------------------------------------------

        if isinstance(
            material,
            dict
        ):

            materialName = str(
                material.get(
                    "MaterialName",
                    ""
                )
            ).strip()

            if materialName:

                return materialName

            code = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()

            if code:

                return code

            for propertyName in (
                "Name",
                "name",
                "Label",
                "label"
            ):

                value = material.get(
                    propertyName,
                    ""
                )

                if value is not None:

                    value = str(
                        value
                    ).strip()

                    if value:

                        return value

            return ""

        # -----------------------------------------------------
        # FREECAD OBJECT
        # -----------------------------------------------------

        for propertyName in (
            "MaterialName",
            "Name",
            "name",
            "Label",
            "label",
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
                # MATERIAL OBJECT
                # -------------------------------------------------

                for nameProperty in (
                    "MaterialName",
                    "Name",
                    "name",
                    "Label",
                    "label",
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
                # PLAIN VALUE
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
        # REAL BOSQO PROPERTY
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
            # REAL FREECAD OBJECT
            # -------------------------------------------------

            part = None

            if row < len(
                self.rowParts
            ):

                part = self.rowParts[
                    row
                ]

            # -------------------------------------------------
            # OBJECT NAME
            # -------------------------------------------------

            objectName = ""

            try:

                objectName = str(
                    part.Name
                )

            except Exception:

                pass

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

                partType = str(
                    typeWidget.currentText()
                )

            else:

                partType = "Personalizada"

            # -------------------------------------------------
            # DIMENSIONS
            # -------------------------------------------------

            lengthItem = self.partsTable.item(
                row,
                2
            )

            widthItem = self.partsTable.item(
                row,
                3
            )

            thicknessItem = self.partsTable.item(
                row,
                4
            )

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

                material = str(
                    materialWidget.currentText()
                )

            else:

                material = ""

            # -------------------------------------------------
            # DATA
            # -------------------------------------------------

            partsData.append(
                {
                    "ObjectName":
                        objectName,

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