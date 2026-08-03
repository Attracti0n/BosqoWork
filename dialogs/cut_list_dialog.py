from PySide import QtWidgets


class CutListDialog(QtWidgets.QDialog):


    def __init__(
        self,
        cutlist,
        parent=None
    ):

        super().__init__(parent)

        self.cutlist = cutlist

        self.setWindowTitle(
            "Lista de corte"
        )

        self.resize(
            900,
            500
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

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels(

            [

                "Código",
                "Pieza",
                "Largo",
                "Ancho",
                "Espesor",
                "Material",
                "Cantidad"

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


        self.optimizeButton = buttons.addButton(
            "Optimizar",
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
            len(self.cutlist.Items)
        )


        for row, item in enumerate(self.cutlist.Items):

            self.table.setItem(
                row,
                0,
                QtWidgets.QTableWidgetItem(
                    str(item.Code)
                )
            )

            self.table.setItem(
                row,
                1,
                QtWidgets.QTableWidgetItem(
                    str(item.Name)
                )
            )

            self.table.setItem(
                row,
                2,
                QtWidgets.QTableWidgetItem(
                    str(item.Length)
                )
            )

            self.table.setItem(
                row,
                3,
                QtWidgets.QTableWidgetItem(
                    str(item.Width)
                )
            )

            self.table.setItem(
                row,
                4,
                QtWidgets.QTableWidgetItem(
                    str(item.Thickness)
                )
            )

            self.table.setItem(
                row,
                5,
                QtWidgets.QTableWidgetItem(
                    str(item.Material)
                )
            )

            self.table.setItem(
                row,
                6,
                QtWidgets.QTableWidgetItem(
                    str(item.Quantity)
                )
            )


        summary = self.cutlist.Summary

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