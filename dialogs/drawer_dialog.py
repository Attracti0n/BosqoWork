from PySide import QtWidgets


# =============================================================
# DRAWER DIALOG
# =============================================================

class DrawerDialog(QtWidgets.QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle(
            "Nuevo cajón"
        )

        self.setMinimumWidth(
            420
        )

        self.setModal(
            True
        )

        self.createUI()


    # =========================================================
    # UI
    # =========================================================

    def createUI(
        self
    ):

        layout = QtWidgets.QVBoxLayout(
            self
        )


        # =====================================================
        # GENERAL
        # =====================================================

        generalGroup = QtWidgets.QGroupBox(
            "Cajón"
        )

        generalLayout = QtWidgets.QFormLayout(
            generalGroup
        )


        self.nameEdit = (
            QtWidgets.QLineEdit()
        )

        self.nameEdit.setText(
            "Nuevo cajón"
        )

        generalLayout.addRow(
            "Nombre:",
            self.nameEdit
        )


        self.systemCombo = (
            QtWidgets.QComboBox()
        )

        self.loadSystems()

        generalLayout.addRow(
            "Sistema:",
            self.systemCombo
        )


        layout.addWidget(
            generalGroup
        )


        # =====================================================
        # DIMENSIONS
        # =====================================================

        dimensionsGroup = QtWidgets.QGroupBox(
            "Dimensiones"
        )

        dimensionsLayout = QtWidgets.QFormLayout(
            dimensionsGroup
        )


        # WIDTH

        self.widthSpin = (
            QtWidgets.QDoubleSpinBox()
        )

        #
        # 540 mm es un valor razonable para un módulo
        # de 600 mm con laterales de 19 mm.
        #

        self.configureDimensionSpin(
            self.widthSpin,
            540
        )

        dimensionsLayout.addRow(
            "Anchura:",
            self.widthSpin
        )


        # HEIGHT

        self.heightSpin = (
            QtWidgets.QDoubleSpinBox()
        )

        self.configureDimensionSpin(
            self.heightSpin,
            150
        )

        dimensionsLayout.addRow(
            "Altura:",
            self.heightSpin
        )


        # DEPTH

        self.depthSpin = (
            QtWidgets.QDoubleSpinBox()
        )

        self.configureDimensionSpin(
            self.depthSpin,
            500
        )

        dimensionsLayout.addRow(
            "Profundidad:",
            self.depthSpin
        )


        layout.addWidget(
            dimensionsGroup
        )


        # =====================================================
        # POSITION
        # =====================================================

        positionGroup = QtWidgets.QGroupBox(
            "Posición"
        )

        positionLayout = QtWidgets.QFormLayout(
            positionGroup
        )


        self.positionXSpin = (
            QtWidgets.QDoubleSpinBox()
        )

        self.configurePositionSpin(
            self.positionXSpin
        )

        positionLayout.addRow(
            "X:",
            self.positionXSpin
        )


        self.positionYSpin = (
            QtWidgets.QDoubleSpinBox()
        )

        self.configurePositionSpin(
            self.positionYSpin
        )

        positionLayout.addRow(
            "Y:",
            self.positionYSpin
        )


        self.positionZSpin = (
            QtWidgets.QDoubleSpinBox()
        )

        self.configurePositionSpin(
            self.positionZSpin
        )

        positionLayout.addRow(
            "Z:",
            self.positionZSpin
        )


        layout.addWidget(
            positionGroup
        )


        # =====================================================
        # PARAMETERS
        # =====================================================

        parametersGroup = QtWidgets.QGroupBox(
            "Parámetros"
        )

        parametersLayout = QtWidgets.QFormLayout(
            parametersGroup
        )


        self.bottomThicknessSpin = (
            QtWidgets.QDoubleSpinBox()
        )

        self.configureThicknessSpin(
            self.bottomThicknessSpin,
            10
        )

        parametersLayout.addRow(
            "Espesor fondo:",
            self.bottomThicknessSpin
        )


        self.sideThicknessSpin = (
            QtWidgets.QDoubleSpinBox()
        )

        self.configureThicknessSpin(
            self.sideThicknessSpin,
            16
        )

        parametersLayout.addRow(
            "Espesor laterales:",
            self.sideThicknessSpin
        )


        self.backThicknessSpin = (
            QtWidgets.QDoubleSpinBox()
        )

        self.configureThicknessSpin(
            self.backThicknessSpin,
            16
        )

        parametersLayout.addRow(
            "Espesor trasera:",
            self.backThicknessSpin
        )


        layout.addWidget(
            parametersGroup
        )


        # =====================================================
        # QUANTITY
        # =====================================================

        quantityGroup = QtWidgets.QGroupBox(
            "Cantidad"
        )

        quantityLayout = QtWidgets.QFormLayout(
            quantityGroup
        )


        self.quantitySpin = (
            QtWidgets.QSpinBox()
        )

        self.quantitySpin.setRange(
            1,
            999
        )

        self.quantitySpin.setValue(
            1
        )

        quantityLayout.addRow(
            "Cantidad:",
            self.quantitySpin
        )


        layout.addWidget(
            quantityGroup
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


    # =========================================================
    # SYSTEMS
    # =========================================================

    def loadSystems(
        self
    ):

        self.systemCombo.clear()

        self.systemCombo.addItem(
            "— Seleccionar sistema —",
            ""
        )

        systems = [

            (
                "Cajón estándar",
                "STANDARD"
            ),

            (
                "Cajón de extracción total",
                "FULL_EXTENSION"
            ),

            (
                "Cajón oculto",
                "HIDDEN"
            )
        ]

        for name, code in systems:

            self.systemCombo.addItem(
                name,
                code
            )


    # =========================================================
    # DIMENSION SPIN
    # =========================================================

    def configureDimensionSpin(
        self,
        spin,
        value
    ):

        spin.setRange(
            1,
            5000
        )

        spin.setDecimals(
            1
        )

        spin.setSingleStep(
            1
        )

        spin.setSuffix(
            " mm"
        )

        spin.setValue(
            value
        )


    # =========================================================
    # POSITION SPIN
    # =========================================================

    def configurePositionSpin(
        self,
        spin
    ):

        spin.setRange(
            -5000,
            5000
        )

        spin.setDecimals(
            1
        )

        spin.setSingleStep(
            1
        )

        spin.setSuffix(
            " mm"
        )

        spin.setValue(
            0
        )


    # =========================================================
    # THICKNESS SPIN
    # =========================================================

    def configureThicknessSpin(
        self,
        spin,
        value
    ):

        spin.setRange(
            1,
            100
        )

        spin.setDecimals(
            1
        )

        spin.setSingleStep(
            1
        )

        spin.setSuffix(
            " mm"
        )

        spin.setValue(
            value
        )


    # =========================================================
    # DATA
    # =========================================================

    def getData(
        self
    ):

        return {

            "Label":
                self.nameEdit.text().strip(),

            "DrawerType":
                self.systemCombo.currentData(),

            "System":
                self.systemCombo.currentData(),

            "Width":
                self.widthSpin.value(),

            "Height":
                self.heightSpin.value(),

            "Depth":
                self.depthSpin.value(),

            "PositionX":
                self.positionXSpin.value(),

            "PositionY":
                self.positionYSpin.value(),

            "PositionZ":
                self.positionZSpin.value(),

            "PositionMode":
                "Automatic",

            "BottomThickness":
                self.bottomThicknessSpin.value(),

            "SideThickness":
                self.sideThicknessSpin.value(),

            "BackThickness":
                self.backThicknessSpin.value(),

            "Quantity":
                self.quantitySpin.value(),

            "Source":
                "Created",

            "Status":
                "Defined"
        }


# =============================================================
# FACTORY
# =============================================================

def create_drawer_dialog(
    parent=None
):

    return DrawerDialog(
        parent
    )