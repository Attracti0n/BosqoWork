import FreeCAD


# =============================================================
# BOSQO SHEET
# =============================================================

class BosqoSheet:

    PARAMETERS = (

        ("B2", "Width"),
        ("B3", "Height"),
        ("B4", "Depth"),
        ("B5", "PanelThickness"),
        ("B6", "BackThickness"),
        ("B7", "BackInset")

    )

    LABELS = (

        ("A1", "Parámetro"),
        ("B1", "Valor"),

        ("A2", "Width"),
        ("A3", "Height"),
        ("A4", "Depth"),
        ("A5", "PanelThickness"),
        ("A6", "BackThickness"),
        ("A7", "BackInset")

    )

    # =========================================================
    # PART TABLE
    # =========================================================

    PART_TABLE_START_ROW = 10

    PART_HEADERS = (

        "Pieza",
        "Tipo",
        "Largo",
        "Ancho",
        "Espesor",
        "Cantidad",
        "Material",
        "Posición",
        "Modo"

    )

    PART_TABLE_MAX_ROWS = 500

    # =========================================================
    # INIT
    # =========================================================

    def __init__(
        self,
        document,
        module
    ):

        self.document = document
        self.module = module
        self.sheet = None

    # =========================================================
    # CREATE
    # =========================================================

    def create(
        self
    ):

        if (
            self.document is None
            or
            self.module is None
        ):

            return None

        # -----------------------------------------------------
        # FIND EXISTING SHEET FROM MODULE
        # -----------------------------------------------------

        try:

            existing = getattr(
                self.module,
                "ParameterSheet",
                None
            )

        except Exception:

            existing = None

        if existing is not None:

            try:

                if (
                    getattr(
                        existing,
                        "TypeId",
                        ""
                    )
                    ==
                    "Spreadsheet::Sheet"
                ):

                    self.sheet = existing

            except Exception:

                self.sheet = None

        # -----------------------------------------------------
        # FIND SHEET BY NAME
        # -----------------------------------------------------

        if self.sheet is None:

            try:

                candidate = (
                    self.document.getObject(
                        "ModuleParameters"
                    )
                )

                if candidate is not None:

                    if (
                        getattr(
                            candidate,
                            "TypeId",
                            ""
                        )
                        ==
                        "Spreadsheet::Sheet"
                    ):

                        self.sheet = candidate

            except Exception:

                self.sheet = None

        # -----------------------------------------------------
        # CREATE SHEET
        # -----------------------------------------------------

        if self.sheet is None:

            try:

                self.sheet = (
                    self.document.addObject(
                        "Spreadsheet::Sheet",
                        "ModuleParameters"
                    )
                )

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error creando Spreadsheet del módulo: "
                    +
                    str(error)
                    +
                    "\n"
                )

                return None

        # -----------------------------------------------------
        # LABEL
        # -----------------------------------------------------

        try:

            self.sheet.Label = (
                "Parámetros - "
                +
                str(
                    getattr(
                        self.module,
                        "Label",
                        "Módulo"
                    )
                )
            )

        except Exception:

            pass

        # -----------------------------------------------------
        # CREATE STRUCTURE
        # -----------------------------------------------------

        self._createTable()

        # -----------------------------------------------------
        # LINK TO MODULE
        # -----------------------------------------------------

        try:

            current = getattr(
                self.module,
                "ParameterSheet",
                None
            )

            if current is not self.sheet:

                self.module.ParameterSheet = (
                    self.sheet
                )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error vinculando Spreadsheet: "
                +
                str(error)
                +
                "\n"
            )

        # -----------------------------------------------------
        # GROUP
        # -----------------------------------------------------

        self._repairGroup()

        # -----------------------------------------------------
        # INITIAL DATA
        # -----------------------------------------------------

        self._safeUpdateFromModule()

        self._safeUpdatePartsTable()

        # -----------------------------------------------------
        # WIDTHS
        # -----------------------------------------------------

        self._setColumnWidths()

        # -----------------------------------------------------
        # OBSERVER
        # -----------------------------------------------------

        BosqoSheetObserver.register(
            self.document
        )

        return self.sheet

    # =========================================================
    # CREATE TABLE
    # =========================================================

    def _createTable(
        self
    ):

        if self.sheet is None:

            return

        # -----------------------------------------------------
        # PARAMETER LABELS
        # -----------------------------------------------------

        for cell, value in self.LABELS:

            try:

                self.sheet.set(
                    cell,
                    value
                )

            except Exception:

                pass

        # -----------------------------------------------------
        # ALIASES
        # -----------------------------------------------------

        for cell, propertyName in self.PARAMETERS:

            try:

                self.sheet.setAlias(
                    cell,
                    propertyName
                )

            except Exception:

                pass

        # -----------------------------------------------------
        # PART TABLE TITLE
        # -----------------------------------------------------

        try:

            self.sheet.set(
                "A9",
                "PIEZAS DEL MÓDULO"
            )

        except Exception:

            pass

        # -----------------------------------------------------
        # PART HEADERS
        # -----------------------------------------------------

        row = self.PART_TABLE_START_ROW

        for index, header in enumerate(
            self.PART_HEADERS
        ):

            column = chr(
                ord("A")
                +
                index
            )

            try:

                self.sheet.set(
                    column + str(row),
                    header
                )

            except Exception:

                pass

    # =========================================================
    # UPDATE PARAMETERS FROM MODULE
    #
    # IMPORTANT:
    #
    # Parameter cells B2:B7 are NOT formulas.
    #
    # We write plain numeric values:
    #
    #     600
    #     720
    #     560
    #
    # instead of:
    #
    #     600 mm
    #
    # because Spreadsheet would interpret "600 mm" as:
    #
    #     =600 mm
    #
    # which can produce #PENDING.
    # =========================================================

    def updateFromModule(
        self
    ):

        if (
            self.sheet is None
            or
            self.module is None
        ):

            return

        for cell, propertyName in self.PARAMETERS:

            try:

                value = getattr(
                    self.module,
                    propertyName
                )

                if hasattr(
                    value,
                    "Value"
                ):

                    value = value.Value

                value = float(
                    value
                )

                # -------------------------------------------------
                # WRITE PLAIN NUMERIC VALUE
                # -------------------------------------------------

                self.sheet.set(
                    cell,
                    str(value)
                )

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error actualizando "
                    +
                    propertyName
                    +
                    " en Spreadsheet: "
                    +
                    str(error)
                    +
                    "\n"
                )

    # =========================================================
    # UPDATE PART TABLE
    #
    # All cells in the part table are literal text.
    # =========================================================

    def updatePartsTable(
        self
    ):

        if (
            self.sheet is None
            or
            self.module is None
        ):

            return

        # -----------------------------------------------------
        # GET REAL MODULE PARTS
        # -----------------------------------------------------

        parts = self._getModuleParts()

        # -----------------------------------------------------
        # CLEAR OLD TABLE
        # -----------------------------------------------------

        first_row = (
            self.PART_TABLE_START_ROW + 1
        )

        last_row = (
            first_row
            +
            self.PART_TABLE_MAX_ROWS
        )

        for row in range(
            first_row,
            last_row
        ):

            for index in range(
                len(self.PART_HEADERS)
            ):

                column = chr(
                    ord("A")
                    +
                    index
                )

                try:

                    self.sheet.set(
                        column + str(row),
                        ""
                    )

                except Exception:

                    pass

        # -----------------------------------------------------
        # WRITE PARTS
        # -----------------------------------------------------

        row = first_row

        for part in parts:

            values = (
                self._getPartTableValues(
                    part
                )
            )

            for index, value in enumerate(
                values
            ):

                column = chr(
                    ord("A")
                    +
                    index
                )

                cell = (
                    column
                    +
                    str(row)
                )

                if value is None:

                    value = ""

                else:

                    value = str(
                        value
                    )

                # -------------------------------------------------
                # LITERAL TEXT
                # -------------------------------------------------

                if value:

                    if not value.startswith("'"):

                        value = (
                            "'"
                            +
                            value
                        )

                try:

                    self.sheet.set(
                        cell,
                        value
                    )

                except Exception:

                    pass

            row += 1

    # =========================================================
    # GET MODULE PARTS
    # =========================================================

    def _getModuleParts(
        self
    ):

        if self.module is None:

            return []

        parts = []

        # -----------------------------------------------------
        # PRIMARY SOURCE
        # -----------------------------------------------------

        try:

            group = list(
                getattr(
                    self.module,
                    "Group",
                    []
                )
            )

        except Exception:

            group = []

        for obj in group:

            if obj is None:

                continue

            if self._isSheet(
                obj
            ):

                continue

            if self._isBosqoPart(
                obj
            ):

                if obj not in parts:

                    parts.append(
                        obj
                    )

        # -----------------------------------------------------
        # FALLBACK
        # -----------------------------------------------------

        for obj in group:

            if obj is None:

                continue

            if obj in parts:

                continue

            if self._isSheet(
                obj
            ):

                continue

            if self._looksLikePart(
                obj
            ):

                parts.append(
                    obj
                )

        return parts

    # =========================================================
    # IS SHEET
    # =========================================================

    def _isSheet(
        self,
        obj
    ):

        try:

            return (
                getattr(
                    obj,
                    "TypeId",
                    ""
                )
                ==
                "Spreadsheet::Sheet"
            )

        except Exception:

            return False

    # =========================================================
    # IS BOSQO PART
    # =========================================================

    def _isBosqoPart(
        self,
        obj
    ):

        try:

            proxy = getattr(
                obj,
                "Proxy",
                None
            )

        except Exception:

            proxy = None

        if proxy is not None:

            try:

                objectType = getattr(
                    proxy,
                    "ObjectType",
                    ""
                )

                if objectType == "BosqoPart":

                    return True

            except Exception:

                pass

        try:

            objectType = getattr(
                obj,
                "ObjectType",
                ""
            )

            if objectType == "BosqoPart":

                return True

        except Exception:

            pass

        return False

    # =========================================================
    # LOOKS LIKE PART
    # =========================================================

    def _looksLikePart(
        self,
        obj
    ):

        required = (
            "Length",
            "Width",
            "Thickness"
        )

        found = 0

        for propertyName in required:

            try:

                getattr(
                    obj,
                    propertyName
                )

                found += 1

            except Exception:

                pass

        return found == 3

    # =========================================================
    # GET PART VALUES
    # =========================================================

    def _getPartTableValues(
        self,
        part
    ):

        # -----------------------------------------------------
        # LABEL
        # -----------------------------------------------------

        try:

            label = str(
                getattr(
                    part,
                    "Label",
                    ""
                )
            )

        except Exception:

            label = ""

        # -----------------------------------------------------
        # TYPE
        # -----------------------------------------------------

        part_type = ""

        for propertyName in (
            "PartType",
            "Type",
            "Role"
        ):

            try:

                value = getattr(
                    part,
                    propertyName
                )

                if hasattr(
                    value,
                    "Value"
                ):

                    value = value.Value

                if value is not None:

                    value = str(
                        value
                    )

                    if value:

                        part_type = value

                        break

            except Exception:

                continue

        # -----------------------------------------------------
        # DIMENSIONS
        # -----------------------------------------------------

        length = self._getPropertyValue(
            part,
            "Length"
        )

        width = self._getPropertyValue(
            part,
            "Width"
        )

        thickness = self._getPropertyValue(
            part,
            "Thickness"
        )

        # -----------------------------------------------------
        # QUANTITY
        # -----------------------------------------------------

        quantity = self._getPropertyValue(
            part,
            "Quantity",
            1
        )

        # -----------------------------------------------------
        # MATERIAL
        # -----------------------------------------------------

        material = ""

        for propertyName in (
            "MaterialCode",
            "Material",
            "MaterialName"
        ):

            try:

                value = getattr(
                    part,
                    propertyName
                )

                if hasattr(
                    value,
                    "Value"
                ):

                    value = value.Value

                if value is not None:

                    value = str(
                        value
                    )

                    if value:

                        material = value

                        break

            except Exception:

                continue

        # -----------------------------------------------------
        # POSITION
        # -----------------------------------------------------

        position = self._getPositionText(
            part
        )

        # -----------------------------------------------------
        # MODE
        # -----------------------------------------------------

        mode = ""

        for propertyName in (
            "PositionMode",
            "PositionType"
        ):

            try:

                value = getattr(
                    part,
                    propertyName
                )

                if hasattr(
                    value,
                    "Value"
                ):

                    value = value.Value

                if value is not None:

                    value = str(
                        value
                    )

                    if value:

                        mode = value

                        break

            except Exception:

                continue

        return (

            label,
            part_type,

            self._formatLength(
                length
            ),

            self._formatLength(
                width
            ),

            self._formatLength(
                thickness
            ),

            quantity,

            material,

            position,

            mode

        )

    # =========================================================
    # GET PROPERTY VALUE
    # =========================================================

    def _getPropertyValue(
        self,
        obj,
        propertyName,
        default=""
    ):

        try:

            value = getattr(
                obj,
                propertyName
            )

        except Exception:

            return default

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

            return value

    # =========================================================
    # FORMAT LENGTH
    # =========================================================

    def _formatLength(
        self,
        value
    ):

        if value == "":

            return ""

        if value is None:

            return ""

        try:

            return (
                str(
                    round(
                        float(value),
                        3
                    )
                )
                +
                " mm"
            )

        except Exception:

            return str(
                value
            )

    # =========================================================
    # POSITION TEXT
    # =========================================================

    def _getPositionText(
        self,
        part
    ):

        values = []

        for propertyName in (
            "PositionX",
            "PositionY",
            "PositionZ"
        ):

            value = self._getPropertyValue(
                part,
                propertyName,
                None
            )

            if value is None:

                return ""

            try:

                values.append(
                    str(
                        round(
                            float(value),
                            3
                        )
                    )
                )

            except Exception:

                values.append(
                    str(value)
                )

        return (
            "X="
            +
            values[0]
            +
            " | Y="
            +
            values[1]
            +
            " | Z="
            +
            values[2]
            +
            " mm"
        )

    # =========================================================
    # UPDATE MODULE FROM SHEET
    # =========================================================

    def updateModuleFromSheet(
        self
    ):

        if (
            self.sheet is None
            or
            self.module is None
        ):

            return False

        changed = False

        for cell, propertyName in self.PARAMETERS:

            # -------------------------------------------------
            # READ REAL CELL VALUE
            # -------------------------------------------------

            try:

                value = self.sheet.get(
                    cell
                )

            except Exception:

                continue

            if value is None:

                continue

            # -------------------------------------------------
            # CONVERT
            # -------------------------------------------------

            try:

                if hasattr(
                    value,
                    "Value"
                ):

                    value = float(
                        value.Value
                    )

                else:

                    value = float(
                        value
                    )

            except Exception:

                try:

                    value = float(
                        str(value)
                    )

                except Exception:

                    continue

            # -------------------------------------------------
            # CURRENT MODULE VALUE
            # -------------------------------------------------

            try:

                current = getattr(
                    self.module,
                    propertyName
                )

                if hasattr(
                    current,
                    "Value"
                ):

                    currentValue = float(
                        current.Value
                    )

                else:

                    currentValue = float(
                        current
                    )

            except Exception:

                currentValue = None

            # -------------------------------------------------
            # NO CHANGE
            # -------------------------------------------------

            if (
                currentValue is not None
                and
                abs(
                    currentValue - value
                )
                <
                0.000001
            ):

                continue

            # -------------------------------------------------
            # SET MODULE PROPERTY
            # -------------------------------------------------

            try:

                setattr(
                    self.module,
                    propertyName,
                    value
                )

                changed = True

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error asignando "
                    +
                    propertyName
                    +
                    " desde Sheet: "
                    +
                    str(error)
                    +
                    "\n"
                )

        return changed

    # =========================================================
    # SAFE UPDATE PARAMETERS
    # =========================================================

    def _safeUpdateFromModule(
        self
    ):

        if self.sheet is None:

            return

        try:

            self.updateFromModule()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error actualizando parámetros de Sheet: "
                +
                str(error)
                +
                "\n"
            )

    # =========================================================
    # SAFE UPDATE PARTS
    # =========================================================

    def _safeUpdatePartsTable(
        self
    ):

        if self.sheet is None:

            return

        try:

            self.updatePartsTable()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error actualizando tabla de piezas: "
                +
                str(error)
                +
                "\n"
            )

    # =========================================================
    # UPDATE ALL
    # =========================================================

    def updateAll(
        self
    ):

        if (
            self.sheet is None
            or
            self.module is None
        ):

            return

        self._safeUpdateFromModule()

        self._safeUpdatePartsTable()

    # =========================================================
    # COLUMN WIDTHS
    # =========================================================

    def _setColumnWidths(
        self
    ):

        if self.sheet is None:

            return

        widths = (

            ("A", 180),
            ("B", 120),
            ("C", 100),
            ("D", 100),
            ("E", 100),
            ("F", 80),
            ("G", 140),
            ("H", 180),
            ("I", 100)

        )

        for column, width in widths:

            try:

                self.sheet.setColumnWidth(
                    column,
                    width
                )

            except Exception:

                pass

    # =========================================================
    # REPAIR GROUP
    # =========================================================

    def _repairGroup(
        self
    ):

        if (
            self.module is None
            or
            self.sheet is None
        ):

            return

        try:

            group = list(
                getattr(
                    self.module,
                    "Group",
                    []
                )
            )

            if self.sheet not in group:

                self.module.addObject(
                    self.sheet
                )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error añadiendo Spreadsheet al Group "
                "del módulo: "
                +
                str(error)
                +
                "\n"
            )


# =============================================================
# SHEET OBSERVER
# =============================================================

class BosqoSheetObserver:

    _observers = {}

    # =========================================================
    # REGISTER
    # =========================================================

    @classmethod
    def register(
        cls,
        document
    ):

        if document is None:

            return

        key = id(
            document
        )

        if key in cls._observers:

            return

        observer = (
            BosqoSheetDocumentObserver(
                document
            )
        )

        try:

            FreeCAD.addDocumentObserver(
                observer
            )

            cls._observers[key] = observer

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error registrando observer del Spreadsheet: "
                +
                str(error)
                +
                "\n"
            )


# =============================================================
# DOCUMENT OBSERVER
# =============================================================

class BosqoSheetDocumentObserver:

    def __init__(
        self,
        document
    ):

        self.document = document

        self._updatingSheet = False
        self._updatingModule = False

        self._refreshAfterRecompute = False

    # =========================================================
    # OBJECT CHANGED
    # =========================================================

    def slotChangedObject(
        self,
        obj,
        property
    ):

        if self._updatingSheet:

            return

        if obj is None:

            return

        # -----------------------------------------------------
        # SPREADSHEET
        # -----------------------------------------------------

        try:

            if (
                getattr(
                    obj,
                    "TypeId",
                    ""
                )
                ==
                "Spreadsheet::Sheet"
            ):

                if (
                    getattr(
                        obj,
                        "Name",
                        ""
                    )
                    ==
                    "ModuleParameters"
                ):

                    module = self._findModule(
                        obj
                    )

                    if module is not None:

                        self._updateModuleFromSheet(
                            obj,
                            module
                        )

                    return

        except Exception:

            return

        # -----------------------------------------------------
        # MODULE
        # -----------------------------------------------------

        if self._isModule(
            obj
        ):

            self._refreshAfterRecompute = True

            return

        # -----------------------------------------------------
        # PART
        # -----------------------------------------------------

        if self._isPart(
            obj
        ):

            self._refreshAfterRecompute = True

            return

    # =========================================================
    # OBJECT CREATED
    # =========================================================

    def slotCreatedObject(
        self,
        obj
    ):

        if obj is None:

            return

        if self._isPart(
            obj
        ):

            self._refreshAfterRecompute = True

    # =========================================================
    # RECOMPUTED DOCUMENT
    # =========================================================

    def slotRecomputedDocument(
        self,
        document
    ):

        if document is not self.document:

            return

        if self._updatingSheet:

            return

        if not self._refreshAfterRecompute:

            return

        self._refreshAfterRecompute = False

        module = self._findBosqoModule()

        if module is None:

            return

        sheet = None

        try:

            sheet = getattr(
                module,
                "ParameterSheet",
                None
            )

        except Exception:

            sheet = None

        # -----------------------------------------------------
        # FALLBACK
        # -----------------------------------------------------

        if sheet is None:

            try:

                sheet = (
                    self.document.getObject(
                        "ModuleParameters"
                    )
                )

            except Exception:

                sheet = None

        if sheet is None:

            return

        try:

            if (
                getattr(
                    sheet,
                    "TypeId",
                    ""
                )
                !=
                "Spreadsheet::Sheet"
            ):

                return

        except Exception:

            return

        # -----------------------------------------------------
        # UPDATE SHEET
        # -----------------------------------------------------

        self._updatingSheet = True

        try:

            manager = BosqoSheet(
                self.document,
                module
            )

            manager.sheet = sheet

            manager.updateFromModule()

            manager.updatePartsTable()

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error actualizando BosqoSheet después "
                "del recompute: "
                +
                str(error)
                +
                "\n"
            )

        finally:

            self._updatingSheet = False

    # =========================================================
    # FIND BOSQO MODULE
    # =========================================================

    def _findBosqoModule(
        self
    ):

        try:

            for obj in self.document.Objects:

                if obj is None:

                    continue

                proxy = getattr(
                    obj,
                    "Proxy",
                    None
                )

                if proxy is None:

                    continue

                if (
                    getattr(
                        proxy,
                        "ObjectType",
                        ""
                    )
                    ==
                    "BosqoModule"
                ):

                    return obj

        except Exception:

            pass

        return None

    # =========================================================
    # FIND MODULE FROM SHEET
    # =========================================================

    def _findModule(
        self,
        sheet
    ):

        if sheet is None:

            return None

        document = getattr(
            sheet,
            "Document",
            None
        )

        if document is None:

            return None

        try:

            for obj in document.Objects:

                if obj is None:

                    continue

                try:

                    parameterSheet = getattr(
                        obj,
                        "ParameterSheet",
                        None
                    )

                    if parameterSheet is not sheet:

                        continue

                    proxy = getattr(
                        obj,
                        "Proxy",
                        None
                    )

                    if proxy is None:

                        continue

                    if (
                        getattr(
                            proxy,
                            "ObjectType",
                            ""
                        )
                        ==
                        "BosqoModule"
                    ):

                        return obj

                except Exception:

                    continue

        except Exception:

            pass

        return None

    # =========================================================
    # UPDATE MODULE FROM SHEET
    # =========================================================

    def _updateModuleFromSheet(
        self,
        sheet,
        module
    ):

        if self._updatingModule:

            return

        self._updatingModule = True

        try:

            manager = BosqoSheet(
                self.document,
                module
            )

            manager.sheet = sheet

            changed = (
                manager.updateModuleFromSheet()
            )

            if changed:

                self._refreshAfterRecompute = True

                try:

                    self.document.recompute()

                except Exception as error:

                    FreeCAD.Console.PrintError(
                        "Error recalculando módulo desde Sheet: "
                        +
                        str(error)
                        +
                        "\n"
                    )

        except Exception as error:

            FreeCAD.Console.PrintError(
                "Error sincronizando Sheet con módulo: "
                +
                str(error)
                +
                "\n"
            )

        finally:

            self._updatingModule = False

    # =========================================================
    # IS MODULE
    # =========================================================

    def _isModule(
        self,
        obj
    ):

        try:

            proxy = getattr(
                obj,
                "Proxy",
                None
            )

            if proxy is None:

                return False

            return (
                getattr(
                    proxy,
                    "ObjectType",
                    ""
                )
                ==
                "BosqoModule"
            )

        except Exception:

            return False

    # =========================================================
    # IS PART
    # =========================================================

    def _isPart(
        self,
        obj
    ):

        if obj is None:

            return False

        try:

            if (
                getattr(
                    obj,
                    "TypeId",
                    ""
                )
                ==
                "Spreadsheet::Sheet"
            ):

                return False

        except Exception:

            pass

        try:

            proxy = getattr(
                obj,
                "Proxy",
                None
            )

        except Exception:

            proxy = None

        if proxy is not None:

            try:

                if (
                    getattr(
                        proxy,
                        "ObjectType",
                        ""
                    )
                    ==
                    "BosqoPart"
                ):

                    return True

            except Exception:

                pass

        try:

            if (
                getattr(
                    obj,
                    "ObjectType",
                    ""
                )
                ==
                "BosqoPart"
            ):

                return True

        except Exception:

            pass

        # -----------------------------------------------------
        # FALLBACK
        # -----------------------------------------------------

        found = 0

        for propertyName in (
            "Length",
            "Width",
            "Thickness"
        ):

            try:

                getattr(
                    obj,
                    propertyName
                )

                found += 1

            except Exception:

                pass

        return found == 3


# =============================================================
# CREATE SHEET
# =============================================================

def create_sheet(
    document,
    module
):

    if (
        document is None
        or
        module is None
    ):

        return None

    try:

        manager = BosqoSheet(
            document,
            module
        )

        return manager.create()

    except Exception as error:

        FreeCAD.Console.PrintError(
            "Error creando BosqoSheet: "
            +
            str(error)
            +
            "\n"
        )

        return None