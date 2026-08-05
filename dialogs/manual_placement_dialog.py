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

        # =====================================================
        # POSICIÓN
        # =====================================================

        positionGroup = QtWidgets.QGroupBox(
            "Posición"
        )

        positionLayout = QtWidgets.QGridLayout()

        # X

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

        # Y

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

        # Z

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

        # =====================================================
        # GIRO
        # =====================================================

        rotationGroup = QtWidgets.QGroupBox(
            "Giro"
        )

        rotationLayout = QtWidgets.QGridLayout()

        # X

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

        # Y

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

        # Z

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

        # =====================================================
        # BOTONES
        # =====================================================

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

        # =====================================================
        # CARGAR DATOS
        # =====================================================

        self.loadData()

    # =========================================================
    # SPINBOX
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
    # ANGLE SPINBOX
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
                self.getPartValue(
                    "PositionX",
                    0
                )
            )
        )

        self.ySpin.setValue(
            self.toFloat(
                self.getPartValue(
                    "PositionY",
                    0
                )
            )
        )

        self.zSpin.setValue(
            self.toFloat(
                self.getPartValue(
                    "PositionZ",
                    0
                )
            )
        )

        self.rxSpin.setValue(
            self.toFloat(
                self.getPartValue(
                    "RotationX",
                    0
                )
            )
        )

        self.rySpin.setValue(
            self.toFloat(
                self.getPartValue(
                    "RotationY",
                    0
                )
            )
        )

        self.rzSpin.setValue(
            self.toFloat(
                self.getPartValue(
                    "RotationZ",
                    0
                )
            )
        )

    # =========================================================
    # GET PART VALUE
    # =========================================================

    def getPartValue(
        self,
        name,
        default=0
    ):

        part = self.part

        # Diccionario

        if isinstance(
            part,
            dict
        ):

            return part.get(
                name,
                default
            )

        # FreeCAD object

        if hasattr(
            part,
            name
        ):

            try:

                return getattr(
                    part,
                    name
                )

            except Exception:

                pass

        return default

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