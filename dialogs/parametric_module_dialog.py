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
            "Módulo"
        )

        self.resize(
            1100,
            750
        )

        self.parameters = parameters

        # Guarda los objetos BosqoPart originales
        # cuando estamos editando un módulo importado.
        self.existingParts = []

        self.createUI()

        self.loadParameters()

        self.loadModuleParts()


    # =========================================================
    # UI
    # =========================================================

    def createUI(
        self
    ):

        mainLayout = QtWidgets.QVBoxLayout()


        # =====================================================
        # TÍTULO
        # =====================================================

        title = QtWidgets.QLabel(
            "Módulo"
        )

        font = title.font()
        font.setBold(True)
        font.setPointSize(
            font.pointSize() + 2
        )

        title.setFont(
            font
        )

        mainLayout.addWidget(
            title
        )


        # =====================================================
        # IDENTIFICACIÓN
        # =====================================================

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


        # =====================================================
        # DIMENSIONES
        # =====================================================

        dimensionsGroup = QtWidgets.QGroupBox(
            "Dimensiones del módulo"
        )

        dimensionsLayout = QtWidgets.QGridLayout()


        # -----------------------------------------------------
        # Ancho
        # -----------------------------------------------------

        self.widthSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Ancho:"
            ),
            0,
            0
        )

        dimensionsLayout.addWidget(
            self.widthSpin,
            0,
            1
        )


        # -----------------------------------------------------
        # Alto
        # -----------------------------------------------------

        self.heightSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Alto:"
            ),
            0,
            2
        )

        dimensionsLayout.addWidget(
            self.heightSpin,
            0,
            3
        )


        # -----------------------------------------------------
        # Profundidad
        # -----------------------------------------------------

        self.depthSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Profundidad:"
            ),
            1,
            0
        )

        dimensionsLayout.addWidget(
            self.depthSpin,
            1,
            1
        )


        # -----------------------------------------------------
        # Espesor panel
        # -----------------------------------------------------

        self.thicknessSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Espesor panel:"
            ),
            1,
            2
        )

        dimensionsLayout.addWidget(
            self.thicknessSpin,
            1,
            3
        )


        # -----------------------------------------------------
        # Espesor fondo
        # -----------------------------------------------------

        self.backThicknessSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Espesor fondo:"
            ),
            2,
            0
        )

        dimensionsLayout.addWidget(
            self.backThicknessSpin,
            2,
            1
        )


        # -----------------------------------------------------
        # Retranqueo
        # -----------------------------------------------------

        self.backInsetSpin = self.createSpinBox()

        dimensionsLayout.addWidget(
            QtWidgets.QLabel(
                "Retranqueo trasero:"
            ),
            2,
            2
        )

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


        # =====================================================
        # PIEZAS
        # =====================================================

        piecesGroup = QtWidgets.QGroupBox(
            "Piezas"
        )

        piecesLayout = QtWidgets.QVBoxLayout()


        # -----------------------------------------------------
        # Tabla
        #
        # No usamos el QDialog visualmente.
        # Solo reutilizamos su tabla y sus métodos.
        # -----------------------------------------------------

        self.partsTable = PartTableDialog(
            parts=[],
            parent=self
        )


        piecesLayout.addWidget(
            self.partsTable.table
        )


        # -----------------------------------------------------
        # Botones de piezas
        # -----------------------------------------------------

        partsButtonsLayout = QtWidgets.QHBoxLayout()


        self.addPartButton = QtWidgets.QPushButton(
            "Añadir pieza"
        )

        self.deletePartButton = QtWidgets.QPushButton(
            "Eliminar"
        )

        self.duplicatePartButton = QtWidgets.QPushButton(
            "Duplicar"
        )


        partsButtonsLayout.addWidget(
            self.addPartButton
        )

        partsButtonsLayout.addWidget(
            self.deletePartButton
        )

        partsButtonsLayout.addWidget(
            self.duplicatePartButton
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


        # =====================================================
        # BOTONES PRINCIPALES
        # =====================================================

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


        # =====================================================
        # CONEXIONES
        # =====================================================

        self.recalculateButton.clicked.connect(
            self.recalculate
        )

        self.saveButton.clicked.connect(
            self.apply
        )

        self.cancelButton.clicked.connect(
            self.reject
        )


        self.addPartButton.clicked.connect(
            self.partsTable.addPart
        )

        self.deletePartButton.clicked.connect(
            self.partsTable.deletePart
        )

        self.duplicatePartButton.clicked.connect(
            self.partsTable.duplicatePart
        )


        self.setLayout(
            mainLayout
        )


    # =========================================================
    # SPINBOX
    # =========================================================

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


    # =========================================================
    # CARGAR PARÁMETROS
    # =========================================================

    def loadParameters(
        self
    ):

        obj = self.parameters


        if obj is None:
            return


        # -----------------------------------------------------
        # Nombre
        # -----------------------------------------------------

        if hasattr(
            obj,
            "ModuleName"
        ):

            self.nameEdit.setText(
                str(
                    obj.ModuleName
                )
            )


        # -----------------------------------------------------
        # Ancho
        # -----------------------------------------------------

        if hasattr(
            obj,
            "ModuleWidth"
        ):

            self.widthSpin.setValue(
                self.quantityValue(
                    obj.ModuleWidth
                )
            )


        # -----------------------------------------------------
        # Alto
        # -----------------------------------------------------

        if hasattr(
            obj,
            "ModuleHeight"
        ):

            self.heightSpin.setValue(
                self.quantityValue(
                    obj.ModuleHeight
                )
            )


        # -----------------------------------------------------
        # Profundidad
        # -----------------------------------------------------

        if hasattr(
            obj,
            "ModuleDepth"
        ):

            self.depthSpin.setValue(
                self.quantityValue(
                    obj.ModuleDepth
                )
            )


        # -----------------------------------------------------
        # Espesor panel
        # -----------------------------------------------------

        if hasattr(
            obj,
            "PanelThickness"
        ):

            self.thicknessSpin.setValue(
                self.quantityValue(
                    obj.PanelThickness
                )
            )


        # -----------------------------------------------------
        # Espesor fondo
        # -----------------------------------------------------

        if hasattr(
            obj,
            "BackThickness"
        ):

            self.backThicknessSpin.setValue(
                self.quantityValue(
                    obj.BackThickness
                )
            )


        # -----------------------------------------------------
        # Retranqueo
        # -----------------------------------------------------

        if hasattr(
            obj,
            "BackInset"
        ):

            self.backInsetSpin.setValue(
                self.quantityValue(
                    obj.BackInset
                )
            )


    # =========================================================
    # QUANTITY
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
    # BUSCAR PIEZAS DEL MÓDULO
    # =========================================================

    def findModuleParts(
        self
    ):

        module = self.parameters


        if module is None:
            return []


        document = getattr(
            module,
            "Document",
            None
        )


        if document is None:
            return []


        result = []


        for part in document.Objects:

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


            if self.belongsToModule(
                part,
                module
            ):

                result.append(
                    part
                )


        return result


    # =========================================================
    # COMPROBAR PERTENENCIA
    # =========================================================

    def belongsToModule(
        self,
        part,
        module
    ):

        # -----------------------------------------------------
        # Parent
        # -----------------------------------------------------

        if hasattr(
            part,
            "Parent"
        ):

            try:

                if part.Parent == module:

                    return True

            except Exception:

                pass


        # -----------------------------------------------------
        # Group
        # -----------------------------------------------------

        if hasattr(
            module,
            "Group"
        ):

            try:

                for child in module.Group:

                    if child == part:

                        return True

            except Exception:

                pass


        return False


    # =========================================================
    # CARGAR PIEZAS
    # =========================================================

    def loadModuleParts(
        self
    ):

        existingParts = self.findModuleParts()


        self.existingParts = (
            existingParts
        )


        # -----------------------------------------------------
        # Hay piezas existentes
        # -----------------------------------------------------

        if existingParts:

            self.partsTable.parts = (
                existingParts
            )

            self.partsTable.loadParts()

            return


        # -----------------------------------------------------
        # No hay piezas:
        # módulo paramétrico
        # -----------------------------------------------------

        self.calculateParts()


    # =========================================================
    # ACTUALIZAR PARÁMETROS
    # =========================================================

    def updateParameters(
        self
    ):

        obj = self.parameters


        if obj is None:
            return


        # -----------------------------------------------------
        # Nombre
        # -----------------------------------------------------

        name = self.nameEdit.text().strip()


        if not name:

            name = "Nuevo módulo"


        if hasattr(
            obj,
            "ModuleName"
        ):

            obj.ModuleName = name


        obj.Label = name


        # -----------------------------------------------------
        # Dimensiones
        # -----------------------------------------------------

        if hasattr(
            obj,
            "ModuleWidth"
        ):

            obj.ModuleWidth = (
                self.widthSpin.value()
            )


        if hasattr(
            obj,
            "ModuleHeight"
        ):

            obj.ModuleHeight = (
                self.heightSpin.value()
            )


        if hasattr(
            obj,
            "ModuleDepth"
        ):

            obj.ModuleDepth = (
                self.depthSpin.value()
            )


        # -----------------------------------------------------
        # Espesores
        # -----------------------------------------------------

        if hasattr(
            obj,
            "PanelThickness"
        ):

            obj.PanelThickness = (
                self.thicknessSpin.value()
            )


        if hasattr(
            obj,
            "BackThickness"
        ):

            obj.BackThickness = (
                self.backThicknessSpin.value()
            )


        if hasattr(
            obj,
            "BackInset"
        ):

            obj.BackInset = (
                self.backInsetSpin.value()
            )


    # =========================================================
    # CALCULAR PIEZAS
    # =========================================================

    def calculateParts(
        self
    ):

        self.updateParameters()


        obj = self.parameters


        if obj is None:
            return


        proxy = getattr(
            obj,
            "Proxy",
            None
        )


        if proxy is None:
            return


        if not hasattr(
            proxy,
            "calculateParts"
        ):

            return


        parts = proxy.calculateParts(
            obj
        )


        if not isinstance(
            parts,
            list
        ):

            parts = []


        self.partsTable.parts = parts


        self.partsTable.loadParts()


    # =========================================================
    # RECALCULAR
    # =========================================================

    def recalculate(
        self
    ):

        self.calculateParts()


    # =========================================================
    # GUARDAR PIEZAS IMPORTADAS
    # =========================================================

    def saveExistingParts(
        self
    ):

        if not self.existingParts:

            return


        tableData = (
            self.partsTable.getData()
        )


        # -----------------------------------------------------
        # Actualizar las piezas existentes
        # -----------------------------------------------------

        count = min(
            len(
                self.existingParts
            ),
            len(
                tableData
            )
        )


        for index in range(
            count
        ):

            part = self.existingParts[
                index
            ]

            data = tableData[
                index
            ]


            # -------------------------------------------------
            # Nombre
            # -------------------------------------------------

            if hasattr(
                part,
                "Label"
            ):

                part.Label = data.get(
                    "Label",
                    part.Label
                )


            # -------------------------------------------------
            # Tipo
            # -------------------------------------------------

            if hasattr(
                part,
                "PartType"
            ):

                part.PartType = data.get(
                    "PartType",
                    ""
                )


            # -------------------------------------------------
            # Largo
            # -------------------------------------------------

            if hasattr(
                part,
                "Length"
            ):

                part.Length = data.get(
                    "Length",
                    0
                )


            # -------------------------------------------------
            # Ancho
            # -------------------------------------------------

            if hasattr(
                part,
                "Width"
            ):

                part.Width = data.get(
                    "Width",
                    0
                )


            # -------------------------------------------------
            # Espesor
            # -------------------------------------------------

            if hasattr(
                part,
                "Thickness"
            ):

                part.Thickness = data.get(
                    "Thickness",
                    0
                )


            # -------------------------------------------------
            # Cantidad
            # -------------------------------------------------

            if hasattr(
                part,
                "Quantity"
            ):

                part.Quantity = data.get(
                    "Quantity",
                    1
                )


            # -------------------------------------------------
            # Material
            # -------------------------------------------------

            if hasattr(
                part,
                "MaterialCode"
            ):

                part.MaterialCode = data.get(
                    "MaterialCode",
                    ""
                )


            part.touch()


    # =========================================================
    # APLICAR / GUARDAR
    # =========================================================

    def apply(
        self
    ):

        # -----------------------------------------------------
        # Guardar datos del módulo
        # -----------------------------------------------------

        self.updateParameters()


        # -----------------------------------------------------
        # Si existen piezas reales/importadas,
        # guardar sus cambios.
        # -----------------------------------------------------

        if self.existingParts:

            self.saveExistingParts()


        # -----------------------------------------------------
        # Si NO existen piezas reales,
        # son piezas paramétricas.
        # -----------------------------------------------------

        else:

            self.calculateParts()


        # -----------------------------------------------------
        # Recompute
        # -----------------------------------------------------

        document = getattr(
            self.parameters,
            "Document",
            None
        )


        if document is not None:

            document.recompute()


        self.accept()


    # =========================================================
    # OBTENER PARÁMETROS
    # =========================================================

    def getParameters(
        self
    ):

        return {

            "ModuleName":
                self.nameEdit.text().strip(),

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


    # =========================================================
    # OBTENER PIEZAS
    # =========================================================

    def getParts(
        self
    ):

        return self.partsTable.getData()