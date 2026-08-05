from PySide import QtWidgets


class ManualPlacementDialog(QtWidgets.QDialog):

    def __init__(
        self,
        part,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.part = part

        self.setWindowTitle(
            "Posición y giro"
        )

        self.resize(
            420,
            300
        )

        layout = QtWidgets.QVBoxLayout(
            self
        )

        #
        # =====================================================
        # POSITION
        # =====================================================
        #

        positionGroup = QtWidgets.QGroupBox(
            "Posición"
        )

        positionLayout = QtWidgets.QGridLayout()

        positionLayout.addWidget(
            QtWidgets.QLabel(
                "X:"
            ),
            0,
            0
        )

        self.xSpin = self.createSpinBox()

        positionLayout.addWidget(
            self.xSpin,
            0,
            1
        )

        positionLayout.addWidget(
            QtWidgets.QLabel(
                "Y:"
            ),
            1,
            0
        )

        self.ySpin = self.createSpinBox()

        positionLayout.addWidget(
            self.ySpin,
            1,
            1
        )

        positionLayout.addWidget(
            QtWidgets.QLabel(
                "Z:"
            ),
            2,
            0
        )

        self.zSpin = self.createSpinBox()

        positionLayout.addWidget(
            self.zSpin,
            2,
            1
        )

        positionGroup.setLayout(
            positionLayout
        )

        layout.addWidget(
            positionGroup
        )

        #
        # =====================================================
        # ROTATION
        # =====================================================
        #

        rotationGroup = QtWidgets.QGroupBox(
            "Giro"
        )

        rotationLayout = QtWidgets.QGridLayout()

        rotationLayout.addWidget(
            QtWidgets.QLabel(
                "Giro X:"
            ),
            0,
            0
        )

        self.rxSpin = self.createAngleSpinBox()

        rotationLayout.addWidget(
            self.rxSpin,
            0,
            1
        )

        rotationLayout.addWidget(
            QtWidgets.QLabel(
                "Giro Y:"
            ),
            1,
            0
        )

        self.rySpin = self.createAngleSpinBox()

        rotationLayout.addWidget(
            self.rySpin,
            1,
            1
        )

        rotationLayout.addWidget(
            QtWidgets.QLabel(
                "Giro Z:"
            ),
            2,
            0
        )

        self.rzSpin = self.createAngleSpinBox()

        rotationLayout.addWidget(
            self.rzSpin,
            2,
            1
        )

        rotationGroup.setLayout(
            rotationLayout
        )

        layout.addWidget(
            rotationGroup
        )

        #
        # =====================================================
        # BUTTONS
        # =====================================================
        #

        buttons = QtWidgets.QHBoxLayout()

        buttons.addStretch()

        cancelButton = QtWidgets.QPushButton(
            "Cancelar"
        )

        okButton = QtWidgets.QPushButton(
            "Aceptar"
        )

        buttons.addWidget(
            cancelButton
        )

        buttons.addWidget(
            okButton
        )

        layout.addLayout(
            buttons
        )

        cancelButton.clicked.connect(
            self.reject
        )

        okButton.clicked.connect(
            self.accept
        )

        #
        # =====================================================
        # LOAD EXISTING VALUES
        # =====================================================
        #

        self.loadData()

    #
    # =========================================================
    # SPINBOX
    # =========================================================
    #

    def createSpinBox(
        self
    ):

        spin = QtWidgets.QDoubleSpinBox()

        spin.setRange(
            -10000,
            10000
        )

        spin.setDecimals(
            2
        )

        spin.setSuffix(
            " mm"
        )

        return spin

    def createAngleSpinBox(
        self
    ):

        spin = QtWidgets.QDoubleSpinBox()

        spin.setRange(
            -360,
            360
        )

        spin.setDecimals(
            2
        )

        spin.setSuffix(
            " °"
        )

        return spin

    #
    # =========================================================
    # LOAD
    # =========================================================
    #

    def loadData(
        self
    ):

        self.xSpin.setValue(
            self.toFloat(
                self.part.get(
                    "PositionX",
                    0
                )
            )
        )

        self.ySpin.setValue(
            self.toFloat(
                self.part.get(
                    "PositionY",
                    0
                )
            )
        )

        self.zSpin.setValue(
            self.toFloat(
                self.part.get(
                    "PositionZ",
                    0
                )
            )
        )

        self.rxSpin.setValue(
            self.toFloat(
                self.part.get(
                    "RotationX",
                    0
                )
            )
        )

        self.rySpin.setValue(
            self.toFloat(
                self.part.get(
                    "RotationY",
                    0
                )
            )
        )

        self.rzSpin.setValue(
            self.toFloat(
                self.part.get(
                    "RotationZ",
                    0
                )
            )
        )

    #
    # =========================================================
    # DATA
    # =========================================================
    #

    def getData(
        self
    ):

        return {

            "PositionX":
                self.xSpin.value(),

            "PositionY":
                self.ySpin.value(),

            "PositionZ":
                self.zSpin.value(),

            "RotationX":
                self.rxSpin.value(),

            "RotationY":
                self.rySpin.value(),

            "RotationZ":
                self.rzSpin.value()

        }

    #
    # =========================================================
    # FLOAT
    # =========================================================
    #

    def toFloat(
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

            return 0.0


class ParametricModuleDialog(QtWidgets.QDialog):

    def __init__(
        self,
        parameters=None,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.parameters = parameters

        self.setWindowTitle(
            "Módulo paramétrico"
        )

        self.resize(
            1250,
            750
        )

        #
        # User-created pieces.
        #

        self.userParts = []

        #
        # Complete calculated list.
        #

        self.parts = []

        self.createUI()

        self.loadParameters()

        self.calculateParts()

    #
    # =========================================================
    # UI
    # =========================================================
    #

    def createUI(
        self
    ):

        mainLayout = QtWidgets.QVBoxLayout(
            self
        )

        #
        # =====================================================
        # MODULE PARAMETERS
        # =====================================================
        #

        moduleGroup = QtWidgets.QGroupBox(
            "Datos del módulo"
        )

        moduleLayout = QtWidgets.QGridLayout()

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
        # =====================================================
        # PARTS
        # =====================================================
        #

        partsGroup = QtWidgets.QGroupBox(
            "Tabla de piezas"
        )

        partsLayout = QtWidgets.QVBoxLayout()

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
            QtWidgets.QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )

        self.table.setAlternatingRowColors(
            True
        )

        partsLayout.addWidget(
            self.table
        )

        #
        # =====================================================
        # BUTTONS
        # =====================================================
        #

        buttonsLayout = QtWidgets.QHBoxLayout()

        self.addPartButton = QtWidgets.QPushButton(
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

        buttonsLayout.addWidget(
            self.addPartButton
        )

        buttonsLayout.addWidget(
            self.deleteButton
        )

        buttonsLayout.addWidget(
            self.duplicateButton
        )

        buttonsLayout.addWidget(
            self.placementButton
        )

        buttonsLayout.addStretch()

        partsLayout.addLayout(
            buttonsLayout
        )

        partsGroup.setLayout(
            partsLayout
        )

        mainLayout.addWidget(
            partsGroup
        )

        #
        # =====================================================
        # BOTTOM
        # =====================================================
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
            "Guardar"
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
        # =====================================================
        # SIGNALS
        # =====================================================
        #

        self.addPartButton.clicked.connect(
            self.addCustomPart
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
            self.calculateParts
        )

        self.saveButton.clicked.connect(
            self.save
        )

        self.cancelButton.clicked.connect(
            self.reject
        )

    #
    # =========================================================
    # SPINBOX
    # =========================================================
    #

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

    #
    # =========================================================
    # LOAD PARAMETERS
    # =========================================================
    #

    def loadParameters(
        self
    ):

        obj = self.parameters

        if obj is None:

            self.nameEdit.setText(
                "Nuevo módulo"
            )

            self.widthSpin.setValue(
                600
            )

            self.heightSpin.setValue(
                720
            )

            self.depthSpin.setValue(
                560
            )

            self.thicknessSpin.setValue(
                19
            )

            self.backThicknessSpin.setValue(
                3
            )

            self.backInsetSpin.setValue(
                0
            )

            return

        #
        # NAME
        #

        if hasattr(
            obj,
            "ModuleName"
        ):

            self.nameEdit.setText(
                str(
                    obj.ModuleName
                )
            )

        elif hasattr(
            obj,
            "Label"
        ):

            self.nameEdit.setText(
                str(
                    obj.Label
                )
            )

        else:

            self.nameEdit.setText(
                "Nuevo módulo"
            )

        #
        # DIMENSIONS
        #

        self.widthSpin.setValue(
            self.getValue(
                getattr(
                    obj,
                    "ModuleWidth",
                    600
                )
            )
        )

        self.heightSpin.setValue(
            self.getValue(
                getattr(
                    obj,
                    "ModuleHeight",
                    720
                )
            )
        )

        self.depthSpin.setValue(
            self.getValue(
                getattr(
                    obj,
                    "ModuleDepth",
                    560
                )
            )
        )

        self.thicknessSpin.setValue(
            self.getValue(
                getattr(
                    obj,
                    "PanelThickness",
                    19
                )
            )
        )

        self.backThicknessSpin.setValue(
            self.getValue(
                getattr(
                    obj,
                    "BackThickness",
                    3
                )
            )
        )

        self.backInsetSpin.setValue(
            self.getValue(
                getattr(
                    obj,
                    "BackInset",
                    0
                )
            )
        )

    #
    # =========================================================
    # UPDATE PARAMETERS
    # =========================================================
    #

    def updateParameters(
        self
    ):

        obj = self.parameters

        if obj is None:

            return

        name = (
            self.nameEdit.text().strip()
            or
            "Nuevo módulo"
        )

        if hasattr(
            obj,
            "ModuleName"
        ):

            obj.ModuleName = name

        if hasattr(
            obj,
            "ModuleWidth"
        ):

            obj.ModuleWidth = (
                self.widthSpin.value()
            )

        if hasattr(
            obj,
            "ModuleHeight"
        ):

            obj.ModuleHeight = (
                self.heightSpin.value()
            )

        if hasattr(
            obj,
            "ModuleDepth"
        ):

            obj.ModuleDepth = (
                self.depthSpin.value()
            )

        if hasattr(
            obj,
            "PanelThickness"
        ):

            obj.PanelThickness = (
                self.thicknessSpin.value()
            )

        if hasattr(
            obj,
            "BackThickness"
        ):

            obj.BackThickness = (
                self.backThicknessSpin.value()
            )

        if hasattr(
            obj,
            "BackInset"
        ):

            obj.BackInset = (
                self.backInsetSpin.value()
            )

    #
    # =========================================================
    # CALCULATE PARTS
    # =========================================================
    #

    def calculateParts(
        self
    ):

        #
        # First save any changes made directly in the table.
        #

        if hasattr(
            self,
            "table"
        ):

            self.updateTableData()

        #
        # Save module parameters.
        #

        self.updateParameters()

        width = (
            self.widthSpin.value()
        )

        height = (
            self.heightSpin.value()
        )

        depth = (
            self.depthSpin.value()
        )

        thickness = (
            self.thicknessSpin.value()
        )

        backThickness = (
            self.backThicknessSpin.value()
        )

        calculated = []

        #
        # =====================================================
        # LEFT
        # =====================================================
        #

        calculated.append(
            self.createStructuralPart(
                "LS",
                "Lateral izquierdo",
                "Side",
                height,
                depth,
                thickness,
                0
            )
        )

        #
        # =====================================================
        # RIGHT
        # =====================================================
        #

        calculated.append(
            self.createStructuralPart(
                "RS",
                "Lateral derecho",
                "Side",
                height,
                depth,
                thickness,
                width - thickness
            )
        )

        #
        # =====================================================
        # BOTTOM
        # =====================================================
        #

        calculated.append(
            self.createStructuralPart(
                "BT",
                "Base",
                "Bottom",
                width - thickness * 2,
                depth,
                thickness,
                0
            )
        )

        #
        # =====================================================
        # TOP
        # =====================================================
        #

        calculated.append(
            self.createStructuralPart(
                "TP",
                "Tapa",
                "Top",
                width - thickness * 2,
                depth,
                thickness,
                height - thickness
            )
        )

        #
        # =====================================================
        # BACK
        # =====================================================
        #

        calculated.append(
            self.createStructuralPart(
                "BK",
                "Trasera",
                "Back",
                height,
                width,
                backThickness,
                0
            )
        )

        #
        # =====================================================
        # USER PARTS
        # =====================================================
        #

        for part in self.userParts:

            calculatedPart = dict(
                part
            )

            #
            # =================================================
            # AUTOMATIC SHELF
            # =================================================
            #
            # The shelf dimensions follow the module.
            #

            if (
                part.get(
                    "Role"
                ) == "Shelf"
                and
                part.get(
                    "PositionMode",
                    "Automatic"
                ) == "Automatic"
            ):

                calculatedPart["Length"] = (
                    width
                    -
                    thickness * 2
                )

                calculatedPart["Width"] = (
                    depth
                )

                calculatedPart["Thickness"] = (
                    thickness
                )

            #
            # =================================================
            # AUTOMATIC DIVIDER
            # =================================================
            #

            elif (
                part.get(
                    "Role"
                ) == "Divider"
                and
                part.get(
                    "PositionMode",
                    "Automatic"
                ) == "Automatic"
            ):

                calculatedPart["Length"] = (
                    height
                    -
                    thickness * 2
                )

                calculatedPart["Width"] = (
                    depth
                )

                calculatedPart["Thickness"] = (
                    thickness
                )

            calculated.append(
                calculatedPart
            )

        #
        # =====================================================
        # AUTOMATIC POSITIONS
        # =====================================================
        #

        self.calculateAutomaticPositions(
            calculated
        )

        #
        # =====================================================
        # SYNCHRONIZE USER PARTS
        # =====================================================
        #
        # This is the important part.
        #
        # The calculated dimensions of automatic pieces are
        # copied back into userParts so loadTable() displays
        # the new dimensions.
        #

        for calculatedPart in calculated:

            code = calculatedPart.get(
                "Code",
                ""
            )

            if not code:

                continue

            for userPart in self.userParts:

                if userPart.get(
                    "Code",
                    ""
                ) != code:

                    continue

                role = userPart.get(
                    "Role",
                    ""
                )

                positionMode = userPart.get(
                    "PositionMode",
                    "Automatic"
                )

                #
                # AUTOMATIC SHELF
                #

                if (
                    role == "Shelf"
                    and
                    positionMode == "Automatic"
                ):

                    userPart["Length"] = (
                        calculatedPart.get(
                            "Length",
                            userPart.get(
                                "Length",
                                0
                            )
                        )
                    )

                    userPart["Width"] = (
                        calculatedPart.get(
                            "Width",
                            userPart.get(
                                "Width",
                                0
                            )
                        )
                    )

                    userPart["Thickness"] = (
                        calculatedPart.get(
                            "Thickness",
                            userPart.get(
                                "Thickness",
                                0
                            )
                        )
                    )

                #
                # AUTOMATIC DIVIDER
                #

                elif (
                    role == "Divider"
                    and
                    positionMode == "Automatic"
                ):

                    userPart["Length"] = (
                        calculatedPart.get(
                            "Length",
                            userPart.get(
                                "Length",
                                0
                            )
                        )
                    )

                    userPart["Width"] = (
                        calculatedPart.get(
                            "Width",
                            userPart.get(
                                "Width",
                                0
                            )
                        )
                    )

                    userPart["Thickness"] = (
                        calculatedPart.get(
                            "Thickness",
                            userPart.get(
                                "Thickness",
                                0
                            )
                        )
                    )

                break

        #
        # =====================================================
        # STORE CALCULATED PARTS
        # =====================================================
        #

        self.parts = calculated

        #
        # =====================================================
        # REFRESH TABLE
        # =====================================================
        #

        self.loadTable()

    #
    # =========================================================
    # STRUCTURAL PART
    # =========================================================
    #

    def createStructuralPart(
        self,
        code,
        label,
        role,
        length,
        width,
        thickness,
        position
    ):

        return {

            "Code":
                code,

            "Label":
                label,

            "Role":
                role,

            "PartType":
                "Estructural",

            "Length":
                length,

            "Width":
                width,

            "Thickness":
                thickness,

            "Quantity":
                1,

            "MaterialCode":
                "",

            "Position":
                position,

            "PositionType":
                "Automatic",

            "PositionMode":
                "Automatic"
        }

    #
    # =========================================================
    # ADD CUSTOM PART
    # =========================================================
    #

    def addCustomPart(
        self
    ):

        self.updateTableData()

        number = 1

        while True:

            code = (
                "CU"
                +
                str(
                    number
                )
            )

            exists = False

            for part in self.userParts:

                if part.get(
                    "Code"
                ) == code:

                    exists = True

                    break

            if not exists:

                break

            number += 1

        #
        # =====================================================
        # DEFAULT DIMENSIONS
        # =====================================================
        #

        internalWidth = (
            self.widthSpin.value()
            -
            self.thicknessSpin.value() * 2
        )

        internalDepth = (
            self.depthSpin.value()
        )

        panelThickness = (
            self.thicknessSpin.value()
        )

        part = {

            "Code":
                code,

            "Label":
                "Nueva pieza "
                +
                str(
                    number
                ),

            "Role":
                "Custom",

            "PartType":
                "Personalizado",

            "Length":
                internalWidth,

            "Width":
                internalDepth,

            "Thickness":
                panelThickness,

            "Quantity":
                1,

            "MaterialCode":
                "",

            #
            # POSITION
            #

            "Position":
                0,

            "PositionX":
                0,

            "PositionY":
                0,

            "PositionZ":
                0,

            #
            # ROTATION
            #

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

        self.userParts.append(
            part
        )

        self.calculateParts()

        self.table.selectRow(
            self.table.rowCount() - 1
        )

    #
    # =========================================================
    # EDIT PLACEMENT
    # =========================================================
    #

    def editPlacement(
        self
    ):

        self.updateTableData()

        row = self.table.currentRow()

        if row < 5:

            QtWidgets.QMessageBox.information(
                self,
                "Posición / giro",
                "Las piezas estructurales "
                "se posicionan automáticamente."
            )

            return

        userIndex = row - 5

        if (
            userIndex < 0
            or
            userIndex >= len(
                self.userParts
            )
        ):

            return

        part = self.userParts[
            userIndex
        ]

        dialog = ManualPlacementDialog(
            part,
            self
        )

        if dialog.exec_():

            data = dialog.getData()

            part.update(
                data
            )

            part["PositionMode"] = (
                "Manual"
            )

            part["PositionType"] = (
                "Manual"
            )

            self.calculateParts()

    #
    # =========================================================
    # DELETE
    # =========================================================
    #

    def deletePart(
        self
    ):

        self.updateTableData()

        row = self.table.currentRow()

        if row < 0:

            return

        if row < 5:

            QtWidgets.QMessageBox.information(
                self,
                "Eliminar pieza",
                "Las piezas estructurales del módulo "
                "no se pueden eliminar."
            )

            return

        userIndex = row - 5

        if (
            userIndex >= 0
            and
            userIndex < len(
                self.userParts
            )
        ):

            del self.userParts[
                userIndex
            ]

        self.calculateParts()

    #
    # =========================================================
    # DUPLICATE
    # =========================================================
    #

    def duplicatePart(
        self
    ):

        self.updateTableData()

        row = self.table.currentRow()

        if row < 5:

            QtWidgets.QMessageBox.information(
                self,
                "Duplicar pieza",
                "Selecciona una pieza creada "
                "por el usuario."
            )

            return

        userIndex = row - 5

        if (
            userIndex < 0
            or
            userIndex >= len(
                self.userParts
            )
        ):

            return

        source = self.userParts[
            userIndex
        ]

        copy = dict(
            source
        )

        number = 1

        while True:

            code = (
                "CU"
                +
                str(
                    number
                )
            )

            exists = False

            for part in self.userParts:

                if part.get(
                    "Code"
                ) == code:

                    exists = True

                    break

            if not exists:

                break

            number += 1

        copy["Code"] = code

        copy["Label"] = (
            "Nueva pieza "
            +
            str(
                number
            )
        )

        self.userParts.append(
            copy
        )

        self.calculateParts()

    #
    # =========================================================
    # AUTOMATIC POSITIONS
    # =========================================================
    #

    def calculateAutomaticPositions(
        self,
        parts
    ):

        #
        # =====================================================
        # SHELVES
        # =====================================================
        #

        shelves = [

            part

            for part in parts

            if part.get(
                "Role"
            ) == "Shelf"

            and
            part.get(
                "PositionMode",
                "Automatic"
            ) == "Automatic"

        ]

        if shelves:

            usableHeight = (
                self.heightSpin.value()
                -
                self.thicknessSpin.value() * 2
            )

            count = len(
                shelves
            )

            #
            # Take shelf thickness into account.
            #

            totalThickness = sum(
                float(
                    part.get(
                        "Thickness",
                        self.thicknessSpin.value()
                    )
                )
                for part in shelves
            )

            freeHeight = (
                usableHeight
                -
                totalThickness
            )

            spacing = (
                freeHeight
                /
                (
                    count + 1
                )
            )

            currentZ = (
                self.thicknessSpin.value()
                +
                spacing
            )

            for part in shelves:

                thickness = float(
                    part.get(
                        "Thickness",
                        self.thicknessSpin.value()
                    )
                )

                part["Position"] = (
                    currentZ
                )

                part["PositionZ"] = (
                    currentZ
                )

                part["PositionType"] = (
                    "Automatic"
                )

                currentZ += (
                    thickness
                    +
                    spacing
                )

        #
        # =====================================================
        # DIVIDERS
        # =====================================================
        #

        dividers = [

            part

            for part in parts

            if part.get(
                "Role"
            ) == "Divider"

            and
            part.get(
                "PositionMode",
                "Automatic"
            ) == "Automatic"

        ]

        if dividers:

            usableWidth = (
                self.widthSpin.value()
                -
                self.thicknessSpin.value() * 2
            )

            count = len(
                dividers
            )

            totalThickness = sum(
                float(
                    part.get(
                        "Thickness",
                        self.thicknessSpin.value()
                    )
                )
                for part in dividers
            )

            freeWidth = (
                usableWidth
                -
                totalThickness
            )

            spacing = (
                freeWidth
                /
                (
                    count + 1
                )
            )

            currentX = (
                self.thicknessSpin.value()
                +
                spacing
            )

            for part in dividers:

                thickness = float(
                    part.get(
                        "Thickness",
                        self.thicknessSpin.value()
                    )
                )

                part["Position"] = (
                    currentX
                )

                part["PositionX"] = (
                    currentX
                )

                part["PositionType"] = (
                    "Automatic"
                )

                currentX += (
                    thickness
                    +
                    spacing
                )

    #
    # =========================================================
    # LOAD TABLE
    # =========================================================
    #

    def loadTable(
        self
    ):

        self.table.blockSignals(
            True
        )

        self.table.setRowCount(
            0
        )

        for row, part in enumerate(
            self.parts
        ):

            self.table.insertRow(
                row
            )

            #
            # NAME
            #

            self.setItem(
                row,
                0,
                part.get(
                    "Label",
                    ""
                )
            )

            #
            # =================================================
            # TYPE
            # =================================================
            #

            typeCombo = QtWidgets.QComboBox()

            typeCombo.addItem(
                "Estructural",
                "Structural"
            )

            typeCombo.addItem(
                "Balda",
                "Shelf"
            )

            typeCombo.addItem(
                "Separador",
                "Divider"
            )

            typeCombo.addItem(
                "Personalizado",
                "Custom"
            )

            role = part.get(
                "Role",
                "Structural"
            )

            index = typeCombo.findData(
                role
            )

            if index < 0:

                index = 0

            typeCombo.setCurrentIndex(
                index
            )

            if row < 5:

                typeCombo.setEnabled(
                    False
                )

            self.table.setCellWidget(
                row,
                1,
                typeCombo
            )

            #
            # =================================================
            # DIMENSIONS
            # =================================================
            #

            self.setItem(
                row,
                2,
                self.number(
                    part.get(
                        "Length",
                        0
                    )
                )
            )

            self.setItem(
                row,
                3,
                self.number(
                    part.get(
                        "Width",
                        0
                    )
                )
            )

            self.setItem(
                row,
                4,
                self.number(
                    part.get(
                        "Thickness",
                        0
                    )
                )
            )

            self.setItem(
                row,
                5,
                self.number(
                    part.get(
                        "Quantity",
                        1
                    )
                )
            )

            #
            # =================================================
            # MATERIAL
            # =================================================
            #

            materialCombo = QtWidgets.QComboBox()

            materialCombo.addItem(
                "— Sin material —",
                ""
            )

            materialCode = part.get(
                "MaterialCode",
                ""
            )

            index = materialCombo.findData(
                materialCode
            )

            if index >= 0:

                materialCombo.setCurrentIndex(
                    index
                )

            self.table.setCellWidget(
                row,
                6,
                materialCombo
            )

            #
            # =================================================
            # POSITION TYPE
            # =================================================
            #

            positionCombo = QtWidgets.QComboBox()

            positionCombo.addItem(
                "Automática",
                "Automatic"
            )

            positionCombo.addItem(
                "Inferior",
                "Bottom"
            )

            positionCombo.addItem(
                "Centro",
                "Center"
            )

            positionCombo.addItem(
                "Superior",
                "Top"
            )

            positionCombo.addItem(
                "Manual",
                "Manual"
            )

            positionType = part.get(
                "PositionType",
                "Automatic"
            )

            index = positionCombo.findData(
                positionType
            )

            if index < 0:

                index = 0

            positionCombo.setCurrentIndex(
                index
            )

            self.table.setCellWidget(
                row,
                7,
                positionCombo
            )

            #
            # =================================================
            # MODE
            # =================================================
            #

            modeCombo = QtWidgets.QComboBox()

            modeCombo.addItem(
                "Automática",
                "Automatic"
            )

            modeCombo.addItem(
                "Manual",
                "Manual"
            )

            mode = part.get(
                "PositionMode",
                "Automatic"
            )

            index = modeCombo.findData(
                mode
            )

            if index < 0:

                index = 0

            modeCombo.setCurrentIndex(
                index
            )

            self.table.setCellWidget(
                row,
                8,
                modeCombo
            )

        self.table.blockSignals(
            False
        )

        #
        # =====================================================
        # COLUMN WIDTHS
        # =====================================================
        #

        self.table.setColumnWidth(
            0,
            180
        )

        self.table.setColumnWidth(
            1,
            120
        )

        self.table.setColumnWidth(
            6,
            180
        )

        self.table.setColumnWidth(
            7,
            110
        )

        self.table.setColumnWidth(
            8,
            110
        )

    #
    # =========================================================
    # UPDATE TABLE DATA
    # =========================================================
    #

    def updateTableData(
        self
    ):

        if not hasattr(
            self,
            "table"
        ):

            return

        for row in range(
            5,
            self.table.rowCount()
        ):

            userIndex = row - 5

            if (
                userIndex < 0
                or
                userIndex >= len(
                    self.userParts
                )
            ):

                continue

            part = self.userParts[
                userIndex
            ]

            #
            # =================================================
            # LABEL
            # =================================================
            #

            item = self.table.item(
                row,
                0
            )

            if item is not None:

                part["Label"] = (
                    item.text()
                )

            #
            # =================================================
            # TYPE / ROLE
            # =================================================
            #

            typeCombo = (
                self.table.cellWidget(
                    row,
                    1
                )
            )

            if typeCombo is not None:

                role = (
                    typeCombo.currentData()
                )

                part["Role"] = role

                if role == "Shelf":

                    part["PartType"] = (
                        "Balda"
                    )

                elif role == "Divider":

                    part["PartType"] = (
                        "Separador"
                    )

                elif role == "Custom":

                    part["PartType"] = (
                        "Personalizado"
                    )

            #
            # =================================================
            # DIMENSIONS
            # =================================================
            #

            part["Length"] = (
                self.getFloat(
                    row,
                    2
                )
            )

            part["Width"] = (
                self.getFloat(
                    row,
                    3
                )
            )

            part["Thickness"] = (
                self.getFloat(
                    row,
                    4
                )
            )

            part["Quantity"] = (
                self.getFloat(
                    row,
                    5
                )
            )

            #
            # =================================================
            # MATERIAL
            # =================================================
            #

            materialCombo = (
                self.table.cellWidget(
                    row,
                    6
                )
            )

            if materialCombo is not None:

                part["MaterialCode"] = (
                    materialCombo.currentData()
                )

            #
            # =================================================
            # POSITION TYPE
            # =================================================
            #

            positionCombo = (
                self.table.cellWidget(
                    row,
                    7
                )
            )

            if positionCombo is not None:

                part["PositionType"] = (
                    positionCombo.currentData()
                )

            #
            # =================================================
            # MODE
            # =================================================
            #

            modeCombo = (
                self.table.cellWidget(
                    row,
                    8
                )
            )

            if modeCombo is not None:

                part["PositionMode"] = (
                    modeCombo.currentData()
                )

    #
    # =========================================================
    # GET DATA
    # =========================================================
    #

    def getData(
        self
    ):

        self.updateTableData()

        self.calculateParts()

        return {

            "Label":
                self.nameEdit.text().strip()
                or
                "Nuevo módulo",

            "Width":
                self.widthSpin.value(),

            "Height":
                self.heightSpin.value(),

            "Depth":
                self.depthSpin.value(),

            "PanelThickness":
                self.thicknessSpin.value(),

            "BackThickness":
                self.backThicknessSpin.value(),

            "BackInset":
                self.backInsetSpin.value(),

            "Parts":
                [
                    dict(
                        part
                    )
                    for part in self.userParts
                ]
        }

    #
    # =========================================================
    # SAVE
    # =========================================================
    #

    def save(
        self
    ):

        self.updateTableData()

        self.updateParameters()

        self.calculateParts()

        self.accept()

    #
    # =========================================================
    # SET ITEM
    # =========================================================
    #

    def setItem(
        self,
        row,
        column,
        value
    ):

        item = QtWidgets.QTableWidgetItem(
            str(
                value
            )
        )

        self.table.setItem(
            row,
            column,
            item
        )

    #
    # =========================================================
    # GET FLOAT
    # =========================================================
    #

    def getFloat(
        self,
        row,
        column
    ):

        item = self.table.item(
            row,
            column
        )

        if item is None:

            return 0

        try:

            return float(
                item.text().replace(
                    ",",
                    "."
                )
            )

        except Exception:

            return 0

    #
    # =========================================================
    # NUMBER
    # =========================================================
    #

    def number(
        self,
        value
    ):

        try:

            value = float(
                value
            )

            if value.is_integer():

                return str(
                    int(
                        value
                    )
                )

            return str(
                round(
                    value,
                    2
                )
            )

        except Exception:

            return "0"

    #
    # =========================================================
    # GET VALUE
    # =========================================================
    #

    def getValue(
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