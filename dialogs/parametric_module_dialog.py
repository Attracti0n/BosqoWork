from PySide import QtWidgets

from dialogs.part_table_dialog import PartTableDialog


class ParametricModuleDialog(QtWidgets.QDialog):


    def __init__(
        self,
        parameters=None,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle(
            "Módulo paramétrico"
        )

        self.resize(
            1100,
            750
        )

        self.parameters = parameters

        self.createUI()

        self.loadParameters()

        self.recalculate()


    #
    # Create UI
    #

    def createUI(
        self
    ):

        mainLayout = QtWidgets.QVBoxLayout()


        #
        # Title
        #

        title = QtWidgets.QLabel(
            "Módulo paramétrico"
        )

        font = title.font()

        font.setBold(
            True
        )

        font.setPointSize(
            font.pointSize() + 2
        )

        title.setFont(
            font
        )

        mainLayout.addWidget(
            title
        )


        #
        # Identification
        #

        identificationGroup = QtWidgets.QGroupBox(
            "Identificación"
        )

        identificationLayout = QtWidgets.QGridLayout()


        #
        # Module name
        #

        identificationLayout.addWidget(
            QtWidgets.QLabel(
                "Nombre del módulo:"
            ),
            0,
            0
        )


        self.nameEdit = QtWidgets.QLineEdit()


        self.nameEdit.setPlaceholderText(
            "Nombre del módulo"
        )


        identificationLayout.addWidget(
            self.nameEdit,
            0,
            1,
            1,
            3
        )


        identificationGroup.setLayout(
            identificationLayout
        )

        mainLayout.addWidget(
            identificationGroup
        )


        #
        # Module parameters
        #

        parametersGroup = QtWidgets.QGroupBox(
            "Parámetros del módulo"
        )

        parametersLayout = QtWidgets.QGridLayout()


        #
        # Module type
        #

        parametersLayout.addWidget(
            QtWidgets.QLabel(
                "Tipo de módulo:"
            ),
            0,
            0
        )


        self.typeCombo = QtWidgets.QComboBox()


        self.typeCombo.addItems(
            [

                "Módulo bajo",
                "Módulo alto",
                "Columna",
                "Armario",
                "Personalizado"

            ]
        )


        parametersLayout.addWidget(
            self.typeCombo,
            0,
            1
        )


        #
        # Width
        #

        self.widthSpin = self.createSpinBox()


        parametersLayout.addWidget(
            QtWidgets.QLabel(
                "Anchura:"
            ),
            1,
            0
        )


        parametersLayout.addWidget(
            self.widthSpin,
            1,
            1
        )


        #
        # Height
        #

        self.heightSpin = self.createSpinBox()


        parametersLayout.addWidget(
            QtWidgets.QLabel(
                "Altura:"
            ),
            1,
            2
        )


        parametersLayout.addWidget(
            self.heightSpin,
            1,
            3
        )


        #
        # Depth
        #

        self.depthSpin = self.createSpinBox()


        parametersLayout.addWidget(
            QtWidgets.QLabel(
                "Profundidad:"
            ),
            2,
            0
        )


        parametersLayout.addWidget(
            self.depthSpin,
            2,
            1
        )


        #
        # Panel thickness
        #

        self.thicknessSpin = self.createSpinBox()


        parametersLayout.addWidget(
            QtWidgets.QLabel(
                "Espesor panel:"
            ),
            2,
            2
        )


        parametersLayout.addWidget(
            self.thicknessSpin,
            2,
            3
        )


        #
        # Back thickness
        #

        self.backThicknessSpin = self.createSpinBox()


        parametersLayout.addWidget(
            QtWidgets.QLabel(
                "Espesor fondo:"
            ),
            3,
            0
        )


        parametersLayout.addWidget(
            self.backThicknessSpin,
            3,
            1
        )


        #
        # Back inset
        #

        self.backInsetSpin = self.createSpinBox()


        parametersLayout.addWidget(
            QtWidgets.QLabel(
                "Retranqueo trasero:"
            ),
            3,
            2
        )


        parametersLayout.addWidget(
            self.backInsetSpin,
            3,
            3
        )


        parametersGroup.setLayout(
            parametersLayout
        )

        mainLayout.addWidget(
            parametersGroup
        )


        #
        # Pieces
        #

        piecesGroup = QtWidgets.QGroupBox(
            "Piezas del módulo"
        )


        piecesLayout = QtWidgets.QVBoxLayout()


        self.partsTable = PartTableDialog(
            parts=[],
            parent=self
        )


        piecesLayout.addWidget(
            self.partsTable.table
        )


        piecesGroup.setLayout(
            piecesLayout
        )


        mainLayout.addWidget(
            piecesGroup
        )


        #
        # Buttons
        #

        buttonLayout = QtWidgets.QHBoxLayout()


        #
        # Recalculate
        #

        self.recalculateButton = QtWidgets.QPushButton(
            "Recalcular"
        )


        self.recalculateButton.clicked.connect(
            self.recalculate
        )


        buttonLayout.addWidget(
            self.recalculateButton
        )


        buttonLayout.addStretch()


        #
        # Apply
        #

        self.applyButton = QtWidgets.QPushButton(
            "Aplicar"
        )


        self.applyButton.clicked.connect(
            self.apply
        )


        buttonLayout.addWidget(
            self.applyButton
        )


        #
        # Cancel
        #

        self.cancelButton = QtWidgets.QPushButton(
            "Cancelar"
        )


        self.cancelButton.clicked.connect(
            self.reject
        )


        buttonLayout.addWidget(
            self.cancelButton
        )


        mainLayout.addLayout(
            buttonLayout
        )


        self.setLayout(
            mainLayout
        )


    #
    # SpinBox
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
    # Load parameters
    #

    def loadParameters(
        self
    ):

        obj = self.parameters


        if obj is None:

            return


        #
        # Name
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


        #
        # Type
        #

        if hasattr(
            obj,
            "ModuleType"
        ):

            index = self.typeCombo.findText(
                str(
                    obj.ModuleType
                )
            )


            if index >= 0:

                self.typeCombo.setCurrentIndex(
                    index
                )


        #
        # Width
        #

        if hasattr(
            obj,
            "ModuleWidth"
        ):

            self.widthSpin.setValue(
                float(
                    obj.ModuleWidth.Value
                )
            )


        #
        # Height
        #

        if hasattr(
            obj,
            "ModuleHeight"
        ):

            self.heightSpin.setValue(
                float(
                    obj.ModuleHeight.Value
                )
            )


        #
        # Depth
        #

        if hasattr(
            obj,
            "ModuleDepth"
        ):

            self.depthSpin.setValue(
                float(
                    obj.ModuleDepth.Value
                )
            )


        #
        # Panel thickness
        #

        if hasattr(
            obj,
            "PanelThickness"
        ):

            self.thicknessSpin.setValue(
                float(
                    obj.PanelThickness.Value
                )
            )


        #
        # Back thickness
        #

        if hasattr(
            obj,
            "BackThickness"
        ):

            self.backThicknessSpin.setValue(
                float(
                    obj.BackThickness.Value
                )
            )


        #
        # Back inset
        #

        if hasattr(
            obj,
            "BackInset"
        ):

            self.backInsetSpin.setValue(
                float(
                    obj.BackInset.Value
                )
            )


    #
    # Update parameters
    #

    def updateParameters(
        self
    ):

        obj = self.parameters


        if obj is None:

            return


        #
        # Name
        #

        name = (
            self.nameEdit.text()
            .strip()
        )


        if not name:

            name = "Nuevo módulo"


        obj.ModuleName = name

        obj.Label = name


        #
        # Type
        #

        if hasattr(
            obj,
            "ModuleType"
        ):

            obj.ModuleType = (
                self.typeCombo.currentText()
            )


        #
        # Dimensions
        #

        obj.ModuleWidth = (
            self.widthSpin.value()
        )


        obj.ModuleHeight = (
            self.heightSpin.value()
        )


        obj.ModuleDepth = (
            self.depthSpin.value()
        )


        #
        # Thickness
        #

        obj.PanelThickness = (
            self.thicknessSpin.value()
        )


        obj.BackThickness = (
            self.backThicknessSpin.value()
        )


        #
        # Back inset
        #

        obj.BackInset = (
            self.backInsetSpin.value()
        )


    #
    # Recalculate
    #

    def recalculate(
        self
    ):

        self.updateParameters()


        if self.parameters is None:

            return


        proxy = self.parameters.Proxy


        if proxy is None:

            return


        #
        # Calculate parts
        #

        parts = proxy.calculateParts(
            self.parameters
        )


        #
        # Update table
        #

        self.partsTable.parts = parts


        self.partsTable.loadParts()


    #
    # Apply
    #

    def apply(
        self
    ):

        self.updateParameters()


        #
        # Recalculate
        #

        self.recalculate()


        #
        # Recompute document
        #

        if self.parameters is not None:

            if self.parameters.Document:

                self.parameters.Document.recompute()


        #
        # Accept dialog
        #

        self.accept()


    #
    # Get parameters
    #

    def getParameters(
        self
    ):

        return {

            "ModuleName":
                self.nameEdit.text().strip(),

            "ModuleType":
                self.typeCombo.currentText(),

            "ModuleWidth":
                self.widthSpin.value(),

            "ModuleHeight":
                self.heightSpin.value(),

            "ModuleDepth":
                self.depthSpin.value(),

            "PanelThickness":
                self.thicknessSpin.value(),

            "BackThickness":
                self.backThicknessSpin.value(),

            "BackInset":
                self.backInsetSpin.value()

        }


    #
    # Get parts
    #

    def getParts(
        self
    ):

        return self.partsTable.getData()