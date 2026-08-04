from PySide import QtWidgets

from library.material_library import MaterialLibrary


class PartTableDialog(QtWidgets.QDialog):


    def __init__(
        self,
        parts=None,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle(
            "Tabla de piezas"
        )

        self.resize(
            1200,
            600
        )

        self.parts = parts or []

        self.rows = []

        self.createUI()

        self.loadParts()


    #
    # UI
    #

    def createUI(
        self
    ):

        layout = QtWidgets.QVBoxLayout()


        #
        # Table
        #

        self.table = QtWidgets.QTableWidget()

        self.table.setColumnCount(
            8
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Nombre",
                "Código",
                "Tipo",
                "Función",
                "Longitud",
                "Anchura",
                "Espesor",
                "Material"
            ]
        )


        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )


        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )


        self.table.setAlternatingRowColors(
            True
        )


        self.table.horizontalHeader().setStretchLastSection(
            True
        )


        layout.addWidget(
            self.table
        )


        #
        # Buttons
        #
        # When the table is embedded inside
        # another dialog these buttons can
        # simply be hidden by the parent.
        #

        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.buttonLayout.addStretch()


        self.okButton = QtWidgets.QPushButton(
            "Aceptar"
        )


        self.cancelButton = QtWidgets.QPushButton(
            "Cancelar"
        )


        self.okButton.clicked.connect(
            self.accept
        )


        self.cancelButton.clicked.connect(
            self.reject
        )


        self.buttonLayout.addWidget(
            self.okButton
        )


        self.buttonLayout.addWidget(
            self.cancelButton
        )


        layout.addLayout(
            self.buttonLayout
        )


        self.setLayout(
            layout
        )


    #
    # Load parts
    #

    def loadParts(
        self
    ):

        self.table.setRowCount(
            0
        )

        self.rows = []


        #
        # Nothing to load
        #

        if not self.parts:

            return


        #
        # Load every part
        #

        for part in self.parts:

            rowData = self.getPartData(
                part
            )


            #
            # Ignore objects that are not
            # actually usable as parts.
            #

            if rowData is None:

                continue


            row = self.table.rowCount()


            self.table.insertRow(
                row
            )


            #
            # Name
            #

            nameEdit = QtWidgets.QLineEdit(
                rowData["Label"]
            )


            self.table.setCellWidget(
                row,
                0,
                nameEdit
            )


            #
            # Code
            #

            codeEdit = QtWidgets.QLineEdit(
                rowData["Code"]
            )


            self.table.setCellWidget(
                row,
                1,
                codeEdit
            )


            #
            # Type
            #

            typeCombo = QtWidgets.QComboBox()


            typeCombo.addItems(
                [
                    "",
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


            index = typeCombo.findText(
                rowData["PartType"]
            )


            if index >= 0:

                typeCombo.setCurrentIndex(
                    index
                )


            self.table.setCellWidget(
                row,
                2,
                typeCombo
            )


            #
            # Role
            #

            roleCombo = QtWidgets.QComboBox()


            roleCombo.addItems(
                [
                    "",
                    "Side",
                    "Top",
                    "Bottom",
                    "Back",
                    "Shelf",
                    "Door",
                    "Drawer",
                    "Custom"
                ]
            )


            index = roleCombo.findText(
                rowData["Role"]
            )


            if index >= 0:

                roleCombo.setCurrentIndex(
                    index
                )


            self.table.setCellWidget(
                row,
                3,
                roleCombo
            )


            #
            # Length
            #

            lengthSpin = self.createSpinBox()


            lengthSpin.setValue(
                self.quantityValue(
                    rowData["Length"]
                )
            )


            self.table.setCellWidget(
                row,
                4,
                lengthSpin
            )


            #
            # Width
            #

            widthSpin = self.createSpinBox()


            widthSpin.setValue(
                self.quantityValue(
                    rowData["Width"]
                )
            )


            self.table.setCellWidget(
                row,
                5,
                widthSpin
            )


            #
            # Thickness
            #

            thicknessSpin = self.createSpinBox()


            thicknessSpin.setValue(
                self.quantityValue(
                    rowData["Thickness"]
                )
            )


            self.table.setCellWidget(
                row,
                6,
                thicknessSpin
            )


            #
            # Material
            #

            materialCombo = self.createMaterialCombo(
                rowData["MaterialCode"]
            )


            self.table.setCellWidget(
                row,
                7,
                materialCombo
            )


            #
            # Store row
            #

            self.rows.append(
                {

                    "source":
                        part,

                    "name":
                        nameEdit,

                    "code":
                        codeEdit,

                    "type":
                        typeCombo,

                    "role":
                        roleCombo,

                    "length":
                        lengthSpin,

                    "width":
                        widthSpin,

                    "thickness":
                        thicknessSpin,

                    "material":
                        materialCombo

                }
            )


    #
    # Get normalized data from a part
    #

    def getPartData(
        self,
        part
    ):

        #
        # Dictionary
        #

        if isinstance(
            part,
            dict
        ):

            return {

                "Label":
                    str(
                        part.get(
                            "Label",
                            ""
                        )
                    ),

                "Code":
                    str(
                        part.get(
                            "Code",
                            ""
                        )
                    ),

                "PartType":
                    str(
                        part.get(
                            "PartType",
                            ""
                        )
                    ),

                "Role":
                    str(
                        part.get(
                            "Role",
                            ""
                        )
                    ),

                "Length":
                    part.get(
                        "Length",
                        0
                    ),

                "Width":
                    part.get(
                        "Width",
                        0
                    ),

                "Thickness":
                    part.get(
                        "Thickness",
                        0
                    ),

                "MaterialCode":
                    str(
                        part.get(
                            "MaterialCode",
                            part.get(
                                "Material",
                                ""
                            )
                        )
                    )

            }


        #
        # FreeCAD object
        #

        if not hasattr(
            part,
            "Label"
        ):

            return None


        #
        # A FeaturePython object may be something
        # other than a BosqoPart.
        #
        # Therefore Code is optional here.
        #

        code = str(
            getattr(
                part,
                "Code",
                ""
            )
        ).strip()


        partType = str(
            getattr(
                part,
                "PartType",
                ""
            )
        ).strip()


        role = str(
            getattr(
                part,
                "Role",
                ""
            )
        ).strip()


        #
        # If the object has none of the
        # BosqoPart identification properties,
        # do not treat it as a part.
        #

        if (
            not code
            and not partType
            and not role
        ):

            return None


        return {

            "Label":
                str(
                    getattr(
                        part,
                        "Label",
                        ""
                    )
                ),

            "Code":
                code,

            "PartType":
                partType,

            "Role":
                role,

            "Length":
                getattr(
                    part,
                    "Length",
                    0
                ),

            "Width":
                getattr(
                    part,
                    "Width",
                    0
                ),

            "Thickness":
                getattr(
                    part,
                    "Thickness",
                    0
                ),

            "MaterialCode":
                str(
                    getattr(
                        part,
                        "MaterialCode",
                        ""
                    )
                )

        }


    #
    # Create material combo
    #

    def createMaterialCombo(
        self,
        currentCode=""
    ):

        combo = QtWidgets.QComboBox()


        combo.addItem(
            "— Sin material —",
            ""
        )


        materials = MaterialLibrary.all()


        for material in materials:

            if not isinstance(
                material,
                dict
            ):

                continue


            code = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()


            if not code:

                continue


            name = str(
                material.get(
                    "MaterialName",
                    ""
                )
            ).strip()


            if name:

                text = (
                    code
                    + " — "
                    + name
                )

            else:

                text = code


            combo.addItem(
                text,
                code
            )


        currentCode = str(
            currentCode
        ).strip()


        index = combo.findData(
            currentCode
        )


        if index >= 0:

            combo.setCurrentIndex(
                index
            )


        return combo


    #
    # Create SpinBox
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
    # Quantity value
    #

    def quantityValue(
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


    #
    # Get data
    #

    def getData(
        self
    ):

        data = []


        for row in self.rows:

            materialCode = (
                row["material"].currentData()
            )


            if materialCode is None:

                materialCode = ""


            data.append(
                {

                    "Label":
                        row["name"]
                        .text()
                        .strip(),

                    "Code":
                        row["code"]
                        .text()
                        .strip(),

                    "PartType":
                        row["type"]
                        .currentText(),

                    "Role":
                        row["role"]
                        .currentText(),

                    "Length":
                        row["length"]
                        .value(),

                    "Width":
                        row["width"]
                        .value(),

                    "Thickness":
                        row["thickness"]
                        .value(),

                    "MaterialCode":
                        materialCode

                }
            )


        return data


    #
    # Apply changes to real BosqoPart
    #

    def applyChanges(
        self
    ):

        document = None


        for row in self.rows:

            part = row["source"]


            #
            # Only real FreeCAD objects
            #

            if isinstance(
                part,
                dict
            ):

                continue


            #
            # Verify that this is a BosqoPart.
            #

            if not hasattr(
                part,
                "Proxy"
            ):

                continue


            proxy = part.Proxy


            if proxy is None:

                continue


            if type(proxy).__name__ != "BosqoPart":

                continue


            #
            # Name
            #

            name = (
                row["name"]
                .text()
                .strip()
            )


            if name:

                part.Label = name


            #
            # Code
            #

            if hasattr(
                part,
                "Code"
            ):

                part.Code = (
                    row["code"]
                    .text()
                    .strip()
                )


            #
            # Type
            #

            if hasattr(
                part,
                "PartType"
            ):

                part.PartType = (
                    row["type"]
                    .currentText()
                )


            #
            # Role
            #

            if hasattr(
                part,
                "Role"
            ):

                part.Role = (
                    row["role"]
                    .currentText()
                )


            #
            # Dimensions
            #

            if hasattr(
                part,
                "Length"
            ):

                part.Length = (
                    row["length"]
                    .value()
                )


            if hasattr(
                part,
                "Width"
            ):

                part.Width = (
                    row["width"]
                    .value()
                )


            if hasattr(
                part,
                "Thickness"
            ):

                part.Thickness = (
                    row["thickness"]
                    .value()
                )


            #
            # Material
            #

            if hasattr(
                part,
                "MaterialCode"
            ):

                materialCode = (
                    row["material"]
                    .currentData()
                )


                if materialCode is None:

                    materialCode = ""


                part.MaterialCode = (
                    materialCode
                )


            #
            # Recompute
            #

            part.touch()


            if document is None:

                document = part.Document


        #
        # Recompute document
        #

        if document is not None:

            document.recompute()