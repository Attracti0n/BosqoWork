from PySide import QtGui

from utils.document_properties import (
    load_project_properties,
    save_project_properties,
)


class ProjectPropertiesDialog(QtGui.QDialog):

    def __init__(self, doc, parent=None):
        super(ProjectPropertiesDialog, self).__init__(parent)

        self.doc = doc

        self.setWindowTitle("Datos del proyecto")
        self.resize(550, 500)

        layout = QtGui.QVBoxLayout(self)

        form = QtGui.QFormLayout()

        self.projectName = QtGui.QLineEdit()
        self.projectNumber = QtGui.QLineEdit()
        self.customer = QtGui.QLineEdit()
        self.phone = QtGui.QLineEdit()
        self.email = QtGui.QLineEdit()
        self.siteAddress = QtGui.QLineEdit()
        self.installationAddress = QtGui.QLineEdit()
        self.notes = QtGui.QTextEdit()

        form.addRow("Nombre del proyecto", self.projectName)
        form.addRow("Número del proyecto", self.projectNumber)
        form.addRow("Cliente", self.customer)
        form.addRow("Móvil", self.phone)
        form.addRow("Email", self.email)
        form.addRow("Dirección fiscal", self.siteAddress)
        form.addRow("Dirección de instalación", self.installationAddress)
        form.addRow("Notas", self.notes)

        layout.addLayout(form)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok |
            QtGui.QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        # Cargar datos del documento
        data = load_project_properties(self.doc)

        self.projectName.setText(data.get("ProjectName", ""))
        self.projectNumber.setText(data.get("ProjectNumber", ""))
        self.customer.setText(data.get("Customer", ""))
        self.phone.setText(data.get("Phone", ""))
        self.email.setText(data.get("Email", ""))
        self.siteAddress.setText(data.get("SiteAddress", ""))
        self.installationAddress.setText(data.get("InstallationAddress", ""))
        self.notes.setPlainText(data.get("Notes", ""))

    def accept(self):

        data = {
            "ProjectName": self.projectName.text(),
            "ProjectNumber": self.projectNumber.text(),
            "Customer": self.customer.text(),
            "Phone": self.phone.text(),
            "Email": self.email.text(),
            "SiteAddress": self.siteAddress.text(),
            "InstallationAddress": self.installationAddress.text(),
            "Notes": self.notes.toPlainText(),
        }

        save_project_properties(self.doc, data)

        super(ProjectPropertiesDialog, self).accept()