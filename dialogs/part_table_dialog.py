import FreeCAD

from PySide import QtWidgets, QtCore

from library.material_library import MaterialLibrary


class ManualPlacementDialog(QtWidgets.QDialog):

    def __init__(
        self,
        part,
        parent=None
    ):

        super().__init__(parent)
        self.part = part
        self.setWindowTitle("Posición y giro")
        self.resize(420, 300)

        layout = QtWidgets.QVBoxLayout(self)

        positionGroup = QtWidgets.QGroupBox("Posición")
        positionLayout = QtWidgets.QGridLayout()

        self.xSpin = self.createSpinBox()
        self.ySpin = self.createSpinBox()
        self.zSpin = self.createSpinBox()

        for row, label, widget in (
            (0, "X:", self.xSpin),
            (1, "Y:", self.ySpin),
            (2, "Z:", self.zSpin)
        ):
            positionLayout.addWidget(QtWidgets.QLabel(label), row, 0)
            positionLayout.addWidget(widget, row, 1)

        positionGroup.setLayout(positionLayout)
        layout.addWidget(positionGroup)

        rotationGroup = QtWidgets.QGroupBox("Giro")
        rotationLayout = QtWidgets.QGridLayout()

        self.rxSpin = self.createAngleSpinBox()
        self.rySpin = self.createAngleSpinBox()
        self.rzSpin = self.createAngleSpinBox()

        for row, label, widget in (
            (0, "Giro X:", self.rxSpin),
            (1, "Giro Y:", self.rySpin),
            (2, "Giro Z:", self.rzSpin)
        ):
            rotationLayout.addWidget(QtWidgets.QLabel(label), row, 0)
            rotationLayout.addWidget(widget, row, 1)

        rotationGroup.setLayout(rotationLayout)
        layout.addWidget(rotationGroup)

        buttons = QtWidgets.QHBoxLayout()
        buttons.addStretch()

        cancelButton = QtWidgets.QPushButton("Cancelar")
        okButton = QtWidgets.QPushButton("Aceptar")

        buttons.addWidget(cancelButton)
        buttons.addWidget(okButton)
        layout.addLayout(buttons)

        cancelButton.clicked.connect(self.reject)
        okButton.clicked.connect(self.accept)

        self.loadData()

    def createSpinBox(self):
        spin = QtWidgets.QDoubleSpinBox()
        spin.setRange(-10000, 10000)
        spin.setDecimals(2)
        spin.setSuffix(" mm")
        return spin

    def createAngleSpinBox(self):
        spin = QtWidgets.QDoubleSpinBox()
        spin.setRange(-360, 360)
        spin.setDecimals(2)
        spin.setSuffix(" °")
        return spin

    def loadData(self):
        self.xSpin.setValue(self.toFloat(self.part.get("PositionX", 0)))
        self.ySpin.setValue(self.toFloat(self.part.get("PositionY", 0)))
        self.zSpin.setValue(self.toFloat(self.part.get("PositionZ", self.part.get("Position", 0))))
        self.rxSpin.setValue(self.toFloat(self.part.get("RotationX", 0)))
        self.rySpin.setValue(self.toFloat(self.part.get("RotationY", 0)))
        self.rzSpin.setValue(self.toFloat(self.part.get("RotationZ", 0)))

    def getData(self):
        return {
            "PositionX": self.xSpin.value(),
            "PositionY": self.ySpin.value(),
            "PositionZ": self.zSpin.value(),
            "RotationX": self.rxSpin.value(),
            "RotationY": self.rySpin.value(),
            "RotationZ": self.rzSpin.value()
        }

    def toFloat(self, value):
        try:
            if hasattr(value, "Value"):
                return float(value.Value)
            return float(value)
        except Exception:
            return 0.0


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
            "Editar módulo"
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

        # Igual que el diálogo paramétrico: calcular inmediatamente
        # para que dimensiones y posiciones de baldas/separadores
        # reflejen las dimensiones actuales del módulo.
        self.recalculate()


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

        self.addButton = QtWidgets.QPushButton(
            "Añadir pieza"
        )

        self.deleteButton = QtWidgets.QPushButton(
            "Eliminar"
        )

        self.duplicateButton = QtWidgets.QPushButton(
            "Duplicar"
        )

        self.placementButton = QtWidgets.QPushButton(
            "Posición / giro"
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

        partButtons.addWidget(
            self.placementButton
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

        self.addButton.clicked.connect(
            self.addPart
        )

        self.deleteButton.clicked.connect(
            self.deletePart
        )

        self.duplicateButton.clicked.connect(
            self.duplicatePart
        )

        self.placementButton.clicked.connect(
            self.editPlacement
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


        #
        # Read current FreeCAD placement when available.
        #

        positionX = 0
        positionY = 0
        positionZ = position

        rotationX = 0
        rotationY = 0
        rotationZ = 0

        try:

            placement = part.Placement

            positionX = float(
                placement.Base.x
            )

            positionY = float(
                placement.Base.y
            )

            positionZ = float(
                placement.Base.z
            )

            yaw, pitch, roll = (
                placement.Rotation.getYawPitchRoll()
            )

            rotationZ = float(yaw)
            rotationY = float(pitch)
            rotationX = float(roll)

        except Exception:

            pass


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

            "PositionX":
                positionX,

            "PositionY":
                positionY,

            "PositionZ":
                positionZ,

            "RotationX":
                rotationX,

            "RotationY":
                rotationY,

            "RotationZ":
                rotationZ,

            "PositionType":
                positionType,

            "PositionMode":
                positionMode,

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

        item.setData(
            QtCore.Qt.ItemDataRole.UserRole + 3,
            data.get(
                "Role",
                "Custom"
            )
        )


        self.table.setItem(
            row,
            0,
            item
        )


        self.rowObjects[row] = obj

        # Guardamos también los datos de colocación de la fila.
        # No son propiedades de BosqoPart; la colocación real se
        # aplica al Placement del objeto al guardar/recalcular.
        item.setData(
            QtCore.Qt.ItemDataRole.UserRole + 2,
            {
                "PositionX": data.get("PositionX", 0),
                "PositionY": data.get("PositionY", 0),
                "PositionZ": data.get("PositionZ", data.get("Position", 0)),
                "RotationX": data.get("RotationX", 0),
                "RotationY": data.get("RotationY", 0),
                "RotationZ": data.get("RotationZ", 0)
            }
        )


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

        #
        # Structural is selectable too.
        # A generated structural piece can be converted
        # into a shelf, divider or custom piece.
        #

        combo.setEnabled(True)


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


        combo = self.table.cellWidget(
            row,
            1
        )

        if combo is None:

            return


        role = combo.currentData()

        item = self.table.item(
            row,
            0
        )

        if item is None:

            return


        code = item.data(
            QtCore.Qt.ItemDataRole.UserRole + 1
        )


        #
        # If a generated structural piece is changed
        # to a user type, it must stop being one of
        # LS / RS / BT / TP / BK.
        #

        structuralCodes = {
            "LS",
            "RS",
            "BT",
            "TP",
            "BK"
        }


        if (
            role != "Structural"
            and
            code in structuralCodes
        ):

            newCode = self.generateCode(
                role
            )

            item.setData(
                QtCore.Qt.ItemDataRole.UserRole + 1,
                newCode
            )

            item.setText(
                item.text()
            )


        #
        # If a user piece is returned to Structural,
        # keep its own dimensions. It becomes a
        # user structural piece, not one of the five
        # generated module panels.
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
        # Update automatic positions.
        #

        self.recalculatePositions(
            refresh=True
        )


        #
        # Immediately update the real object.
        #

        if self.module is not None:

            data = self.getRowData(
                row
            )

            if data is not None:

                part = data.get(
                    "Object"
                )

                if part is not None:

                    self.applyPartData(
                        part,
                        data
                    )

                    self.module.Document.recompute()


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


        self.recalculate()


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


        self.recalculate()


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
                "Custom",

            "PartType":
                "Personalizado",

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

            "PositionX":
                0,

            "PositionY":
                0,

            "PositionZ":
                0,

            "RotationX":
                0,

            "RotationY":
                0,

            "RotationZ":
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
    # EDIT PLACEMENT
    # =========================================================

    def editPlacement(
        self
    ):

        row = self.table.currentRow()

        if row < 0:

            QtWidgets.QMessageBox.information(
                self,
                "Posición / giro",
                "Selecciona primero una pieza."
            )

            return

        role = self.getRole(row)

        if role == "Structural":

            QtWidgets.QMessageBox.information(
                self,
                "Posición / giro",
                "Las piezas estructurales se posicionan automáticamente."
            )

            return

        data = self.getRowData(row)

        if data is None:
            return

        dialog = ManualPlacementDialog(
            data,
            self
        )

        if dialog.exec_():

            placementData = dialog.getData()

            item = self.table.item(row, 0)

            if item is not None:

                item.setData(
                    QtCore.Qt.ItemDataRole.UserRole + 2,
                    placementData
                )

            modeCombo = self.table.cellWidget(row, 8)
            positionCombo = self.table.cellWidget(row, 7)

            if modeCombo is not None:
                index = modeCombo.findData("Manual")
                if index >= 0:
                    modeCombo.setCurrentIndex(index)

            if positionCombo is not None:
                index = positionCombo.findData("Manual")
                if index >= 0:
                    positionCombo.setCurrentIndex(index)

            self.recalculate()


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

        if self.getRole(row) == "Structural":

            QtWidgets.QMessageBox.information(
                self,
                "Duplicar pieza",
                "Selecciona una pieza creada por el usuario."
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
    # LIVE PART
    # =========================================================

    def getLivePart(
        self,
        part=None,
        code=None
    ):

        if self.module is not None and code is not None:

            try:
                code = str(code)

                for candidate in list(self.module.Group):
                    try:
                        candidateCode = str(
                            getattr(candidate, "Code", "")
                        )
                        if candidateCode == code:
                            return candidate
                    except Exception:
                        continue
            except Exception:
                pass

        if part is None:
            return None

        try:
            name = part.Name
            document = part.Document
            if document is None:
                return None
            current = document.getObject(name)
            if current is None:
                return None
            current.Label
            return current
        except Exception:
            return None


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


        uiRole = typeCombo.currentData()

        role = uiRole

        if uiRole == "Structural":

            originalRole = item.data(
                QtCore.Qt.ItemDataRole.UserRole + 3
            )

            if originalRole in (
                "Side",
                "Top",
                "Bottom",
                "Back"
            ):

                role = originalRole

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


        # Keep the object attached to the row. Never replace an existing
        # live object by looking it up again by Code.
        objectValue = item.data(
            QtCore.Qt.ItemDataRole.UserRole
        )

        code = item.data(
            QtCore.Qt.ItemDataRole.UserRole + 1
        )

        if objectValue is not None:
            try:
                name = objectValue.Name
                document = objectValue.Document
                if document is None or document.getObject(name) is None:
                    objectValue = None
            except Exception:
                objectValue = None

        # Only search by Code when the row has no object.
        if objectValue is None and code:
            objectValue = self.getLivePart(
                None,
                code
            )

        if objectValue is not None:
            item.setData(
                QtCore.Qt.ItemDataRole.UserRole,
                objectValue
            )


        # Existing automatic shelves/dividers keep their real
        # dimensions if the table cell is temporarily empty or zero.
        # The table remains authoritative when it contains valid values.
        length = self.getFloat(row, 2)
        width = self.getFloat(row, 3)
        thickness = self.getFloat(row, 4)

        if (
            objectValue is not None
            and
            role in ("Shelf", "Divider")
            and
            positionMode == "Automatic"
            and
            (length <= 0 or width <= 0 or thickness <= 0)
        ):
            try:
                objectLength = self.value(getattr(objectValue, "Length", 0))
                objectWidth = self.value(getattr(objectValue, "Width", 0))
                objectThickness = self.value(getattr(objectValue, "Thickness", 0))

                if objectLength > 0:
                    length = objectLength
                if objectWidth > 0:
                    width = objectWidth
                if objectThickness > 0:
                    thickness = objectThickness
            except Exception:
                pass


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
                length,

            "Width":
                width,

            "Thickness":
                thickness,

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

            "PositionX":
                (
                    item.data(
                        QtCore.Qt.ItemDataRole.UserRole + 2
                    ) or {}
                ).get(
                    "PositionX",
                    0
                ),

            "PositionY":
                (
                    item.data(
                        QtCore.Qt.ItemDataRole.UserRole + 2
                    ) or {}
                ).get(
                    "PositionY",
                    0
                ),

            "PositionZ":
                (
                    item.data(
                        QtCore.Qt.ItemDataRole.UserRole + 2
                    ) or {}
                ).get(
                    "PositionZ",
                    self.getFloat(row, 7)
                ),

            "RotationX":
                (
                    item.data(
                        QtCore.Qt.ItemDataRole.UserRole + 2
                    ) or {}
                ).get(
                    "RotationX",
                    0
                ),

            "RotationY":
                (
                    item.data(
                        QtCore.Qt.ItemDataRole.UserRole + 2
                    ) or {}
                ).get(
                    "RotationY",
                    0
                ),

            "RotationZ":
                (
                    item.data(
                        QtCore.Qt.ItemDataRole.UserRole + 2
                    ) or {}
                ).get(
                    "RotationZ",
                    0
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

        for rowIndex, data in enumerate(rows):

            part = data.get(
                "Object"
            )


            #
            # New piece

            if part is None:

                part = self.createPart(
                    data
                )

                if part is None:
                    continue

                # This exact object belongs to this exact table row.
                data["Object"] = part

                item = self.table.item(
                    rowIndex,
                    0
                )

                if item is not None:
                    item.setData(
                        QtCore.Qt.ItemDataRole.UserRole,
                        part
                    )
                    item.setData(
                        QtCore.Qt.ItemDataRole.UserRole + 1,
                        data.get("Code", "")
                    )


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

        if part is None:
            return

        # Always resolve the live FreeCAD object.
        part = self.getLivePart(
            part,
            data.get("Code", "")
        )

        if part is None:
            return

        # -----------------------------------------------------
        # Prepare data exactly in the form used by ModuleBuilder.
        # -----------------------------------------------------

        role = data.get(
            "Role",
            "Custom"
        )

        code = str(
            data.get(
                "Code",
                ""
            )
        )

        if not code:

            code = self.generateCode(
                role
            )

        positionMode = data.get(
            "PositionMode",
            "Automatic"
        )

        # Work on a copy. This is important because the dictionary
        # belongs to the table row and may be reused later.
        partData = dict(
            data
        )

        partData["Code"] = code
        partData["Role"] = role
        partData["Source"] = partData.get(
            "Source",
            "Module"
        )
        partData["Label"] = partData.get(
            "Label",
            "Pieza"
        )
        partData["PartType"] = partData.get(
            "PartType",
            "Personalizado"
        )
        partData["Material"] = partData.get(
            "Material",
            ""
        )
        partData["MaterialCode"] = partData.get(
            "MaterialCode",
            ""
        )
        partData["Quantity"] = partData.get(
            "Quantity",
            1
        )
        partData["PositionMode"] = positionMode

        # -----------------------------------------------------
        # Axis definition
        # -----------------------------------------------------

        if role == "Shelf":

            partData["LengthAxis"] = "X"
            partData["WidthAxis"] = "Y"
            partData["ThicknessAxis"] = "Z"

        elif role == "Divider":

            partData["LengthAxis"] = "Z"
            partData["WidthAxis"] = "Y"
            partData["ThicknessAxis"] = "X"

        else:

            # Custom pieces use the standard local XYZ axes.
            # Structural parts are not forcibly remapped here.
            if role == "Custom":
                partData["LengthAxis"] = "X"
                partData["WidthAxis"] = "Y"
                partData["ThicknessAxis"] = "Z"

        # -----------------------------------------------------
        # Placement
        # -----------------------------------------------------
        # BosqoPart is a FeaturePython and does not expose a
        # Placement property. Placement must therefore travel
        # through Proxy.setData(), exactly as it does in
        # ModuleBuilder.
        #
        # Structural parts deliberately keep their calculated
        # module placement. The table only supplies placement
        # for shelves, dividers and custom/manual pieces.
        # -----------------------------------------------------

        if role in (
            "Shelf",
            "Divider",
            "Custom"
        ):

            if role == "Shelf":

                if positionMode == "Automatic":
                    x = self.thicknessSpin.value()
                    y = 0
                    z = float(
                        partData.get(
                            "PositionZ",
                            partData.get("Position", 0)
                        )
                    )

                else:
                    x = float(
                        partData.get(
                            "PositionX",
                            self.thicknessSpin.value()
                        )
                    )
                    y = float(
                        partData.get(
                            "PositionY",
                            0
                        )
                    )
                    z = float(
                        partData.get(
                            "PositionZ",
                            partData.get("Position", 0)
                        )
                    )

            elif role == "Divider":

                if positionMode == "Automatic":
                    x = float(
                        partData.get(
                            "PositionX",
                            partData.get("Position", 0)
                        )
                    )
                    y = 0
                    z = self.thicknessSpin.value()

                else:
                    x = float(
                        partData.get(
                            "PositionX",
                            partData.get("Position", 0)
                        )
                    )
                    y = float(
                        partData.get(
                            "PositionY",
                            0
                        )
                    )
                    z = float(
                        partData.get(
                            "PositionZ",
                            self.thicknessSpin.value()
                        )
                    )

            else:

                x = float(
                    partData.get(
                        "PositionX",
                        0
                    )
                )
                y = float(
                    partData.get(
                        "PositionY",
                        0
                    )
                )
                z = float(
                    partData.get(
                        "PositionZ",
                        partData.get("Position", 0)
                    )
                )

            rx = float(
                partData.get(
                    "RotationX",
                    0
                )
            )
            ry = float(
                partData.get(
                    "RotationY",
                    0
                )
            )
            rz = float(
                partData.get(
                    "RotationZ",
                    0
                )
            )

            rotation = (
                FreeCAD.Rotation(
                    FreeCAD.Vector(1, 0, 0),
                    rx
                )
                *
                FreeCAD.Rotation(
                    FreeCAD.Vector(0, 1, 0),
                    ry
                )
                *
                FreeCAD.Rotation(
                    FreeCAD.Vector(0, 0, 1),
                    rz
                )
            )

            partData["Placement"] = FreeCAD.Placement(
                FreeCAD.Vector(
                    x,
                    y,
                    z
                ),
                rotation
            )

        # -----------------------------------------------------
        # IMPORTANT: one single update path.
        # -----------------------------------------------------

        proxy = getattr(
            part,
            "Proxy",
            None
        )

        setData = getattr(
            proxy,
            "setData",
            None
        ) if proxy is not None else None

        try:

            if callable(setData):

                setData(
                    part,
                    partData
                )

            else:

                # Fallback only for old/invalid BosqoPart objects.
                # Do not ever assign Placement directly.
                for key, value in partData.items():

                    if key == "Placement":
                        continue

                    if hasattr(
                        part,
                        key
                    ):
                        setattr(
                            part,
                            key,
                            value
                        )

            part.touch()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error aplicando datos a pieza "
                + str(code)
                + ": "
                + str(error)
                + "\n"
            )


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

                self.applyStructuralPart(
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

            # Actualizar las piezas que ya existen sin reconstruir el
            # módulo. Esto es importante para módulos importados.
            for row in range(self.table.rowCount()):

                role = self.getRole(
                    row
                )

                if role == "Structural":

                    #
                    # Already applied by
                    # applyStructuralPart().
                    #

                    continue


                data = self.getRowData(
                    row
                )

                if data is None:
                    continue

                part = data.get(
                    "Object"
                )

                if part is None:
                    continue

                self.applyPartData(
                    part,
                    data
                )

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
        elif code in (
            "TR1",
            "TR2",
            "TR3"
        ):
            self.setText(row, 2, self.number(
                self.widthSpin.value() - self.thicknessSpin.value() * 2
            ))
            self.setText(row, 3, self.number(
                min(100, self.depthSpin.value())
            ))
            self.setText(row, 4, self.number(
                self.thicknessSpin.value()
            ))

        elif code in (
            "BK1",
            "BK2",
            "BK3"
        ):
            self.setText(row, 2, self.number(
                min(100, self.heightSpin.value())
            ))
            self.setText(row, 3, self.number(
                self.widthSpin.value() - self.thicknessSpin.value() * 2
            ))
            self.setText(row, 4, self.number(
                self.backThicknessSpin.value()
            ))


    # APPLY STRUCTURAL RECALCULATION
    # =========================================================

    def applyStructuralPart(
        self,
        row
    ):

        item = self.table.item(
            row,
            0
        )

        if item is None:
            return


        part = item.data(
            QtCore.Qt.ItemDataRole.UserRole
        )

        code = item.data(
            QtCore.Qt.ItemDataRole.UserRole + 1
        )

        part = self.getLivePart(
            part,
            code
        )

        if part is None:
            return

        item.setData(
            QtCore.Qt.ItemDataRole.UserRole,
            part
        )


        if code not in (
            "LS",
            "RS",
            "BT",
            "TP",
            "BK",
            "TR1",
            "TR2",
            "TR3",
            "BK1",
            "BK2",
            "BK3"
        ):
            return


        #
        # Read current module values.
        #

        width = self.widthSpin.value()
        height = self.heightSpin.value()
        depth = self.depthSpin.value()
        thickness = self.thicknessSpin.value()
        backThickness = self.backThicknessSpin.value()
        backInset = self.backInsetSpin.value()


        #
        # Build the SAME data structure used by
        # ModuleCalculator.
        #
        # This is intentional: we do not invent a
        # second placement system for PartTableDialog.
        #

        data = {

            "Code":
                code,

            "PartType":
                "Estructural",

            "Source":
                "Module",

            "Quantity":
                1,

            "PositionMode":
                "Automatic",

            "PositionType":
                "Automatic",

            "Position":
                0,

            "Placement":
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        0,
                        0,
                        0
                    ),
                    FreeCAD.Rotation()
                )
        }


        #
        # =====================================================
        # LEFT / RIGHT SIDE
        # =====================================================

        if code in (
            "LS",
            "RS"
        ):

            data["Role"] = "Side"

            data["Length"] = height
            data["Width"] = depth
            data["Thickness"] = thickness

            data["LengthAxis"] = "Z"
            data["WidthAxis"] = "Y"
            data["ThicknessAxis"] = "X"

            if code == "LS":

                data["Label"] = (
                    "Lateral izquierdo"
                )

                x = 0

            else:

                data["Label"] = (
                    "Lateral derecho"
                )

                x = (
                    width
                    -
                    thickness
                )


            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        x,
                        0,
                        0
                    ),
                    FreeCAD.Rotation()
                )
            )


        #
        # =====================================================
        # BOTTOM
        # =====================================================

        elif code == "BT":

            data["Role"] = "Bottom"

            data["Label"] = "Base"

            data["Length"] = (
                width
                -
                thickness * 2
            )

            data["Width"] = depth

            data["Thickness"] = thickness

            data["LengthAxis"] = "X"
            data["WidthAxis"] = "Y"
            data["ThicknessAxis"] = "Z"

            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        thickness,
                        0,
                        0
                    ),
                    FreeCAD.Rotation()
                )
            )


        #
        # =====================================================
        # TOP
        # =====================================================

        elif code == "TP":

            data["Role"] = "Top"

            data["Label"] = "Tapa"

            data["Length"] = (
                width
                -
                thickness * 2
            )

            data["Width"] = depth

            data["Thickness"] = thickness

            data["LengthAxis"] = "X"
            data["WidthAxis"] = "Y"
            data["ThicknessAxis"] = "Z"

            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        thickness,
                        0,
                        height
                        -
                        thickness
                    ),
                    FreeCAD.Rotation()
                )
            )


        #
        # =====================================================
        elif code in (
            "TR1",
            "TR2",
            "TR3"
        ):

            data["Role"] = "Top"
            data["Label"] = "Travesaño superior " + code[-1]

            railCodes = []
            for tableRow in range(self.table.rowCount()):
                tableItem = self.table.item(tableRow, 0)
                if tableItem is None:
                    continue
                tableCode = str(tableItem.data(
                    QtCore.Qt.ItemDataRole.UserRole + 1
                ) or "")
                if tableCode in ("TR1", "TR2", "TR3"):
                    railCodes.append(tableCode)

            railCount = 3 if len(railCodes) >= 3 else 2
            railIndex = int(code[-1]) - 1
            railDepth = min(100.0, depth)
            availableDepth = depth - railDepth
            y = 0 if railCount <= 1 else availableDepth / (railCount - 1) * railIndex

            data["Length"] = width - thickness * 2
            data["Width"] = railDepth
            data["Thickness"] = thickness
            data["LengthAxis"] = "X"
            data["WidthAxis"] = "Y"
            data["ThicknessAxis"] = "Z"
            data["Placement"] = FreeCAD.Placement(
                FreeCAD.Vector(thickness, y, height - thickness),
                FreeCAD.Rotation()
            )

        elif code in (
            "BK1",
            "BK2",
            "BK3"
        ):

            data["Role"] = "Back"
            data["Label"] = "Travesaño trasero " + code[-1]

            railCodes = []
            for tableRow in range(self.table.rowCount()):
                tableItem = self.table.item(tableRow, 0)
                if tableItem is None:
                    continue
                tableCode = str(tableItem.data(
                    QtCore.Qt.ItemDataRole.UserRole + 1
                ) or "")
                if tableCode in ("BK1", "BK2", "BK3"):
                    railCodes.append(tableCode)

            railCount = 3 if len(railCodes) >= 3 else 2
            railIndex = int(code[-1]) - 1
            railHeight = min(100.0, height)
            availableHeight = height - railHeight
            z = 0 if railCount <= 1 else availableHeight / (railCount - 1) * railIndex

            data["Length"] = railHeight
            data["Width"] = width - thickness * 2
            data["Thickness"] = backThickness
            data["LengthAxis"] = "Z"
            data["WidthAxis"] = "X"
            data["ThicknessAxis"] = "Y"

            y = depth - backInset - backThickness

            data["Placement"] = FreeCAD.Placement(
                FreeCAD.Vector(thickness, y, z),
                FreeCAD.Rotation()
            )

        # BACK
        # =====================================================

        else:

            data["Role"] = "Back"

            data["Label"] = "Trasera"

            data["Length"] = height

            data["Width"] = width

            data["Thickness"] = backThickness

            data["LengthAxis"] = "Z"
            data["WidthAxis"] = "X"
            data["ThicknessAxis"] = "Y"

            y = (
                depth
                -
                backInset
                -
                backThickness
            )

            data["Placement"] = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        0,
                        y,
                        0
                    ),
                    FreeCAD.Rotation()
                )
            )


        #
        # =====================================================
        # UPDATE TABLE
        # =====================================================

        self.setText(
            row,
            2,
            self.number(
                data["Length"]
            )
        )

        self.setText(
            row,
            3,
            self.number(
                data["Width"]
            )
        )

        self.setText(
            row,
            4,
            self.number(
                data["Thickness"]
            )
        )


        #
        # =====================================================
        # APPLY TO BOSQOPART
        # =====================================================

        try:

            proxy = getattr(
                part,
                "Proxy",
                None
            )


            #
            # IMPORTANT:
            #
            # Use BosqoPart.setData(), exactly as
            # ModuleBuilder does.
            #
            # This updates LengthAxis, WidthAxis,
            # ThicknessAxis AND Placement through
            # the normal BosqoPart data path.
            #

            if proxy is not None:

                setData = getattr(
                    proxy,
                    "setData",
                    None
                )

                if callable(setData):

                    setData(
                        part,
                        data
                    )

                else:

                    for key, value in data.items():

                        if hasattr(
                            part,
                            key
                        ):

                            setattr(
                                part,
                                key,
                                value
                            )


            #
            # Placement is intentionally NOT assigned directly.
            # BosqoPart is a FeaturePython and its placement is
            # handled by its Proxy.setData() implementation.
            #

            #
            # Mark geometry dirty.
            #

            part.touch()


        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error aplicando datos estructurales "
                + str(code)
                + ": "
                + str(error)
                + "\n"
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
        # =====================================================
        # AUTOMATIC SHELVES
        # =====================================================
        #
        # This follows ModuleCalculator exactly:
        #
        # usable height
        # - thickness of all shelves
        # = free height
        #
        # The shelf is placed in the centre of the
        # available spaces, not on the base.
        #

        if shelves:

            panelThickness = (
                self.thicknessSpin.value()
            )

            moduleHeight = (
                self.heightSpin.value()
            )

            usableHeight = (
                moduleHeight
                -
                panelThickness * 2
            )

            totalShelfThickness = (
                panelThickness
                *
                len(shelves)
            )

            freeHeight = (
                usableHeight
                -
                totalShelfThickness
            )

            spacing = (
                freeHeight
                /
                (
                    len(shelves)
                    +
                    1
                )
            )


            for index, row in enumerate(
                shelves
            ):

                z = (
                    panelThickness
                    +
                    spacing
                    *
                    (
                        index
                        +
                        1
                    )
                    +
                    panelThickness
                    *
                    index
                )


                #
                # Table position.
                #

                self.setText(
                    row,
                    7,
                    self.number(
                        z
                    )
                )


                #
                # Store complete placement data.
                #

                self.setPlacementData(
                    row,
                    positionX=panelThickness,
                    positionY=0,
                    positionZ=z,
                    rotationX=0,
                    rotationY=0,
                    rotationZ=0
                )


                # Placement is stored in the row data.



        #
        # =====================================================
        # AUTOMATIC DIVIDERS
        # =====================================================

        if dividers:

            panelThickness = (
                self.thicknessSpin.value()
            )

            moduleWidth = (
                self.widthSpin.value()
            )

            usableWidth = (
                moduleWidth
                -
                panelThickness * 2
            )

            totalDividerThickness = (
                panelThickness
                *
                len(dividers)
            )

            freeWidth = (
                usableWidth
                -
                totalDividerThickness
            )

            spacing = (
                freeWidth
                /
                (
                    len(dividers)
                    +
                    1
                )
            )


            for index, row in enumerate(
                dividers
            ):

                x = (
                    panelThickness
                    +
                    spacing
                    *
                    (
                        index
                        +
                        1
                    )
                    +
                    panelThickness
                    *
                    index
                )


                self.setText(
                    row,
                    7,
                    self.number(
                        x
                    )
                )


                self.setPlacementData(
                    row,
                    positionX=x,
                    positionY=0,
                    positionZ=panelThickness,
                    rotationX=0,
                    rotationY=0,
                    rotationZ=0
                )


                # Placement is stored in the row data.



        if refresh:

            self.table.viewport().update()

    # =========================================================
    # PLACEMENT DATA
    # =========================================================

    def setPlacementData(
        self,
        row,
        positionX=None,
        positionY=None,
        positionZ=None,
        rotationX=None,
        rotationY=None,
        rotationZ=None
    ):

        item = self.table.item(row, 0)

        if item is None:
            return

        data = (
            item.data(
                QtCore.Qt.ItemDataRole.UserRole + 2
            )
            or
            {}
        )

        data = dict(data)

        if positionX is not None:
            data["PositionX"] = positionX

        if positionY is not None:
            data["PositionY"] = positionY

        if positionZ is not None:
            data["PositionZ"] = positionZ

        if rotationX is not None:
            data["RotationX"] = rotationX

        if rotationY is not None:
            data["RotationY"] = rotationY

        if rotationZ is not None:
            data["RotationZ"] = rotationZ

        item.setData(
            QtCore.Qt.ItemDataRole.UserRole + 2,
            data
        )


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