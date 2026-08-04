from PySide import QtWidgets, QtCore, QtGui


class MaterialDialog(QtWidgets.QDialog):


    MATERIAL_TYPES = [

        "Tablero",
        "Canto",
        "Herraje",
        "Consumible",
        "Embalaje",
        "Otro"

    ]


    CATEGORIES = {

        "Tablero": [

            "MDF",
            "Aglomerado",
            "Contrachapado",
            "OSB",
            "HDF",
            "Madera maciza",
            "Tablero alistonado",
            "Otro"

        ],

        "Canto": [

            "ABS",
            "PVC",
            "Melamina",
            "Chapa natural",
            "Madera maciza",
            "Otro"

        ],

        "Herraje": [

            "Bisagra",
            "Corredera",
            "Tirador",
            "Conector",
            "Soporte",
            "Pata",
            "Otro"

        ],

        "Consumible": [

            "Adhesivo",
            "Tornillería",
            "Lija",
            "Producto de acabado",
            "Otro"

        ],

        "Embalaje": [

            "Cartón",
            "Plástico",
            "Espuma",
            "Protección",
            "Otro"

        ],

        "Otro": [

            "Otro"

        ]

    }


    SUPPLIERS = [

        "Gabarro",
        "Emedec",
        "Esteba",
        "Moldyport",
        "Barnisol",
        "Isaval",
        "Emuca",
        "Blum",
        "Hettich",
        "Otro"

    ]


    FINISHES = [

        "Crudo",
        "Melamina",
        "Chapado natural",
        "Lacado",
        "Laminado",
        "HPL",
        "Barnizado",
        "Pintado",
        "Otro"

    ]


    GRAIN_DIRECTIONS = [

        "Sin veta",
        "Longitudinal",
        "Transversal",
        "Ambas direcciones"

    ]


    PRICE_UNITS = [

        "€/m²",
        "€/m",
        "€/ud"

    ]


    DEFAULT_PRICE_UNITS = {

        "Tablero": "€/m²",
        "Canto": "€/m",
        "Herraje": "€/ud",
        "Consumible": "€/ud",
        "Embalaje": "€/ud",
        "Otro": "€/ud"

    }


    def __init__(
        self,
        parent=None,
        data=None
    ):

        super().__init__(
            parent
        )


        self.data = data or {}


        self.setWindowTitle(
            "Nuevo material"
        )


        self.resize(
            450,
            650
        )


        self.createUI()


        self.loadData()



    #
    # UI
    #

    def createUI(
        self
    ):

        main_layout = QtWidgets.QVBoxLayout()


        form_layout = QtWidgets.QFormLayout()


        #
        # Code
        #

        self.codeEdit = QtWidgets.QLineEdit()


        form_layout.addRow(
            "Código:",
            self.codeEdit
        )


        #
        # Name
        #

        self.nameEdit = QtWidgets.QLineEdit()


        form_layout.addRow(
            "Nombre:",
            self.nameEdit
        )


        #
        # Material type
        #

        self.typeCombo = QtWidgets.QComboBox()


        self.typeCombo.addItems(
            self.MATERIAL_TYPES
        )


        self.typeCombo.currentTextChanged.connect(
            self.updateCategories
        )


        self.typeCombo.currentTextChanged.connect(
            self.updatePriceUnit
        )


        form_layout.addRow(
            "Tipo:",
            self.typeCombo
        )


        #
        # Category
        #

        self.categoryCombo = QtWidgets.QComboBox()


        form_layout.addRow(
            "Categoría:",
            self.categoryCombo
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


        form_layout.addRow(
            "Espesor:",
            self.thicknessSpin
        )


        #
        # Sheet length
        #

        self.sheetLengthSpin = QtWidgets.QDoubleSpinBox()


        self.sheetLengthSpin.setRange(
            0,
            10000
        )


        self.sheetLengthSpin.setDecimals(
            2
        )


        self.sheetLengthSpin.setSuffix(
            " mm"
        )


        form_layout.addRow(
            "Largo tablero:",
            self.sheetLengthSpin
        )


        #
        # Sheet width
        #

        self.sheetWidthSpin = QtWidgets.QDoubleSpinBox()


        self.sheetWidthSpin.setRange(
            0,
            10000
        )


        self.sheetWidthSpin.setDecimals(
            2
        )


        self.sheetWidthSpin.setSuffix(
            " mm"
        )


        form_layout.addRow(
            "Ancho tablero:",
            self.sheetWidthSpin
        )


        #
        # Supplier
        #

        self.supplierCombo = QtWidgets.QComboBox()


        self.supplierCombo.addItems(
            self.SUPPLIERS
        )


        form_layout.addRow(
            "Proveedor:",
            self.supplierCombo
        )


        #
        # Finish
        #

        self.finishCombo = QtWidgets.QComboBox()


        self.finishCombo.addItems(
            self.FINISHES
        )


        form_layout.addRow(
            "Acabado:",
            self.finishCombo
        )


        #
        # Grain direction
        #

        self.grainCombo = QtWidgets.QComboBox()


        self.grainCombo.addItems(
            self.GRAIN_DIRECTIONS
        )


        form_layout.addRow(
            "Dirección veta:",
            self.grainCombo
        )


        #
        # Color code
        #

        self.colorCodeEdit = QtWidgets.QLineEdit()


        self.colorCodeEdit.setPlaceholderText(
            "Ej. RAL 9016"
        )


        form_layout.addRow(
            "Código de color:",
            self.colorCodeEdit
        )


        #
        # Texture
        #

        texture_layout = QtWidgets.QHBoxLayout()


        self.textureEdit = QtWidgets.QLineEdit()


        self.textureEdit.setReadOnly(
            True
        )


        self.textureButton = QtWidgets.QPushButton(
            "Seleccionar..."
        )


        self.textureButton.clicked.connect(
            self.selectTexture
        )


        texture_layout.addWidget(
            self.textureEdit
        )


        texture_layout.addWidget(
            self.textureButton
        )


        form_layout.addRow(
            "Textura:",
            texture_layout
        )


        #
        # Texture preview
        #

        self.texturePreview = QtWidgets.QLabel()


        self.texturePreview.setFixedSize(
            160,
            100
        )


        self.texturePreview.setAlignment(
            QtCore.Qt.AlignCenter
        )


        self.texturePreview.setFrameShape(
            QtWidgets.QFrame.Box
        )


        self.texturePreview.setText(
            "Sin textura"
        )


        form_layout.addRow(
            "Vista previa:",
            self.texturePreview
        )


        #
        # Price
        #

        self.priceSpin = QtWidgets.QDoubleSpinBox()


        self.priceSpin.setRange(
            0,
            100000
        )


        self.priceSpin.setDecimals(
            4
        )


        self.priceSpin.setSuffix(
            " €"
        )


        form_layout.addRow(
            "Precio:",
            self.priceSpin
        )


        #
        # Price unit
        #

        self.priceUnitCombo = QtWidgets.QComboBox()


        self.priceUnitCombo.addItems(
            self.PRICE_UNITS
        )


        form_layout.addRow(
            "Unidad de precio:",
            self.priceUnitCombo
        )


        main_layout.addLayout(
            form_layout
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


        main_layout.addWidget(
            buttons
        )


        self.setLayout(
            main_layout
        )



    #
    # Load existing data
    #

    def loadData(
        self
    ):

        material_type = self.data.get(
            "MaterialType",
            "Tablero"
        )


        if material_type not in self.MATERIAL_TYPES:

            material_type = "Tablero"


        self.typeCombo.setCurrentText(
            material_type
        )


        #
        # Categories
        #

        self.updateCategories(
            material_type
        )


        #
        # Text fields
        #

        self.codeEdit.setText(
            str(
                self.data.get(
                    "Code",
                    ""
                )
            )
        )


        self.nameEdit.setText(
            str(
                self.data.get(
                    "MaterialName",
                    ""
                )
            )
        )


        #
        # Dimensions
        #

        self.thicknessSpin.setValue(
            float(
                self.data.get(
                    "Thickness",
                    19
                )
            )
        )


        self.sheetLengthSpin.setValue(
            float(
                self.data.get(
                    "SheetLength",
                    2800
                )
            )
        )


        self.sheetWidthSpin.setValue(
            float(
                self.data.get(
                    "SheetWidth",
                    2070
                )
            )
        )


        #
        # Supplier
        #

        supplier = self.data.get(
            "Supplier",
            ""
        )


        if supplier:

            if supplier not in self.SUPPLIERS:

                self.supplierCombo.addItem(
                    supplier
                )


            self.supplierCombo.setCurrentText(
                supplier
            )


        #
        # Finish
        #

        finish = self.data.get(
            "Finish",
            ""
        )


        if finish:

            if finish not in self.FINISHES:

                self.finishCombo.addItem(
                    finish
                )


            self.finishCombo.setCurrentText(
                finish
            )


        #
        # Grain
        #

        grain = self.data.get(
            "GrainDirection",
            ""
        )


        if grain:

            if grain not in self.GRAIN_DIRECTIONS:

                self.grainCombo.addItem(
                    grain
                )


            self.grainCombo.setCurrentText(
                grain
            )


        #
        # Color
        #

        self.colorCodeEdit.setText(
            str(
                self.data.get(
                    "ColorCode",
                    ""
                )
            )
        )


        #
        # Texture
        #

        texture = self.data.get(
            "TexturePath",
            ""
        )


        self.textureEdit.setText(
            str(
                texture
            )
        )


        self.updateTexturePreview(
            texture
        )


        #
        # Price
        #

        self.priceSpin.setValue(
            float(
                self.data.get(
                    "Price",
                    0
                )
            )
        )


        #
        # Price unit
        #

        price_unit = self.data.get(
            "PriceUnit",
            ""
        )


        if price_unit in self.PRICE_UNITS:

            self.priceUnitCombo.setCurrentText(
                price_unit

            )

        else:

            self.updatePriceUnit(
                material_type
            )



    #
    # Categories
    #

    def updateCategories(
        self,
        material_type
    ):

        current = self.categoryCombo.currentText()


        self.categoryCombo.blockSignals(
            True
        )


        self.categoryCombo.clear()


        categories = self.CATEGORIES.get(
            material_type,
            [
                "Otro"
            ]
        )


        self.categoryCombo.addItems(
            categories
        )


        stored_category = self.data.get(
            "Category",
            ""
        )


        if stored_category:

            if stored_category not in categories:

                self.categoryCombo.addItem(
                    stored_category
                )


            self.categoryCombo.setCurrentText(
                stored_category
            )

        elif current in categories:

            self.categoryCombo.setCurrentText(
                current
            )


        self.categoryCombo.blockSignals(
            False
        )



    #
    # Price unit
    #

    def updatePriceUnit(
        self,
        material_type
    ):

        unit = self.DEFAULT_PRICE_UNITS.get(
            material_type,
            "€/ud"
        )


        if not self.data.get(
            "PriceUnit",
            ""
        ):

            self.priceUnitCombo.setCurrentText(
                unit
            )



    #
    # Select texture
    #

    def selectTexture(
        self
    ):

        path, _ = QtWidgets.QFileDialog.getOpenFileName(

            self,

            "Seleccionar textura",

            "",

            "Imágenes (*.png *.jpg *.jpeg *.bmp *.webp)"

        )


        if not path:

            return


        self.textureEdit.setText(
            path
        )


        self.updateTexturePreview(
            path
        )



    #
    # Texture preview
    #

    def updateTexturePreview(
        self,
        path
    ):

        if not path:

            self.texturePreview.clear()

            self.texturePreview.setText(
                "Sin textura"
            )

            return


        pixmap = QtGui.QPixmap(
            path
        )


        if pixmap.isNull():

            self.texturePreview.clear()

            self.texturePreview.setText(
                "Imagen no disponible"
            )

            return


        pixmap = pixmap.scaled(

            self.texturePreview.size(),

            QtCore.Qt.KeepAspectRatio,

            QtCore.Qt.SmoothTransformation

        )


        self.texturePreview.setPixmap(
            pixmap
        )



    #
    # Return data
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
                self.categoryCombo.currentText(),

            "Thickness":
                self.thicknessSpin.value(),

            "SheetLength":
                self.sheetLengthSpin.value(),

            "SheetWidth":
                self.sheetWidthSpin.value(),

            "Supplier":
                self.supplierCombo.currentText(),

            "Finish":
                self.finishCombo.currentText(),

            "GrainDirection":
                self.grainCombo.currentText(),

            "ColorCode":
                self.colorCodeEdit.text().strip(),

            "TexturePath":
                self.textureEdit.text().strip(),

            "Price":
                self.priceSpin.value(),

            "PriceUnit":
                self.priceUnitCombo.currentText()

        }