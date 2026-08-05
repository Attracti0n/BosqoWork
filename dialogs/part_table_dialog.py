from PySide import QtWidgets

from library.material_library import MaterialLibrary
from core.builders.module_builder import ModuleBuilder


class PartTableDialog(QtWidgets.QDialog):

    def __init__(
        self,
        module=None,
        parts=None,
        parent=None
    ):
        super().__init__(parent)

        self.setWindowTitle(
            "Redactar módulo"
        )

        self.resize(
            1100,
            750
        )

        self.module = module

        self.parts = (
            parts
            if isinstance(parts, list)
            else []
        )

        self.originalParts = list(
            self.parts
        )

        self.createUI()

        self.loadModuleParameters()

        self.loadParts()

    # =========================================================
    # UI
    # =========================================================

    def createUI(self):

        mainLayout = QtWidgets.QVBoxLayout()

        # -----------------------------------------------------
        # Título
        # -----------------------------------------------------

        title = QtWidgets.QLabel(
            "Redactar módulo"
        )

        font = title.font()
        font.setBold(True)
        font.setPointSize(
            font.pointSize() + 2
        )

        title.setFont(font)

        mainLayout.addWidget(
            title
        )

        # -----------------------------------------------------
        # Identificación
        # -----------------------------------------------------

        identificationGroup = QtWidgets.QGroupBox(
            "Identificación"
        )

        identificationLayout = QtWidgets.QGridLayout()

        identificationLayout.addWidget(
            QtWidgets.QLabel(
                "Nombre del módulo:"
            ),
            0,
            0
        )

        self.nameEdit = QtWidgets.QLineEdit()

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

        # -----------------------------------------------------
        # Dimensiones del módulo
        # -----------------------------------------------------

        dimensionsGroup = QtWidgets.QGroupBox(
            "Dimensiones del módulo"
        )

        dimensionsLayout = QtWidgets.QGridLayout()

        # Ancho

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Ancho:"
            ),
            0,
            0
        )

        self.widthSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            self.widthSpin,
            0,
            1
        )

        # Alto

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Alto:"
            ),
            0,
            2
        )

        self.heightSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            self.heightSpin,
            0,
            3
        )

        # Profundidad

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Profundidad:"
            ),
            1,
            0
        )

        self.depthSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            self.depthSpin,
            1,
            1
        )

        # Espesor panel

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Espesor panel:"
            ),
            1,
            2
        )

        self.thicknessSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            self.thicknessSpin,
            1,
            3
        )

        # Espesor fondo

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Espesor fondo:"
            ),
            2,
            0
        )

        self.backThicknessSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            self.backThicknessSpin,
            2,
            1
        )

        # Retranqueo trasero

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Retranqueo trasero:"
            ),
            2,
            2
        )

        self.backInsetSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            self.backInsetSpin,
            2,
            3
        )

        dimensionsGroup.setLayout(
            dimensionsLayout
        )

        mainLayout.addWidget(
            dimensionsGroup
        )

        # -----------------------------------------------------
        # Tabla de piezas
        # -----------------------------------------------------

        piecesGroup = QtWidgets.QGroupBox(
            "Tabla de piezas"
        )

        piecesLayout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget()

        self.table.setColumnCount(
            7
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Pieza",
                "Tipo",
                "Largo",
                "Ancho",
                "Espesor",
                "Cantidad",
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

        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked
            | QtWidgets.QAbstractItemView.EditKeyPressed
        )

        piecesLayout.addWidget(
            self.table
        )

        # -----------------------------------------------------
        # Botones de piezas
        # -----------------------------------------------------

        partsButtonsLayout = QtWidgets.QHBoxLayout()

        self.addButton = QtWidgets.QPushButton(
            "Añadir pieza"
        )

        self.deleteButton = QtWidgets.QPushButton(
            "Eliminar"
        )

        self.duplicateButton = QtWidgets.QPushButton(
            "Duplicar"
        )

        partsButtonsLayout.addWidget(
            self.addButton
        )

        partsButtonsLayout.addWidget(
            self.deleteButton
        )

        partsButtonsLayout.addWidget(
            self.duplicateButton
        )

        partsButtonsLayout.addStretch()

        piecesLayout.addLayout(
            partsButtonsLayout
        )

        piecesGroup.setLayout(
            piecesLayout
        )

        mainLayout.addWidget(
            piecesGroup
        )

        # -----------------------------------------------------
        # Botones principales
        # -----------------------------------------------------

        buttonLayout = QtWidgets.QHBoxLayout()

        self.recalculateButton = QtWidgets.QPushButton(
            "Recalcular"
        )

        buttonLayout.addWidget(
            self.recalculateButton
        )

        buttonLayout.addStretch()

        self.saveButton = QtWidgets.QPushButton(
            "Guardar cambios"
        )

        self.cancelButton = QtWidgets.QPushButton(
            "Cancelar"
        )

        buttonLayout.addWidget(
            self.saveButton
        )

        buttonLayout.addWidget(
            self.cancelButton
        )

        mainLayout.addLayout(
            buttonLayout
        )

        # -----------------------------------------------------
        # Conexiones
        # -----------------------------------------------------

        self.addButton.clicked.connect(
            self.addPart
        )

        self.deleteButton.clicked.connect(
            self.deletePart
        )

        self.duplicateButton.clicked.connect(
            self.duplicatePart
        )

        self.recalculateButton.clicked.connect(
            self.recalculate
        )

        self.saveButton.clicked.connect(
            self.saveChanges
        )

        self.cancelButton.clicked.connect(
            self.reject
        )

        self.setLayout(
            mainLayout
        )

    # =========================================================
    # SPINBOX
    # =========================================================

    def createSpinBox(self):

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

    # =========================================================
    # CARGAR PARÁMETROS DEL MÓDULO
    # =========================================================

    def loadModuleParameters(self):

        module = self.module

        if module is None:
            return

        # -----------------------------------------------------
        # Nombre
        # -----------------------------------------------------

        self.nameEdit.setText(
            str(
                getattr(
                    module,
                    "Label",
                    ""
                )
            )
        )

        # -----------------------------------------------------
        # Ancho
        # -----------------------------------------------------

        if hasattr(
            module,
            "Width"
        ):

            try:

                self.widthSpin.setValue(
                    float(
                        module.Width.Value
                    )
                )

            except Exception:
                pass

        # -----------------------------------------------------
        # Alto
        # -----------------------------------------------------

        if hasattr(
            module,
            "Height"
        ):

            try:

                self.heightSpin.setValue(
                    float(
                        module.Height.Value
                    )
                )

            except Exception:
                pass

        # -----------------------------------------------------
        # Profundidad
        # -----------------------------------------------------

        if hasattr(
            module,
            "Depth"
        ):

            try:

                self.depthSpin.setValue(
                    float(
                        module.Depth.Value
                    )
                )

            except Exception:
                pass

        # -----------------------------------------------------
        # Espesor panel
        # -----------------------------------------------------

        if hasattr(
            module,
            "PanelThickness"
        ):

            try:

                self.thicknessSpin.setValue(
                    float(
                        module.PanelThickness.Value
                    )
                )

            except Exception:
                pass

        # -----------------------------------------------------
        # Espesor fondo
        # -----------------------------------------------------

        if hasattr(
            module,
            "BackThickness"
        ):

            try:

                self.backThicknessSpin.setValue(
                    float(
                        module.BackThickness.Value
                    )
                )

            except Exception:
                pass

        # -----------------------------------------------------
        # Retranqueo trasero
        # -----------------------------------------------------

        if hasattr(
            module,
            "BackInset"
        ):

            try:

                self.backInsetSpin.setValue(
                    float(
                        module.BackInset.Value
                    )
                )

            except Exception:
                pass

    # =========================================================
    # CONVERTIR QUANTITY
    # =========================================================

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

            return 0

    # =========================================================
    # CARGAR PIEZAS
    # =========================================================

    def loadParts(self):

        self.table.setRowCount(
            0
        )

        for part in self.parts:

            data = self.partToData(
                part
            )

            if data is None:
                continue

            self.addPartRow(
                data
            )

        self.resizeColumns()

    # =========================================================
    # BOSQOPART → DATOS
    # =========================================================

    def partToData(
        self,
        part
    ):

        # -----------------------------------------------------
        # Si ya recibimos un diccionario
        # -----------------------------------------------------

        if isinstance(
            part,
            dict
        ):

            return dict(
                part
            )

        # -----------------------------------------------------
        # Comprobar objeto FreeCAD
        # -----------------------------------------------------

        if not hasattr(
            part,
            "Proxy"
        ):

            return None

        proxy = part.Proxy

        if proxy is None:
            return None

        # -----------------------------------------------------
        # Material
        # -----------------------------------------------------

        materialCode = ""

        if hasattr(
            part,
            "MaterialCode"
        ):

            try:

                materialCode = str(
                    part.MaterialCode
                ).strip()

            except Exception:

                materialCode = ""

        # -----------------------------------------------------
        # Datos
        # -----------------------------------------------------

        return {

            "Label":
                str(
                    getattr(
                        part,
                        "Label",
                        "Pieza"
                    )
                ),

            "PartType":
                str(
                    getattr(
                        part,
                        "PartType",
                        "Personalizado"
                    )
                ),

            "Length":
                self.quantityValue(
                    getattr(
                        part,
                        "Length",
                        0
                    )
                ),

            "Width":
                self.quantityValue(
                    getattr(
                        part,
                        "Width",
                        0
                    )
                ),

            "Thickness":
                self.quantityValue(
                    getattr(
                        part,
                        "Thickness",
                        0
                    )
                ),

            "Quantity":
                self.quantityValue(
                    getattr(
                        part,
                        "Quantity",
                        1
                    )
                ),

            "MaterialCode":
                materialCode

        }

    # =========================================================
    # AÑADIR FILA
    # =========================================================

    def addPartRow(
        self,
        data=None
    ):

        if data is None:
            data = {}

        row = self.table.rowCount()

        self.table.insertRow(
            row
        )

        self.setText(
            row,
            0,
            data.get(
                "Label",
                "Nueva pieza"
            )
        )

        self.setText(
            row,
            1,
            data.get(
                "PartType",
                "Personalizado"
            )
        )

        self.setText(
            row,
            2,
            self.number(
                data.get(
                    "Length",
                    600
                )
            )
        )

        self.setText(
            row,
            3,
            self.number(
                data.get(
                    "Width",
                    560
                )
            )
        )

        self.setText(
            row,
            4,
            self.number(
                data.get(
                    "Thickness",
                    19
                )
            )
        )

        self.setText(
            row,
            5,
            self.number(
                data.get(
                    "Quantity",
                    1
                )
            )
        )

        self.createMaterialCombo(
            row,
            data.get(
                "MaterialCode",
                ""
            )
        )

    # =========================================================
    # ESCRIBIR CELDA
    # =========================================================

    def setText(
        self,
        row,
        column,
        value
    ):

        item = QtWidgets.QTableWidgetItem(
            str(value)
        )

        self.table.setItem(
            row,
            column,
            item
        )

    # =========================================================
    # FORMATEAR NÚMERO
    # =========================================================

    def number(
        self,
        value
    ):

        if value is None:
            return ""

        try:

            number = float(value)

            if number.is_integer():

                return str(
                    int(number)
                )

            return str(number)

        except Exception:

            return str(value)

    # =========================================================
    # MATERIAL
    # =========================================================

    def createMaterialCombo(
        self,
        row,
        selectedCode=""
    ):

        combo = QtWidgets.QComboBox()

        combo.addItem(
            "— Sin material —",
            ""
        )

        try:

            materials = MaterialLibrary.all()

        except Exception:

            materials = []

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

        selectedCode = str(
            selectedCode
        ).strip()

        index = combo.findData(
            selectedCode
        )

        if index >= 0:

            combo.setCurrentIndex(
                index
            )

        self.table.setCellWidget(
            row,
            6,
            combo
        )

    # =========================================================
    # AÑADIR PIEZA
    # =========================================================

    def addPart(self):

        data = {

            "Label":
                "Nueva pieza",

            "PartType":
                "Personalizado",

            "Length":
                600,

            "Width":
                560,

            "Thickness":
                19,

            "Quantity":
                1,

            "MaterialCode":
                ""

        }

        row = self.table.rowCount()

        self.addPartRow(
            data
        )

        self.table.selectRow(
            row
        )

        self.table.setCurrentCell(
            row,
            0
        )

        self.table.editItem(
            self.table.item(
                row,
                0
            )
        )

    # =========================================================
    # ELIMINAR PIEZA
    # =========================================================

    def deletePart(self):

        row = self.table.currentRow()

        if row < 0:

            QtWidgets.QMessageBox.information(
                self,
                "Eliminar pieza",
                "Selecciona primero una pieza."
            )

            return

        result = QtWidgets.QMessageBox.question(
            self,
            "Eliminar pieza",
            "¿Seguro que quieres eliminar la pieza seleccionada?",
            QtWidgets.QMessageBox.Yes
            | QtWidgets.QMessageBox.No
        )

        if result != QtWidgets.QMessageBox.Yes:
            return

        self.table.removeRow(
            row
        )

    # =========================================================
    # DUPLICAR PIEZA
    # =========================================================

    def duplicatePart(self):

        row = self.table.currentRow()

        if row < 0:

            QtWidgets.QMessageBox.information(
                self,
                "Duplicar pieza",
                "Selecciona primero una pieza."
            )

            return

        data = self.getRowData(
            row
        )

        if data is None:
            return

        data["Label"] = (
            data.get(
                "Label",
                "Pieza"
            )
            + " copia"
        )

        newRow = self.table.rowCount()

        self.addPartRow(
            data
        )

        self.table.selectRow(
            newRow
        )

    # =========================================================
    # RECALCULAR
    # =========================================================

    def recalculate(self):

        if self.module is None:

            QtWidgets.QMessageBox.warning(
                self,
                "Recalcular",
                "No hay ningún módulo asociado."
            )

            return

        try:

            # -------------------------------------------------
            # Primero guardar los parámetros del diálogo
            # en el BosqoModule.
            # -------------------------------------------------

            self.updateModuleParameters()

            # -------------------------------------------------
            # Recalcular módulo
            # -------------------------------------------------

            ModuleBuilder.build(
                self.module
            )

            # -------------------------------------------------
            # Recompute
            # -------------------------------------------------

            self.module.Document.recompute()

            # -------------------------------------------------
            # Volver a obtener las piezas reales
            # -------------------------------------------------

            self.parts = (
                self.module.Proxy.getParts(
                    self.module
                )
            )

            # -------------------------------------------------
            # Actualizar tabla
            # -------------------------------------------------

            self.loadParts()

        except Exception as error:

            QtWidgets.QMessageBox.warning(
                self,
                "Recalcular",
                "No se han podido recalcular las piezas:\n\n"
                + str(error)
            )

    # =========================================================
    # ACTUALIZAR PARÁMETROS DEL MÓDULO
    # =========================================================

    def updateModuleParameters(self):

        module = self.module

        if module is None:
            return

        # -----------------------------------------------------
        # Nombre
        # -----------------------------------------------------

        name = self.nameEdit.text().strip()

        if not name:

            name = "Módulo"

        module.Label = name

        # -----------------------------------------------------
        # Ancho
        # -----------------------------------------------------

        if hasattr(
            module,
            "Width"
        ):

            module.Width = (
                self.widthSpin.value()
            )

        # -----------------------------------------------------
        # Alto
        # -----------------------------------------------------

        if hasattr(
            module,
            "Height"
        ):

            module.Height = (
                self.heightSpin.value()
            )

        # -----------------------------------------------------
        # Profundidad
        # -----------------------------------------------------

        if hasattr(
            module,
            "Depth"
        ):

            module.Depth = (
                self.depthSpin.value()
            )

        # -----------------------------------------------------
        # Espesor panel
        # -----------------------------------------------------

        if hasattr(
            module,
            "PanelThickness"
        ):

            module.PanelThickness = (
                self.thicknessSpin.value()
            )

        # -----------------------------------------------------
        # Espesor fondo
        # -----------------------------------------------------

        if hasattr(
            module,
            "BackThickness"
        ):

            module.BackThickness = (
                self.backThicknessSpin.value()
            )

        # -----------------------------------------------------
        # Retranqueo
        # -----------------------------------------------------

        if hasattr(
            module,
            "BackInset"
        ):

            module.BackInset = (
                self.backInsetSpin.value()
            )

    # =========================================================
    # OBTENER DATOS DE UNA FILA
    # =========================================================

    def getRowData(
        self,
        row
    ):

        if row < 0:
            return None

        materialCode = ""

        combo = self.table.cellWidget(
            row,
            6
        )

        if combo is not None:

            materialCode = combo.currentData()

        return {

            "Label":
                self.getText(
                    row,
                    0
                ),

            "PartType":
                self.getText(
                    row,
                    1
                ),

            "Length":
                self.getFloat(
                    row,
                    2
                ),

            "Width":
                self.getFloat(
                    row,
                    3
                ),

            "Thickness":
                self.getFloat(
                    row,
                    4
                ),

            "Quantity":
                self.getFloat(
                    row,
                    5
                ),

            "MaterialCode":
                materialCode

        }

    # =========================================================
    # OBTENER TEXTO
    # =========================================================

    def getText(
        self,
        row,
        column
    ):

        item = self.table.item(
            row,
            column
        )

        if item is None:
            return ""

        return item.text().strip()

    # =========================================================
    # OBTENER FLOAT
    # =========================================================

    def getFloat(
        self,
        row,
        column
    ):

        value = self.getText(
            row,
            column
        )

        try:

            return float(
                value.replace(
                    ",",
                    "."
                )
            )

        except Exception:

            return 0

    # =========================================================
    # OBTENER TODA LA TABLA
    # =========================================================

    def getData(self):

        data = []

        for row in range(
            self.table.rowCount()
        ):

            part = self.getRowData(
                row
            )

            if part is None:
                continue

            data.append(
                part
            )

        return data

    # =========================================================
    # GUARDAR CAMBIOS
    # =========================================================

    def saveChanges(self):

        if self.module is None:
            return

        try:

            # -------------------------------------------------
            # Guardar parámetros del módulo
            # -------------------------------------------------

            self.updateModuleParameters()

            # -------------------------------------------------
            # Recalcular / construir
            # -------------------------------------------------

            ModuleBuilder.build(
                self.module
            )

            # -------------------------------------------------
            # Recompute
            # -------------------------------------------------

            self.module.Document.recompute()

            # -------------------------------------------------
            # Aceptar
            # -------------------------------------------------

            self.accept()

        except Exception as error:

            QtWidgets.QMessageBox.warning(
                self,
                "Guardar cambios",
                "No se han podido guardar los cambios:\n\n"
                + str(error)
            )

    # =========================================================
    # DOBLE CLICK
    # =========================================================

    def onCellDoubleClicked(
        self,
        index
    ):

        row = index.row()
        column = index.column()

        if column != 6:
            return

        combo = self.table.cellWidget(
            row,
            column
        )

        if combo is not None:

            combo.showPopup()

    # =========================================================
    # AJUSTAR COLUMNAS
    # =========================================================

    def resizeColumns(self):

        self.table.resizeColumnsToContents()

        self.table.setColumnWidth(
            0,
            180
        )

        self.table.setColumnWidth(
            1,
            130
        )

        self.table.setColumnWidth(
            2,
            90
        )

        self.table.setColumnWidth(
            3,
            90
        )

        self.table.setColumnWidth(
            4,
            90
        )

        self.table.setColumnWidth(
            5,
            80
        )

        self.table.setColumnWidth(
            6,
            220
        )