from PySide import QtWidgets

from library.material_library import MaterialLibrary


class PartDialog(QtWidgets.QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle(
            "Nueva pieza"
        )

        self.resize(
            350,
            400
        )

        self.createUI()


    #
    # Create UI
    #

    def createUI(
        self
    ):

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
                "Balda",
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

        self.lengthSpin.setSuffix(
            " mm"
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

        self.widthSpin.setSuffix(
            " mm"
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

        self.thicknessSpin.setSuffix(
            " mm"
        )

        layout.addRow(
            "Espesor:",
            self.thicknessSpin
        )


        #
        # Material
        #

        self.materialCombo = QtWidgets.QComboBox()

        self.loadMaterials()

        layout.addRow(
            "Material:",
            self.materialCombo
        )


        #
        # Material change
        #

        self.materialCombo.currentIndexChanged.connect(
            self.onMaterialChanged
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
    # Load materials
    #

    def loadMaterials(
        self
    ):

        self.materialCombo.clear()


        #
        # No material
        #

        self.materialCombo.addItem(
            "— Sin material —",
            ""
        )


        #
        # Get materials from persistent library
        #

        materials = MaterialLibrary.all()


        #
        # Materials from JSON are dictionaries
        #

        for material in materials:

            if not isinstance(
                material,
                dict
            ):

                continue


            #
            # Code
            #

            code = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()


            if not code:

                continue


            #
            # Name
            #

            name = str(
                material.get(
                    "MaterialName",
                    ""
                )
            ).strip()


            #
            # Display text
            #

            if name:

                text = (
                    code
                    + " — "
                    + name
                )

            else:

                text = code


            #
            # Add material
            #

            self.materialCombo.addItem(
                text,
                code
            )


    #
    # Material changed
    #

    def onMaterialChanged(
        self,
        index
    ):

        code = self.materialCombo.itemData(
            index
        )


        if not code:

            return


        material = MaterialLibrary.get(
            code
        )


        if material is None:

            return


        #
        # Get thickness
        #

        if isinstance(
            material,
            dict
        ):

            thickness = material.get(
                "Thickness",
                None
            )

        else:

            thickness = getattr(
                material,
                "Thickness",
                None
            )


        #
        # Update thickness
        #

        if thickness is None:

            return


        try:

            self.thicknessSpin.setValue(
                float(
                    thickness.Value
                )
            )

        except Exception:

            try:

                self.thicknessSpin.setValue(
                    float(
                        thickness
                    )
                )

            except Exception:

                pass


    #
    # Return data
    #

    def getData(
        self
    ):

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

            "MaterialCode":
                self.materialCombo.currentData()

        }