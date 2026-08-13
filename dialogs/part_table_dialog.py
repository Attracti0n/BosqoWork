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

        super().__init__(parent)

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

        # -----------------------------------------------------
        # POSITION
        # -----------------------------------------------------

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
                QtWidgets.QLabel(label),
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

        # -----------------------------------------------------
        # ROTATION
        # -----------------------------------------------------

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
                QtWidgets.QLabel(label),
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

        # -----------------------------------------------------
        # BUTTONS
        # -----------------------------------------------------

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

    # ---------------------------------------------------------
    # SPINBOX
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # DATA
    # ---------------------------------------------------------

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

    def getData(
        self
    ):

        return {
            "PositionX": self.xSpin.value(),
            "PositionY": self.ySpin.value(),
            "PositionZ": self.zSpin.value(),
            "RotationX": self.rxSpin.value(),
            "RotationY": self.rySpin.value(),
            "RotationZ": self.rzSpin.value()
        }

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

class PartTableDialog(QtWidgets.QDialog):

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

        super().__init__(parent)

        self.module = module

        self.moduleSource = (
            self.getModuleSource()
        )

        self.userParts = []

        self.structuralPlacements = {}

        self.parts = list(
            parts or []
        )

        # -----------------------------------------------------
        # STATE GUARDS
        # -----------------------------------------------------

        self._loading_table = False
        self._updating_imported = False
        self._changing_type = False
        self._changing_material = False
        self._changing_mode = False
        self._recalculating_imported = False
        self._updating_module = False
        self._building = False

        self.setWindowTitle(
            "Tabla de piezas"
        )

        self.resize(
            1250,
            750
        )

        self.createUI()

        self.loadModule()

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

            return str(
                getattr(
                    self.module,
                    "ModuleSource",
                    "Parametric"
                )
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
    # UI
    # =========================================================

    def createUI(
        self
    ):

        main_layout = QtWidgets.QVBoxLayout(
            self
        )

        # -----------------------------------------------------
        # MODULE
        # -----------------------------------------------------

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
                QtWidgets.QLabel(label),
                row,
                column
            )

            module_layout.addWidget(
                widget,
                row,
                column + 1
            )

        # -----------------------------------------------------
        # TOP TYPE
        # -----------------------------------------------------

        self.topTypeCombo = QtWidgets.QComboBox()

        self.topTypeCombo.addItems(
            [
                "Tapa completa",
                "2 travesaños",
                "3 travesaños"
            ]
        )

        # -----------------------------------------------------
        # BACK TYPE
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # PART TABLE
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # PART BUTTONS
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # BOTTOM
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # CONNECTIONS
        # -----------------------------------------------------

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
            "getUserParts"
        ):

            try:

                self.userParts = [
                    dict(item)
                    for item in proxy.getUserParts(
                        self.module
                    )
                    if isinstance(
                        item,
                        dict
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
    # UPDATE MODULE
    # =========================================================

    def updateModule(
        self
    ):

        if self.module is None:
            return

        if self._updating_module:
            return

        self._updating_module = True

        try:

            name = (
                self.nameEdit.text().strip()
                or
                "Nuevo módulo"
            )

            if hasattr(
                self.module,
                "ModuleName"
            ):

                try:
                    self.module.ModuleName = name
                except Exception:
                    pass

            if hasattr(
                self.module,
                "Label"
            ):

                try:
                    self.module.Label = name
                except Exception:
                    pass

            for name, widget in (
                ("Width", self.widthSpin),
                ("Height", self.heightSpin),
                ("Depth", self.depthSpin),
                ("PanelThickness", self.thicknessSpin),
                ("BackThickness", self.backThicknessSpin),
                ("BackInset", self.backInsetSpin)
            ):

                if not hasattr(
                    self.module,
                    name
                ):
                    continue

                try:

                    setattr(
                        self.module,
                        name,
                        widget.value()
                    )

                except Exception:
                    pass

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

        finally:

            self._updating_module = False

    # =========================================================
    # SAVE USER PART DATA
    # =========================================================

    def persistUserParts(
        self
    ):

        if self.module is None:
            return

        proxy = getattr(
            self.module,
            "Proxy",
            None
        )

        if proxy is None:
            return

        if not hasattr(
            proxy,
            "setUserParts"
        ):

            return

        try:

            proxy.setUserParts(
                self.module,
                [
                    dict(item)
                    for item in self.userParts
                ]
            )

        except Exception:
            pass

    # =========================================================
    # SAVE STRUCTURAL PLACEMENTS
    # =========================================================

    def persistStructuralPlacements(
        self
    ):

        if self.module is None:
            return

        proxy = getattr(
            self.module,
            "Proxy",
            None
        )

        if proxy is None:
            return

        if not hasattr(
            proxy,
            "setStructuralPlacements"
        ):

            return

        try:

            proxy.setStructuralPlacements(
                self.module,
                dict(
                    self.structuralPlacements
                )
            )

        except Exception:
            pass

    # =========================================================
    # STRUCTURE
    # =========================================================

    def onStructureChanged(
        self,
        value
    ):

        if self._loading_table:
            return

        if self._building:
            return

        if self.isImported():
            return

        self.calculateParts()

    # =========================================================
    # IMPORTED PARTS
    # =========================================================

    def loadImportedParts(
        self
    ):

        if self._loading_table:
            return

        if self.module is None:

            self.parts = []

            self.loadTable()

            return

        parts = []

        for child in getattr(
            self.module,
            "Group",
            []
        ):

            if child is None:
                continue

            if child is self.module:
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
    # SAVED IMPORTED DATA
    # =========================================================

    def getSavedImportedPartData(
        self,
        part
    ):

        if not self.isImported():
            return {}

        proxy = getattr(
            self.module,
            "Proxy",
            None
        )

        if proxy is None:
            return {}

        if not hasattr(
            proxy,
            "getUserParts"
        ):

            return {}

        try:

            saved = proxy.getUserParts(
                self.module
            )

        except Exception:

            return {}

        object_name = str(
            getattr(
                part,
                "Name",
                ""
            )
        )

        label = str(
            getattr(
                part,
                "Label",
                ""
            )
        )

        for item in saved:

            if not isinstance(
                item,
                dict
            ):
                continue

            stored_name = str(
                item.get(
                    "ObjectName",
                    ""
                )
            )

            if (
                stored_name
                and
                stored_name == object_name
            ):

                return dict(item)

            stored_code = str(
                item.get(
                    "Code",
                    ""
                )
            )

            if (
                stored_code
                and
                stored_code == object_name
            ):

                return dict(item)

            stored_label = str(
                item.get(
                    "Name",
                    ""
                )
            )

            if (
                stored_label
                and
                stored_label == label
            ):

                return dict(item)

        return {}

    # =========================================================
    # LOAD TABLE
    # =========================================================

    def loadTable(
        self
    ):

        if self._loading_table:
            return

        self._loading_table = True

        try:

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

                data = self.partToData(
                    part
                )

                # ---------------------------------------------
                # LABEL
                # ---------------------------------------------

                self.setItem(
                    row,
                    0,
                    data.get(
                        "Label",
                        ""
                    )
                )

                # ---------------------------------------------
                # TYPE
                # ---------------------------------------------

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

                    role = "Structural"

                index = type_combo.findData(
                    role
                )

                if index < 0:

                    index = type_combo.findData(
                        "Custom"
                    )

                if index >= 0:

                    type_combo.setCurrentIndex(
                        index
                    )

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

                # ---------------------------------------------
                # DIMENSIONS
                # ---------------------------------------------

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

                # ---------------------------------------------
                # MATERIAL
                # ---------------------------------------------

                material_combo = (
                    self.createMaterialCombo(
                        data.get(
                            "MaterialCode",
                            ""
                        )
                    )
                )

                self.table.setCellWidget(
                    row,
                    6,
                    material_combo
                )

                # ---------------------------------------------
                # MODE
                # ---------------------------------------------

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
                    data.get(
                        "PositionMode",
                        "Automatic"
                    )
                )

                if mode not in (
                    "Automatic",
                    "Manual"
                ):

                    mode = "Automatic"

                index = mode_combo.findData(
                    mode
                )

                if index < 0:
                    index = 0

                mode_combo.setCurrentIndex(
                    index
                )

                mode_combo.setEnabled(
                    self.isImported()
                    or
                    not structural
                    or
                    self.isBeam(part)
                )

                self.table.setCellWidget(
                    row,
                    7,
                    mode_combo
                )

                # ---------------------------------------------
                # CONNECTIONS AFTER CREATION
                # ---------------------------------------------

                type_combo.currentIndexChanged.connect(
                    lambda index, r=row:
                    self.typeChanged(r)
                )

                material_combo.currentIndexChanged.connect(
                    lambda index, r=row:
                    self.materialChanged(r)
                )

                mode_combo.currentIndexChanged.connect(
                    lambda index, r=row:
                    self.modeChanged(r)
                )

            self.resizeColumns()

        finally:

            self.table.blockSignals(
                False
            )

            self._loading_table = False

    # =========================================================
    # PART -> DATA
    # =========================================================

    def partToData(
        self,
        part
    ):

        data = {}

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
            "Material",
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

            if not hasattr(
                part,
                name
            ):
                continue

            try:

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

        # -----------------------------------------------------
        # IMPORTED SAVED DATA
        # -----------------------------------------------------

        if self.isImported():

            saved = self.getSavedImportedPartData(
                part
            )

            if saved:

                if saved.get(
                    "Name",
                    ""
                ):

                    data["Label"] = str(
                        saved.get(
                            "Name"
                        )
                    )

                if saved.get(
                    "Type",
                    ""
                ):

                    saved_type = str(
                        saved.get(
                            "Type"
                        )
                    ).strip()

                    type_map = {
                        "Personalizado": "Custom",
                        "Personalizada": "Custom",
                        "Estructural": "Structural",
                        "Lateral": "Structural",
                        "Base": "Structural",
                        "Superior": "Structural",
                        "Trasera": "Structural",
                        "Balda": "Shelf",
                        "Separador": "Divider"
                    }

                    data["Role"] = type_map.get(
                        saved_type,
                        saved_type
                    )

                    data["PartType"] = (
                        saved_type
                    )

                for name in (
                    "Length",
                    "Width",
                    "Thickness",
                    "Quantity"
                ):

                    if name in saved:

                        data[name] = (
                            saved[name]
                        )

                if "Material" in saved:

                    data["MaterialCode"] = (
                        saved.get(
                            "Material",
                            ""
                        )
                    )

                elif "MaterialCode" in saved:

                    data["MaterialCode"] = (
                        saved.get(
                            "MaterialCode",
                            ""
                        )
                    )

                if not hasattr(
                    part,
                    "PositionMode"
                ):

                    data["PositionMode"] = (
                        saved.get(
                            "PositionMode",
                            "Manual"
                        )
                    )

        # -----------------------------------------------------
        # REAL PLACEMENT
        # -----------------------------------------------------

        try:

            placement = part.Placement

            data["PositionX"] = float(
                placement.Base.x
            )

            data["PositionY"] = float(
                placement.Base.y
            )

            data["PositionZ"] = float(
                placement.Base.z
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

        mode = str(
            data.get(
                "PositionMode",
                "Manual"
            )
        )

        if mode not in (
            "Automatic",
            "Manual"
        ):

            mode = "Manual"

        data["PositionMode"] = mode
        data["PositionType"] = mode

        return data

    # =========================================================
    # TABLE -> PARAMETRIC DATA
    # =========================================================

    def updateTableData(
        self
    ):

        if self._loading_table:
            return

        if self.isImported():
            return

        for row in range(
            self.table.rowCount()
        ):

            if row < 5:
                continue

            userIndex = row - 5

            if userIndex >= len(
                self.userParts
            ):
                continue

            part = self.userParts[
                userIndex
            ]

            item = self.table.item(
                row,
                0
            )

            if item is not None:

                part["Label"] = (
                    item.text().strip()
                )

            part["Length"] = self.getFloat(
                row,
                2
            )

            part["Width"] = self.getFloat(
                row,
                3
            )

            part["Thickness"] = self.getFloat(
                row,
                4
            )

            part["Quantity"] = self.getFloat(
                row,
                5
            )

            type_combo = self.table.cellWidget(
                row,
                1
            )

            if type_combo is not None:

                role = type_combo.currentData()

                part["Role"] = role

                if role == "Shelf":

                    part["PartType"] = "Balda"

                elif role == "Divider":

                    part["PartType"] = "Separador"

                elif role == "Custom":

                    part["PartType"] = "Personalizado"

                else:

                    part["PartType"] = "Estructural"

            material_combo = self.table.cellWidget(
                row,
                6
            )

            if material_combo is not None:

                part["MaterialCode"] = (
                    material_combo.currentData()
                    or
                    ""
                )

            mode_combo = self.table.cellWidget(
                row,
                7
            )

            if mode_combo is not None:

                mode = mode_combo.currentData()

                if mode not in (
                    "Automatic",
                    "Manual"
                ):

                    mode = "Manual"

                part["PositionMode"] = mode
                part["PositionType"] = mode

    # =========================================================
    # IMPORTED TABLE DATA
    # =========================================================

    def updateImportedTableData(
        self,
        preserveAutomaticDimensions=True
    ):

        if self._updating_imported:
            return

        if not self.isImported():
            return

        self._updating_imported = True

        try:

            proxy = getattr(
                self.module,
                "Proxy",
                None
            )

            if proxy is None:
                return

            if not hasattr(
                proxy,
                "getUserParts"
            ):

                return

            try:

                saved_parts = [
                    dict(item)
                    for item in proxy.getUserParts(
                        self.module
                    )
                    if isinstance(
                        item,
                        dict
                    )
                ]

            except Exception:

                saved_parts = []

            for row, part in enumerate(
                self.parts
            ):

                if row >= self.table.rowCount():
                    continue

                data = {}

                # ---------------------------------------------
                # NAME
                # ---------------------------------------------

                item = self.table.item(
                    row,
                    0
                )

                if item is not None:

                    data["Label"] = (
                        item.text().strip()
                    )

                # ---------------------------------------------
                # TYPE
                # ---------------------------------------------

                type_combo = self.table.cellWidget(
                    row,
                    1
                )

                if type_combo is not None:

                    role = type_combo.currentData()

                    data["Role"] = role

                    if role == "Shelf":

                        data["Type"] = "Balda"
                        data["PartType"] = "Balda"

                    elif role == "Divider":

                        data["Type"] = "Separador"
                        data["PartType"] = "Separador"

                    elif role == "Custom":

                        data["Type"] = "Personalizada"
                        data["PartType"] = "Personalizada"

                    else:

                        data["Type"] = "Estructural"
                        data["PartType"] = "Estructural"

                # ---------------------------------------------
                # MODE
                # ---------------------------------------------

                mode_combo = self.table.cellWidget(
                    row,
                    7
                )

                if mode_combo is not None:

                    mode = mode_combo.currentData()

                    if mode not in (
                        "Automatic",
                        "Manual"
                    ):

                        mode = "Manual"

                    data["PositionMode"] = mode
                    data["PositionType"] = mode

                # ---------------------------------------------
                # AUTOMATIC?
                # ---------------------------------------------

                automatic = (
                    data.get(
                        "PositionMode",
                        getattr(
                            part,
                            "PositionMode",
                            "Manual"
                        )
                    )
                    ==
                    "Automatic"
                )

                automatic_role = (
                    data.get(
                        "Role",
                        getattr(
                            part,
                            "Role",
                            "Custom"
                        )
                    )
                    in
                    (
                        "Shelf",
                        "Divider"
                    )
                )

                skip_dimensions = (
                    preserveAutomaticDimensions
                    and
                    automatic
                    and
                    automatic_role
                )

                # ---------------------------------------------
                # DIMENSIONS
                # ---------------------------------------------

                if not skip_dimensions:

                    data["Length"] = self.getFloat(
                        row,
                        2
                    )

                    data["Width"] = self.getFloat(
                        row,
                        3
                    )

                    data["Thickness"] = self.getFloat(
                        row,
                        4
                    )

                    data["Quantity"] = self.getFloat(
                        row,
                        5
                    )

                else:

                    data["Length"] = self.value(
                        getattr(
                            part,
                            "Length",
                            0
                        )
                    )

                    data["Width"] = self.value(
                        getattr(
                            part,
                            "Width",
                            0
                        )
                    )

                    data["Thickness"] = self.value(
                        getattr(
                            part,
                            "Thickness",
                            0
                        )
                    )

                    data["Quantity"] = self.value(
                        getattr(
                            part,
                            "Quantity",
                            1
                        )
                    )

                # ---------------------------------------------
                # MATERIAL
                # ---------------------------------------------

                material_combo = self.table.cellWidget(
                    row,
                    6
                )

                if material_combo is not None:

                    material = (
                        material_combo.currentData()
                        or
                        ""
                    )

                    data["Material"] = str(
                        material
                    )

                    data["MaterialCode"] = str(
                        material
                    )

                # ---------------------------------------------
                # APPLY TO REAL OBJECT
                # ---------------------------------------------

                apply_data = dict(
                    data
                )

                if skip_dimensions:

                    apply_data.pop(
                        "Length",
                        None
                    )

                    apply_data.pop(
                        "Width",
                        None
                    )

                    apply_data.pop(
                        "Thickness",
                        None
                    )

                self.applyImportedPartData(
                    part,
                    apply_data
                )

                # ---------------------------------------------
                # FIND SAVED RECORD
                # ---------------------------------------------

                object_name = str(
                    getattr(
                        part,
                        "Name",
                        ""
                    )
                )

                record = None

                for item in saved_parts:

                    if str(
                        item.get(
                            "ObjectName",
                            ""
                        )
                    ) == object_name:

                        record = item
                        break

                if record is None:

                    record = {
                        "ObjectName":
                            object_name
                    }

                    saved_parts.append(
                        record
                    )

                # ---------------------------------------------
                # RECORD
                # ---------------------------------------------

                record["Name"] = data.get(
                    "Label",
                    getattr(
                        part,
                        "Label",
                        ""
                    )
                )

                record["Type"] = data.get(
                    "Type",
                    "Personalizada"
                )

                record["Role"] = data.get(
                    "Role",
                    getattr(
                        part,
                        "Role",
                        "Custom"
                    )
                )

                record["PositionMode"] = data.get(
                    "PositionMode",
                    getattr(
                        part,
                        "PositionMode",
                        "Manual"
                    )
                )

                record["PositionType"] = data.get(
                    "PositionType",
                    record["PositionMode"]
                )

                record["Quantity"] = data.get(
                    "Quantity",
                    self.value(
                        getattr(
                            part,
                            "Quantity",
                            1
                        )
                    )
                )

                record["Material"] = data.get(
                    "Material",
                    ""
                )

                record["MaterialCode"] = data.get(
                    "MaterialCode",
                    ""
                )

                if not skip_dimensions:

                    record["Length"] = data.get(
                        "Length",
                        0
                    )

                    record["Width"] = data.get(
                        "Width",
                        0
                    )

                    record["Thickness"] = data.get(
                        "Thickness",
                        0
                    )

                else:

                    record["Length"] = self.value(
                        getattr(
                            part,
                            "Length",
                            0
                        )
                    )

                    record["Width"] = self.value(
                        getattr(
                            part,
                            "Width",
                            0
                        )
                    )

                    record["Thickness"] = self.value(
                        getattr(
                            part,
                            "Thickness",
                            0
                        )
                    )

            # -------------------------------------------------
            # ONE SINGLE PERSIST OPERATION
            # -------------------------------------------------

            if hasattr(
                proxy,
                "setUserParts"
            ):

                proxy.setUserParts(
                    self.module,
                    saved_parts
                )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error actualizando tabla importada: "
                +
                str(error)
                +
                "\n"
            )

        finally:

            self._updating_imported = False

    # =========================================================
    # APPLY IMPORTED DATA
    # =========================================================

    def applyImportedPartData(
        self,
        part,
        data
    ):

        if "Label" in data:

            try:

                part.Label = str(
                    data["Label"]
                )

            except Exception:
                pass

        property_map = {
            "Length": "Length",
            "Width": "Width",
            "Thickness": "Thickness",
            "Quantity": "Quantity",
            "MaterialCode": "MaterialCode",
            "Role": "Role",
            "PartType": "PartType",
            "PositionType": "PositionType",
            "PositionMode": "PositionMode"
        }

        for data_name, property_name in (
            property_map.items()
        ):

            if data_name not in data:
                continue

            if not hasattr(
                part,
                property_name
            ):
                continue

            try:

                setattr(
                    part,
                    property_name,
                    data[data_name]
                )

            except Exception:
                pass

        if "Material" in data:

            for name in (
                "Material",
                "MaterialName",
                "MaterialCode"
            ):

                if not hasattr(
                    part,
                    name
                ):
                    continue

                try:

                    setattr(
                        part,
                        name,
                        data["Material"]
                    )

                    break

                except Exception:
                    pass

        role = str(
            data.get(
                "Role",
                getattr(
                    part,
                    "Role",
                    "Custom"
                )
            )
        )

        if role == "Shelf":

            self.setPartAxis(
                part,
                "LengthAxis",
                "X"
            )

            self.setPartAxis(
                part,
                "WidthAxis",
                "Y"
            )

            self.setPartAxis(
                part,
                "ThicknessAxis",
                "Z"
            )

        elif role == "Divider":

            self.setPartAxis(
                part,
                "LengthAxis",
                "Z"
            )

            self.setPartAxis(
                part,
                "WidthAxis",
                "Y"
            )

            self.setPartAxis(
                part,
                "ThicknessAxis",
                "X"
            )

        elif role == "Back":

            self.setPartAxis(
                part,
                "LengthAxis",
                "Z"
            )

            self.setPartAxis(
                part,
                "WidthAxis",
                "X"
            )

            self.setPartAxis(
                part,
                "ThicknessAxis",
                "Y"
            )

        else:

            self.setPartAxis(
                part,
                "LengthAxis",
                "X"
            )

            self.setPartAxis(
                part,
                "WidthAxis",
                "Y"
            )

            self.setPartAxis(
                part,
                "ThicknessAxis",
                "Z"
            )

        try:

            part.touch()

        except Exception:
            pass

    # =========================================================
    # CALCULATE
    # =========================================================

    def calculateParts(
        self
    ):

        if self._building:
            return

        self._building = True

        try:

            # -------------------------------------------------
            # IMPORTED
            # -------------------------------------------------

            if self.isImported():

                self.updateModule()

                self.updateImportedTableData(
                    preserveAutomaticDimensions=True
                )

                self.recalculateImported()

                self.loadImportedParts()

                return

            # -------------------------------------------------
            # PARAMETRIC
            # -------------------------------------------------

            if self.module is None:
                return

            self.updateTableData()

            self.updateModule()

            self.recalculateAutomaticUserPartPositions()

            self.updateModule()

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

            except Exception:

                self.parts = []

            self.loadTable()

        finally:

            self._building = False

    # =========================================================
    # AUTOMATIC PARAMETRIC USER POSITIONS
    # =========================================================

    def recalculateAutomaticUserPartPositions(
        self
    ):

        if not self.userParts:
            return

        thickness = (
            self.thicknessSpin.value()
        )

        height = (
            self.heightSpin.value()
        )

        width = (
            self.widthSpin.value()
        )

        depth = (
            self.depthSpin.value()
        )

        # -----------------------------------------------------
        # SHELVES
        # -----------------------------------------------------

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
                and
                str(
                    part.get(
                        "PositionMode",
                        "Automatic"
                    )
                )
                ==
                "Automatic"
            )
        ]

        if shelves:

            usable_height = max(
                0,
                height - thickness * 2
            )

            total = (
                thickness
                *
                len(shelves)
            )

            free = max(
                0,
                usable_height - total
            )

            spacing = (
                free
                /
                (len(shelves) + 1)
            )

            for index, part in enumerate(
                shelves
            ):

                z = (
                    thickness
                    +
                    spacing * (index + 1)
                    +
                    thickness * index
                )

                part["Length"] = max(
                    0,
                    width - thickness * 2
                )

                part["Width"] = depth
                part["Thickness"] = thickness

                part["Position"] = z

                part["PositionX"] = thickness
                part["PositionY"] = 0
                part["PositionZ"] = z

                part["RotationX"] = 0
                part["RotationY"] = 0
                part["RotationZ"] = 0

                part["PositionType"] = "Automatic"
                part["PositionMode"] = "Automatic"

        # -----------------------------------------------------
        # DIVIDERS
        # -----------------------------------------------------

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
                and
                str(
                    part.get(
                        "PositionMode",
                        "Automatic"
                    )
                )
                ==
                "Automatic"
            )
        ]

        if dividers:

            usable_width = max(
                0,
                width - thickness * 2
            )

            total = (
                thickness
                *
                len(dividers)
            )

            free = max(
                0,
                usable_width - total
            )

            spacing = (
                free
                /
                (len(dividers) + 1)
            )

            for index, part in enumerate(
                dividers
            ):

                x = (
                    thickness
                    +
                    spacing * (index + 1)
                    +
                    thickness * index
                )

                part["Length"] = max(
                    0,
                    height - thickness * 2
                )

                part["Width"] = depth
                part["Thickness"] = thickness

                part["Position"] = x

                part["PositionX"] = x
                part["PositionY"] = 0
                part["PositionZ"] = thickness

                part["RotationX"] = 0
                part["RotationY"] = 0
                part["RotationZ"] = 0

                part["PositionType"] = "Automatic"
                part["PositionMode"] = "Automatic"

    # =========================================================
    # TYPE
    # =========================================================

    def typeChanged(
        self,
        row
    ):

        if self._loading_table:
            return

        if self._changing_type:
            return

        if row < 0:
            return

        if row >= len(
            self.parts
        ):
            return

        self._changing_type = True

        try:

            combo = self.table.cellWidget(
                row,
                1
            )

            if combo is None:
                return

            role = combo.currentData()

            # -------------------------------------------------
            # IMPORTED
            # -------------------------------------------------

            if self.isImported():

                part = self.parts[
                    row
                ]

                mode_combo = self.table.cellWidget(
                    row,
                    7
                )

                if role in (
                    "Shelf",
                    "Divider"
                ):

                    mode = "Automatic"

                    if mode_combo is not None:

                        index = mode_combo.findData(
                            "Automatic"
                        )

                        if index >= 0:

                            mode_combo.setCurrentIndex(
                                index
                            )

                else:

                    mode = (
                        mode_combo.currentData()
                        if mode_combo is not None
                        else
                        "Manual"
                    )

                part_type = (
                    "Balda"
                    if role == "Shelf"
                    else
                    "Separador"
                    if role == "Divider"
                    else
                    "Personalizada"
                    if role == "Custom"
                    else
                    "Estructural"
                )

                self.applyImportedPartData(
                    part,
                    {
                        "Role": role,
                        "PartType": part_type,
                        "PositionMode": mode,
                        "PositionType": mode
                    }
                )

                self.updateModule()

                self.updateImportedTableData(
                    preserveAutomaticDimensions=True
                )

                self.recalculateImported()

                self.loadImportedParts()

                if row < self.table.rowCount():

                    self.table.selectRow(
                        row
                    )

                return

            # -------------------------------------------------
            # PARAMETRIC
            # -------------------------------------------------

            if row < 5:
                return

            userIndex = row - 5

            if userIndex >= len(
                self.userParts
            ):
                return

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

        finally:

            self._changing_type = False

    # =========================================================
    # MODE
    # =========================================================

    def modeChanged(
        self,
        row
    ):

        if self._loading_table:
            return

        if self._changing_mode:
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

        mode = combo.currentData()

        if mode not in (
            "Automatic",
            "Manual"
        ):

            mode = "Manual"

        self._changing_mode = True

        try:

            # -------------------------------------------------
            # IMPORTED
            # -------------------------------------------------

            if self.isImported():

                part = self.parts[
                    row
                ]

                role = str(
                    getattr(
                        part,
                        "Role",
                        "Custom"
                    )
                )

                self.setPartMode(
                    part,
                    mode
                )

                if (
                    mode == "Automatic"
                    and
                    role in (
                        "Shelf",
                        "Divider"
                    )
                ):

                    self.updateModule()

                    self.recalculateImported()

                else:

                    try:

                        part.touch()

                    except Exception:
                        pass

                    try:

                        if part.Document is not None:

                            part.Document.recompute()

                    except Exception:
                        pass

                self.updateImportedTableData(
                    preserveAutomaticDimensions=True
                )

                self.loadImportedParts()

                if row < self.table.rowCount():

                    self.table.selectRow(
                        row
                    )

                return

            # -------------------------------------------------
            # PARAMETRIC
            # -------------------------------------------------

            if row < 5:
                return

            userIndex = row - 5

            if userIndex >= len(
                self.userParts
            ):
                return

            part = self.userParts[
                userIndex
            ]

            part["PositionMode"] = mode
            part["PositionType"] = mode

            self.calculateParts()

        finally:

            self._changing_mode = False

    # =========================================================
    # MATERIAL
    # =========================================================

    def materialChanged(
        self,
        row
    ):

        if self._loading_table:
            return

        if self._changing_material:
            return

        if row < 0:
            return

        combo = self.table.cellWidget(
            row,
            6
        )

        if combo is None:
            return

        material = (
            combo.currentData()
            or
            ""
        )

        self._changing_material = True

        try:

            if not self.isImported():

                if row < 5:
                    return

                userIndex = row - 5

                if userIndex >= len(
                    self.userParts
                ):
                    return

                self.userParts[
                    userIndex
                ]["MaterialCode"] = str(
                    material
                )

                return

            self.updateImportedTableData(
                preserveAutomaticDimensions=True
            )

        finally:

            self._changing_material = False

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

            materials = MaterialLibrary.all()

        except Exception:

            materials = []

        if isinstance(
            materials,
            dict
        ):

            materials = list(
                materials.values()
            )

        for material in materials:

            if isinstance(
                material,
                dict
            ):

                code = str(
                    material.get(
                        "Code",
                        ""
                    )
                ).strip()

                name = str(
                    material.get(
                        "MaterialName",
                        ""
                    )
                ).strip()

                if not code:
                    continue

                text = (
                    code
                    +
                    " — "
                    +
                    name
                    if name
                    else
                    code
                )

                combo.addItem(
                    text,
                    code
                )

            else:

                text = self.extractMaterialName(
                    material
                )

                if text:

                    combo.addItem(
                        text,
                        text
                    )

        selected = str(
            selectedCode or ""
        ).strip()

        if selected:

            index = combo.findData(
                selected
            )

            if index < 0:

                index = combo.findText(
                    selected
                )

            if index < 0:

                combo.insertItem(
                    0,
                    selected,
                    selected
                )

                index = 0

            combo.setCurrentIndex(
                index
            )

        return combo

    def extractMaterialName(
        self,
        material
    ):

        if material is None:
            return ""

        if isinstance(
            material,
            str
        ):

            return material.strip()

        if isinstance(
            material,
            dict
        ):

            for name in (
                "MaterialName",
                "Code",
                "Name",
                "name",
                "Label",
                "label"
            ):

                value = str(
                    material.get(
                        name,
                        ""
                    )
                ).strip()

                if value:
                    return value

            return ""

        for name in (
            "MaterialName",
            "Name",
            "name",
            "Label",
            "label",
            "Code",
            "code"
        ):

            try:

                value = str(
                    getattr(
                        material,
                        name
                    )
                ).strip()

                if value:
                    return value

            except Exception:
                pass

        return ""

    # =========================================================
    # ADD CUSTOM
    # =========================================================

    def addCustomPart(
        self
    ):

        if self.isImported():

            self.addImportedPart()

            return

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
            "CU" + str(number)
            in used
        ):

            number += 1

        internal_width = max(
            0,
            self.widthSpin.value()
            -
            self.thicknessSpin.value() * 2
        )

        part = {
            "Code":
                "CU" + str(number),

            "Label":
                "Nueva pieza " + str(number),

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
    # ADD IMPORTED
    # =========================================================

    def addImportedPart(
        self
    ):

        if self.module is None:
            return

        document = getattr(
            self.module,
            "Document",
            None
        )

        if document is None:
            return

        try:

            from objects.bosqo_part import (
                create_part
            )

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
                    self.thicknessSpin.value() * 2
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
                "Manual",

            "LengthAxis":
                "X",

            "WidthAxis":
                "Y",

            "ThicknessAxis":
                "Z"
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

        if self.isImported():

            result = QtWidgets.QMessageBox.question(
                self,
                "Eliminar pieza",
                "¿Seguro que quieres eliminar "
                "la pieza seleccionada?",
                QtWidgets.QMessageBox.Yes
                |
                QtWidgets.QMessageBox.No
            )

            if result != QtWidgets.QMessageBox.Yes:
                return

            document = getattr(
                part,
                "Document",
                None
            )

            if document is not None:

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

            return

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

        if self.isImported():

            self.duplicateImportedPart(
                self.parts[
                    row
                ]
            )

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

            if part.get(
                "Code"
            ) == code:

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
            "CU" + str(number)
            in used
        ):

            number += 1

        source["Code"] = (
            "CU" + str(number)
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

        document = getattr(
            source,
            "Document",
            None
        )

        if document is None:
            return

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
            "PositionMode",
            "LengthAxis",
            "WidthAxis",
            "ThicknessAxis"
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

        try:

            new_part.Shape = (
                source.Shape.copy()
            )

        except Exception:
            pass

        try:

            new_part.Placement = (
                source.Placement
            )

        except Exception:
            pass

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

            used.add(
                str(
                    getattr(
                        part,
                        "Code",
                        ""
                    )
                )
            )

        number = 1

        while (
            "CU" + str(number)
            in used
        ):

            number += 1

        return (
            "CU" + str(number)
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

        # -----------------------------------------------------
        # IMPORTED
        # -----------------------------------------------------

        if self.isImported():

            data = self.partToData(
                part
            )

            dialog = ManualPlacementDialog(
                data,
                self
            )

            try:

                accepted = dialog.exec_()

            except AttributeError:

                accepted = dialog.exec()

            if not accepted:
                return

            self.applyPlacementToRealPart(
                part,
                dialog.getData()
            )

            return

        # -----------------------------------------------------
        # PARAMETRIC
        # -----------------------------------------------------

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
            code.startswith("TT")
            or
            code.startswith("TB")
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

        if code in self.structuralPlacements:

            data.update(
                self.structuralPlacements[
                    code
                ]
            )

        for user_part in self.userParts:

            if user_part.get(
                "Code"
            ) == code:

                data.update(
                    user_part
                )

                break

        dialog = ManualPlacementDialog(
            data,
            self
        )

        try:

            accepted = dialog.exec_()

        except AttributeError:

            accepted = dialog.exec()

        if not accepted:
            return

        placement_data = (
            dialog.getData()
        )

        if structural:

            self.structuralPlacements[
                code
            ] = placement_data

            self.persistStructuralPlacements()

        else:

            for user_part in self.userParts:

                if user_part.get(
                    "Code"
                ) == code:

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

            for name, value in (
                ("PositionX", x),
                ("PositionY", y),
                ("PositionZ", z),
                ("RotationX", rx),
                ("RotationY", ry),
                ("RotationZ", rz)
            ):

                if hasattr(
                    part,
                    name
                ):

                    try:

                        setattr(
                            part,
                            name,
                            value
                        )

                    except Exception:
                        pass

            self.setPartMode(
                part,
                "Manual"
            )

            try:

                part.touch()

            except Exception:
                pass

            if part.Document is not None:

                part.Document.recompute()

            self.loadImportedParts()

            for current_row, current in enumerate(
                self.parts
            ):

                if current is part:

                    self.table.selectRow(
                        current_row
                    )

                    break

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error aplicando Placement: "
                +
                str(error)
                +
                "\n"
            )

    # =========================================================
    # RECALCULATE IMPORTED
    # =========================================================

    def recalculateImported(
        self
    ):

        if self._recalculating_imported:
            return

        self._recalculating_imported = True

        try:

            if self.module is None:
                return

            width = self.widthSpin.value()
            height = self.heightSpin.value()
            depth = self.depthSpin.value()
            thickness = self.thicknessSpin.value()

            # -------------------------------------------------
            # SHELVES
            # -------------------------------------------------

            shelves = [
                part
                for part in self.parts
                if (
                    str(
                        getattr(
                            part,
                            "Role",
                            ""
                        )
                    )
                    ==
                    "Shelf"
                    and
                    str(
                        getattr(
                            part,
                            "PositionMode",
                            "Manual"
                        )
                    )
                    ==
                    "Automatic"
                )
            ]

            if shelves:

                usable_height = max(
                    0,
                    height - thickness * 2
                )

                total_thickness = (
                    thickness
                    *
                    len(shelves)
                )

                free_height = max(
                    0,
                    usable_height - total_thickness
                )

                spacing = (
                    free_height
                    /
                    (len(shelves) + 1)
                )

                shelf_length = max(
                    0,
                    width - thickness * 2
                )

                shelf_width = max(
                    0,
                    depth
                )

                for index, part in enumerate(
                    shelves
                ):

                    z = (
                        thickness
                        +
                        spacing * (index + 1)
                        +
                        thickness * index
                    )

                    self.setPartDimension(
                        part,
                        "Length",
                        shelf_length
                    )

                    self.setPartDimension(
                        part,
                        "Width",
                        shelf_width
                    )

                    self.setPartDimension(
                        part,
                        "Thickness",
                        thickness
                    )

                    self.setPartAxis(
                        part,
                        "LengthAxis",
                        "X"
                    )

                    self.setPartAxis(
                        part,
                        "WidthAxis",
                        "Y"
                    )

                    self.setPartAxis(
                        part,
                        "ThicknessAxis",
                        "Z"
                    )

                    self.setRealPosition(
                        part,
                        x=thickness,
                        z=z
                    )

                    self.setPartMode(
                        part,
                        "Automatic"
                    )

            # -------------------------------------------------
            # DIVIDERS
            # -------------------------------------------------

            dividers = [
                part
                for part in self.parts
                if (
                    str(
                        getattr(
                            part,
                            "Role",
                            ""
                        )
                    )
                    ==
                    "Divider"
                    and
                    str(
                        getattr(
                            part,
                            "PositionMode",
                            "Manual"
                        )
                    )
                    ==
                    "Automatic"
                )
            ]

            if dividers:

                usable_width = max(
                    0,
                    width - thickness * 2
                )

                total_thickness = (
                    thickness
                    *
                    len(dividers)
                )

                free_width = max(
                    0,
                    usable_width - total_thickness
                )

                spacing = (
                    free_width
                    /
                    (len(dividers) + 1)
                )

                divider_length = max(
                    0,
                    height - thickness * 2
                )

                divider_width = max(
                    0,
                    depth
                )

                for index, part in enumerate(
                    dividers
                ):

                    x = (
                        thickness
                        +
                        spacing * (index + 1)
                        +
                        thickness * index
                    )

                    self.setPartDimension(
                        part,
                        "Length",
                        divider_length
                    )

                    self.setPartDimension(
                        part,
                        "Width",
                        divider_width
                    )

                    self.setPartDimension(
                        part,
                        "Thickness",
                        thickness
                    )

                    self.setPartAxis(
                        part,
                        "LengthAxis",
                        "Z"
                    )

                    self.setPartAxis(
                        part,
                        "WidthAxis",
                        "Y"
                    )

                    self.setPartAxis(
                        part,
                        "ThicknessAxis",
                        "X"
                    )

                    self.setRealPosition(
                        part,
                        x=x,
                        z=thickness
                    )

                    self.setPartMode(
                        part,
                        "Automatic"
                    )

            # -------------------------------------------------
            # RECOMPUTE
            # -------------------------------------------------

            try:

                if self.module.Document is not None:

                    self.module.Document.recompute()

            except Exception:
                pass

            self.persistImportedCalculatedParts()

        finally:

            self._recalculating_imported = False

    # =========================================================
    # PERSIST IMPORTED CALCULATED PARTS
    # =========================================================

    def persistImportedCalculatedParts(
        self
    ):

        if self.module is None:
            return

        proxy = getattr(
            self.module,
            "Proxy",
            None
        )

        if proxy is None:
            return

        if not hasattr(
            proxy,
            "getUserParts"
        ):

            return

        if not hasattr(
            proxy,
            "setUserParts"
        ):

            return

        try:

            saved_parts = [
                dict(item)
                for item in proxy.getUserParts(
                    self.module
                )
                if isinstance(
                    item,
                    dict
                )
            ]

        except Exception:

            saved_parts = []

        changed = False

        for part in self.parts:

            role = str(
                getattr(
                    part,
                    "Role",
                    "Custom"
                )
            )

            if role not in (
                "Shelf",
                "Divider"
            ):

                continue

            mode = str(
                getattr(
                    part,
                    "PositionMode",
                    "Manual"
                )
            )

            if mode != "Automatic":
                continue

            object_name = str(
                getattr(
                    part,
                    "Name",
                    ""
                )
            )

            record = None

            for item in saved_parts:

                if str(
                    item.get(
                        "ObjectName",
                        ""
                    )
                ) == object_name:

                    record = item
                    break

            if record is None:

                record = {
                    "ObjectName":
                        object_name
                }

                saved_parts.append(
                    record
                )

            record["Name"] = str(
                getattr(
                    part,
                    "Label",
                    ""
                )
            )

            record["Type"] = (
                "Balda"
                if role == "Shelf"
                else
                "Separador"
            )

            record["Role"] = role

            record["PositionMode"] = (
                "Automatic"
            )

            record["PositionType"] = (
                "Automatic"
            )

            record["Length"] = self.value(
                getattr(
                    part,
                    "Length",
                    0
                )
            )

            record["Width"] = self.value(
                getattr(
                    part,
                    "Width",
                    0
                )
            )

            record["Thickness"] = self.value(
                getattr(
                    part,
                    "Thickness",
                    0
                )
            )

            record["Quantity"] = self.value(
                getattr(
                    part,
                    "Quantity",
                    1
                )
            )

            record["PositionX"] = self.value(
                getattr(
                    part,
                    "PositionX",
                    part.Placement.Base.x
                )
            )

            record["PositionY"] = self.value(
                getattr(
                    part,
                    "PositionY",
                    part.Placement.Base.y
                )
            )

            record["PositionZ"] = self.value(
                getattr(
                    part,
                    "PositionZ",
                    part.Placement.Base.z
                )
            )

            changed = True

        if not changed:
            return

        try:

            proxy.setUserParts(
                self.module,
                saved_parts
            )

        except Exception:
            pass

    # =========================================================
    # PART DIMENSIONS
    # =========================================================

    def setPartDimension(
        self,
        part,
        name,
        value
    ):

        if not hasattr(
            part,
            name
        ):
            return

        try:

            setattr(
                part,
                name,
                float(value)
            )

        except Exception:

            try:

                setattr(
                    part,
                    name,
                    value
                )

            except Exception:
                pass

    def setPartAxis(
        self,
        part,
        name,
        value
    ):

        if not hasattr(
            part,
            name
        ):
            return

        try:

            setattr(
                part,
                name,
                value
            )

        except Exception:
            pass

    def setPartMode(
        self,
        part,
        mode
    ):

        if hasattr(
            part,
            "PositionMode"
        ):

            try:

                part.PositionMode = mode

            except Exception:
                pass

        if hasattr(
            part,
            "PositionType"
        ):

            try:

                part.PositionType = mode

            except Exception:
                pass

    # =========================================================
    # AUTOMATIC POSITION HELPERS
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

        if part not in shelves:
            return 0

        index = shelves.index(
            part
        )

        usableHeight = max(
            0,
            self.heightSpin.value()
            -
            self.thicknessSpin.value() * 2
        )

        totalThickness = (
            self.thicknessSpin.value()
            *
            len(shelves)
        )

        freeHeight = max(
            0,
            usableHeight - totalThickness
        )

        spacing = (
            freeHeight
            /
            (len(shelves) + 1)
        )

        return (
            self.thicknessSpin.value()
            +
            spacing * (index + 1)
            +
            self.thicknessSpin.value() * index
        )

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

        if part not in dividers:
            return 0

        index = dividers.index(
            part
        )

        usableWidth = max(
            0,
            self.widthSpin.value()
            -
            self.thicknessSpin.value() * 2
        )

        totalThickness = (
            self.thicknessSpin.value()
            *
            len(dividers)
        )

        freeWidth = max(
            0,
            usableWidth - totalThickness
        )

        spacing = (
            freeWidth
            /
            (len(dividers) + 1)
        )

        return (
            self.thicknessSpin.value()
            +
            spacing * (index + 1)
            +
            self.thicknessSpin.value() * index
        )

    # =========================================================
    # REAL POSITION
    # =========================================================

    def setRealPosition(
        self,
        part,
        x=None,
        z=None
    ):

        try:

            placement = part.Placement

            base = FreeCAD.Vector(
                placement.Base.x,
                placement.Base.y,
                placement.Base.z
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

                    try:

                        part.PositionX = float(
                            x
                        )

                    except Exception:
                        pass

                if hasattr(
                    part,
                    "Position"
                ):

                    try:

                        part.Position = float(
                            x
                        )

                    except Exception:
                        pass

            if z is not None:

                if hasattr(
                    part,
                    "PositionZ"
                ):

                    try:

                        part.PositionZ = float(
                            z
                        )

                    except Exception:
                        pass

            if hasattr(
                part,
                "PositionY"
            ):

                try:

                    part.PositionY = float(
                        base.y
                    )

                except Exception:
                    pass

            try:

                part.touch()

            except Exception:
                pass

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error posicionando pieza: "
                +
                str(error)
                +
                "\n"
            )

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
            code.startswith("TT")
            or
            code.startswith("TB")
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save(
        self
    ):

        try:

            if self.isImported():

                # ---------------------------------------------
                # SINGLE FINAL SYNC
                # ---------------------------------------------

                self.updateModule()

                self.updateImportedTableData(
                    preserveAutomaticDimensions=True
                )

                self.recalculateImported()

                self.updateModule()

                self.persistImportedCalculatedParts()

                try:

                    if self.module.Document is not None:

                        self.module.Document.recompute()

                except Exception:
                    pass

                self.accept()

                return

            # -------------------------------------------------
            # PARAMETRIC
            # -------------------------------------------------

            self.updateTableData()

            self.updateModule()

            self.calculateParts()

            self.updateTableData()

            self.updateModule()

            self.persistUserParts()
            self.persistStructuralPlacements()

            try:

                if self.module is not None:
                    self.module.Document.recompute()

            except Exception:
                pass

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
                str(value)
            )
        )

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
                    int(number)
                )

            return str(
                round(
                    number,
                    2
                )
            )

        except Exception:

            return "0"

    def setCombo(
        self,
        combo,
        value
    ):

        index = combo.findText(
            str(value)
        )

        if index >= 0:

            combo.setCurrentIndex(
                index
            )

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