import FreeCAD
from PySide import QtWidgets, QtCore


# =============================================================
# MANUAL PLACEMENT DIALOG
# =============================================================

class ManualPlacementDialog(
    QtWidgets.QDialog
):

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

    # =========================================================
    # ANGLE SPIN BOX
    # =========================================================

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
    # FLOAT
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
# PART TABLE DIALOG
# =============================================================

class PartTableDialog(
    QtWidgets.QDialog
):

    #
    # Structural codes generated by ModuleBuilder.
    #

    STRUCTURAL_CODES = {

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

        #
        # Source of module.
        #
        # Parametric:
        #     normal ModuleBuilder workflow.
        #
        # Imported:
        #     real FreeCAD objects.
        #

        self.moduleSource = self.getModuleSource()

        #
        # User parts for parametric modules.
        #

        self.userParts = []

        #
        # Manual structural placements.
        #

        self.structuralPlacements = {}

        #
        # Current real/generated parts.
        #

        self.parts = []

        if parts:

            self.parts = list(
                parts
            )

        #
        # Prevent recursive updates.
        #

        self._loading_table = False

        #
        # Prevent recursive imported updates.
        #

        self._updating_imported = False

        self.setWindowTitle(
            "Tabla de piezas"
        )

        self.resize(
            1250,
            750
        )

        self.createUI()

        self.loadModule()

        #
        # Imported modules must NEVER be rebuilt.
        #

        if self.isImported():

            self.loadImportedParts()

        else:

            self.calculateParts()

    # =========================================================
    # MODULE SOURCE
    # =========================================================

    def getModuleSource(
        self
    ):

        if self.module is None:

            return "Parametric"

        try:

            source = getattr(
                self.module,
                "ModuleSource",
                "Parametric"
            )

            return str(
                source
            ).strip()

        except Exception:

            return "Parametric"

    def isImported(
        self
    ):

        return (
            self.moduleSource.lower()
            ==
            "imported"
        )

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

        for label, widget, row, column in fields:

            module_layout.addWidget(
                QtWidgets.QLabel(
                    label
                ),
                row,
                column
            )

            module_layout.addWidget(
                widget,
                row,
                column + 1
            )

        #
        # TOP TYPE
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
        # BACK TYPE
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

        #
        # 8 COLUMNS
        #
        # 0 Pieza
        # 1 Tipo
        # 2 Largo
        # 3 Ancho
        # 4 Espesor
        # 5 Cantidad
        # 6 Material
        # 7 Modo
        #

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
            self.onStructureChanged
        )

        self.backTypeCombo.currentIndexChanged.connect(
            self.onStructureChanged
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
    # MODULE DATA
    # =========================================================

    def loadModule(
        self
    ):

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
        # NAME
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
        # DIMENSIONS
        #

        self.widthSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "Width",
                    600
                )
            )
        )

        self.heightSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "Height",
                    720
                )
            )
        )

        self.depthSpin.setValue(
            self.value(
                getattr(
                    self.module,
                    "Depth",
                    560
                )
            )
        )

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

        self.setCombo(
            self.topTypeCombo,
            getattr(
                self.module,
                "TopType",
                "Tapa completa"
            )
        )

        self.setCombo(
            self.backTypeCombo,
            getattr(
                self.module,
                "BackType",
                "Trasera sobrepuesta"
            )
        )

        #
        # PARAMETRIC USER PARTS
        #

        if not self.isImported():

            proxy = getattr(
                self.module,
                "Proxy",
                None
            )

            if proxy is not None:

                if hasattr(
                    proxy,
                    "getUserParts"
                ):

                    try:

                        self.userParts = [

                            dict(
                                item
                            )

                            for item in
                            proxy.getUserParts(
                                self.module
                            )

                        ]

                    except Exception:

                        self.userParts = []

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

    # =========================================================
    # MODULE STRUCTURE CHANGED
    # =========================================================

    def onStructureChanged(
        self,
        value
    ):

        if self._loading_table:

            return

        if self.isImported():

            return

        self.calculateParts()

    # =========================================================
    # UPDATE MODULE
    # =========================================================

    def updateModule(
        self
    ):

        if self.module is None:

            return

        try:

            self.module.ModuleName = (
                self.nameEdit.text().strip()
                or
                "Nuevo módulo"
            )

        except Exception:

            pass

        try:

            self.module.Label = (
                self.module.ModuleName
            )

        except Exception:

            pass

        #
        # Dimensions.
        #

        for name, widget in (
            (
                "Width",
                self.widthSpin
            ),
            (
                "Height",
                self.heightSpin
            ),
            (
                "Depth",
                self.depthSpin
            ),
            (
                "PanelThickness",
                self.thicknessSpin
            ),
            (
                "BackThickness",
                self.backThicknessSpin
            ),
            (
                "BackInset",
                self.backInsetSpin
            )
        ):

            if hasattr(
                self.module,
                name
            ):

                try:

                    setattr(
                        self.module,
                        name,
                        widget.value()
                    )

                except Exception:

                    pass

        #
        # Structure.
        #

        if hasattr(
            self.module,
            "TopType"
        ):

            try:

                self.module.TopType = (
                    self.topTypeCombo.currentText()
                )

            except Exception:

                pass

        if hasattr(
            self.module,
            "BackType"
        ):

            try:

                self.module.BackType = (
                    self.backTypeCombo.currentText()
                )

            except Exception:

                pass

        #
        # Parametric storage.
        #

        if self.isImported():

            return

        proxy = getattr(
            self.module,
            "Proxy",
            None
        )

        if proxy is None:

            return

        if hasattr(
            proxy,
            "setUserParts"
        ):

            try:

                proxy.setUserParts(
                    self.module,
                    self.userParts
                )

            except Exception:

                pass

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
    # CALCULATE
    # =========================================================

    def calculateParts(
        self
    ):

        #
        # =====================================================
        # IMPORTED
        # =====================================================
        #

        if self.isImported():

            self.updateTableData()

            self.recalculateImported()

            self.loadImportedParts()

            return

        #
        # =====================================================
        # PARAMETRIC
        # =====================================================
        #

        if self.module is None:

            return

        self.updateTableData()

        self.updateModule()

        #
        # Automatic positions.
        #

        self.recalculateAutomaticUserPartPositions()

        self.updateModule()

        #
        # ModuleBuilder.
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
        # Get real generated parts.
        #

        proxy = getattr(
            self.module,
            "Proxy",
            None
        )

        if proxy is None:

            self.parts = []

            return

        try:

            self.parts = list(
                proxy.getParts(
                    self.module
                )
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

            return

        self.loadTable()

    # =========================================================
    # IMPORTED PARTS
    # =========================================================

    def loadImportedParts(
        self
    ):

        if self.module is None:

            self.parts = []

            self.loadTable()

            return

        parts = []

        #
        # The imported module owns the real objects.
        #

        for child in getattr(
            self.module,
            "Group",
            []
        ):

            if child is self.module:

                continue

            if child is None:

                continue

            if not hasattr(
                child,
                "Placement"
            ):

                continue

            parts.append(
                child
            )

        self.parts = parts

        self.loadTable()

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
                # DATA
                #

                data = self.partToData(
                    part
                )

                #
                # LABEL
                #

                self.setItem(
                    row,
                    0,
                    data.get(
                        "Label",
                        ""
                    )
                )

                #
                # TYPE
                #

                type_combo = (
                    QtWidgets.QComboBox()
                )

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

                role = data.get(
                    "Role",
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

                index = type_combo.findData(
                    type_role
                )

                if index < 0:

                    index = (
                        type_combo.findData(
                            "Custom"
                        )
                    )

                if index >= 0:

                    type_combo.setCurrentIndex(
                        index
                    )

                #
                # Structural pieces are locked.
                #

                structural = (
                    self.isStructuralPart(
                        part
                    )
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
                # DIMENSIONS
                #

                self.setItem(
                    row,
                    2,
                    self.number(
                        data.get(
                            "Length",
                            0
                        )
                    )
                )

                self.setItem(
                    row,
                    3,
                    self.number(
                        data.get(
                            "Width",
                            0
                        )
                    )
                )

                self.setItem(
                    row,
                    4,
                    self.number(
                        data.get(
                            "Thickness",
                            0
                        )
                    )
                )

                self.setItem(
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

                material_combo = (
                    self.createMaterialCombo(
                        data.get(
                            "MaterialCode",
                            ""
                        )
                    )
                )

                material_combo.setEnabled(
                    not structural
                )

                self.table.setCellWidget(
                    row,
                    6,
                    material_combo
                )

                #
                # MODE
                #

                mode_combo = (
                    QtWidgets.QComboBox()
                )

                mode_combo.addItem(
                    "Automática",
                    "Automatic"
                )

                mode_combo.addItem(
                    "Manual",
                    "Manual"
                )

                mode = data.get(
                    "PositionMode",
                    "Automatic"
                )

                index = mode_combo.findData(
                    mode
                )

                if index < 0:

                    index = 0

                mode_combo.setCurrentIndex(
                    index
                )

                if self.isImported():

                    mode_combo.setEnabled(
                        True
                    )

                else:

                    mode_combo.setEnabled(
                        not structural
                        or
                        self.isBeam(part)
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
    # PART -> DATA
    # =========================================================

    def partToData(
        self,
        part
    ):

        data = {}

        #
        # Basic properties.
        #

        for name in (
            "Code",
            "Label",
            "Role",
            "PartType",
            "Length",
            "Width",
            "Thickness",
            "Quantity",
            "MaterialCode",
            "Position",
            "PositionX",
            "PositionY",
            "PositionZ",
            "RotationX",
            "RotationY",
            "RotationZ",
            "PositionType",
            "PositionMode"
        ):

            try:

                if hasattr(
                    part,
                    name
                ):

                    value = getattr(
                        part,
                        name
                    )

                    if hasattr(
                        value,
                        "Value"
                    ):

                        value = float(
                            value.Value
                        )

                    data[name] = value

            except Exception:

                pass

        #
        # Defaults.
        #

        data.setdefault(
            "Label",
            getattr(
                part,
                "Label",
                ""
            )
        )

        data.setdefault(
            "Code",
            getattr(
                part,
                "Name",
                ""
            )
        )

        data.setdefault(
            "Role",
            "Custom"
        )

        data.setdefault(
            "PartType",
            "Personalizado"
        )

        data.setdefault(
            "Length",
            0
        )

        data.setdefault(
            "Width",
            0
        )

        data.setdefault(
            "Thickness",
            0
        )

        data.setdefault(
            "Quantity",
            1
        )

        data.setdefault(
            "MaterialCode",
            ""
        )

        #
        # Placement.
        #

        try:

            placement = part.Placement

            data["PositionX"] = (
                float(
                    placement.Base.x
                )
            )

            data["PositionY"] = (
                float(
                    placement.Base.y
                )
            )

            data["PositionZ"] = (
                float(
                    placement.Base.z
                )
            )

            #
            # Keep explicit rotation properties
            # if they exist.
            #

            if hasattr(
                part,
                "RotationX"
            ):

                data["RotationX"] = (
                    self.value(
                        part.RotationX
                    )
                )

            else:

                data.setdefault(
                    "RotationX",
                    0
                )

            if hasattr(
                part,
                "RotationY"
            ):

                data["RotationY"] = (
                    self.value(
                        part.RotationY
                    )
                )

            else:

                data.setdefault(
                    "RotationY",
                    0
                )

            if hasattr(
                part,
                "RotationZ"
            ):

                data["RotationZ"] = (
                    self.value(
                        part.RotationZ
                    )
                )

            else:

                data.setdefault(
                    "RotationZ",
                    0
                )

            data.setdefault(
                "PositionType",
                "Manual"
            )

            data.setdefault(
                "PositionMode",
                "Manual"
            )

        except Exception:

            data.setdefault(
                "PositionX",
                0
            )

            data.setdefault(
                "PositionY",
                0
            )

            data.setdefault(
                "PositionZ",
                0
            )

            data.setdefault(
                "RotationX",
                0
            )

            data.setdefault(
                "RotationY",
                0
            )

            data.setdefault(
                "RotationZ",
                0
            )

            data.setdefault(
                "PositionMode",
                "Manual"
            )

        return data

    # =========================================================
    # TABLE -> DATA
    # =========================================================

    def updateTableData(
        self
    ):

        if self._loading_table:

            return

        if self.isImported():

            self.updateImportedTableData()

            return

        #
        # Parametric.
        #
        # There is no Position column anymore.
        # Position data is handled by PositionMode
        # and the Placement dialog.
        #

        for row in range(
            self.table.rowCount()
        ):

            if row >= len(
                self.parts
            ):

                continue

            #
            # First structural rows.
            #

            if row < 5:

                continue

            userIndex = row - 5

            if userIndex < 0:

                continue

            if userIndex >= len(
                self.userParts
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
                    item.text().strip()
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
            # TYPE
            #

            type_combo = (
                self.table.cellWidget(
                    row,
                    1
                )
            )

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

                elif role == "Custom":

                    part["PartType"] = (
                        "Personalizado"
                    )

                else:

                    part["PartType"] = (
                        "Estructural"
                    )

            #
            # MATERIAL
            #

            material_combo = (
                self.table.cellWidget(
                    row,
                    6
                )
            )

            if material_combo is not None:

                part["MaterialCode"] = (
                    material_combo.currentData()
                    or
                    ""
                )

            #
            # MODE
            #

            mode_combo = (
                self.table.cellWidget(
                    row,
                    7
                )
            )

            if mode_combo is not None:

                part["PositionMode"] = (
                    mode_combo.currentData()
                )

                #
                # Keep PositionType internally
                # for compatibility with old data.
                #

                if (
                    part["PositionMode"]
                    ==
                    "Automatic"
                ):

                    part["PositionType"] = (
                        "Automatic"
                    )

    # =========================================================
    # UPDATE IMPORTED TABLE
    # =========================================================

    def updateImportedTableData(
        self
    ):

        if self._updating_imported:

            return

        self._updating_imported = True

        try:

            for row, part in enumerate(
                self.parts
            ):

                if row >= self.table.rowCount():

                    continue

                data = {}

                #
                # LABEL
                #

                item = self.table.item(
                    row,
                    0
                )

                if item is not None:

                    data["Label"] = (
                        item.text().strip()
                    )

                #
                # DIMENSIONS
                #

                data["Length"] = (
                    self.getFloat(
                        row,
                        2
                    )
                )

                data["Width"] = (
                    self.getFloat(
                        row,
                        3
                    )
                )

                data["Thickness"] = (
                    self.getFloat(
                        row,
                        4
                    )
                )

                data["Quantity"] = (
                    self.getFloat(
                        row,
                        5
                    )
                )

                #
                # TYPE
                #

                type_combo = (
                    self.table.cellWidget(
                        row,
                        1
                    )
                )

                if type_combo is not None:

                    data["Role"] = (
                        type_combo.currentData()
                    )

                #
                # MATERIAL
                #

                material_combo = (
                    self.table.cellWidget(
                        row,
                        6
                    )
                )

                if material_combo is not None:

                    data["MaterialCode"] = (
                        material_combo.currentData()
                        or
                        ""
                    )

                #
                # MODE
                #

                mode_combo = (
                    self.table.cellWidget(
                        row,
                        7
                    )
                )

                if mode_combo is not None:

                    data["PositionMode"] = (
                        mode_combo.currentData()
                    )

                    if (
                        data["PositionMode"]
                        ==
                        "Automatic"
                    ):

                        data["PositionType"] = (
                            "Automatic"
                        )

                self.applyImportedPartData(
                    part,
                    data
                )

        finally:

            self._updating_imported = False

    # =========================================================
    # APPLY IMPORTED PART DATA
    # =========================================================

    def applyImportedPartData(
        self,
        part,
        data
    ):

        #
        # Label.
        #

        if "Label" in data:

            try:

                part.Label = (
                    data["Label"]
                )

            except Exception:

                pass

        #
        # Dimensions.
        #

        for name in (
            "Length",
            "Width",
            "Thickness",
            "Quantity",
            "MaterialCode"
        ):

            if name not in data:

                continue

            if not hasattr(
                part,
                name
            ):

                continue

            try:

                setattr(
                    part,
                    name,
                    data[name]
                )

            except Exception:

                pass

        #
        # Role.
        #

        role = data.get(
            "Role"
        )

        if role is not None:

            if hasattr(
                part,
                "Role"
            ):

                try:

                    part.Role = role

                except Exception:

                    pass

        #
        # Position metadata.
        #

        for name in (
            "PositionType",
            "PositionMode"
        ):

            if name not in data:

                continue

            if hasattr(
                part,
                name
            ):

                try:

                    setattr(
                        part,
                        name,
                        data[name]
                    )

                except Exception:

                    pass

        #
        # Recompute object.
        #

        try:

            part.touch()

        except Exception:

            pass

    # =========================================================
    # AUTOMATIC POSITIONS
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

                part["PositionX"] = (
                    panelThickness
                )

                part["PositionY"] = 0

                part["PositionZ"] = z

                part["RotationX"] = 0
                part["RotationY"] = 0
                part["RotationZ"] = 0

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

                part["PositionX"] = x

                part["PositionY"] = 0

                part["PositionZ"] = (
                    panelThickness
                )

                part["RotationX"] = 0
                part["RotationY"] = 0
                part["RotationZ"] = 0

                part["PositionType"] = (
                    "Automatic"
                )

                part["PositionMode"] = (
                    "Automatic"
                )

    # =========================================================
    # TYPE CHANGED
    # =========================================================

    def typeChanged(
        self,
        userIndex
    ):

        if self._loading_table:

            return

        if self.isImported():

            self.updateImportedTableData()

            return

        if userIndex < 0:

            return

        if userIndex >= len(
            self.userParts
        ):

            return

        row = userIndex + 5

        combo = self.table.cellWidget(
            row,
            1
        )

        if combo is None:

            return

        role = combo.currentData()

        part = self.userParts[
            userIndex
        ]

        part["Role"] = role

        if role == "Shelf":

            part["PartType"] = "Balda"
            part["PositionMode"] = "Automatic"
            part["PositionType"] = "Automatic"

        elif role == "Divider":

            part["PartType"] = "Separador"
            part["PositionMode"] = "Automatic"
            part["PositionType"] = "Automatic"

        elif role == "Custom":

            part["PartType"] = "Personalizado"

        else:

            part["PartType"] = "Estructural"

        self.calculateParts()

    # =========================================================
    # MODE CHANGED
    # =========================================================

    def modeChanged(
        self,
        userIndex
    ):

        if self._loading_table:

            return

        if self.isImported():

            self.updateImportedTableData()

            return

        if userIndex < 0:

            return

        if userIndex >= len(
            self.userParts
        ):

            return

        row = userIndex + 5

        combo = self.table.cellWidget(
            row,
            7
        )

        if combo is None:

            return

        mode = combo.currentData()

        part = self.userParts[
            userIndex
        ]

        part["PositionMode"] = mode

        if mode == "Automatic":

            part["PositionType"] = (
                "Automatic"
            )

        else:

            part["PositionType"] = (
                "Manual"
            )

        self.calculateParts()

    # =========================================================
    # MATERIAL CHANGED
    # =========================================================

    def materialChanged(
        self,
        userIndex
    ):

        if self._loading_table:

            return

        if self.isImported():

            self.updateImportedTableData()

            return

        if userIndex < 0:

            return

        if userIndex >= len(
            self.userParts
        ):

            return

        row = userIndex + 5

        combo = self.table.cellWidget(
            row,
            6
        )

        if combo is not None:

            self.userParts[
                userIndex
            ]["MaterialCode"] = (
                combo.currentData()
                or
                ""
            )

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

        return combo

    # =========================================================
    # ADD CUSTOM PART
    # =========================================================

    def addCustomPart(
        self
    ):

        #
        # =====================================================
        # IMPORTED
        # =====================================================
        #

        if self.isImported():

            self.addImportedPart()

            return

        #
        # =====================================================
        # PARAMETRIC
        # =====================================================
        #

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
            str(number)
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
                self.table.rowCount()
                -
                1
            )

    # =========================================================
    # ADD IMPORTED PART
    # =========================================================

    def addImportedPart(
        self
    ):

        if self.module is None:

            return

        document = (
            self.module.Document
        )

        if document is None:

            return

        try:

            from objects.bosqo_part import (
                create_part
            )

        except Exception as error:

            QtWidgets.QMessageBox.warning(
                self,
                "Añadir pieza",
                "No se pudo importar el creador de piezas:\n"
                +
                str(error)
            )

            return

        try:

            part = create_part(
                document
            )

        except Exception:

            try:

                part = document.addObject(
                    "Part::FeaturePython",
                    "BosqoPart"
                )

            except Exception as error:

                QtWidgets.QMessageBox.warning(
                    self,
                    "Añadir pieza",
                    "No se pudo crear la pieza:\n"
                    +
                    str(error)
                )

                return

        #
        # Properties.
        #

        defaults = {

            "Code":
                self.nextImportedCode(),

            "Label":
                "Nueva pieza",

            "Role":
                "Custom",

            "PartType":
                "Personalizado",

            "Length":
                max(
                    0,
                    self.widthSpin.value()
                    -
                    self.thicknessSpin.value()
                    *
                    2
                ),

            "Width":
                self.depthSpin.value(),

            "Thickness":
                self.thicknessSpin.value(),

            "Quantity":
                1,

            "MaterialCode":
                "",

            "PositionMode":
                "Manual",

            "PositionType":
                "Manual"

        }

        for name, value in defaults.items():

            if not hasattr(
                part,
                name
            ):

                continue

            try:

                setattr(
                    part,
                    name,
                    value
                )

            except Exception:

                pass

        #
        # Add to module.
        #

        try:

            self.module.addObject(
                part
            )

        except Exception:

            pass

        try:

            document.recompute()

        except Exception:

            pass

        self.loadImportedParts()

        row = (
            self.table.rowCount()
            -
            1
        )

        if row >= 0:

            self.table.selectRow(
                row
            )

            self.table.setCurrentCell(
                row,
                0
            )

            item = self.table.item(
                row,
                0
            )

            if item is not None:

                self.table.editItem(
                    item
                )

    # =========================================================
    # DELETE
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

        part = self.parts[
            row
        ]

        #
        # =====================================================
        # IMPORTED
        # =====================================================
        #

        if self.isImported():

            result = (
                QtWidgets.QMessageBox.question(
                    self,
                    "Eliminar pieza",
                    "¿Seguro que quieres eliminar "
                    "la pieza seleccionada?",
                    QtWidgets.QMessageBox.StandardButton.Yes
                    |
                    QtWidgets.QMessageBox.StandardButton.No
                )
            )

            if (
                result
                !=
                QtWidgets.QMessageBox.StandardButton.Yes
            ):

                return

            self.deleteImportedPart(
                part
            )

            return

        #
        # =====================================================
        # PARAMETRIC
        # =====================================================
        #

        code = str(
            getattr(
                part,
                "Code",
                ""
            )
        )

        if code in self.STRUCTURAL_CODES:

            QtWidgets.QMessageBox.information(
                self,
                "Eliminar pieza",
                "Las piezas estructurales no se pueden eliminar."
            )

            return

        self.userParts = [

            user_part

            for user_part in self.userParts

            if user_part.get(
                "Code"
            )
            !=
            code

        ]

        self.calculateParts()

    # =========================================================
    # DELETE IMPORTED
    # =========================================================

    def deleteImportedPart(
        self,
        part
    ):

        document = (
            getattr(
                part,
                "Document",
                None
            )
        )

        if document is None:

            return

        try:

            document.removeObject(
                part.Name
            )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error eliminando pieza importada: "
                +
                str(error)
                +
                "\n"
            )

            return

        try:

            document.recompute()

        except Exception:

            pass

        self.loadImportedParts()

    # =========================================================
    # DUPLICATE
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

        #
        # =====================================================
        # IMPORTED
        # =====================================================
        #

        if self.isImported():

            self.duplicateImportedPart(
                self.parts[row]
            )

            return

        #
        # =====================================================
        # PARAMETRIC
        # =====================================================
        #

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

            QtWidgets.QMessageBox.information(
                self,
                "Duplicar pieza",
                "Selecciona una pieza añadida por el usuario."
            )

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
            str(number)
            in used
        ):

            number += 1

        source["Code"] = (
            "CU"
            +
            str(number)
        )

        source["Label"] = (
            "Nueva pieza "
            +
            str(number)
        )

        self.userParts.append(
            source
        )

        self.calculateParts()

    # =========================================================
    # DUPLICATE IMPORTED
    # =========================================================

    def duplicateImportedPart(
        self,
        source
    ):

        document = (
            getattr(
                source,
                "Document",
                None
            )
        )

        if document is None:

            return

        #
        # Create new object.
        #

        try:

            from objects.bosqo_part import (
                create_part
            )

            new_part = create_part(
                document
            )

        except Exception:

            try:

                new_part = document.addObject(
                    "Part::FeaturePython",
                    "BosqoPart"
                )

            except Exception as error:

                QtWidgets.QMessageBox.warning(
                    self,
                    "Duplicar pieza",
                    "No se pudo crear la copia:\n"
                    +
                    str(error)
                )

                return

        #
        # Copy properties.
        #

        properties = (

            "Code",
            "Role",
            "PartType",
            "Length",
            "Width",
            "Thickness",
            "Quantity",
            "MaterialCode",
            "Position",
            "PositionX",
            "PositionY",
            "PositionZ",
            "RotationX",
            "RotationY",
            "RotationZ",
            "PositionType",
            "PositionMode"
        )

        for name in properties:

            if not hasattr(
                source,
                name
            ):

                continue

            if not hasattr(
                new_part,
                name
            ):

                continue

            try:

                setattr(
                    new_part,
                    name,
                    getattr(
                        source,
                        name
                    )
                )

            except Exception:

                pass

        #
        # New code.
        #

        try:

            new_part.Code = (
                self.nextImportedCode()
            )

        except Exception:

            pass

        try:

            new_part.Label = (
                str(
                    getattr(
                        source,
                        "Label",
                        "Nueva pieza"
                    )
                )
                +
                " copia"
            )

        except Exception:

            pass

        #
        # Copy Shape when available.
        #

        try:

            if hasattr(
                source,
                "Shape"
            ):

                new_part.Shape = (
                    source.Shape.copy()
                )

        except Exception:

            pass

        #
        # Copy Placement.
        #

        try:

            new_part.Placement = (
                source.Placement
            )

        except Exception:

            pass

        #
        # Add to module.
        #

        try:

            self.module.addObject(
                new_part
            )

        except Exception:

            pass

        try:

            document.recompute()

        except Exception:

            pass

        self.loadImportedParts()

    # =========================================================
    # NEXT IMPORTED CODE
    # =========================================================

    def nextImportedCode(
        self
    ):

        used = set()

        for part in self.parts:

            code = str(
                getattr(
                    part,
                    "Code",
                    ""
                )
            )

            if code.startswith(
                "CU"
            ):

                try:

                    used.add(
                        int(
                            code[2:]
                        )
                    )

                except Exception:

                    pass

        number = 1

        while number in used:

            number += 1

        return (
            "CU"
            +
            str(
                number
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

        if row >= len(
            self.parts
        ):

            return

        part = self.parts[
            row
        ]

        #
        # =====================================================
        # IMPORTED
        # =====================================================
        #
        # All real objects are editable.
        #

        if self.isImported():

            data = self.partToData(
                part
            )

            dialog = ManualPlacementDialog(
                data,
                self
            )

            if not dialog.exec_():

                return

            placement_data = (
                dialog.getData()
            )

            self.applyPlacementToRealPart(
                part,
                placement_data
            )

            return

        #
        # =====================================================
        # PARAMETRIC
        # =====================================================
        #

        code = str(
            getattr(
                part,
                "Code",
                ""
            )
        )

        structural = (
            code
            in
            self.STRUCTURAL_CODES
        )

        beam = (
            code.startswith(
                "TT"
            )
            or
            code.startswith(
                "TB"
            )
        )

        if structural and not beam:

            QtWidgets.QMessageBox.information(
                self,
                "Posición / giro",
                "Esta pieza estructural se posiciona automáticamente."
            )

            return

        data = {

            "PositionX":
                self.value(
                    part.Placement.Base.x
                ),

            "PositionY":
                self.value(
                    part.Placement.Base.y
                ),

            "PositionZ":
                self.value(
                    part.Placement.Base.z
                ),

            "RotationX":
                0,

            "RotationY":
                0,

            "RotationZ":
                0

        }

        if code in (
            self.structuralPlacements
        ):

            data.update(
                self.structuralPlacements[
                    code
                ]
            )

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

        if beam:

            self.structuralPlacements[
                code
            ] = placement_data

            self.calculateParts()

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
    # APPLY REAL PLACEMENT
    # =========================================================

    def applyPlacementToRealPart(
        self,
        part,
        data
    ):

        try:

            x = float(
                data.get(
                    "PositionX",
                    0
                )
            )

            y = float(
                data.get(
                    "PositionY",
                    0
                )
            )

            z = float(
                data.get(
                    "PositionZ",
                    0
                )
            )

            rx = float(
                data.get(
                    "RotationX",
                    0
                )
            )

            ry = float(
                data.get(
                    "RotationY",
                    0
                )
            )

            rz = float(
                data.get(
                    "RotationZ",
                    0
                )
            )

            rotation = (

                FreeCAD.Rotation(
                    FreeCAD.Vector(
                        1,
                        0,
                        0
                    ),
                    rx
                )

                *

                FreeCAD.Rotation(
                    FreeCAD.Vector(
                        0,
                        1,
                        0
                    ),
                    ry
                )

                *

                FreeCAD.Rotation(
                    FreeCAD.Vector(
                        0,
                        0,
                        1
                    ),
                    rz
                )

            )

            part.Placement = (
                FreeCAD.Placement(
                    FreeCAD.Vector(
                        x,
                        y,
                        z
                    ),
                    rotation
                )
            )

            if hasattr(
                part,
                "PositionX"
            ):

                part.PositionX = x

            if hasattr(
                part,
                "PositionY"
            ):

                part.PositionY = y

            if hasattr(
                part,
                "PositionZ"
            ):

                part.PositionZ = z

            if hasattr(
                part,
                "RotationX"
            ):

                part.RotationX = rx

            if hasattr(
                part,
                "RotationY"
            ):

                part.RotationY = ry

            if hasattr(
                part,
                "RotationZ"
            ):

                part.RotationZ = rz

            if hasattr(
                part,
                "PositionMode"
            ):

                part.PositionMode = (
                    "Manual"
                )

            if hasattr(
                part,
                "PositionType"
            ):

                part.PositionType = (
                    "Manual"
                )

            part.touch()

            if part.Document is not None:

                part.Document.recompute()

            self.loadImportedParts()

            #
            # Restore selected row.
            #

            for row, current in enumerate(
                self.parts
            ):

                if current is part:

                    self.table.selectRow(
                        row
                    )

                    break

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error aplicando Placement: "
                +
                str(
                    error
                )
                +
                "\n"
            )

    # =========================================================
    # RECALCULATE IMPORTED
    # =========================================================

    def recalculateImported(
        self
    ):

        #
        # IMPORTANT:
        #
        # We DO NOT call ModuleBuilder.
        #

        self.updateImportedTableData()

        #
        # Automatic imported pieces.
        #

        for part in self.parts:

            try:

                mode = str(
                    getattr(
                        part,
                        "PositionMode",
                        "Manual"
                    )
                )

                role = str(
                    getattr(
                        part,
                        "Role",
                        "Custom"
                    )
                )

                if (
                    mode == "Automatic"
                    and
                    role == "Shelf"
                ):

                    z = (
                        self.getAutomaticShelfPosition(
                            part
                        )
                    )

                    self.setRealPosition(
                        part,
                        z=z
                    )

                elif (
                    mode == "Automatic"
                    and
                    role == "Divider"
                ):

                    x = (
                        self.getAutomaticDividerPosition(
                            part
                        )
                    )

                    self.setRealPosition(
                        part,
                        x=x
                    )

            except Exception:

                pass

        try:

            if self.module is not None:

                self.module.Document.recompute()

        except Exception:

            pass

    # =========================================================
    # AUTOMATIC IMPORTED SHELF
    # =========================================================

    def getAutomaticShelfPosition(
        self,
        part
    ):

        shelves = [

            current

            for current in self.parts

            if str(
                getattr(
                    current,
                    "Role",
                    ""
                )
            )
            ==
            "Shelf"

            and

            str(
                getattr(
                    current,
                    "PositionMode",
                    "Manual"
                )
            )
            ==
            "Automatic"

        ]

        if not shelves:

            return 0

        index = shelves.index(
            part
        )

        usableHeight = max(
            0,
            self.heightSpin.value()
            -
            self.thicknessSpin.value()
            *
            2
        )

        totalThickness = (
            self.thicknessSpin.value()
            *
            len(
                shelves
            )
        )

        freeHeight = max(
            0,
            usableHeight
            -
            totalThickness
        )

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

        return (

            self.thicknessSpin.value()

            +

            spacing
            *
            (
                index
                +
                1
            )

            +

            self.thicknessSpin.value()
            *
            index

        )

    # =========================================================
    # AUTOMATIC IMPORTED DIVIDER
    # =========================================================

    def getAutomaticDividerPosition(
        self,
        part
    ):

        dividers = [

            current

            for current in self.parts

            if str(
                getattr(
                    current,
                    "Role",
                    ""
                )
            )
            ==
            "Divider"

            and

            str(
                getattr(
                    current,
                    "PositionMode",
                    "Manual"
                )
            )
            ==
            "Automatic"

        ]

        if not dividers:

            return 0

        index = dividers.index(
            part
        )

        usableWidth = max(
            0,
            self.widthSpin.value()
            -
            self.thicknessSpin.value()
            *
            2
        )

        totalThickness = (
            self.thicknessSpin.value()
            *
            len(
                dividers
            )
        )

        freeWidth = max(
            0,
            usableWidth
            -
            totalThickness
        )

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

        return (

            self.thicknessSpin.value()

            +

            spacing
            *
            (
                index
                +
                1
            )

            +

            self.thicknessSpin.value()
            *
            index

        )

    # =========================================================
    # SET REAL POSITION
    # =========================================================

    def setRealPosition(
        self,
        part,
        x=None,
        z=None
    ):

        try:

            placement = (
                part.Placement
            )

            base = (
                placement.Base
            )

            if x is not None:

                base.x = float(
                    x
                )

            if z is not None:

                base.z = float(
                    z
                )

            part.Placement = (
                FreeCAD.Placement(
                    base,
                    placement.Rotation
                )
            )

            if x is not None:

                if hasattr(
                    part,
                    "PositionX"
                ):

                    part.PositionX = (
                        float(
                            x
                        )
                    )

                if hasattr(
                    part,
                    "Position"
                ):

                    part.Position = (
                        float(
                            x
                        )
                    )

            if z is not None:

                if hasattr(
                    part,
                    "PositionZ"
                ):

                    part.PositionZ = (
                        float(
                            z
                        )
                    )

                if hasattr(
                    part,
                    "Position"
                ):

                    part.Position = (
                        float(
                            z
                        )
                    )

            part.touch()

        except Exception:

            pass

    # =========================================================
    # STRUCTURAL
    # =========================================================

    def isStructuralPart(
        self,
        part
    ):

        code = str(
            getattr(
                part,
                "Code",
                ""
            )
        )

        if code in self.STRUCTURAL_CODES:

            return True

        role = str(
            getattr(
                part,
                "Role",
                ""
            )
        )

        return role in (
            "Side",
            "Bottom",
            "Top",
            "Back",
            "TopBeam",
            "BackBeam"
        )

    # =========================================================
    # BEAM
    # =========================================================

    def isBeam(
        self,
        part
    ):

        code = str(
            getattr(
                part,
                "Code",
                ""
            )
        )

        return (
            code.startswith(
                "TT"
            )
            or
            code.startswith(
                "TB"
            )
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save(
        self
    ):

        try:

            #
            # =================================================
            # IMPORTED
            # =================================================
            #

            if self.isImported():

                self.updateImportedTableData()

                self.recalculateImported()

                try:

                    self.module.Document.recompute()

                except Exception:

                    pass

                self.accept()

                return

            #
            # =================================================
            # PARAMETRIC
            # =================================================
            #

            self.updateTableData()

            self.updateModule()

            self.calculateParts()

            self.updateTableData()

            self.updateModule()

            self.accept()

        except Exception as error:

            QtWidgets.QMessageBox.warning(
                self,
                "Guardar",
                "Error guardando el módulo:\n\n"
                +
                str(
                    error
                )
            )

    # =========================================================
    # TABLE HELPERS
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
            7: 110

        }

        for column, width in widths.items():

            self.table.setColumnWidth(
                column,
                width
            )