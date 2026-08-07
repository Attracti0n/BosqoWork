import FreeCAD

from PySide import QtWidgets, QtCore


# =============================================================
# MANUAL PLACEMENT DIALOG
# =============================================================

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

        position_group = QtWidgets.QGroupBox(
            "Posición"
        )

        position_layout = QtWidgets.QGridLayout()

        self.xSpin = self.createSpinBox()
        self.ySpin = self.createSpinBox()
        self.zSpin = self.createSpinBox()

        for row, label, widget in (
            (0, "X:", self.xSpin),
            (1, "Y:", self.ySpin),
            (2, "Z:", self.zSpin)
        ):

            position_layout.addWidget(
                QtWidgets.QLabel(
                    label
                ),
                row,
                0
            )

            position_layout.addWidget(
                widget,
                row,
                1
            )

        position_group.setLayout(
            position_layout
        )

        layout.addWidget(
            position_group
        )

        #
        # =====================================================
        # ROTATION
        # =====================================================
        #

        rotation_group = QtWidgets.QGroupBox(
            "Giro"
        )

        rotation_layout = QtWidgets.QGridLayout()

        self.rxSpin = self.createAngleSpinBox()
        self.rySpin = self.createAngleSpinBox()
        self.rzSpin = self.createAngleSpinBox()

        for row, label, widget in (
            (0, "Giro X:", self.rxSpin),
            (1, "Giro Y:", self.rySpin),
            (2, "Giro Z:", self.rzSpin)
        ):

            rotation_layout.addWidget(
                QtWidgets.QLabel(
                    label
                ),
                row,
                0
            )

            rotation_layout.addWidget(
                widget,
                row,
                1
            )

        rotation_group.setLayout(
            rotation_layout
        )

        layout.addWidget(
            rotation_group
        )

        #
        # =====================================================
        # BUTTONS
        # =====================================================
        #

        buttons = QtWidgets.QHBoxLayout()

        buttons.addStretch()

        cancel_button = QtWidgets.QPushButton(
            "Cancelar"
        )

        ok_button = QtWidgets.QPushButton(
            "Aceptar"
        )

        buttons.addWidget(
            cancel_button
        )

        buttons.addWidget(
            ok_button
        )

        layout.addLayout(
            buttons
        )

        cancel_button.clicked.connect(
            self.reject
        )

        ok_button.clicked.connect(
            self.accept
        )

        self.loadData()


    # =========================================================
    # SPIN BOX
    # =========================================================

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


    # =========================================================
    # LOAD DATA
    # =========================================================

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
                    self.part.get(
                        "Position",
                        0
                    )
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


    # =========================================================
    # GET DATA
    # =========================================================

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


    # =========================================================
    # TO FLOAT
    # =========================================================

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


# =============================================================
# PARAMETRIC MODULE DIALOG
# =============================================================

class ParametricModuleDialog(
    QtWidgets.QDialog
):

    def __init__(
        self,
        module=None,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.module = module

        #
        # Only user-created pieces.
        #
        # Structural pieces are generated
        # by ModuleBuilder.
        #

        self.userParts = []

        #
        # Manual placement of structural beams.
        #

        self.structuralPlacements = {}

        #
        # Material selected for structural pieces.
        #
        # This is kept while the dialog is open.
        #

        self.structuralMaterials = {}

        #
        # Current generated parts.
        #

        self.parts = []

        #
        # Prevent recursive table updates.
        #

        self._loading_table = False

        self.setWindowTitle(
            "Módulo paramétrico"
        )

        self.resize(
            1250,
            750
        )

        self.createUI()

        self.loadModule()

        self.calculateParts()


    # =========================================================
    # CREATE UI
    # =========================================================

    def createUI(
        self
    ):

        main_layout = QtWidgets.QVBoxLayout(
            self
        )

        #
        # =====================================================
        # MODULE DATA
        # =====================================================
        #

        module_group = QtWidgets.QGroupBox(
            "Datos del módulo"
        )

        module_layout = QtWidgets.QGridLayout()

        self.nameEdit = QtWidgets.QLineEdit()

        self.widthSpin = self.createSpinBox()
        self.heightSpin = self.createSpinBox()
        self.depthSpin = self.createSpinBox()
        self.thicknessSpin = self.createSpinBox()
        self.backThicknessSpin = self.createSpinBox()
        self.backInsetSpin = self.createSpinBox()

        module_layout.addWidget(
            QtWidgets.QLabel(
                "Nombre del módulo:"
            ),
            0,
            0
        )

        module_layout.addWidget(
            self.nameEdit,
            0,
            1,
            1,
            5
        )

        fields = [

            (
                "Ancho:",
                self.widthSpin,
                1,
                0
            ),

            (
                "Alto:",
                self.heightSpin,
                1,
                2
            ),

            (
                "Profundidad:",
                self.depthSpin,
                2,
                0
            ),

            (
                "Espesor panel:",
                self.thicknessSpin,
                2,
                2
            ),

            (
                "Espesor fondo:",
                self.backThicknessSpin,
                3,
                0
            ),

            (
                "Retranqueo trasero:",
                self.backInsetSpin,
                3,
                2
            )

        ]

        for label, widget, row, col in fields:

            module_layout.addWidget(
                QtWidgets.QLabel(
                    label
                ),
                row,
                col
            )

            module_layout.addWidget(
                widget,
                row,
                col + 1
            )

        #
        # =====================================================
        # TOP TYPE
        # =====================================================
        #

        self.topTypeCombo = QtWidgets.QComboBox()

        self.topTypeCombo.addItems(
            [
                "Tapa completa",
                "2 travesaños",
                "3 travesaños"
            ]
        )

        #
        # =====================================================
        # BACK TYPE
        # =====================================================
        #

        self.backTypeCombo = QtWidgets.QComboBox()

        self.backTypeCombo.addItems(
            [
                "Trasera sobrepuesta",
                "Trasera oculta",
                "2 travesaños",
                "3 travesaños",
                "Sin trasera"
            ]
        )

        module_layout.addWidget(
            QtWidgets.QLabel(
                "Tipo de tapa:"
            ),
            4,
            0
        )

        module_layout.addWidget(
            self.topTypeCombo,
            4,
            1
        )

        module_layout.addWidget(
            QtWidgets.QLabel(
                "Tipo de trasera:"
            ),
            4,
            2
        )

        module_layout.addWidget(
            self.backTypeCombo,
            4,
            3
        )

        module_group.setLayout(
            module_layout
        )

        main_layout.addWidget(
            module_group
        )

        #
        # =====================================================
        # PARTS TABLE
        # =====================================================
        #

        parts_group = QtWidgets.QGroupBox(
            "Tabla de piezas"
        )

        parts_layout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget()

        self.table.setColumnCount(
            8
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

        parts_layout.addWidget(
            self.table
        )

        #
        # =====================================================
        # PART BUTTONS
        # =====================================================
        #

        buttons_layout = QtWidgets.QHBoxLayout()

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

        buttons_layout.addWidget(
            self.addButton
        )

        buttons_layout.addWidget(
            self.deleteButton
        )

        buttons_layout.addWidget(
            self.duplicateButton
        )

        buttons_layout.addWidget(
            self.placementButton
        )

        buttons_layout.addStretch()

        parts_layout.addLayout(
            buttons_layout
        )

        parts_group.setLayout(
            parts_layout
        )

        main_layout.addWidget(
            parts_group
        )

        #
        # =====================================================
        # BOTTOM BUTTONS
        # =====================================================
        #

        bottom_layout = QtWidgets.QHBoxLayout()

        self.recalculateButton = QtWidgets.QPushButton(
            "Recalcular"
        )

        self.saveButton = QtWidgets.QPushButton(
            "Guardar"
        )

        self.cancelButton = QtWidgets.QPushButton(
            "Cancelar"
        )

        bottom_layout.addWidget(
            self.recalculateButton
        )

        bottom_layout.addStretch()

        bottom_layout.addWidget(
            self.saveButton
        )

        bottom_layout.addWidget(
            self.cancelButton
        )

        main_layout.addLayout(
            bottom_layout
        )

        #
        # =====================================================
        # CONNECTIONS
        # =====================================================
        #

        self.addButton.clicked.connect(
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

        self.topTypeCombo.currentIndexChanged.connect(
            self.calculateParts
        )

        self.backTypeCombo.currentIndexChanged.connect(
            self.calculateParts
        )


    # =========================================================
    # SPIN BOX
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

        #
        # =====================================================
        # NEW MODULE
        # =====================================================
        #

        if self.module is None:

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
                10
            )

            self.backInsetSpin.setValue(
                0
            )

            return

        #
        # =====================================================
        # NAME
        # =====================================================
        #

        self.nameEdit.setText(
            str(
                getattr(
                    self.module,
                    "ModuleName",
                    getattr(
                        self.module,
                        "Label",
                        "Nuevo módulo"
                    )
                )
            )
        )

        #
        # =====================================================
        # DIMENSIONS
        #
        # IMPORTANT:
        # ModuleBuilder uses Width / Height / Depth.
        # ModuleWidth / ModuleHeight / ModuleDepth are
        # supported only as fallback for older modules.
        # =====================================================
        #

        self.widthSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "Width",
                    getattr(
                        self.module,
                        "ModuleWidth",
                        600
                    )
                )
            )
        )

        self.heightSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "Height",
                    getattr(
                        self.module,
                        "ModuleHeight",
                        720
                    )
                )
            )
        )

        self.depthSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "Depth",
                    getattr(
                        self.module,
                        "ModuleDepth",
                        560
                    )
                )
            )
        )

        #
        # =====================================================
        # THICKNESSES
        # =====================================================
        #

        self.thicknessSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "PanelThickness",
                    19
                )
            )
        )

        self.backThicknessSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "BackThickness",
                    10
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

        #
        # =====================================================
        # TOP TYPE
        # =====================================================
        #

        self.setCombo(
            self.topTypeCombo,
            getattr(
                self.module,
                "TopType",
                "Tapa completa"
            )
        )

        #
        # =====================================================
        # BACK TYPE
        # =====================================================
        #

        self.setCombo(
            self.backTypeCombo,
            getattr(
                self.module,
                "BackType",
                "Trasera sobrepuesta"
            )
        )

        #
        # =====================================================
        # PROXY
        # =====================================================
        #

        proxy = getattr(
            self.module,
            "Proxy",
            None
        )

        if proxy is None:

            return

        #
        # =====================================================
        # USER PARTS
        # =====================================================
        #

        if hasattr(
            proxy,
            "getUserParts"
        ):

            try:

                self.userParts = [

                    dict(
                        item
                    )

                    for item in proxy.getUserParts(
                        self.module
                    )

                ]

            except Exception:

                self.userParts = []

        elif hasattr(
            self.module,
            "Parts"
        ):

            try:

                self.userParts = [

                    dict(
                        item
                    )

                    for item in self.module.Parts

                ]

            except Exception:

                self.userParts = []

        #
        # =====================================================
        # STRUCTURAL PLACEMENTS
        # =====================================================
        #

        if hasattr(
            proxy,
            "getStructuralPlacements"
        ):

            try:

                self.structuralPlacements = dict(
                    proxy.getStructuralPlacements(
                        self.module
                    )
                )

            except Exception:

                self.structuralPlacements = {}

        else:

            self.structuralPlacements = {}


    # =========================================================
    # UPDATE MODULE
    # =========================================================

    def updateModule(
        self
    ):

        if self.module is None:

            return

        #
        # =====================================================
        # IDENTIFICATION
        # =====================================================
        #

        name = (
            self.nameEdit.text().strip()
            or
            "Nuevo módulo"
        )

        if hasattr(
            self.module,
            "ModuleName"
        ):

            self.module.ModuleName = name

        self.module.Label = name

        #
        # =====================================================
        # DIMENSIONS
        #
        # ModuleBuilder reads Width / Height / Depth.
        # Therefore these MUST be updated.
        #
        # Older aliases are also updated when present.
        # =====================================================
        #

        width = self.widthSpin.value()
        height = self.heightSpin.value()
        depth = self.depthSpin.value()

        if hasattr(
            self.module,
            "Width"
        ):

            self.module.Width = width

        if hasattr(
            self.module,
            "ModuleWidth"
        ):

            self.module.ModuleWidth = width

        if hasattr(
            self.module,
            "Height"
        ):

            self.module.Height = height

        if hasattr(
            self.module,
            "ModuleHeight"
        ):

            self.module.ModuleHeight = height

        if hasattr(
            self.module,
            "Depth"
        ):

            self.module.Depth = depth

        if hasattr(
            self.module,
            "ModuleDepth"
        ):

            self.module.ModuleDepth = depth

        #
        # =====================================================
        # THICKNESSES
        # =====================================================
        #

        self.module.PanelThickness = (
            self.thicknessSpin.value()
        )

        self.module.BackThickness = (
            self.backThicknessSpin.value()
        )

        self.module.BackInset = (
            self.backInsetSpin.value()
        )

        #
        # =====================================================
        # TYPES
        # =====================================================
        #

        if hasattr(
            self.module,
            "TopType"
        ):

            self.module.TopType = (
                self.topTypeCombo.currentText()
            )

        if hasattr(
            self.module,
            "BackType"
        ):

            self.module.BackType = (
                self.backTypeCombo.currentText()
            )

        #
        # =====================================================
        # PROXY
        # =====================================================
        #

        proxy = getattr(
            self.module,
            "Proxy",
            None
        )

        if proxy is None:

            return

        #
        # =====================================================
        # USER PARTS
        # =====================================================
        #

        if hasattr(
            proxy,
            "setUserParts"
        ):

            try:

                proxy.setUserParts(
                    self.module,
                    self.userParts
                )

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error guardando piezas de usuario: "
                    +
                    str(error)
                    +
                    "\n"
                )

        elif hasattr(
            self.module,
            "Parts"
        ):

            try:

                self.module.Parts = [

                    dict(
                        part
                    )

                    for part in self.userParts

                ]

            except Exception:

                pass

        #
        # =====================================================
        # STRUCTURAL PLACEMENTS
        # =====================================================
        #

        if hasattr(
            proxy,
            "setStructuralPlacements"
        ):

            try:

                proxy.setStructuralPlacements(
                    self.module,
                    self.structuralPlacements
                )

            except Exception:

                pass


    # =========================================================
    # CALCULATE PARTS
    # =========================================================

    def calculateParts(
        self
    ):

        if self.module is None:

            return

        #
        # =====================================================
        # STEP 1
        #
        # Read the table only for user-editable information:
        # label, material, quantity, type, manual dimensions,
        # etc.
        #
        # Automatic shelf/divider dimensions are NOT taken
        # from the old table values.
        # =====================================================
        #

        self.updateTableData()

        #
        # =====================================================
        # STEP 2
        #
        # Update module Width / Height / Depth first.
        # =====================================================
        #

        self.updateModule()

        #
        # =====================================================
        # STEP 3
        #
        # Recalculate automatic shelf/divider positions.
        # =====================================================
        #

        self.recalculateAutomaticUserPartPositions()

        #
        # =====================================================
        # STEP 4
        #
        # Recalculate automatic dimensions of user parts.
        #
        # This is deliberately done here as well as inside
        # ModuleBuilder. This guarantees that the data which
        # will be stored and shown in the table is already
        # correct before rebuilding the module.
        # =====================================================
        #

        self.recalculateAutomaticUserPartDimensions()

        #
        # Save the corrected user data.
        #

        self.updateModule()

        #
        # =====================================================
        # STEP 5
        # BUILD
        # =====================================================
        #

        try:

            from core.builders.module_builder import (
                ModuleBuilder
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error importando ModuleBuilder: "
                +
                str(error)
                +
                "\n"
            )

            return

        try:

            ModuleBuilder.build(
                self.module,
                self.userParts
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error construyendo módulo: "
                +
                str(error)
                +
                "\n"
            )

            return

        #
        # =====================================================
        # STEP 6
        # GET GENERATED PARTS
        # =====================================================
        #

        proxy = getattr(
            self.module,
            "Proxy",
            None
        )

        if proxy is None:

            return

        if hasattr(
            proxy,
            "getParts"
        ):

            try:

                self.parts = proxy.getParts(
                    self.module
                )

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error obteniendo piezas: "
                    +
                    str(error)
                    +
                    "\n"
                )

                self.parts = []

        else:

            self.parts = []

        #
        # =====================================================
        # STEP 7
        #
        # Restore material selections for generated structural
        # pieces.
        # =====================================================
        #

        self.applyStructuralMaterials()

        #
        # =====================================================
        # STEP 8
        # REBUILD TABLE
        # =====================================================
        #

        self.loadTable()


    # =========================================================
    # RECALCULATE AUTOMATIC USER PART DIMENSIONS
    # =========================================================

    def recalculateAutomaticUserPartDimensions(
        self
    ):

        width = self.widthSpin.value()
        height = self.heightSpin.value()
        depth = self.depthSpin.value()
        thickness = self.thicknessSpin.value()
        backThickness = self.backThicknessSpin.value()
        backInset = self.backInsetSpin.value()

        #
        # Useful depth.
        #
        # Same logic used by ModuleBuilder.
        #

        useful_depth = (
            depth
            -
            backInset
            -
            backThickness
        )

        if useful_depth < 0:

            useful_depth = 0

        #
        # =====================================================
        # USER PARTS
        # =====================================================
        #

        for part in self.userParts:

            role = str(
                part.get(
                    "Role",
                    "Custom"
                )
            )

            mode = str(
                part.get(
                    "PositionMode",
                    "Automatic"
                )
            )

            #
            # -------------------------------------------------
            # SHELF
            # -------------------------------------------------
            #

            if (
                role == "Shelf"
                and
                mode == "Automatic"
            ):

                part["PartType"] = (
                    "Balda"
                )

                part["Length"] = max(
                    0,
                    width
                    -
                    thickness * 2
                )

                part["Width"] = max(
                    0,
                    useful_depth
                )

                part["Thickness"] = max(
                    0,
                    thickness
                )

                part["LengthAxis"] = "X"
                part["WidthAxis"] = "Y"
                part["ThicknessAxis"] = "Z"

            #
            # -------------------------------------------------
            # DIVIDER
            # -------------------------------------------------
            #

            elif (
                role == "Divider"
                and
                mode == "Automatic"
            ):

                part["PartType"] = (
                    "Separador"
                )

                part["Length"] = max(
                    0,
                    height
                    -
                    thickness * 2
                )

                part["Width"] = max(
                    0,
                    useful_depth
                )

                part["Thickness"] = max(
                    0,
                    thickness
                )

                part["LengthAxis"] = "Z"
                part["WidthAxis"] = "Y"
                part["ThicknessAxis"] = "X"

            #
            # -------------------------------------------------
            # CUSTOM
            # -------------------------------------------------
            #

            elif role == "Custom":

                part["PartType"] = (
                    "Personalizado"
                )

            #
            # -------------------------------------------------
            # DEFAULTS
            # -------------------------------------------------
            #

            if "Quantity" not in part:

                part["Quantity"] = 1

            if "MaterialCode" not in part:

                part["MaterialCode"] = ""

            if "PositionMode" not in part:

                part["PositionMode"] = (
                    "Automatic"
                )

            if "PositionType" not in part:

                part["PositionType"] = (
                    part.get(
                        "PositionMode",
                        "Automatic"
                    )
                )


    # =========================================================
    # AUTOMATIC USER PART POSITIONS
    # =========================================================

    def recalculateAutomaticUserPartPositions(
        self
    ):

        if not self.userParts:

            return

        panelThickness = (
            self.thicknessSpin.value()
        )

        moduleHeight = (
            self.heightSpin.value()
        )

        moduleWidth = (
            self.widthSpin.value()
        )

        #
        # =====================================================
        # SHELVES
        # =====================================================
        #

        shelves = [

            part

            for part in self.userParts

            if (
                str(
                    part.get(
                        "Role",
                        ""
                    )
                )
                ==
                "Shelf"
            )

            and

            str(
                part.get(
                    "PositionMode",
                    "Automatic"
                )
            )
            ==
            "Automatic"

            and

            str(
                part.get(
                    "PositionType",
                    "Automatic"
                )
            )
            ==
            "Automatic"

        ]

        if shelves:

            usableHeight = (
                moduleHeight
                -
                panelThickness * 2
            )

            if usableHeight < 0:

                usableHeight = 0

            totalShelfThickness = (
                panelThickness
                *
                len(
                    shelves
                )
            )

            freeHeight = (
                usableHeight
                -
                totalShelfThickness
            )

            if freeHeight < 0:

                freeHeight = 0

            spacing = (
                freeHeight
                /
                (
                    len(
                        shelves
                    )
                    +
                    1
                )
            )

            for index, part in enumerate(
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

                part["Position"] = z

                part["PositionType"] = (
                    "Automatic"
                )

                part["PositionMode"] = (
                    "Automatic"
                )

                part["PositionX"] = (
                    panelThickness
                )

                part["PositionY"] = 0

                part["PositionZ"] = z

                part["RotationX"] = 0
                part["RotationY"] = 0
                part["RotationZ"] = 0

        #
        # =====================================================
        # DIVIDERS
        # =====================================================
        #

        dividers = [

            part

            for part in self.userParts

            if (
                str(
                    part.get(
                        "Role",
                        ""
                    )
                )
                ==
                "Divider"
            )

            and

            str(
                part.get(
                    "PositionMode",
                    "Automatic"
                )
            )
            ==
            "Automatic"

            and

            str(
                part.get(
                    "PositionType",
                    "Automatic"
                )
            )
            ==
            "Automatic"

        ]

        if dividers:

            usableWidth = (
                moduleWidth
                -
                panelThickness * 2
            )

            if usableWidth < 0:

                usableWidth = 0

            totalDividerThickness = (
                panelThickness
                *
                len(
                    dividers
                )
            )

            freeWidth = (
                usableWidth
                -
                totalDividerThickness
            )

            if freeWidth < 0:

                freeWidth = 0

            spacing = (
                freeWidth
                /
                (
                    len(
                        dividers
                    )
                    +
                    1
                )
            )

            for index, part in enumerate(
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

                part["Position"] = x

                part["PositionType"] = (
                    "Automatic"
                )

                part["PositionMode"] = (
                    "Automatic"
                )

                part["PositionX"] = x

                part["PositionY"] = 0

                part["PositionZ"] = (
                    panelThickness
                )

                part["RotationX"] = 0
                part["RotationY"] = 0
                part["RotationZ"] = 0


    # =========================================================
    # LOAD TABLE
    # =========================================================

    def loadTable(
        self
    ):

        self._loading_table = True

        try:

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
                # =================================================
                # LABEL
                # =================================================
                #

                self.setItem(
                    row,
                    0,
                    getattr(
                        part,
                        "Label",
                        ""
                    )
                )

                #
                # =================================================
                # CODE
                # =================================================
                #

                code = str(
                    getattr(
                        part,
                        "Code",
                        ""
                    )
                )

                #
                # =================================================
                # ROLE
                # =================================================
                #

                role = str(
                    getattr(
                        part,
                        "Role",
                        "Custom"
                    )
                )

                #
                # =================================================
                # TYPE COMBO
                # =================================================
                #

                type_combo = QtWidgets.QComboBox()

                type_combo.addItem(
                    "Estructural",
                    "Structural"
                )

                type_combo.addItem(
                    "Balda",
                    "Shelf"
                )

                type_combo.addItem(
                    "Separador",
                    "Divider"
                )

                type_combo.addItem(
                    "Personalizado",
                    "Custom"
                )

                if role in (
                    "Side",
                    "Bottom",
                    "Top",
                    "Back",
                    "TopBeam",
                    "BackBeam"
                ):

                    type_role = (
                        "Structural"
                    )

                else:

                    type_role = role

                index = (
                    type_combo.findData(
                        type_role
                    )
                )

                if index >= 0:

                    type_combo.setCurrentIndex(
                        index
                    )

                #
                # Structural type remains fixed.
                #

                structural = (
                    code
                    in
                    {
                        "LS",
                        "RS",
                        "BT",
                        "TP",
                        "BK",
                        "TT1",
                        "TT2",
                        "TT3",
                        "TB1",
                        "TB2",
                        "TB3"
                    }
                )

                type_combo.setEnabled(
                    not structural
                )

                self.table.setCellWidget(
                    row,
                    1,
                    type_combo
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
                        getattr(
                            part,
                            "Length",
                            0
                        )
                    )
                )

                self.setItem(
                    row,
                    3,
                    self.number(
                        getattr(
                            part,
                            "Width",
                            0
                        )
                    )
                )

                self.setItem(
                    row,
                    4,
                    self.number(
                        getattr(
                            part,
                            "Thickness",
                            0
                        )
                    )
                )

                self.setItem(
                    row,
                    5,
                    self.number(
                        getattr(
                            part,
                            "Quantity",
                            1
                        )
                    )
                )

                #
                # =================================================
                # MATERIAL
                #
                # ACTIVE FOR ALL PIECES.
                # =================================================
                #

                material_code = str(
                    getattr(
                        part,
                        "MaterialCode",
                        ""
                    )
                )

                material_combo = (
                    self.createMaterialCombo(
                        material_code
                    )
                )

                material_combo.currentIndexChanged.connect(
                    lambda value,
                    r=row:
                    self.materialChanged(
                        r
                    )
                )

                #
                # IMPORTANT:
                #
                # Material is NOT disabled for structural
                # pieces.
                #

                material_combo.setEnabled(
                    True
                )

                self.table.setCellWidget(
                    row,
                    6,
                    material_combo
                )

                #
                # =================================================
                # MODE
                # =================================================
                #

                mode_combo = QtWidgets.QComboBox()

                mode_combo.addItem(
                    "Automática",
                    "Automatic"
                )

                mode_combo.addItem(
                    "Manual",
                    "Manual"
                )

                mode = str(
                    getattr(
                        part,
                        "PositionMode",
                        "Automatic"
                    )
                )

                mode_index = (
                    mode_combo.findData(
                        mode
                    )
                )

                if mode_index < 0:

                    mode_index = 0

                mode_combo.setCurrentIndex(
                    mode_index
                )

                #
                # Structural pieces fixed,
                # beams can be manually positioned.
                #

                beam = (
                    code.startswith(
                        "TT"
                    )
                    or
                    code.startswith(
                        "TB"
                    )
                )

                mode_combo.setEnabled(
                    beam
                    or
                    not structural
                )

                mode_combo.currentIndexChanged.connect(
                    lambda value,
                    r=row:
                    self.modeChanged(
                        r
                    )
                )

                self.table.setCellWidget(
                    row,
                    7,
                    mode_combo
                )

            self.resizeColumns()

        finally:

            self._loading_table = False


    # =========================================================
    # MATERIAL COMBO
    # =========================================================

    def createMaterialCombo(
        self,
        selectedCode=""
    ):

        combo = QtWidgets.QComboBox()

        combo.addItem(
            "— Sin material —",
            ""
        )

        try:

            from library.material_library import (
                MaterialLibrary
            )

            materials = (
                MaterialLibrary.all()
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error cargando biblioteca de materiales: "
                +
                str(error)
                +
                "\n"
            )

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

        selected = str(
            selectedCode
            or
            ""
        )

        index = combo.findData(
            selected
        )

        if index >= 0:

            combo.setCurrentIndex(
                index
            )

        else:

            combo.setCurrentIndex(
                0
            )

        return combo


    # =========================================================
    # MATERIAL CHANGED
    # =========================================================

    def materialChanged(
        self,
        row
    ):

        if self._loading_table:

            return

        if row < 0:

            return

        if row >= len(
            self.parts
        ):

            return

        combo = self.table.cellWidget(
            row,
            6
        )

        if combo is None:

            return

        material_code = (
            combo.currentData()
            or
            ""
        )

        part = self.parts[
            row
        ]

        code = str(
            getattr(
                part,
                "Code",
                ""
            )
        )

        #
        # Store in generated part immediately.
        #

        try:

            if hasattr(
                part,
                "MaterialCode"
            ):

                part.MaterialCode = (
                    material_code
                )

                part.touch()

        except Exception:

            pass

        #
        # User part.
        #

        for user_part in self.userParts:

            if (
                str(
                    user_part.get(
                        "Code",
                        ""
                    )
                )
                ==
                code
            ):

                user_part[
                    "MaterialCode"
                ] = material_code

                break

        #
        # Structural piece.
        #

        if code in {

            "LS",
            "RS",
            "BT",
            "TP",
            "BK",
            "TT1",
            "TT2",
            "TT3",
            "TB1",
            "TB2",
            "TB3"

        }:

            self.structuralMaterials[
                code
            ] = material_code


    # =========================================================
    # APPLY STRUCTURAL MATERIALS
    # =========================================================

    def applyStructuralMaterials(
        self
    ):

        if not self.structuralMaterials:

            return

        for part in self.parts:

            code = str(
                getattr(
                    part,
                    "Code",
                    ""
                )
            )

            if code not in (
                self.structuralMaterials
            ):

                continue

            material_code = (
                self.structuralMaterials[
                    code
                ]
            )

            try:

                if hasattr(
                    part,
                    "MaterialCode"
                ):

                    part.MaterialCode = (
                        material_code
                    )

                    part.touch()

            except Exception:

                pass


    # =========================================================
    # UPDATE TABLE DATA
    # =========================================================

    def updateTableData(
        self
    ):

        if self._loading_table:

            return

        structural_codes = {

            "LS",
            "RS",
            "BT",
            "TP",
            "BK",
            "TT1",
            "TT2",
            "TT3",
            "TB1",
            "TB2",
            "TB3"

        }

        current_user = {

            str(
                part.get(
                    "Code",
                    ""
                )
            ):
                part

            for part in self.userParts

        }

        for row in range(
            self.table.rowCount()
        ):

            if row >= len(
                self.parts
            ):

                continue

            item = self.table.item(
                row,
                0
            )

            if item is None:

                continue

            part_object = self.parts[
                row
            ]

            code = str(
                getattr(
                    part_object,
                    "Code",
                    ""
                )
            )

            type_combo = (
                self.table.cellWidget(
                    row,
                    1
                )
            )

            mode_combo = (
                self.table.cellWidget(
                    row,
                    7
                )
            )

            material_combo = (
                self.table.cellWidget(
                    row,
                    6
                )
            )

            #
            # =================================================
            # STRUCTURAL
            # =================================================
            #

            if code in structural_codes:

                #
                # Material is still editable.
                #

                if material_combo is not None:

                    material_code = (
                        material_combo.currentData()
                        or
                        ""
                    )

                    self.structuralMaterials[
                        code
                    ] = material_code

                    try:

                        if hasattr(
                            part_object,
                            "MaterialCode"
                        ):

                            part_object.MaterialCode = (
                                material_code
                            )

                    except Exception:

                        pass

                #
                # Beam placement.
                #

                if (
                    code.startswith(
                        "TT"
                    )
                    or
                    code.startswith(
                        "TB"
                    )
                ):

                    mode = (

                        mode_combo.currentData()

                        if mode_combo is not None

                        else

                        "Automatic"

                    )

                    if mode == "Manual":

                        data = (
                            self.partPlacementData(
                                part_object
                            )
                        )

                        self.structuralPlacements[
                            code
                        ] = data

                    else:

                        self.structuralPlacements.pop(
                            code,
                            None
                        )

                continue

            #
            # =================================================
            # USER PART
            # =================================================
            #

            part = current_user.get(
                code
            )

            if part is None:

                continue

            #
            # Label.
            #

            part["Label"] = (
                item.text()
            )

            #
            # Type.
            #

            if type_combo is not None:

                role = (
                    type_combo.currentData()
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
            # Dimensions.
            #
            # IMPORTANT:
            #
            # For automatic Shelf / Divider we DO NOT read
            # the old table dimensions here.
            #
            # Otherwise the old values would overwrite the
            # freshly calculated values.
            #

            role = str(
                part.get(
                    "Role",
                    "Custom"
                )
            )

            position_mode = str(
                part.get(
                    "PositionMode",
                    "Automatic"
                )
            )

            if not (
                role in (
                    "Shelf",
                    "Divider"
                )
                and
                position_mode == "Automatic"
            ):

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

            #
            # Quantity.
            #

            part["Quantity"] = (
                self.getFloat(
                    row,
                    5
                )
            )

            #
            # Material.
            #

            if material_combo is not None:

                part["MaterialCode"] = (
                    material_combo.currentData()
                    or
                    ""
                )

            #
            # Position mode.
            #

            if mode_combo is not None:

                part["PositionMode"] = (
                    mode_combo.currentData()
                )

                part["PositionType"] = (
                    part["PositionMode"]
                )


    # =========================================================
    # MODE CHANGED
    # =========================================================

    def modeChanged(
        self,
        row
    ):

        if self._loading_table:

            return

        if row < 0:

            return

        if row >= len(
            self.parts
        ):

            return

        combo = self.table.cellWidget(
            row,
            7
        )

        if combo is None:

            return

        mode = (
            combo.currentData()
        )

        part_object = self.parts[
            row
        ]

        code = str(
            getattr(
                part_object,
                "Code",
                ""
            )
        )

        #
        # User part.
        #

        for user_part in self.userParts:

            if (
                str(
                    user_part.get(
                        "Code",
                        ""
                    )
                )
                ==
                code
            ):

                user_part[
                    "PositionMode"
                ] = mode

                if mode == "Automatic":

                    user_part[
                        "PositionType"
                    ] = "Automatic"

                break

        #
        # Recalculate.
        #

        self.calculateParts()


    # =========================================================
    # PART PLACEMENT DATA
    # =========================================================

    def partPlacementData(
        self,
        part
    ):

        placement = getattr(
            part,
            "Placement",
            FreeCAD.Placement()
        )

        return {

            "PositionX":
                self.value(
                    placement.Base.x
                ),

            "PositionY":
                self.value(
                    placement.Base.y
                ),

            "PositionZ":
                self.value(
                    placement.Base.z
                ),

            "RotationX":
                0,

            "RotationY":
                0,

            "RotationZ":
                0

        }


    # =========================================================
    # EDIT PLACEMENT
    # =========================================================

    def editPlacement(
        self
    ):

        row = self.table.currentRow()

        if row < 0:

            return

        if row >= len(
            self.parts
        ):

            return

        part = self.parts[
            row
        ]

        code = str(
            getattr(
                part,
                "Code",
                ""
            )
        )

        structural_codes = {

            "LS",
            "RS",
            "BT",
            "TP",
            "BK"

        }

        beam = (
            code.startswith(
                "TT"
            )
            or
            code.startswith(
                "TB"
            )
        )

        structural = (
            code in structural_codes
            or
            beam
        )

        #
        # Fixed structural pieces.
        #

        if structural and not beam:

            QtWidgets.QMessageBox.information(
                self,
                "Posición / giro",
                "Esta pieza estructural se posiciona automáticamente."
            )

            return

        #
        # Current placement.
        #

        placement = getattr(
            part,
            "Placement",
            FreeCAD.Placement()
        )

        data = {

            "PositionX":
                self.value(
                    placement.Base.x
                ),

            "PositionY":
                self.value(
                    placement.Base.y
                ),

            "PositionZ":
                self.value(
                    placement.Base.z
                ),

            "RotationX":
                0,

            "RotationY":
                0,

            "RotationZ":
                0

        }

        #
        # Structural beam placement.
        #

        if code in self.structuralPlacements:

            data.update(
                self.structuralPlacements[
                    code
                ]
            )

        #
        # User part placement.
        #

        if not structural:

            for user_part in self.userParts:

                if (
                    user_part.get(
                        "Code"
                    )
                    ==
                    code
                ):

                    for key in (
                        "PositionX",
                        "PositionY",
                        "PositionZ",
                        "RotationX",
                        "RotationY",
                        "RotationZ"
                    ):

                        data[key] = (
                            user_part.get(
                                key,
                                data[key]
                            )
                        )

                    break

        dialog = ManualPlacementDialog(
            data,
            self
        )

        if not dialog.exec_():

            return

        placement_data = (
            dialog.getData()
        )

        #
        # Beam.
        #

        if beam:

            self.structuralPlacements[
                code
            ] = placement_data

            mode_combo = (
                self.table.cellWidget(
                    row,
                    7
                )
            )

            if mode_combo is not None:

                index = (
                    mode_combo.findData(
                        "Manual"
                    )
                )

                if index >= 0:

                    mode_combo.setCurrentIndex(
                        index
                    )

        #
        # User piece.
        #

        else:

            for user_part in self.userParts:

                if (
                    user_part.get(
                        "Code"
                    )
                    ==
                    code
                ):

                    user_part.update(
                        placement_data
                    )

                    user_part[
                        "PositionMode"
                    ] = "Manual"

                    user_part[
                        "PositionType"
                    ] = "Manual"

                    break

        self.calculateParts()


    # =========================================================
    # ADD CUSTOM PART
    # =========================================================

    def addCustomPart(
        self
    ):

        self.updateTableData()

        used = {

            str(
                part.get(
                    "Code",
                    ""
                )
            )

            for part in self.userParts

        }

        number = 1

        while (
            "CU"
            +
            str(
                number
            )
            in used
        ):

            number += 1

        internal_width = (

            self.widthSpin.value()
            -
            self.thicknessSpin.value()
            *
            2

        )

        if internal_width < 0:

            internal_width = 0

        part = {

            "Code":
                "CU"
                +
                str(
                    number
                ),

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
                internal_width,

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

            "PositionMode":
                "Manual",

            "PositionType":
                "Manual"

        }

        self.userParts.append(
            part
        )

        self.calculateParts()

        if self.table.rowCount() > 0:

            self.table.selectRow(
                self.table.rowCount() - 1
            )


    # =========================================================
    # DELETE PART
    # =========================================================

    def deletePart(
        self
    ):

        row = self.table.currentRow()

        if row < 0:

            return

        if row >= len(
            self.parts
        ):

            return

        code = str(
            getattr(
                self.parts[row],
                "Code",
                ""
            )
        )

        if code in {

            "LS",
            "RS",
            "BT",
            "TP",
            "BK",
            "TT1",
            "TT2",
            "TT3",
            "TB1",
            "TB2",
            "TB3"

        }:

            QtWidgets.QMessageBox.information(
                self,
                "Eliminar pieza",
                "Las piezas estructurales no se pueden eliminar."
            )

            return

        self.userParts = [

            part

            for part in self.userParts

            if part.get(
                "Code"
            )
            !=
            code

        ]

        self.calculateParts()


    # =========================================================
    # DUPLICATE PART
    # =========================================================

    def duplicatePart(
        self
    ):

        row = self.table.currentRow()

        if row < 0:

            return

        if row >= len(
            self.parts
        ):

            return

        code = str(
            getattr(
                self.parts[row],
                "Code",
                ""
            )
        )

        source = None

        for part in self.userParts:

            if (
                part.get(
                    "Code"
                )
                ==
                code
            ):

                source = dict(
                    part
                )

                break

        if source is None:

            return

        used = {

            str(
                part.get(
                    "Code",
                    ""
                )
            )

            for part in self.userParts

        }

        number = 1

        while (
            "CU"
            +
            str(
                number
            )
            in used
        ):

            number += 1

        source["Code"] = (
            "CU"
            +
            str(
                number
            )
        )

        source["Label"] = (
            "Nueva pieza "
            +
            str(
                number
            )
        )

        self.userParts.append(
            source
        )

        self.calculateParts()


    # =========================================================
    # SAVE
    # =========================================================

    def save(
        self
    ):

        try:

            #
            # Preserve current table information.
            #

            self.updateTableData()

            #
            # Recalculate automatic positions.
            #

            self.recalculateAutomaticUserPartPositions()

            #
            # Recalculate automatic dimensions.
            #

            self.recalculateAutomaticUserPartDimensions()

            #
            # Save module.
            #

            self.updateModule()

            #
            # Final build.
            #

            self.calculateParts()

            #
            # Preserve material selections.
            #

            self.updateTableData()

            self.accept()

        except Exception as error:

            QtWidgets.QMessageBox.warning(
                self,
                "Guardar",
                "Error guardando el módulo:\n\n"
                +
                str(error)
            )


    # =========================================================
    # TABLE ITEM
    # =========================================================

    def setItem(
        self,
        row,
        column,
        value
    ):

        self.table.setItem(
            row,
            column,
            QtWidgets.QTableWidgetItem(
                str(
                    value
                )
            )
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


    # =========================================================
    # VALUE
    # =========================================================

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

            return 0.0


    # =========================================================
    # NUMBER
    # =========================================================

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


    # =========================================================
    # SET COMBO
    # =========================================================

    def setCombo(
        self,
        combo,
        value
    ):

        index = combo.findText(
            str(
                value
            )
        )

        if index >= 0:

            combo.setCurrentIndex(
                index
            )


    # =========================================================
    # RESIZE COLUMNS
    # =========================================================

    def resizeColumns(
        self
    ):

        self.table.resizeColumnsToContents()

        widths = {

            0: 190,
            1: 130,
            2: 90,
            3: 90,
            4: 90,
            5: 80,
            6: 200,
            7: 120

        }

        for column, width in widths.items():

            self.table.setColumnWidth(
                column,
                width
            )