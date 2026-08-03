from PySide import QtWidgets

from library.module_templates import MODULE_TEMPLATES


class ModuleDialog(QtWidgets.QDialog):


    def __init__(
        self,
        data=None,
        parent=None
    ):

        super().__init__(parent)

        self.data = data or {}

        self.setWindowTitle(
            "Nuevo módulo"
        )

        self.resize(
            350,
            350
        )

        self.createUI()

        self.loadData()


    #
    # UI
    #

    def createUI(self):

        layout = QtWidgets.QFormLayout()


        #
        # Name
        #

        self.nameEdit = QtWidgets.QLineEdit()

        layout.addRow(
            "Nombre:",
            self.nameEdit
        )


        #
        # Template
        #

        self.templateCombo = QtWidgets.QComboBox()

        for key, template in MODULE_TEMPLATES.items():

            self.templateCombo.addItem(
                template["name"],
                key
            )

        layout.addRow(
            "Tipo:",
            self.templateCombo
        )


        #
        # Width
        #

        self.widthSpin = QtWidgets.QDoubleSpinBox()

        self.widthSpin.setRange(
            1,
            5000
        )

        layout.addRow(
            "Ancho:",
            self.widthSpin
        )


        #
        # Height
        #

        self.heightSpin = QtWidgets.QDoubleSpinBox()

        self.heightSpin.setRange(
            1,
            5000
        )

        layout.addRow(
            "Alto:",
            self.heightSpin
        )


        #
        # Depth
        #

        self.depthSpin = QtWidgets.QDoubleSpinBox()

        self.depthSpin.setRange(
            1,
            5000
        )

        layout.addRow(
            "Fondo:",
            self.depthSpin
        )


        #
        # Buttons
        #

        buttons = QtWidgets.QDialogButtonBox(

            QtWidgets.QDialogButtonBox.Ok |
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
    # Load initial data
    #

    def loadData(self):

        self.nameEdit.setText(

            self.data.get(
                "Label",
                "Nuevo módulo"
            )

        )


        width = self.data.get(
            "Width",
            600
        )

        height = self.data.get(
            "Height",
            720
        )

        depth = self.data.get(
            "Depth",
            560
        )


        try:

            width = float(width)

        except Exception:

            width = float(width.Value)


        try:

            height = float(height)

        except Exception:

            height = float(height.Value)


        try:

            depth = float(depth)

        except Exception:

            depth = float(depth.Value)


        self.widthSpin.setValue(width)

        self.heightSpin.setValue(height)

        self.depthSpin.setValue(depth)


        template = self.data.get(
            "Template",
            None
        )

        if template is not None:

            index = self.templateCombo.findData(
                template
            )

            if index >= 0:

                self.templateCombo.setCurrentIndex(
                    index
                )


    #
    # Result
    #

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