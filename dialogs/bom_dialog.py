from PySide import QtWidgets


class BOMDialog(QtWidgets.QDialog):


    def __init__(
        self,
        bom,
        parent=None
    ):

        super().__init__(parent)

        self.bom = bom

        self.setWindowTitle(
            "Bill of Materials"
        )

        self.resize(
            1000,
            550
        )

        self.createUI()

        self.loadData()


    #
    # UI
    #

    def createUI(self):

        layout = QtWidgets.QVBoxLayout()


        #
        # Table
        #

        self.table = QtWidgets.QTableWidget()

        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels(

            [

                "Código",
                "Nombre",
                "Material",
                "Acabado",
                "Largo",
                "Ancho",
                "Espesor",
                "Cantidad",
                "Estado"

            ]

        )

        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        self.table.horizontalHeader().setStretchLastSection(
            True
        )

        layout.addWidget(
            self.table
        )


        #
        # Summary
        #

        summaryGroup = QtWidgets.QGroupBox(
            "Resumen"
        )

        form = QtWidgets.QFormLayout()

        self.totalParts = QtWidgets.QLabel()

        self.totalUnique = QtWidgets.QLabel()

        self.totalMaterials = QtWidgets.QLabel()

        self.totalArea = QtWidgets.QLabel()

        self.totalVolume = QtWidgets.QLabel()

        form.addRow(
            "Total piezas:",
            self.totalParts
        )

        form.addRow(
            "Piezas distintas:",
            self.totalUnique
        )

        form.addRow(
            "Materiales:",
            self.totalMaterials
        )

        form.addRow(
            "Área:",
            self.totalArea
        )

        form.addRow(
            "Volumen:",
            self.totalVolume
        )

        summaryGroup.setLayout(
            form
        )

        layout.addWidget(
            summaryGroup
        )


        #
        # Buttons
        #

        buttons = QtWidgets.QDialogButtonBox()

        self.excelButton = buttons.addButton(
            "Excel",
            QtWidgets.QDialogButtonBox.ActionRole
        )

        self.pdfButton = buttons.addButton(
            "PDF",
            QtWidgets.QDialogButtonBox.ActionRole
        )

        buttons.addButton(
            QtWidgets.QDialogButtonBox.Close
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(
            buttons
        )

        self.setLayout(
            layout
        )


    #
    # Load
    #

    def loadData(self):

        self.table.setRowCount(
            len(self.bom.Items)
        )


        for row, item in enumerate(self.bom.Items):

            values = [

                item.Code,
                item.Name,
                item.Material,
                item.Finish,
                item.Length,
                item.Width,
                item.Thickness,
                item.Quantity,
                item.Status

            ]

            for column, value in enumerate(values):

                self.table.setItem(

                    row,

                    column,

                    QtWidgets.QTableWidgetItem(
                        str(value)
                    )

                )


        summary = self.bom.Summary

        self.totalParts.setText(
            str(summary.TotalParts)
        )

        self.totalUnique.setText(
            str(summary.TotalUniqueParts)
        )

        self.totalMaterials.setText(
            str(summary.TotalMaterials)
        )

        self.totalArea.setText(
            str(summary.TotalArea)
        )

        self.totalVolume.setText(
            str(summary.TotalVolume)
        )

        self.table.resizeColumnsToContents()