from PySide import QtWidgets


class PartDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "Nueva pieza"
        )

        self.resize(
            350,
            400
        )

        self.createUI()


    def createUI(self):

        layout = QtWidgets.QFormLayout()


        #
        # Name
        #

        self.nameEdit = QtWidgets.QLineEdit()

        self.nameEdit.setText(
            "Nueva pieza"
        )


        layout.addRow(
            "Nombre:",
            self.nameEdit
        )


        #
        # Type
        #

        self.typeCombo = QtWidgets.QComboBox()

        self.typeCombo.addItems(
            [
                "Panel lateral",
                "Estante",
                "Fondo",
                "Base",
                "Travesaño",
                "Puerta",
                "Frente cajón",
                "Personalizado"
            ]
        )


        layout.addRow(
            "Tipo:",
            self.typeCombo
        )


        #
        # Dimensions
        #

        self.lengthSpin = QtWidgets.QDoubleSpinBox()

        self.lengthSpin.setRange(
            1,
            5000
        )

        self.lengthSpin.setValue(
            600
        )


        layout.addRow(
            "Longitud:",
            self.lengthSpin
        )


        self.widthSpin = QtWidgets.QDoubleSpinBox()

        self.widthSpin.setRange(
            1,
            5000
        )

        self.widthSpin.setValue(
            560
        )


        layout.addRow(
            "Anchura:",
            self.widthSpin
        )


        self.thicknessSpin = QtWidgets.QDoubleSpinBox()

        self.thicknessSpin.setRange(
            1,
            100
        )

        self.thicknessSpin.setValue(
            18
        )


        layout.addRow(
            "Espesor:",
            self.thicknessSpin
        )


        #
        # Material
        #

        self.materialEdit = QtWidgets.QLineEdit()

        self.materialEdit.setText(
            "MDF 18"
        )


        layout.addRow(
            "Material:",
            self.materialEdit
        )


        #
        # Buttons
        #

        buttons = QtWidgets.QDialogButtonBox()

        buttons.addButton(
            QtWidgets.QDialogButtonBox.Ok
        )

        buttons.addButton(
            QtWidgets.QDialogButtonBox.Cancel
        )


        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )


        layout.addRow(
            buttons
        )


        self.setLayout(
            layout
        )


    #
    # Return data
    #

    def getData(self):

        return {

            "Label":
                self.nameEdit.text(),

            "PartType":
                self.typeCombo.currentText(),

            "Length":
                self.lengthSpin.value(),

            "Width":
                self.widthSpin.value(),

            "Thickness":
                self.thicknessSpin.value(),

            "Material":
                self.materialEdit.text()

        }