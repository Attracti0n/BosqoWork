from PySide import QtWidgets

from dialogs.manual_placement_dialog import ManualPlacementDialog

from core.calculators.module_calculator import ModuleCalculator


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

        self.module = module

        self.originalParts = (
            parts or []
        )

        #
        # User parts.
        #
        # Structural parts are NOT stored here.
        #

        self.userParts = []

        #
        # Complete visible list.
        #

        self.parts = []

        self.setWindowTitle(
            "Editar módulo"
        )

        self.resize(
            1250,
            750
        )

        self.createUI()

        self.loadModule()

        self.loadParts()

        self.calculateParts()


    # =========================================================
    # UI
    # =========================================================

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

        #
        # NAME
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
        # WIDTH
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
        # HEIGHT
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
        # DEPTH
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
        # PANEL THICKNESS
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
        # BACK THICKNESS
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
        # BACK INSET
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
        # =====================================================
        # PARTS TABLE
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
    # LOAD MODULE
    # =========================================================

    def loadModule(
        self
    ):

        module = self.module

        if module is None:

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
            module,
            "ModuleName"
        ):

            self.nameEdit.setText(
                str(
                    module.ModuleName
                )
            )

        elif hasattr(
            module,
            "Label"
        ):

            self.nameEdit.setText(
                str(
                    module.Label
                )
            )

        else:

            self.nameEdit.setText(
                "Módulo"
            )

        #
        # DIMENSIONS
        #

        self.widthSpin.setValue(
            self.getValue(
                getattr(
                    module,
                    "Width",
                    600
                )
            )
        )

        self.heightSpin.setValue(
            self.getValue(
                getattr(
                    module,
                    "Height",
                    720
                )
            )
        )

        self.depthSpin.setValue(
            self.getValue(
                getattr(
                    module,
                    "Depth",
                    560
                )
            )
        )

        self.thicknessSpin.setValue(
            self.getValue(
                getattr(
                    module,
                    "PanelThickness",
                    19
                )
            )
        )

        self.backThicknessSpin.setValue(
            self.getValue(
                getattr(
                    module,
                    "BackThickness",
                    3
                )
            )
        )

        self.backInsetSpin.setValue(
            self.getValue(
                getattr(
                    module,
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

        self.userParts = []

        #
        # Structural codes.
        #

        structuralCodes = {
            "LS",
            "RS",
            "BT",
            "TP",
            "BK"
        }

        for part in self.originalParts:

            #
            # Convert BosqoPart -> dictionary
            #

            if hasattr(
                part,
                "Code"
            ):

                code = str(
                    part.Code
                )

            else:

                if isinstance(
                    part,
                    dict
                ):

                    code = str(
                        part.get(
                            "Code",
                            ""
                        )
                    )

                else:

                    continue

            #
            # Structural pieces are generated
            # automatically and therefore are
            # not user parts.
            #

            if code in structuralCodes:

                continue

            #
            # Read data.
            #

            if isinstance(
                part,
                dict
            ):

                data = dict(
                    part
                )

            else:

                data = {

                    "Code":
                        code,

                    "Label":
                        getattr(
                            part,
                            "Label",
                            "Pieza"
                        ),

                    "Role":
                        getattr(
                            part,
                            "Role",
                            "Custom"
                        ),

                    "PartType":
                        getattr(
                            part,
                            "PartType",
                            "Personalizado"
                        ),

                    "Length":
                        self.getValue(
                            getattr(
                                part,
                                "Length",
                                100
                            )
                        ),

                    "Width":
                        self.getValue(
                            getattr(
                                part,
                                "Width",
                                100
                            )
                        ),

                    "Thickness":
                        self.getValue(
                            getattr(
                                part,
                                "Thickness",
                                19
                            )
                        ),

                    "Quantity":
                        self.getValue(
                            getattr(
                                part,
                                "Quantity",
                                1
                            )
                        ),

                    "MaterialCode":
                        getattr(
                            part,
                            "MaterialCode",
                            ""
                        ),

                    "Position":
                        self.getValue(
                            getattr(
                                part,
                                "Position",
                                0
                            )
                        ),

                    "PositionType":
                        getattr(
                            part,
                            "PositionType",
                            "Automatic"
                        ),

                    "PositionMode":
                        getattr(
                            part,
                            "PositionMode",
                            "Automatic"
                        ),

                    "PositionX":
                        self.getValue(
                            getattr(
                                part,
                                "PositionX",
                                0
                            )
                        ),

                    "PositionY":
                        self.getValue(
                            getattr(
                                part,
                                "PositionY",
                                0
                            )
                        ),

                    "PositionZ":
                        self.getValue(
                            getattr(
                                part,
                                "PositionZ",
                                0
                            )
                        ),

                    "RotationX":
                        self.getValue(
                            getattr(
                                part,
                                "RotationX",
                                0
                            )
                        ),

                    "RotationY":
                        self.getValue(
                            getattr(
                                part,
                                "RotationY",
                                0
                            )
                        ),

                    "RotationZ":
                        self.getValue(
                            getattr(
                                part,
                                "RotationZ",
                                0
                            )
                        )
                }

            #
            # Make sure required fields exist.
            #

            data.setdefault(
                "Role",
                "Custom"
            )

            data.setdefault(
                "PartType",
                "Personalizado"
            )

            data.setdefault(
                "PositionMode",
                "Automatic"
            )

            data.setdefault(
                "PositionType",
                "Automatic"
            )

            data.setdefault(
                "Quantity",
                1
            )

            #
            # Store.
            #

            self.userParts.append(
                data
            )


    # =========================================================
    # UPDATE MODULE
    # =========================================================

    def updateModule(
        self
    ):

        module = self.module

        if module is None:

            return

        name = (
            self.nameEdit.text().strip()
            or
            "Módulo"
        )

        if hasattr(
            module,
            "ModuleName"
        ):

            module.ModuleName = name

        #
        # Label
        #

        if hasattr(
            module,
            "Label"
        ):

            module.Label = name

        #
        # WIDTH
        #

        if hasattr(
            module,
            "Width"
        ):

            module.Width = (
                self.widthSpin.value()
            )

        #
        # HEIGHT
        #

        if hasattr(
            module,
            "Height"
        ):

            module.Height = (
                self.heightSpin.value()
            )

        #
        # DEPTH
        #

        if hasattr(
            module,
            "Depth"
        ):

            module.Depth = (
                self.depthSpin.value()
            )

        #
        # PANEL THICKNESS
        #

        if hasattr(
            module,
            "PanelThickness"
        ):

            module.PanelThickness = (
                self.thicknessSpin.value()
            )

        #
        # BACK THICKNESS
        #

        if hasattr(
            module,
            "BackThickness"
        ):

            module.BackThickness = (
                self.backThicknessSpin.value()
            )

        #
        # BACK INSET
        #

        if hasattr(
            module,
            "BackInset"
        ):

            module.BackInset = (
                self.backInsetSpin.value()
            )

        module.touch()


    # =========================================================
    # CALCULATE PARTS
    # =========================================================

    def calculateParts(
        self
    ):

        #
        # First save current table values.
        #

        self.updateTableData()

        #
        # Update module parameters.
        #

        self.updateModule()

        #
        # Read dimensions.
        #

        width = self.widthSpin.value()

        height = self.heightSpin.value()

        depth = self.depthSpin.value()

        thickness = self.thicknessSpin.value()

        backThickness = (
            self.backThicknessSpin.value()
        )

        #
        # =====================================================
        # STRUCTURAL
        # =====================================================
        #

        calculated = []

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

            calculated.append(
                dict(
                    part
                )
            )

        #
        # =====================================================
        # AUTOMATIC POSITIONS
        # =====================================================
        #

        self.calculateAutomaticPositions(
            calculated
        )

        self.parts = calculated

        #
        # Refresh visible table.
        #

        self.loadTable()


    # =========================================================
    # STRUCTURAL PART
    # =========================================================

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


    # =========================================================
    # AUTOMATIC POSITIONS
    # =========================================================

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

            moduleHeight = (
                self.heightSpin.value()
            )

            thickness = (
                self.thicknessSpin.value()
            )

            count = len(
                shelves
            )

            internalHeight = (
                moduleHeight
                -
                thickness * 2
            )

            availableHeight = (
                internalHeight
                -
                thickness * count
            )

            if count > 0:

                spacing = (
                    availableHeight
                    /
                    (
                        count + 1
                    )
                )

                for index, part in enumerate(
                    shelves,
                    start=1
                ):

                    z = (
                        thickness
                        +
                        spacing * index
                        +
                        thickness * (
                            index - 1
                        )
                    )

                    part["Position"] = z

                    part["PositionX"] = (
                        thickness
                    )

                    part["PositionY"] = 0

                    part["PositionZ"] = z

                    part["PositionType"] = (
                        "Automatic"
                    )

                    part["PositionMode"] = (
                        "Automatic"
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

            moduleWidth = (
                self.widthSpin.value()
            )

            thickness = (
                self.thicknessSpin.value()
            )

            count = len(
                dividers
            )

            internalWidth = (
                moduleWidth
                -
                thickness * 2
            )

            availableWidth = (
                internalWidth
                -
                thickness * count
            )

            if count > 0:

                spacing = (
                    availableWidth
                    /
                    (
                        count + 1
                    )
                )

                for index, part in enumerate(
                    dividers,
                    start=1
                ):

                    x = (
                        thickness
                        +
                        spacing * index
                        +
                        thickness * (
                            index - 1
                        )
                    )

                    part["Position"] = x

                    part["PositionX"] = x

                    part["PositionY"] = 0

                    part["PositionZ"] = (
                        thickness
                    )

                    part["PositionType"] = (
                        "Automatic"
                    )

                    part["PositionMode"] = (
                        "Automatic"
                    )


    # =========================================================
    # ADD CUSTOM PART
    # =========================================================

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
        # Default dimensions.
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
                str(number),

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

        self.userParts.append(
            part
        )

        self.calculateParts()

        self.table.selectRow(
            self.table.rowCount() - 1
        )


    # =========================================================
    # EDIT PLACEMENT
    # =========================================================

    def editPlacement(
        self
    ):

        self.updateTableData()

        row = self.table.currentRow()

        if row < 0:

            return

        #
        # Structural pieces.
        #

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


    # =========================================================
    # DELETE
    # =========================================================

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
                "Las piezas estructurales "
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


    # =========================================================
    # DUPLICATE
    # =========================================================

    def duplicatePart(
        self
    ):

        self.updateTableData()

        row = self.table.currentRow()

        if row < 5:

            QtWidgets.QMessageBox.information(
                self,
                "Duplicar pieza",
                "Selecciona una pieza "
                "creada por el usuario."
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
            str(number)
        )

        self.userParts.append(
            copy
        )

        self.calculateParts()


    # =========================================================
    # LOAD TABLE
    # =========================================================

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
            # TYPE
            #

            typeCombo = QtWidgets.QComboBox()

            typeCombo.addItem(
                "Estructural",
                "Side"
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
                "Custom"
            )

            index = typeCombo.findData(
                role
            )

            if index < 0:

                index = 3

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
            # DIMENSIONS
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
            # MATERIAL
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

            if materialCode:

                materialCombo.addItem(
                    str(materialCode),
                    materialCode
                )

                materialCombo.setCurrentIndex(
                    1
                )

            self.table.setCellWidget(
                row,
                6,
                materialCombo
            )

            #
            # POSITION TYPE
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
            # MODE
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
        # COLUMN WIDTHS
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


    # =========================================================
    # UPDATE TABLE DATA
    # =========================================================

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
            # LABEL
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
            # TYPE
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

                else:

                    part["PartType"] = (
                        "Personalizado"
                    )

            #
            # DIMENSIONS
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
            # MATERIAL
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
            # POSITION TYPE
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
            # MODE
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


    # =========================================================
    # GET DATA
    # =========================================================

    def getData(
        self
    ):

        self.updateTableData()

        #
        # Return ONLY user parts.
        #
        # Structural pieces are generated by
        # ModuleBuilder.
        #

        return [
            dict(
                part
            )
            for part in self.userParts
        ]


    # =========================================================
    # SAVE
    # =========================================================

    def save(
        self
    ):

        self.updateTableData()

        self.updateModule()

        #
        # Do not directly modify BosqoParts here.
        #
        # The command calls ModuleBuilder.
        #

        self.accept()


    # =========================================================
    # SET ITEM
    # =========================================================

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


    # =========================================================
    # GET FLOAT
    # =========================================================

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

            return 0.0

        try:

            return float(
                item.text().replace(
                    ",",
                    "."
                )
            )

        except Exception:

            return 0.0


    # =========================================================
    # NUMBER
    # =========================================================

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


    # =========================================================
    # GET VALUE
    # =========================================================

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

            return 0.0