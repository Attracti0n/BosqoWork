import FreeCAD
import FreeCADGui
import os
import math

from PySide import QtWidgets, QtCore

from app_paths import ICONS_DIR


class ModulePlacementDialog(QtWidgets.QDialog):

    def __init__(
        self,
        module,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.module = module

        self.setWindowTitle(
            "Posición y giro del módulo"
        )

        self.resize(
            420,
            360
        )

        self.createUI()

        self.loadPlacement()


    # =========================================================
    # UI
    # =========================================================

    def createUI(
        self
    ):

        layout = QtWidgets.QVBoxLayout(
            self
        )


        #
        # =====================================================
        # POSITION
        # =====================================================
        #

        positionGroup = QtWidgets.QGroupBox(
            "Posición"
        )

        positionLayout = QtWidgets.QGridLayout()

        positionLayout.addWidget(
            QtWidgets.QLabel(
                "X:"
            ),
            0,
            0
        )

        self.xSpin = self.createDoubleSpinBox()

        positionLayout.addWidget(
            self.xSpin,
            0,
            1
        )


        positionLayout.addWidget(
            QtWidgets.QLabel(
                "Y:"
            ),
            1,
            0
        )

        self.ySpin = self.createDoubleSpinBox()

        positionLayout.addWidget(
            self.ySpin,
            1,
            1
        )


        positionLayout.addWidget(
            QtWidgets.QLabel(
                "Z:"
            ),
            2,
            0
        )

        self.zSpin = self.createDoubleSpinBox()

        positionLayout.addWidget(
            self.zSpin,
            2,
            1
        )


        positionGroup.setLayout(
            positionLayout
        )

        layout.addWidget(
            positionGroup
        )


        #
        # =====================================================
        # ROTATION
        # =====================================================
        #

        rotationGroup = QtWidgets.QGroupBox(
            "Giro"
        )

        rotationLayout = QtWidgets.QGridLayout()


        rotationLayout.addWidget(
            QtWidgets.QLabel(
                "X:"
            ),
            0,
            0
        )

        self.rxSpin = self.createAngleSpinBox()

        rotationLayout.addWidget(
            self.rxSpin,
            0,
            1
        )


        rotationLayout.addWidget(
            QtWidgets.QLabel(
                "Y:"
            ),
            1,
            0
        )

        self.rySpin = self.createAngleSpinBox()

        rotationLayout.addWidget(
            self.rySpin,
            1,
            1
        )


        rotationLayout.addWidget(
            QtWidgets.QLabel(
                "Z:"
            ),
            2,
            0
        )

        self.rzSpin = self.createAngleSpinBox()

        rotationLayout.addWidget(
            self.rzSpin,
            2,
            1
        )


        rotationGroup.setLayout(
            rotationLayout
        )

        layout.addWidget(
            rotationGroup
        )


        #
        # =====================================================
        # BUTTONS
        # =====================================================
        #

        buttonLayout = QtWidgets.QHBoxLayout()

        buttonLayout.addStretch()


        self.cancelButton = QtWidgets.QPushButton(
            "Cancelar"
        )

        self.okButton = QtWidgets.QPushButton(
            "Aceptar"
        )


        self.cancelButton.clicked.connect(
            self.reject
        )

        self.okButton.clicked.connect(
            self.applyPlacement
        )


        buttonLayout.addWidget(
            self.cancelButton
        )

        buttonLayout.addWidget(
            self.okButton
        )


        layout.addLayout(
            buttonLayout
        )


    # =========================================================
    # SPIN BOXES
    # =========================================================

    def createDoubleSpinBox(
        self
    ):

        spin = QtWidgets.QDoubleSpinBox()

        spin.setDecimals(
            2
        )

        spin.setRange(
            -1000000.0,
            1000000.0
        )

        spin.setSingleStep(
            1.0
        )

        spin.setSuffix(
            " mm"
        )

        return spin


    def createAngleSpinBox(
        self
    ):

        spin = QtWidgets.QDoubleSpinBox()

        spin.setDecimals(
            2
        )

        spin.setRange(
            -360.0,
            360.0
        )

        spin.setSingleStep(
            1.0
        )

        spin.setSuffix(
            " °"
        )

        return spin


    # =========================================================
    # LOAD PLACEMENT
    # =========================================================

    def loadPlacement(
        self
    ):

        placement = self.module.Placement

        #
        # Position
        #

        self.xSpin.setValue(
            placement.Base.x
        )

        self.ySpin.setValue(
            placement.Base.y
        )

        self.zSpin.setValue(
            placement.Base.z
        )


        #
        # Rotation
        #
        # Convert quaternion to XYZ Euler angles.
        #

        rx, ry, rz = (
            self.rotationToEulerXYZ(
                placement.Rotation
            )
        )

        self.rxSpin.setValue(
            rx
        )

        self.rySpin.setValue(
            ry
        )

        self.rzSpin.setValue(
            rz
        )


    # =========================================================
    # ROTATION -> EULER XYZ
    # =========================================================

    def rotationToEulerXYZ(
        self,
        rotation
    ):

        qx = float(
            rotation.Q[0]
        )

        qy = float(
            rotation.Q[1]
        )

        qz = float(
            rotation.Q[2]
        )

        qw = float(
            rotation.Q[3]
        )


        #
        # Roll X
        #

        sinr_cosp = (
            2.0
            *
            (
                qw * qx
                +
                qy * qz
            )
        )

        cosr_cosp = (
            1.0
            -
            2.0
            *
            (
                qx * qx
                +
                qy * qy
            )
        )

        roll = math.atan2(
            sinr_cosp,
            cosr_cosp
        )


        #
        # Pitch Y
        #

        sinp = (
            2.0
            *
            (
                qw * qy
                -
                qz * qx
            )
        )

        if abs(
            sinp
        ) >= 1.0:

            pitch = math.copysign(
                math.pi / 2.0,
                sinp
            )

        else:

            pitch = math.asin(
                sinp
            )


        #
        # Yaw Z
        #

        siny_cosp = (
            2.0
            *
            (
                qw * qz
                +
                qx * qy
            )
        )

        cosy_cosp = (
            1.0
            -
            2.0
            *
            (
                qy * qy
                +
                qz * qz
            )
        )

        yaw = math.atan2(
            siny_cosp,
            cosy_cosp
        )


        return (
            math.degrees(roll),
            math.degrees(pitch),
            math.degrees(yaw)
        )


    # =========================================================
    # EULER XYZ -> ROTATION
    # =========================================================

    def eulerXYZToRotation(
        self,
        rx,
        ry,
        rz
    ):

        #
        # Convert degrees to radians.
        #

        x = math.radians(
            rx
        )

        y = math.radians(
            ry
        )

        z = math.radians(
            rz
        )


        cx = math.cos(
            x / 2.0
        )

        sx = math.sin(
            x / 2.0
        )

        cy = math.cos(
            y / 2.0
        )

        sy = math.sin(
            y / 2.0
        )

        cz = math.cos(
            z / 2.0
        )

        sz = math.sin(
            z / 2.0
        )


        #
        # Quaternion for XYZ rotation.
        #

        qw = (
            cx * cy * cz
            -
            sx * sy * sz
        )

        qx = (
            sx * cy * cz
            +
            cx * sy * sz
        )

        qy = (
            cx * sy * cz
            -
            sx * cy * sz
        )

        qz = (
            cx * cy * sz
            +
            sx * sy * cz
        )


        return FreeCAD.Rotation(
            qx,
            qy,
            qz,
            qw
        )


    # =========================================================
    # APPLY
    # =========================================================

    def applyPlacement(
        self
    ):

        try:

            #
            # Position
            #

            position = FreeCAD.Vector(
                self.xSpin.value(),
                self.ySpin.value(),
                self.zSpin.value()
            )


            #
            # Rotation
            #

            rotation = (
                self.eulerXYZToRotation(
                    self.rxSpin.value(),
                    self.rySpin.value(),
                    self.rzSpin.value()
                )
            )


            #
            # Create new placement.
            #

            newPlacement = FreeCAD.Placement(
                position,
                rotation
            )


            #
            # Assign to module.
            #
            # BosqoModule.onChanged("Placement")
            # will automatically move all module pieces.
            #

            self.module.Placement = (
                newPlacement
            )


            #
            # Recompute.
            #

            FreeCAD.ActiveDocument.recompute()


            self.accept()


        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error aplicando posición del módulo: "
                +
                str(error)
                +
                "\n"
            )


# =============================================================
# COMMAND
# =============================================================

class ModulePlacementCommand:


    # =========================================================
    # RESOURCES
    # =========================================================

    def GetResources(
        self
    ):

        return {

            "Pixmap":
                os.path.join(
                    ICONS_DIR,
                    "placement.svg"
                ),

            "MenuText":
                "Posición del módulo",

            "ToolTip":
                "Editar posición y giro del módulo",

            "Accel":
                ""

        }


    # =========================================================
    # ACTIVE
    # =========================================================

    def IsActive(
        self
    ):

        document = (
            FreeCAD.ActiveDocument
        )

        if document is None:
            return False

        module = (
            document.getObject(
                "BosqoModule"
            )
        )

        if module is None:
            return False

        return hasattr(
            module,
            "Placement"
        )


    # =========================================================
    # GET MODULE
    # =========================================================

    def getModule(
        self
    ):

        document = (
            FreeCAD.ActiveDocument
        )

        if document is None:
            return None


        #
        # First try selected object.
        #

        selection = (
            FreeCADGui.Selection.getSelection()
        )

        for obj in selection:

            if (
                getattr(
                    obj,
                    "ObjectType",
                    ""
                )
                ==
                "BosqoModule"
            ):

                return obj


        #
        # Normally use the BosqoModule name.
        #

        module = (
            document.getObject(
                "BosqoModule"
            )
        )

        if module is not None:

            if hasattr(
                module,
                "Placement"
            ):

                return module


        #
        # Last fallback.
        #

        for obj in document.Objects:

            if (
                getattr(
                    obj,
                    "ObjectType",
                    ""
                )
                ==
                "BosqoModule"
            ):

                if hasattr(
                    obj,
                    "Placement"
                ):

                    return obj


        return None


    # =========================================================
    # ACTIVATED
    # =========================================================

    def Activated(
        self
    ):

        module = self.getModule()

        if module is None:

            FreeCAD.Console.PrintError(
                "No se ha encontrado el módulo Bosqo.\n"
            )

            return


        if not hasattr(
            module,
            "Placement"
        ):

            FreeCAD.Console.PrintError(
                "El módulo no tiene Placement.\n"
            )

            return


        dialog = ModulePlacementDialog(
            module,
            FreeCADGui.getMainWindow()
        )


        dialog.exec_()


# =============================================================
# REGISTER
# =============================================================

FreeCADGui.addCommand(
    "Bosqo_ModulePlacement",
    ModulePlacementCommand()
)