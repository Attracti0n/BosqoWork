from PySide import QtWidgets

from library.material_library import MaterialLibrary


class MaterialLibraryDialog(QtWidgets.QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle(
            "Biblioteca de materiales"
        )

        self.resize(
            900,
            550
        )

        self.createUI()

        self.loadMaterials()


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
            "Biblioteca de materiales"
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
        # Table
        #

        self.table = QtWidgets.QTableWidget()

        self.table.setColumnCount(
            9
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Código",
                "Material",
                "Tipo",
                "Espesor",
                "Largo",
                "Ancho",
                "Proveedor",
                "Precio",
                "Unidad"
            ]
        )

        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )

        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.horizontalHeader().setStretchLastSection(
            True
        )

        self.table.doubleClicked.connect(
            self.editMaterial
        )

        mainLayout.addWidget(
            self.table
        )


        #
        # Buttons
        #

        buttonLayout = QtWidgets.QHBoxLayout()


        self.newButton = QtWidgets.QPushButton(
            "Nuevo"
        )

        self.editButton = QtWidgets.QPushButton(
            "Editar"
        )

        self.duplicateButton = QtWidgets.QPushButton(
            "Duplicar"
        )

        self.deleteButton = QtWidgets.QPushButton(
            "Eliminar"
        )

        self.reloadButton = QtWidgets.QPushButton(
            "Recargar"
        )


        buttonLayout.addWidget(
            self.newButton
        )

        buttonLayout.addWidget(
            self.editButton
        )

        buttonLayout.addWidget(
            self.duplicateButton
        )

        buttonLayout.addWidget(
            self.deleteButton
        )

        buttonLayout.addStretch()

        buttonLayout.addWidget(
            self.reloadButton
        )


        mainLayout.addLayout(
            buttonLayout
        )


        #
        # Close button
        #

        closeButton = QtWidgets.QPushButton(
            "Cerrar"
        )

        closeButton.clicked.connect(
            self.accept
        )

        mainLayout.addWidget(
            closeButton
        )


        #
        # Connections
        #

        self.newButton.clicked.connect(
            self.newMaterial
        )

        self.editButton.clicked.connect(
            self.editMaterial
        )

        self.duplicateButton.clicked.connect(
            self.duplicateMaterial
        )

        self.deleteButton.clicked.connect(
            self.deleteMaterial
        )

        self.reloadButton.clicked.connect(
            self.reloadMaterials
        )


        self.setLayout(
            mainLayout
        )


    #
    # Load materials
    #

    def loadMaterials(
        self
    ):

        self.table.setRowCount(
            0
        )


        materials = MaterialLibrary.all()


        for material in materials:

            if not isinstance(
                material,
                dict
            ):

                continue


            row = self.table.rowCount()

            self.table.insertRow(
                row
            )


            code = str(
                material.get(
                    "Code",
                    ""
                )
            )

            name = str(
                material.get(
                    "MaterialName",
                    ""
                )
            )

            materialType = str(
                material.get(
                    "MaterialType",
                    ""
                )
            )

            thickness = self.number(
                material.get(
                    "Thickness",
                    ""
                )
            )

            sheetLength = self.number(
                material.get(
                    "SheetLength",
                    ""
                )
            )

            sheetWidth = self.number(
                material.get(
                    "SheetWidth",
                    ""
                )
            )

            supplier = str(
                material.get(
                    "Supplier",
                    ""
                )
            )

            price = self.number(
                material.get(
                    "Price",
                    ""
                )
            )

            currency = str(
                material.get(
                    "Currency",
                    "EUR"
                )
            )

            unit = self.getPriceUnit(
                materialType
            )


            values = [

                code,

                name,

                materialType,

                thickness,

                sheetLength,

                sheetWidth,

                supplier,

                price,

                unit

            ]


            for column, value in enumerate(
                values
            ):

                item = QtWidgets.QTableWidgetItem(
                    str(
                        value
                    )
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )


        #
        # Resize columns
        #

        self.table.resizeColumnsToContents()


        #
        # Set useful widths
        #

        self.table.setColumnWidth(
            0,
            100
        )

        self.table.setColumnWidth(
            1,
            220
        )

        self.table.setColumnWidth(
            2,
            110
        )

        self.table.setColumnWidth(
            6,
            140
        )


    #
    # Number formatting
    #

    def number(
        self,
        value
    ):

        if value is None:

            return ""


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
                number
            )

        except Exception:

            return str(
                value
            )


    #
    # Price unit
    #

    def getPriceUnit(
        self,
        materialType
    ):

        materialType = str(
            materialType
        ).strip().lower()


        if materialType == "tablero":

            return "€/m²"


        if materialType == "canto":

            return "€/ml"


        if materialType == "herraje":

            return "€/unidad"


        return "—"


    #
    # Get selected material
    #

    def getSelectedMaterial(
        self
    ):

        row = self.table.currentRow()


        if row < 0:

            return None


        item = self.table.item(
            row,
            0
        )


        if item is None:

            return None


        code = item.text().strip()


        if not code:

            return None


        materials = MaterialLibrary.all()


        for material in materials:

            if not isinstance(
                material,
                dict
            ):

                continue


            storedCode = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()


            if storedCode == code:

                return dict(
                    material
                )


        return None


    #
    # New material
    #

    def newMaterial(
        self
    ):

        dialog = MaterialEditDialog(
            parent=self
        )


        if dialog.exec_() != QtWidgets.QDialog.Accepted:

            return


        data = dialog.getData()


        if not data.get(
            "Code",
            ""
        ).strip():

            return


        if MaterialLibrary.exists(
            data["Code"]
        ):

            QtWidgets.QMessageBox.warning(
                self,
                "Material existente",
                "Ya existe un material con ese código."
            )

            return


        if MaterialLibrary.add(
            data
        ):

            self.reloadMaterials()

        else:

            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                "No se ha podido guardar el material."
            )


    #
    # Edit material
    #

    def editMaterial(
        self,
        *args
    ):

        material = self.getSelectedMaterial()


        if material is None:

            QtWidgets.QMessageBox.information(
                self,
                "Editar material",
                "Selecciona primero un material."
            )

            return


        originalCode = material.get(
            "Code",
            ""
        )


        dialog = MaterialEditDialog(
            material=material,
            parent=self
        )


        if dialog.exec_() != QtWidgets.QDialog.Accepted:

            return


        data = dialog.getData()


        newCode = data.get(
            "Code",
            ""
        ).strip()


        if not newCode:

            return


        #
        # Code changed
        #

        if newCode != originalCode:

            if MaterialLibrary.exists(
                newCode
            ):

                QtWidgets.QMessageBox.warning(
                    self,
                    "Material existente",
                    "Ya existe otro material con ese código."
                )

                return


            #
            # Remove old material
            #

            MaterialLibrary.remove(
                originalCode
            )


            #
            # Add with new code
            #

            if not MaterialLibrary.add(
                data
            ):

                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    "No se ha podido guardar el material."
                )

                return


        else:

            if not MaterialLibrary.update(
                data
            ):

                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    "No se ha podido actualizar el material."
                )

                return


        self.reloadMaterials()


    #
    # Duplicate material
    #

    def duplicateMaterial(
        self
    ):

        material = self.getSelectedMaterial()


        if material is None:

            QtWidgets.QMessageBox.information(
                self,
                "Duplicar material",
                "Selecciona primero un material."
            )

            return


        material["Code"] = (
            str(
                material.get(
                    "Code",
                    ""
                )
            )
            + "_COPY"
        )


        material["MaterialName"] = (
            str(
                material.get(
                    "MaterialName",
                    ""
                )
            )
            + " copia"
        )


        dialog = MaterialEditDialog(
            material=material,
            parent=self
        )


        if dialog.exec_() != QtWidgets.QDialog.Accepted:

            return


        data = dialog.getData()


        code = data.get(
            "Code",
            ""
        ).strip()


        if not code:

            return


        if MaterialLibrary.exists(
            code
        ):

            QtWidgets.QMessageBox.warning(
                self,
                "Material existente",
                "Ya existe un material con ese código."
            )

            return


        if MaterialLibrary.add(
            data
        ):

            self.reloadMaterials()

        else:

            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                "No se ha podido duplicar el material."
            )


    #
    # Delete material
    #

    def deleteMaterial(
        self
    ):

        material = self.getSelectedMaterial()


        if material is None:

            QtWidgets.QMessageBox.information(
                self,
                "Eliminar material",
                "Selecciona primero un material."
            )

            return


        code = str(
            material.get(
                "Code",
                ""
            )
        )


        name = str(
            material.get(
                "MaterialName",
                ""
            )
        )


        result = QtWidgets.QMessageBox.question(
            self,
            "Eliminar material",
            (
                "¿Seguro que quieres eliminar el material?\n\n"
                + code
                + " — "
                + name
            ),
            QtWidgets.QMessageBox.Yes
            | QtWidgets.QMessageBox.No
        )


        if result != QtWidgets.QMessageBox.Yes:

            return


        if MaterialLibrary.remove(
            code
        ):

            self.reloadMaterials()

        else:

            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                "No se ha podido eliminar el material."
            )


    #
    # Reload
    #

    def reloadMaterials(
        self
    ):

        MaterialLibrary.reload()

        self.loadMaterials()


# ============================================================
# MATERIAL EDIT DIALOG
# ============================================================


class MaterialEditDialog(QtWidgets.QDialog):

    def __init__(
        self,
        material=None,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.material = (
            dict(
                material
            )
            if isinstance(
                material,
                dict
            )
            else {}
        )


        self.setWindowTitle(
            "Editar material"
            if material
            else "Nuevo material"
        )


        self.resize(
            450,
            550
        )


        self.createUI()

        self.loadData()


    #
    # Create UI
    #

    def createUI(
        self
    ):

        layout = QtWidgets.QFormLayout()


        #
        # Code
        #

        self.codeEdit = QtWidgets.QLineEdit()

        layout.addRow(
            "Código:",
            self.codeEdit
        )


        #
        # Material name
        #

        self.nameEdit = QtWidgets.QLineEdit()

        layout.addRow(
            "Material:",
            self.nameEdit
        )


        #
        # Material type
        #

        self.typeCombo = QtWidgets.QComboBox()

        self.typeCombo.addItems(
            [
                "Tablero",
                "Canto",
                "Herraje",
                "Otro"
            ]
        )

        layout.addRow(
            "Tipo:",
            self.typeCombo
        )


        #
        # Category
        #

        self.categoryEdit = QtWidgets.QLineEdit()

        layout.addRow(
            "Categoría:",
            self.categoryEdit
        )


        #
        # Thickness
        #

        self.thicknessSpin = QtWidgets.QDoubleSpinBox()

        self.thicknessSpin.setRange(
            0,
            100
        )

        self.thicknessSpin.setDecimals(
            2
        )

        self.thicknessSpin.setSuffix(
            " mm"
        )

        layout.addRow(
            "Espesor:",
            self.thicknessSpin
        )


        #
        # Sheet length
        #

        self.lengthSpin = QtWidgets.QDoubleSpinBox()

        self.lengthSpin.setRange(
            0,
            10000
        )

        self.lengthSpin.setDecimals(
            2
        )

        self.lengthSpin.setSuffix(
            " mm"
        )

        layout.addRow(
            "Largo:",
            self.lengthSpin
        )


        #
        # Sheet width
        #

        self.widthSpin = QtWidgets.QDoubleSpinBox()

        self.widthSpin.setRange(
            0,
            10000
        )

        self.widthSpin.setDecimals(
            2
        )

        self.widthSpin.setSuffix(
            " mm"
        )

        layout.addRow(
            "Ancho:",
            self.widthSpin
        )


        #
        # Supplier
        #

        self.supplierEdit = QtWidgets.QLineEdit()

        layout.addRow(
            "Proveedor:",
            self.supplierEdit
        )


        #
        # Finish
        #

        self.finishEdit = QtWidgets.QLineEdit()

        layout.addRow(
            "Acabado:",
            self.finishEdit
        )


        #
        # Grain direction
        #

        self.grainCombo = QtWidgets.QComboBox()

        self.grainCombo.addItems(
            [
                "Sin veta",
                "Longitudinal",
                "Transversal"
            ]
        )

        layout.addRow(
            "Dirección veta:",
            self.grainCombo
        )


        #
        # Price
        #

        self.priceSpin = QtWidgets.QDoubleSpinBox()

        self.priceSpin.setRange(
            0,
            1000000
        )

        self.priceSpin.setDecimals(
            2
        )

        self.priceSpin.setSuffix(
            " €"
        )

        layout.addRow(
            "Precio:",
            self.priceSpin
        )


        #
        # Price unit
        #

        self.unitLabel = QtWidgets.QLabel(
            "—"
        )

        layout.addRow(
            "Unidad:",
            self.unitLabel
        )


        #
        # Currency
        #

        self.currencyCombo = QtWidgets.QComboBox()

        self.currencyCombo.addItems(
            [
                "EUR",
                "USD",
                "GBP"
            ]
        )

        layout.addRow(
            "Moneda:",
            self.currencyCombo
        )


        #
        # Type changed
        #

        self.typeCombo.currentIndexChanged.connect(
            self.updatePriceUnit
        )


        #
        # Buttons
        #

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel
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
    # Load data
    #

    def loadData(
        self
    ):

        if not self.material:

            self.updatePriceUnit()

            return


        self.codeEdit.setText(
            str(
                self.material.get(
                    "Code",
                    ""
                )
            )
        )


        self.nameEdit.setText(
            str(
                self.material.get(
                    "MaterialName",
                    ""
                )
            )
        )


        materialType = str(
            self.material.get(
                "MaterialType",
                ""
            )
        )


        index = self.typeCombo.findText(
            materialType
        )


        if index >= 0:

            self.typeCombo.setCurrentIndex(
                index
            )


        self.categoryEdit.setText(
            str(
                self.material.get(
                    "Category",
                    ""
                )
            )
        )


        self.setSpinValue(
            self.thicknessSpin,
            self.material.get(
                "Thickness",
                0
            )
        )


        self.setSpinValue(
            self.lengthSpin,
            self.material.get(
                "SheetLength",
                0
            )
        )


        self.setSpinValue(
            self.widthSpin,
            self.material.get(
                "SheetWidth",
                0
            )
        )


        self.supplierEdit.setText(
            str(
                self.material.get(
                    "Supplier",
                    ""
                )
            )
        )


        self.finishEdit.setText(
            str(
                self.material.get(
                    "Finish",
                    ""
                )
            )
        )


        grain = str(
            self.material.get(
                "GrainDirection",
                ""
            )
        )


        index = self.grainCombo.findText(
            grain
        )


        if index >= 0:

            self.grainCombo.setCurrentIndex(
                index
            )


        self.setSpinValue(
            self.priceSpin,
            self.material.get(
                "Price",
                0
            )
        )


        currency = str(
            self.material.get(
                "Currency",
                "EUR"
            )
        )


        index = self.currencyCombo.findText(
            currency
        )


        if index >= 0:

            self.currencyCombo.setCurrentIndex(
                index
            )


        self.updatePriceUnit()


    #
    # Set spin value
    #

    def setSpinValue(
        self,
        widget,
        value
    ):

        try:

            widget.setValue(
                float(
                    value
                )
            )

        except Exception:

            widget.setValue(
                0
            )


    #
    # Update price unit
    #

    def updatePriceUnit(
        self,
        index=None
    ):

        materialType = self.typeCombo.currentText()

        materialType = materialType.lower()


        if materialType == "tablero":

            unit = "€/m²"


        elif materialType == "canto":

            unit = "€/ml"


        elif materialType == "herraje":

            unit = "€/unidad"


        else:

            unit = "—"


        self.unitLabel.setText(
            unit
        )


    #
    # Get data
    #

    def getData(
        self
    ):

        return {

            "Code":
                self.codeEdit.text().strip(),

            "MaterialName":
                self.nameEdit.text().strip(),

            "MaterialType":
                self.typeCombo.currentText(),

            "Category":
                self.categoryEdit.text().strip(),

            "Thickness":
                self.thicknessSpin.value(),

            "SheetLength":
                self.lengthSpin.value(),

            "SheetWidth":
                self.widthSpin.value(),

            "Supplier":
                self.supplierEdit.text().strip(),

            "Finish":
                self.finishEdit.text().strip(),

            "GrainDirection":
                self.grainCombo.currentText(),

            "Price":
                self.priceSpin.value(),

            "Currency":
                self.currencyCombo.currentText()

        }