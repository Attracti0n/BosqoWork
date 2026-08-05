from PySide import QtWidgets, QtCore

from library.material_library import MaterialLibrary


class PartTableDialog(QtWidgets.QDialog):

    def __init__(
        self,
        module=None,
        parts=None,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle(
            "Redactar módulo"
        )

        self.resize(
            1250,
            750
        )

        #
        # Real BosqoModule object
        #

        self.module = module

        #
        # Parts
        #

        self.parts = (
            parts
            if isinstance(
                parts,
                list
            )
            else []
        )

        #
        # Row -> original object
        #

        self.rowObjects = {}

        #
        # Build interface
        #

        self.createUI()

        #
        # Load module data
        #

        self.loadModuleData()

        #
        # Load parts
        #

        self.loadParts()


    # =========================================================
    # UI
    # =========================================================

    def createUI(
        self
    ):

        mainLayout = QtWidgets.QVBoxLayout()


        #
        # MODULE PARAMETERS
        #

        moduleGroup = QtWidgets.QGroupBox(
            "Datos del módulo"
        )

        moduleLayout = QtWidgets.QGridLayout()


        #
        # Name
        #

        moduleLayout.addWidget(
            QtWidgets.QLabel(
                "Nombre del módulo:"
            ),
            0,
            0
        )

        self.nameEdit = QtWidgets.QLineEdit()

        moduleLayout.addWidget(
            self.nameEdit,
            0,
            1,
            1,
            3
        )


        #
        # Width
        #

        moduleLayout.addWidget(
            QtWidgets.QLabel(
                "Ancho:"
            ),
            1,
            0
        )

        self.widthSpin = self.createSpinBox()

        moduleLayout.addWidget(
            self.widthSpin,
            1,
            1
        )


        #
        # Height
        #

        moduleLayout.addWidget(
            QtWidgets.QLabel(
                "Alto:"
            ),
            1,
            2
        )

        self.heightSpin = self.createSpinBox()

        moduleLayout.addWidget(
            self.heightSpin,
            1,
            3
        )


        #
        # Depth
        #

        moduleLayout.addWidget(
            QtWidgets.QLabel(
                "Profundidad:"
            ),
            2,
            0
        )

        self.depthSpin = self.createSpinBox()

        moduleLayout.addWidget(
            self.depthSpin,
            2,
            1
        )


        #
        # Panel thickness
        #

        moduleLayout.addWidget(
            QtWidgets.QLabel(
                "Espesor panel:"
            ),
            2,
            2
        )

        self.thicknessSpin = self.createSpinBox()

        moduleLayout.addWidget(
            self.thicknessSpin,
            2,
            3
        )


        #
        # Back thickness
        #

        moduleLayout.addWidget(
            QtWidgets.QLabel(
                "Espesor fondo:"
            ),
            3,
            0
        )

        self.backThicknessSpin = self.createSpinBox()

        moduleLayout.addWidget(
            self.backThicknessSpin,
            3,
            1
        )


        #
        # Back inset
        #

        moduleLayout.addWidget(
            QtWidgets.QLabel(
                "Retranqueo trasero:"
            ),
            3,
            2
        )

        self.backInsetSpin = self.createSpinBox()

        moduleLayout.addWidget(
            self.backInsetSpin,
            3,
            3
        )


        moduleGroup.setLayout(
            moduleLayout
        )

        mainLayout.addWidget(
            moduleGroup
        )


        #
        # PARTS
        #

        partsGroup = QtWidgets.QGroupBox(
            "Tabla de piezas"
        )

        partsLayout = QtWidgets.QVBoxLayout()


        #
        # Table
        #

        self.table = QtWidgets.QTableWidget()

        self.table.setColumnCount(
            9
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Pieza",
                "Tipo",
                "Largo",
                "Ancho",
                "Espesor",
                "Cantidad",
                "Material",
                "Posición",
                "Modo"
            ]
        )


        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked
            |
            QtWidgets.QAbstractItemView.EditTrigger.EditKeyPressed
        )


        partsLayout.addWidget(
            self.table
        )


        #
        # PART BUTTONS
        #

        partButtons = QtWidgets.QHBoxLayout()


        self.addShelfButton = QtWidgets.QPushButton(
            "Añadir balda"
        )

        self.addDividerButton = QtWidgets.QPushButton(
            "Añadir separador"
        )

        self.addButton = QtWidgets.QPushButton(
            "Añadir pieza"
        )

        self.deleteButton = QtWidgets.QPushButton(
            "Eliminar"
        )

        self.duplicateButton = QtWidgets.QPushButton(
            "Duplicar"
        )


        partButtons.addWidget(
            self.addShelfButton
        )

        partButtons.addWidget(
            self.addDividerButton
        )

        partButtons.addWidget(
            self.addButton
        )

        partButtons.addWidget(
            self.deleteButton
        )

        partButtons.addWidget(
            self.duplicateButton
        )

        partButtons.addStretch()


        partsLayout.addLayout(
            partButtons
        )


        partsGroup.setLayout(
            partsLayout
        )

        mainLayout.addWidget(
            partsGroup
        )


        #
        # BOTTOM BUTTONS
        #

        bottomLayout = QtWidgets.QHBoxLayout()


        self.recalculateButton = QtWidgets.QPushButton(
            "Recalcular"
        )

        bottomLayout.addWidget(
            self.recalculateButton
        )

        bottomLayout.addStretch()


        self.saveButton = QtWidgets.QPushButton(
            "Guardar cambios"
        )

        self.cancelButton = QtWidgets.QPushButton(
            "Cancelar"
        )


        bottomLayout.addWidget(
            self.saveButton
        )

        bottomLayout.addWidget(
            self.cancelButton
        )


        mainLayout.addLayout(
            bottomLayout
        )


        #
        # CONNECTIONS
        #

        self.addShelfButton.clicked.connect(
            self.addShelf
        )

        self.addDividerButton.clicked.connect(
            self.addDivider
        )

        self.addButton.clicked.connect(
            self.addPart
        )

        self.deleteButton.clicked.connect(
            self.deletePart
        )

        self.duplicateButton.clicked.connect(
            self.duplicatePart
        )

        self.recalculateButton.clicked.connect(
            self.recalculate
        )

        self.saveButton.clicked.connect(
            self.saveChanges
        )

        self.cancelButton.clicked.connect(
            self.reject
        )


        self.setLayout(
            mainLayout
        )


    # =========================================================
    # SPINBOX
    # =========================================================

    def createSpinBox(
        self
    ):

        spin = QtWidgets.QDoubleSpinBox()

        spin.setRange(
            0,
            10000
        )

        spin.setDecimals(
            2
        )

        spin.setSuffix(
            " mm"
        )

        return spin


    # =========================================================
    # MODULE DATA
    # =========================================================

    def loadModuleData(
        self
    ):

        if self.module is None:

            return


        #
        # Name
        #

        if hasattr(
            self.module,
            "Label"
        ):

            self.nameEdit.setText(
                str(
                    self.module.Label
                )
            )


        #
        # Dimensions
        #

        self.widthSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "Width",
                    0
                )
            )
        )

        self.heightSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "Height",
                    0
                )
            )
        )

        self.depthSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "Depth",
                    0
                )
            )
        )


        #
        # Thickness
        #

        self.thicknessSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "PanelThickness",
                    0
                )
            )
        )

        self.backThicknessSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "BackThickness",
                    0
                )
            )
        )

        self.backInsetSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "BackInset",
                    0
                )
            )
        )


    # =========================================================
    # LOAD PARTS
    # =========================================================

    def loadParts(
        self
    ):

        self.table.setRowCount(
            0
        )

        self.rowObjects = {}


        for part in self.parts:

            #
            # Dictionary
            #

            if isinstance(
                part,
                dict
            ):

                data = dict(
                    part
                )

            #
            # FreeCAD object
            #

            else:

                data = self.objectToData(
                    part
                )

            if data is None:

                continue


            self.addPartRow(
                data
            )


        self.resizeColumns()


        #
        # Apply automatic positions
        #

        self.recalculatePositions(
            refresh=False
        )


    # =========================================================
    # OBJECT -> DATA
    # =========================================================

    def objectToData(
        self,
        part
    ):

        if part is None:

            return None


        role = str(
            getattr(
                part,
                "Role",
                ""
            )
        )


        if role == "Shelf":

            partType = "Balda"

        elif role == "Divider":

            partType = "Separador"

        elif role == "Custom":

            partType = "Personalizado"

        else:

            partType = "Estructural"


        positionMode = str(
            getattr(
                part,
                "PositionMode",
                "Automatic"
            )
        )


        if positionMode not in (
            "Automatic",
            "Manual"
        ):

            positionMode = "Automatic"


        position = self.value(
            getattr(
                part,
                "Position",
                0
            )
        )


        #
        # Determine position type
        #

        positionType = (
            getattr(
                part,
                "PositionType",
                None
            )
        )


        if positionType is None:

            positionType = "Automatic"


        return {

            "Object":
                part,

            "Code":
                str(
                    getattr(
                        part,
                        "Code",
                        ""
                    )
                ),

            "Label":
                str(
                    getattr(
                        part,
                        "Label",
                        "Pieza"
                    )
                ),

            "Role":
                role,

            "PartType":
                partType,

            "Length":
                self.value(
                    getattr(
                        part,
                        "Length",
                        0
                    )
                ),

            "Width":
                self.value(
                    getattr(
                        part,
                        "Width",
                        0
                    )
                ),

            "Thickness":
                self.value(
                    getattr(
                        part,
                        "Thickness",
                        0
                    )
                ),

            "Quantity":
                self.value(
                    getattr(
                        part,
                        "Quantity",
                        1
                    )
                ),

            "MaterialCode":
                str(
                    getattr(
                        part,
                        "MaterialCode",
                        ""
                    )
                ),

            "Position":
                position,

            "PositionType":
                positionType,

            "PositionMode":
                positionMode
        }


    # =========================================================
    # ADD ROW
    # =========================================================

    def addPartRow(
        self,
        data=None
    ):

        if data is None:

            data = {}


        row = self.table.rowCount()

        self.table.insertRow(
            row
        )


        #
        # NAME
        #

        item = QtWidgets.QTableWidgetItem(
            str(
                data.get(
                    "Label",
                    "Nueva pieza"
                )
            )
        )


        obj = data.get(
            "Object"
        )


        item.setData(
            QtCore.Qt.ItemDataRole.UserRole,
            obj
        )

        item.setData(
            QtCore.Qt.ItemDataRole.UserRole + 1,
            data.get(
                "Code",
                ""
            )
        )


        self.table.setItem(
            row,
            0,
            item
        )


        self.rowObjects[row] = obj


        #
        # TYPE
        #

        self.createTypeCombo(
            row,
            data.get(
                "PartType",
                "Estructural"
            )
        )


        #
        # DIMENSIONS
        #

        self.setText(
            row,
            2,
            self.number(
                data.get(
                    "Length",
                    0
                )
            )
        )

        self.setText(
            row,
            3,
            self.number(
                data.get(
                    "Width",
                    0
                )
            )
        )

        self.setText(
            row,
            4,
            self.number(
                data.get(
                    "Thickness",
                    0
                )
            )
        )


        #
        # QUANTITY
        #

        self.setText(
            row,
            5,
            self.number(
                data.get(
                    "Quantity",
                    1
                )
            )
        )


        #
        # MATERIAL
        #

        self.createMaterialCombo(
            row,
            data.get(
                "MaterialCode",
                ""
            )
        )


        #
        # POSITION
        #

        self.createPositionCombo(
            row,
            data
        )


        #
        # MODE
        #

        self.createPositionModeCombo(
            row,
            data.get(
                "PositionMode",
                "Automatic"
            )
        )


        self.updateRowState(
            row
        )


    # =========================================================
    # TYPE COMBO
    # =========================================================

    def createTypeCombo(
        self,
        row,
        selected
    ):

        combo = QtWidgets.QComboBox()


        combo.addItem(
            "Estructural",
            "Structural"
        )

        combo.addItem(
            "Balda",
            "Shelf"
        )

        combo.addItem(
            "Separador",
            "Divider"
        )

        combo.addItem(
            "Personalizado",
            "Custom"
        )


        #
        # Select
        #

        index = -1


        if selected in (
            "Estructural",
            "Balda",
            "Separador",
            "Personalizado"
        ):

            index = combo.findText(
                selected
            )

        else:

            index = combo.findData(
                selected
            )


        if index < 0:

            index = 0


        combo.setCurrentIndex(
            index
        )


        combo.currentIndexChanged.connect(
            lambda value,
            r=row:
            self.typeChanged(r)
        )


        self.table.setCellWidget(
            row,
            1,
            combo
        )


    # =========================================================
    # TYPE CHANGED
    # =========================================================

    def typeChanged(
        self,
        row
    ):

        self.updateRowState(
            row
        )


        #
        # Recalculate dimensions for
        # shelf / divider when selected.
        #

        combo = self.table.cellWidget(
            row,
            1
        )


        if combo is None:

            return


        role = combo.currentData()


        if role == "Shelf":

            self.setText(
                row,
                2,
                self.number(
                    self.widthSpin.value()
                    -
                    self.thicknessSpin.value() * 2
                )
            )

            self.setText(
                row,
                3,
                self.number(
                    self.depthSpin.value()
                )
            )

            self.setText(
                row,
                4,
                self.number(
                    self.thicknessSpin.value()
                )
            )


        elif role == "Divider":

            self.setText(
                row,
                2,
                self.number(
                    self.heightSpin.value()
                    -
                    self.thicknessSpin.value() * 2
                )
            )

            self.setText(
                row,
                3,
                self.number(
                    self.depthSpin.value()
                )
            )

            self.setText(
                row,
                4,
                self.number(
                    self.thicknessSpin.value()
                )
            )


        self.recalculatePositions(
            refresh=True
        )


    # =========================================================
    # MATERIAL COMBO
    # =========================================================

    def createMaterialCombo(
        self,
        row,
        selectedCode=""
    ):

        combo = QtWidgets.QComboBox()


        combo.addItem(
            "— Sin material —",
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
                    " — "
                    +
                    name
                )

            else:

                text = code


            combo.addItem(
                text,
                code
            )


        index = combo.findData(
            str(
                selectedCode
            )
        )


        if index >= 0:

            combo.setCurrentIndex(
                index
            )


        self.table.setCellWidget(
            row,
            6,
            combo
        )


    # =========================================================
    # POSITION COMBO
    # =========================================================

    def createPositionCombo(
        self,
        row,
        data
    ):

        combo = QtWidgets.QComboBox()


        combo.addItem(
            "Automática",
            "Automatic"
        )

        combo.addItem(
            "Inferior",
            "Bottom"
        )

        combo.addItem(
            "Centro",
            "Center"
        )

        combo.addItem(
            "Superior",
            "Top"
        )

        combo.addItem(
            "Manual",
            "Manual"
        )


        positionType = data.get(
            "PositionType",
            "Automatic"
        )


        index = combo.findData(
            positionType
        )


        if index < 0:

            index = 0


        combo.setCurrentIndex(
            index
        )


        combo.currentIndexChanged.connect(
            lambda value,
            r=row:
            self.positionTypeChanged(r)
        )


        self.table.setCellWidget(
            row,
            7,
            combo
        )


    # =========================================================
    # POSITION TYPE CHANGED
    # =========================================================

    def positionTypeChanged(
        self,
        row
    ):

        combo = self.table.cellWidget(
            row,
            7
        )


        if combo is None:

            return


        positionType = combo.currentData()


        #
        # Manual position:
        #
        # the position value remains editable.
        #

        if positionType == "Manual":

            modeCombo = self.table.cellWidget(
                row,
                8
            )


            if modeCombo is not None:

                modeCombo.setCurrentIndex(
                    modeCombo.findData(
                        "Manual"
                    )
                )


            self.updateRowState(
                row
            )

            return


        #
        # Automatic
        #

        if positionType == "Automatic":

            modeCombo = self.table.cellWidget(
                row,
                8
            )


            if modeCombo is not None:

                modeCombo.setCurrentIndex(
                    modeCombo.findData(
                        "Automatic"
                    )
                )


            self.recalculatePositions(
                refresh=True
            )

            return


        #
        # Fixed positions
        #

        self.setFixedPosition(
            row,
            positionType
        )


        self.updateRowState(
            row
        )


    # =========================================================
    # POSITION MODE
    # =========================================================

    def createPositionModeCombo(
        self,
        row,
        selected
    ):

        combo = QtWidgets.QComboBox()


        combo.addItem(
            "Automática",
            "Automatic"
        )

        combo.addItem(
            "Manual",
            "Manual"
        )


        if selected == "Manual":

            combo.setCurrentIndex(
                1
            )

        else:

            combo.setCurrentIndex(
                0
            )


        combo.currentIndexChanged.connect(
            lambda value,
            r=row:
            self.positionModeChanged(r)
        )


        self.table.setCellWidget(
            row,
            8,
            combo
        )


    # =========================================================
    # POSITION MODE CHANGED
    # =========================================================

    def positionModeChanged(
        self,
        row
    ):

        combo = self.table.cellWidget(
            row,
            8
        )


        if combo is None:

            return


        mode = combo.currentData()


        positionCombo = self.table.cellWidget(
            row,
            7
        )


        if mode == "Automatic":

            if positionCombo is not None:

                positionCombo.setCurrentIndex(
                    positionCombo.findData(
                        "Automatic"
                    )
                )


            self.recalculatePositions(
                refresh=True
            )


        else:

            if positionCombo is not None:

                positionCombo.setCurrentIndex(
                    positionCombo.findData(
                        "Manual"
                    )
                )


        self.updateRowState(
            row
        )


    # =========================================================
    # FIXED POSITION
    # =========================================================

    def setFixedPosition(
        self,
        row,
        positionType
    ):

        role = self.getRole(
            row
        )


        thickness = (
            self.thicknessSpin.value()
        )


        if role == "Shelf":

            if positionType == "Bottom":

                position = thickness

            elif positionType == "Center":

                position = (
                    self.heightSpin.value()
                    /
                    2
                )

            elif positionType == "Top":

                position = (
                    self.heightSpin.value()
                    -
                    thickness
                )

            else:

                return


        elif role == "Divider":

            if positionType == "Bottom":

                position = thickness

            elif positionType == "Center":

                position = (
                    self.widthSpin.value()
                    /
                    2
                )

            elif positionType == "Top":

                position = (
                    self.widthSpin.value()
                    -
                    thickness
                )

            else:

                return


        else:

            return


        #
        # Store position in numeric cell.
        #

        self.setText(
            row,
            7,
            self.number(
                position
            )
        )


        #
        # Manual/fixed positioning means
        # do not redistribute it.
        #

        modeCombo = self.table.cellWidget(
            row,
            8
        )


        if modeCombo is not None:

            modeCombo.setCurrentIndex(
                modeCombo.findData(
                    "Manual"
                )
            )


    # =========================================================
    # ROW STATE
    # =========================================================

    def updateRowState(
        self,
        row
    ):

        typeCombo = self.table.cellWidget(
            row,
            1
        )

        positionCombo = self.table.cellWidget(
            row,
            7
        )

        modeCombo = self.table.cellWidget(
            row,
            8
        )


        if typeCombo is None:

            return


        role = typeCombo.currentData()


        positional = role in (
            "Shelf",
            "Divider",
            "Custom"
        )


        #
        # Structural pieces do not need
        # a position selector.
        #

        if positionCombo is not None:

            positionCombo.setEnabled(
                positional
            )


        if modeCombo is not None:

            modeCombo.setEnabled(
                positional
            )


        #
        # Numeric position cell
        #

        positionItem = self.table.item(
            row,
            7
        )


        #
        # IMPORTANT:
        #
        # ItemIsEditable belongs to Qt.ItemFlag.
        #

        if positionItem is not None:

            positionItem.setFlags(
                positionItem.flags()
                |
                QtCore.Qt.ItemFlag.ItemIsEditable
            )


    # =========================================================
    # ADD SHELF
    # =========================================================

    def addShelf(
        self
    ):

        number = (
            self.countRole(
                "Shelf"
            )
            +
            1
        )


        data = {

            "Object":
                None,

            "Code":
                "",

            "Label":
                "Balda "
                +
                str(
                    number
                ),

            "Role":
                "Shelf",

            "PartType":
                "Balda",

            "Length":
                self.widthSpin.value()
                -
                self.thicknessSpin.value() * 2,

            "Width":
                self.depthSpin.value(),

            "Thickness":
                self.thicknessSpin.value(),

            "Quantity":
                1,

            "MaterialCode":
                "",

            "Position":
                0,

            "PositionType":
                "Automatic",

            "PositionMode":
                "Automatic"
        }


        self.addPartRow(
            data
        )


        self.recalculatePositions(
            refresh=True
        )


        self.table.selectRow(
            self.table.rowCount() - 1
        )


    # =========================================================
    # ADD DIVIDER
    # =========================================================

    def addDivider(
        self
    ):

        number = (
            self.countRole(
                "Divider"
            )
            +
            1
        )


        data = {

            "Object":
                None,

            "Code":
                "",

            "Label":
                "Separador "
                +
                str(
                    number
                ),

            "Role":
                "Divider",

            "PartType":
                "Separador",

            "Length":
                self.heightSpin.value()
                -
                self.thicknessSpin.value() * 2,

            "Width":
                self.depthSpin.value(),

            "Thickness":
                self.thicknessSpin.value(),

            "Quantity":
                1,

            "MaterialCode":
                "",

            "Position":
                0,

            "PositionType":
                "Automatic",

            "PositionMode":
                "Automatic"
        }


        self.addPartRow(
            data
        )


        self.recalculatePositions(
            refresh=True
        )


        self.table.selectRow(
            self.table.rowCount() - 1
        )


    # =========================================================
    # ADD CUSTOM PART
    # =========================================================

    def addPart(
        self
    ):

        #
        # New piece defaults to
        # Estructural.
        #

        data = {

            "Object":
                None,

            "Code":
                "",

            "Label":
                "Nueva pieza",

            "Role":
                "Structural",

            "PartType":
                "Estructural",

            "Length":
                self.widthSpin.value(),

            "Width":
                self.depthSpin.value(),

            "Thickness":
                self.thicknessSpin.value(),

            "Quantity":
                1,

            "MaterialCode":
                "",

            "Position":
                0,

            "PositionType":
                "Manual",

            "PositionMode":
                "Manual"
        }


        row = self.table.rowCount()


        self.addPartRow(
            data
        )


        self.table.selectRow(
            row
        )


        self.table.setCurrentCell(
            row,
            0
        )


        self.table.editItem(
            self.table.item(
                row,
                0
            )
        )


    # =========================================================
    # DELETE
    # =========================================================

    def deletePart(
        self
    ):

        row = self.table.currentRow()


        if row < 0:

            QtWidgets.QMessageBox.information(
                self,
                "Eliminar pieza",
                "Selecciona primero una pieza."
            )

            return


        result = QtWidgets.QMessageBox.question(
            self,
            "Eliminar pieza",
            "¿Seguro que quieres eliminar la pieza seleccionada?",
            QtWidgets.QMessageBox.StandardButton.Yes
            |
            QtWidgets.QMessageBox.StandardButton.No
        )


        if (
            result
            !=
            QtWidgets.QMessageBox.StandardButton.Yes
        ):

            return


        #
        # Remove real object immediately
        # only after confirmation.
        #

        item = self.table.item(
            row,
            0
        )


        obj = None


        if item is not None:

            obj = item.data(
                QtCore.Qt.ItemDataRole.UserRole
            )


        if (
            obj is not None
            and
            self.module is not None
        ):

            try:

                self.module.removeObject(
                    obj
                )

                self.module.Document.removeObject(
                    obj.Name
                )

            except Exception:
                pass


        self.table.removeRow(
            row
        )


        self.rebuildRowObjects()


    # =========================================================
    # DUPLICATE
    # =========================================================

    def duplicatePart(
        self
    ):

        row = self.table.currentRow()


        if row < 0:

            QtWidgets.QMessageBox.information(
                self,
                "Duplicar pieza",
                "Selecciona primero una pieza."
            )

            return


        data = self.getRowData(
            row
        )


        if data is None:

            return


        data["Object"] = None

        data["Code"] = ""

        data["Label"] = (
            data.get(
                "Label",
                "Pieza"
            )
            +
            " copia"
        )


        newRow = self.table.rowCount()


        self.addPartRow(
            data
        )


        self.table.selectRow(
            newRow
        )


    # =========================================================
    # GET ROW DATA
    # =========================================================

    def getRowData(
        self,
        row
    ):

        if row < 0:

            return None


        item = self.table.item(
            row,
            0
        )


        if item is None:

            return None


        typeCombo = self.table.cellWidget(
            row,
            1
        )


        if typeCombo is None:

            return None


        positionCombo = self.table.cellWidget(
            row,
            7
        )

        modeCombo = self.table.cellWidget(
            row,
            8
        )

        materialCombo = self.table.cellWidget(
            row,
            6
        )


        role = typeCombo.currentData()

        partType = typeCombo.currentText()


        positionType = "Automatic"


        if positionCombo is not None:

            positionType = (
                positionCombo.currentData()
            )


        positionMode = "Automatic"


        if modeCombo is not None:

            positionMode = (
                modeCombo.currentData()
            )


        materialCode = ""


        if materialCombo is not None:

            value = materialCombo.currentData()

            if value:

                materialCode = str(
                    value
                )


        objectValue = item.data(
            QtCore.Qt.ItemDataRole.UserRole
        )


        code = item.data(
            QtCore.Qt.ItemDataRole.UserRole + 1
        )


        return {

            "Object":
                objectValue,

            "Code":
                str(
                    code
                    if code is not None
                    else ""
                ),

            "Label":
                item.text().strip(),

            "Role":
                role,

            "PartType":
                partType,

            "Length":
                self.getFloat(
                    row,
                    2
                ),

            "Width":
                self.getFloat(
                    row,
                    3
                ),

            "Thickness":
                self.getFloat(
                    row,
                    4
                ),

            "Quantity":
                self.getFloat(
                    row,
                    5
                ),

            "MaterialCode":
                materialCode,

            "Position":
                self.getFloat(
                    row,
                    7
                ),

            "PositionType":
                positionType,

            "PositionMode":
                positionMode
        }


    # =========================================================
    # GET DATA
    # =========================================================

    def getData(
        self
    ):

        data = []


        for row in range(
            self.table.rowCount()
        ):

            part = self.getRowData(
                row
            )


            if part is not None:

                data.append(
                    part
                )


        return data


    # =========================================================
    # APPLY CHANGES
    # =========================================================

    def applyChanges(
        self
    ):

        if self.module is None:

            return


        #
        # Update module
        #

        self.updateModule()


        #
        # Read all rows
        #

        rows = []


        for row in range(
            self.table.rowCount()
        ):

            data = self.getRowData(
                row
            )


            if data is not None:

                rows.append(
                    data
                )


        #
        # Apply/create parts
        #

        for data in rows:

            part = data.get(
                "Object"
            )


            #
            # New piece
            #

            if part is None:

                part = self.createPart(
                    data
                )

                if part is None:

                    continue


                #
                # Store reference in table
                #

                item = self.table.item(
                    rows.index(data),
                    0
                )


                if item is not None:

                    item.setData(
                        QtCore.Qt.ItemDataRole.UserRole,
                        part
                    )


            #
            # Apply data
            #

            self.applyPartData(
                part,
                data
            )


        #
        # Recompute
        #

        self.module.Document.recompute()


        #
        # Refresh original parts list
        #

        self.parts = (
            self.module.Proxy.getParts(
                self.module
            )
        )


    # =========================================================
    # CREATE PART
    # =========================================================

    def createPart(
        self,
        data
    ):

        if self.module is None:

            return None


        try:

            from objects.bosqo_part import create_part


            part = create_part(
                self.module.Document
            )


            #
            # Generate code
            #

            code = data.get(
                "Code",
                ""
            )


            if not code:

                code = self.generateCode(
                    data.get(
                        "Role",
                        "Custom"
                    )
                )


            data["Code"] = code


            #
            # Add to module
            #

            self.module.addObject(
                part
            )


            #
            # Apply data
            #

            if hasattr(
                part,
                "Code"
            ):

                part.Code = code


            return part


        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error creando pieza: "
                +
                str(
                    error
                )
                +
                "\n"
            )

            return None


    # =========================================================
    # GENERATE CODE
    # =========================================================

    def generateCode(
        self,
        role
    ):

        if role == "Shelf":

            prefix = "SH"

        elif role == "Divider":

            prefix = "DV"

        elif role == "Structural":

            prefix = "CU"

        else:

            prefix = "CU"


        used = set()


        if self.module is not None:

            for part in self.module.Group:

                if not hasattr(
                    part,
                    "Code"
                ):

                    continue


                code = str(
                    part.Code
                )


                if code:

                    used.add(
                        code
                    )


        number = 1


        while (
            prefix
            +
            str(
                number
            )
            in used
        ):

            number += 1


        return (
            prefix
            +
            str(
                number
            )
        )


    # =========================================================
    # SAVE
    # =========================================================

    def saveChanges(
        self
    ):

        try:

            self.recalculatePositions(
                refresh=False
            )


            self.applyChanges()


            self.accept()


        except Exception as error:

            QtWidgets.QMessageBox.warning(
                self,
                "Guardar cambios",
                "Error guardando cambios:\n\n"
                +
                str(
                    error
                )
            )


    # =========================================================
    # UPDATE MODULE
    # =========================================================

    def updateModule(
        self
    ):

        if self.module is None:

            return


        self.module.Label = (
            self.nameEdit.text().strip()
            or
            "Módulo"
        )


        self.module.Width = (
            self.widthSpin.value()
        )

        self.module.Height = (
            self.heightSpin.value()
        )

        self.module.Depth = (
            self.depthSpin.value()
        )

        self.module.PanelThickness = (
            self.thicknessSpin.value()
        )

        self.module.BackThickness = (
            self.backThicknessSpin.value()
        )

        self.module.BackInset = (
            self.backInsetSpin.value()
        )


    # =========================================================
    # APPLY PART DATA
    # =========================================================

    def applyPartData(
        self,
        part,
        data
    ):

        #
        # Label
        #

        if hasattr(
            part,
            "Label"
        ):

            part.Label = data[
                "Label"
            ]


        #
        # Code
        #

        if hasattr(
            part,
            "Code"
        ):

            code = data.get(
                "Code",
                ""
            )


            if not code:

                code = self.generateCode(
                    data.get(
                        "Role",
                        "Custom"
                    )
                )


            part.Code = code


        #
        # Dimensions
        #

        if hasattr(
            part,
            "Length"
        ):

            part.Length = data[
                "Length"
            ]


        if hasattr(
            part,
            "Width"
        ):

            part.Width = data[
                "Width"
            ]


        if hasattr(
            part,
            "Thickness"
        ):

            part.Thickness = data[
                "Thickness"
            ]


        #
        # Quantity
        #

        if hasattr(
            part,
            "Quantity"
        ):

            part.Quantity = data[
                "Quantity"
            ]


        #
        # Material
        #

        if hasattr(
            part,
            "MaterialCode"
        ):

            part.MaterialCode = data[
                "MaterialCode"
            ]


        #
        # Role
        #

        if hasattr(
            part,
            "Role"
        ):

            part.Role = data[
                "Role"
            ]


        #
        # Position
        #

        if hasattr(
            part,
            "Position"
        ):

            part.Position = data[
                "Position"
            ]


        #
        # Position type
        #

        if hasattr(
            part,
            "PositionType"
        ):

            part.PositionType = data.get(
                "PositionType",
                "Automatic"
            )


        #
        # Position mode
        #

        if hasattr(
            part,
            "PositionMode"
        ):

            part.PositionMode = data.get(
                "PositionMode",
                "Automatic"
            )


        part.touch()


    # =========================================================
    # RECALCULATE
    # =========================================================

    def recalculate(
        self
    ):

        #
        # Update module values first.
        #

        self.updateModule()


        #
        # Recalculate table dimensions.
        #
        # IMPORTANT:
        #
        # We deliberately DO NOT call
        # ModuleBuilder.build().
        #
        # Otherwise imported/custom parts
        # could be considered obsolete and
        # removed.
        #

        for row in range(
            self.table.rowCount()
        ):

            typeCombo = self.table.cellWidget(
                row,
                1
            )


            if typeCombo is None:

                continue


            role = typeCombo.currentData()


            #
            # Shelf
            #

            if role == "Shelf":

                self.setText(
                    row,
                    2,
                    self.number(
                        self.widthSpin.value()
                        -
                        self.thicknessSpin.value() * 2
                    )
                )

                self.setText(
                    row,
                    3,
                    self.number(
                        self.depthSpin.value()
                    )
                )

                self.setText(
                    row,
                    4,
                    self.number(
                        self.thicknessSpin.value()
                    )
                )


            #
            # Divider
            #

            elif role == "Divider":

                self.setText(
                    row,
                    2,
                    self.number(
                        self.heightSpin.value()
                        -
                        self.thicknessSpin.value() * 2
                    )
                )

                self.setText(
                    row,
                    3,
                    self.number(
                        self.depthSpin.value()
                    )
                )

                self.setText(
                    row,
                    4,
                    self.number(
                        self.thicknessSpin.value()
                    )
                )


            #
            # Structural pieces
            #

            elif role == "Structural":

                self.recalculateStructuralRow(
                    row
                )


        #
        # Automatic positions
        #

        self.recalculatePositions(
            refresh=True
        )


        #
        # If module exists, update the
        # existing geometry through the
        # current parts.
        #

        if self.module is not None:

            self.module.Document.recompute()


    # =========================================================
    # STRUCTURAL ROW
    # =========================================================

    def recalculateStructuralRow(
        self,
        row
    ):

        item = self.table.item(
            row,
            0
        )


        if item is None:

            return


        code = item.data(
            QtCore.Qt.ItemDataRole.UserRole + 1
        )


        if code == "LS":

            self.setText(
                row,
                2,
                self.number(
                    self.heightSpin.value()
                )
            )

            self.setText(
                row,
                3,
                self.number(
                    self.depthSpin.value()
                )
            )

            self.setText(
                row,
                4,
                self.number(
                    self.thicknessSpin.value()
                )
            )


        elif code == "RS":

            self.setText(
                row,
                2,
                self.number(
                    self.heightSpin.value()
                )
            )

            self.setText(
                row,
                3,
                self.number(
                    self.depthSpin.value()
                )
            )

            self.setText(
                row,
                4,
                self.number(
                    self.thicknessSpin.value()
                )
            )


        elif code in (
            "BT",
            "TP"
        ):

            self.setText(
                row,
                2,
                self.number(
                    self.widthSpin.value()
                    -
                    self.thicknessSpin.value() * 2
                )
            )

            self.setText(
                row,
                3,
                self.number(
                    self.depthSpin.value()
                )
            )

            self.setText(
                row,
                4,
                self.number(
                    self.thicknessSpin.value()
                )
            )


        elif code == "BK":

            self.setText(
                row,
                2,
                self.number(
                    self.heightSpin.value()
                )
            )

            self.setText(
                row,
                3,
                self.number(
                    self.widthSpin.value()
                )
            )

            self.setText(
                row,
                4,
                self.number(
                    self.backThicknessSpin.value()
                )
            )


    # =========================================================
    # AUTOMATIC POSITIONS
    # =========================================================

    def recalculatePositions(
        self,
        refresh=True
    ):

        shelves = []

        dividers = []


        #
        # Find automatic shelves/dividers.
        #

        for row in range(
            self.table.rowCount()
        ):

            role = self.getRole(
                row
            )


            if role not in (
                "Shelf",
                "Divider"
            ):

                continue


            modeCombo = self.table.cellWidget(
                row,
                8
            )


            positionCombo = self.table.cellWidget(
                row,
                7
            )


            if modeCombo is None:

                continue


            if (
                modeCombo.currentData()
                !=
                "Automatic"
            ):

                continue


            if positionCombo is None:

                continue


            if (
                positionCombo.currentData()
                !=
                "Automatic"
            ):

                continue


            if role == "Shelf":

                shelves.append(
                    row
                )

            else:

                dividers.append(
                    row
                )


        #
        # SHELVES
        #

        if shelves:

            usableHeight = (
                self.heightSpin.value()
                -
                self.thicknessSpin.value() * 2
            )


            spacing = (
                usableHeight
                /
                (
                    len(
                        shelves
                    )
                    +
                    1
                )
            )


            for index, row in enumerate(
                shelves,
                start=1
            ):

                position = (
                    self.thicknessSpin.value()
                    +
                    spacing * index
                )


                self.setText(
                    row,
                    7,
                    self.number(
                        position
                    )
                )


        #
        # DIVIDERS
        #

        if dividers:

            usableWidth = (
                self.widthSpin.value()
                -
                self.thicknessSpin.value() * 2
            )


            spacing = (
                usableWidth
                /
                (
                    len(
                        dividers
                    )
                    +
                    1
                )
            )


            for index, row in enumerate(
                dividers,
                start=1
            ):

                position = (
                    self.thicknessSpin.value()
                    +
                    spacing * index
                )


                self.setText(
                    row,
                    7,
                    self.number(
                        position
                    )
                )


        if refresh:

            self.table.viewport().update()


    # =========================================================
    # ROLE
    # =========================================================

    def getRole(
        self,
        row
    ):

        combo = self.table.cellWidget(
            row,
            1
        )


        if combo is None:

            return ""


        return combo.currentData()


    # =========================================================
    # COUNT ROLE
    # =========================================================

    def countRole(
        self,
        role
    ):

        count = 0


        for row in range(
            self.table.rowCount()
        ):

            if self.getRole(
                row
            ) == role:

                count += 1


        return count


    # =========================================================
    # HELPERS
    # =========================================================

    def getText(
        self,
        row,
        column
    ):

        item = self.table.item(
            row,
            column
        )


        if item is None:

            return ""


        return item.text().strip()


    def getFloat(
        self,
        row,
        column
    ):

        value = self.getText(
            row,
            column
        )


        if not value:

            return 0


        try:

            return float(
                value.replace(
                    ",",
                    "."
                )
            )

        except Exception:

            return 0


    def setText(
        self,
        row,
        column,
        value
    ):

        item = self.table.item(
            row,
            column
        )


        if item is None:

            item = QtWidgets.QTableWidgetItem()

            self.table.setItem(
                row,
                column,
                item
            )


        item.setText(
            str(
                value
            )
        )


    def number(
        self,
        value
    ):

        try:

            number = float(
                value
            )


            if number.is_integer():

                return str(
                    int(
                        number
                    )
                )


            return str(
                round(
                    number,
                    2
                )
            )

        except Exception:

            return "0"


    def value(
        self,
        value
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

            return 0


    def rebuildRowObjects(
        self
    ):

        self.rowObjects = {}


        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0
            )


            if item is None:

                continue


            self.rowObjects[row] = item.data(
                QtCore.Qt.ItemDataRole.UserRole
            )


    def resizeColumns(
        self
    ):

        self.table.resizeColumnsToContents()


        widths = {

            0: 180,
            1: 130,
            2: 90,
            3: 90,
            4: 90,
            5: 80,
            6: 220,
            7: 130,
            8: 110
        }


        for column, width in widths.items():

            self.table.setColumnWidth(
                column,
                width
            )