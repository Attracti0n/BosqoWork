from PySide import QtWidgets

from library.module_templates import MODULE_TEMPLATES



class ModuleDialog(QtWidgets.QDialog):


    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "Nuevo módulo"
        )

        self.resize(
            350,
            350
        )

        self.createUI()



    def createUI(self):

        layout = QtWidgets.QFormLayout()


        #
        # Name
        #

        self.nameEdit = QtWidgets.QLineEdit()

        self.nameEdit.setText(
            "Nuevo módulo"
        )

        layout.addRow(
            "Nombre:",
            self.nameEdit
        )


        #
        # Template
        #

        self.templateCombo = QtWidgets.QComboBox()


        for key, data in MODULE_TEMPLATES.items():

            self.templateCombo.addItem(
                data["name"],
                key
            )


        layout.addRow(
            "Tipo:",
            self.templateCombo
        )


        #
        # Dimensions
        #

        self.widthSpin = QtWidgets.QDoubleSpinBox()

        self.widthSpin.setRange(
            1,
            5000
        )

        self.widthSpin.setValue(
            600
        )


        layout.addRow(
            "Ancho:",
            self.widthSpin
        )



        self.heightSpin = QtWidgets.QDoubleSpinBox()

        self.heightSpin.setRange(
            1,
            5000
        )

        self.heightSpin.setValue(
            720
        )


        layout.addRow(
            "Alto:",
            self.heightSpin
        )



        self.depthSpin = QtWidgets.QDoubleSpinBox()

        self.depthSpin.setRange(
            1,
            5000
        )

        self.depthSpin.setValue(
            560
        )


        layout.addRow(
            "Fondo:",
            self.depthSpin
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



    def getData(self):

        return {

            "Label":
                self.nameEdit.text(),


            "Template":
                self.templateCombo.currentData(),


            "Width":
                self.widthSpin.value(),


            "Height":
                self.heightSpin.value(),


            "Depth":
                self.depthSpin.value()

        }