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


    # =========================================================
    # CREATE UI
    # =========================================================

    def createUI(
        self
    ):

        layout = QtWidgets.QFormLayout()


        # =====================================================
        # NAME
        # =====================================================

        self.nameEdit = QtWidgets.QLineEdit()

        self.nameEdit.setText(
            "Nueva pieza"
        )

        layout.addRow(
            "Nombre:",
            self.nameEdit
        )


        # =====================================================
        # DIMENSIONS
        # =====================================================

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


        # =====================================================
        # MATERIAL
        # =====================================================

        self.materialCombo = (
            QtWidgets.QComboBox()
        )

        self.loadMaterials()

        layout.addRow(
            "Material:",
            self.materialCombo
        )


        # =====================================================
        # MATERIAL CHANGE
        # =====================================================

        self.materialCombo.currentIndexChanged.connect(
            self.onMaterialChanged
        )


        # =====================================================
        # BUTTONS
        # =====================================================

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


    # =========================================================
    # LOAD MATERIALS
    # =========================================================

    def loadMaterials(
        self
    ):

        self.materialCombo.clear()


        # =====================================================
        # NO MATERIAL
        # =====================================================

        self.materialCombo.addItem(
            "— Sin material —",
            ""
        )


        # =====================================================
        # GET MATERIALS
        # =====================================================

        try:

            materials = (
                MaterialLibrary.all()
            )

        except Exception:

            materials = []


        # =====================================================
        # ONLY BOARDS
        # =====================================================

        for material in materials:

            if not isinstance(
                material,
                dict
            ):

                continue


            # -------------------------------------------------
            # MATERIAL TYPE
            # -------------------------------------------------

            materialType = str(
                material.get(
                    "MaterialType",
                    ""
                )
            ).strip()


            #
            # Only Tablero is a base
            # material for a new part.
            #

            if materialType.lower() != "tablero":

                continue


            # -------------------------------------------------
            # CODE
            # -------------------------------------------------

            code = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()


            if not code:

                continue


            # -------------------------------------------------
            # NAME
            # -------------------------------------------------

            name = str(
                material.get(
                    "MaterialName",
                    ""
                )
            ).strip()


            # -------------------------------------------------
            # DISPLAY TEXT
            # -------------------------------------------------

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


            # -------------------------------------------------
            # ADD MATERIAL
            # -------------------------------------------------

            self.materialCombo.addItem(
                text,
                code
            )


    # =========================================================
    # MATERIAL CHANGED
    # =========================================================

    def onMaterialChanged(
        self,
        index
    ):

        code = (
            self.materialCombo.itemData(
                index
            )
        )


        if not code:

            return


        try:

            material = MaterialLibrary.get(
                code
            )

        except Exception:

            material = None


        if material is None:

            return


        # =====================================================
        # GET THICKNESS
        # =====================================================

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


        # =====================================================
        # UPDATE THICKNESS
        # =====================================================

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


    # =========================================================
    # RETURN DATA
    # =========================================================

    def getData(
        self
    ):

        return {

            "Label":
                self.nameEdit.text(),

            "Length":
                self.lengthSpin.value(),

            "Width":
                self.widthSpin.value(),

            "Thickness":
                self.thicknessSpin.value(),

            "MaterialCode":
                self.materialCombo.currentData()

        }