import FreeCAD

from objects.bosqo_part import create_part
from core.recognizers.panel_recognizer import PanelRecognizer


class ImportBuilder:

    # =========================================================
    # BOUND BOX
    # =========================================================

    @staticmethod
    def _get_bound_box(obj):

        #
        # Preferimos Shape porque contiene la geometría
        # principal de los objetos Part.
        #

        if hasattr(obj, "Shape"):

            try:

                shape = obj.Shape

                if shape is not None and not shape.isNull():

                    return shape.BoundBox

            except Exception:
                pass

        #
        # Si no hay Shape válido, intentamos Mesh.
        #

        if hasattr(obj, "Mesh"):

            try:

                mesh = obj.Mesh

                if mesh is not None:

                    return mesh.BoundBox

            except Exception:
                pass

        return None

    # =========================================================
    # ROTATION
    # =========================================================

    @staticmethod
    def _get_rotation(obj):

        #
        # Primero intentamos Placement del objeto.
        #

        if hasattr(obj, "Placement"):

            try:

                return obj.Placement.Rotation

            except Exception:
                pass

        #
        # Como alternativa, intentamos Shape.Placement.
        #

        if hasattr(obj, "Shape"):

            try:

                return obj.Shape.Placement.Rotation

            except Exception:
                pass

        return FreeCAD.Rotation()

    # =========================================================
    # POSITION
    # =========================================================

    @staticmethod
    def _apply_placement(part, obj):

        #
        # Recuperar la posición real de la geometría importada.
        #

        bound = ImportBuilder._get_bound_box(obj)

        if bound is not None:

            try:

                part.Placement.Base = FreeCAD.Vector(
                    float(bound.XMin),
                    float(bound.YMin),
                    float(bound.ZMin)
                )

            except Exception as error:

                FreeCAD.Console.PrintWarning(
                    "No se pudo recuperar la posición "
                    f"de {obj.Label}: {error}\n"
                )

        else:

            FreeCAD.Console.PrintWarning(
                f"No se encontró BoundBox para {obj.Label}\n"
            )

        #
        # Recuperar rotación original.
        #

        try:

            rotation = ImportBuilder._get_rotation(
                obj
            )

            part.Placement.Rotation = rotation

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                "No se pudo recuperar la rotación "
                f"de {obj.Label}: {error}\n"
            )

    # =========================================================
    # BUILD
    # =========================================================

    @staticmethod
    def build(document, objects):

        parts = []

        # =====================================================
        # IMPORT OBJECTS
        # =====================================================

        for obj in objects:

            # =================================================
            # DEBUG ORIGINAL OBJECT
            # =================================================

            FreeCAD.Console.PrintMessage(
                "\n========================================\n"
            )

            FreeCAD.Console.PrintMessage(
                "IMPORTANDO OBJETO\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Label: {obj.Label}\n"
            )

            try:

                FreeCAD.Console.PrintMessage(
                    f"Original Placement: "
                    f"{obj.Placement}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"Original Base: "
                    f"{obj.Placement.Base}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"Original Rotation: "
                    f"{obj.Placement.Rotation}\n"
                )

            except Exception:

                FreeCAD.Console.PrintMessage(
                    "Original Placement: no disponible\n"
                )

            # =================================================
            # RECOGNIZE PANEL
            # =================================================

            try:

                panel = PanelRecognizer.recognize(
                    obj
                )

            except Exception as error:

                FreeCAD.Console.PrintWarning(
                    f"{obj.Label}: {error}\n"
                )

                continue

            # =================================================
            # CHECK PANEL
            # =================================================

            if not panel.IsPanel:

                FreeCAD.Console.PrintWarning(
                    f"{obj.Label}: {panel.Message}\n"
                )

                continue

            # =================================================
            # CREATE BOSQO PART
            # =================================================

            try:

                part = create_part(
                    document
                )

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "No se pudo crear BosqoPart "
                    f"para {obj.Label}: {error}\n"
                )

                continue

            # =================================================
            # LABEL
            # =================================================

            part.Label = obj.Label

            # =================================================
            # BASIC DATA
            # =================================================

            try:

                #
                # IMPORTANTE:
                #
                # Las dimensiones vienen directamente del
                # PanelRecognizer.
                #
                # No hacemos redondeos.
                #

                part.Length = abs(
                    float(panel.Length)
                )

                part.Width = abs(
                    float(panel.Width)
                )

                part.Thickness = abs(
                    float(panel.Thickness)
                )

                part.LengthAxis = (
                    panel.LengthAxis
                )

                part.WidthAxis = (
                    panel.WidthAxis
                )

                part.ThicknessAxis = (
                    panel.ThicknessAxis
                )

            except Exception as error:

                FreeCAD.Console.PrintError(
                    "Error asignando datos geométricos "
                    f"a {obj.Label}: {error}\n"
                )

                try:

                    document.removeObject(
                        part.Name
                    )

                except Exception:
                    pass

                continue

            # =================================================
            # SOURCE
            # =================================================

            part.Source = "Imported"

            # =================================================
            # ORIGINAL OBJECT
            # =================================================

            if hasattr(
                part,
                "OriginalObject"
            ):

                try:

                    part.OriginalObject = obj

                except Exception as error:

                    FreeCAD.Console.PrintWarning(
                        "No se pudo guardar "
                        f"OriginalObject de {obj.Label}: "
                        f"{error}\n"
                    )

            # =================================================
            # PLACEMENT
            # =================================================
            #
            # La geometría del BosqoPart es LOCAL.
            #
            # GeometryBuilder crea:
            #
            #     Box(0,0,0)
            #
            # Por tanto necesitamos trasladar esa geometría
            # a la posición original mediante Placement.
            #

            ImportBuilder._apply_placement(
                part,
                obj
            )

            # =================================================
            # DEBUG BOUND BOX
            # =================================================

            bound = ImportBuilder._get_bound_box(
                obj
            )

            if bound is not None:

                FreeCAD.Console.PrintMessage(
                    "\n===== IMPORTED BOUND BOX =====\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"XMin: {bound.XMin}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"YMin: {bound.YMin}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"ZMin: {bound.ZMin}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"XLength: {bound.XLength}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"YLength: {bound.YLength}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"ZLength: {bound.ZLength}\n"
                )

            # =================================================
            # HIDE ORIGINAL
            # =================================================

            if hasattr(
                obj,
                "ViewObject"
            ):

                try:

                    obj.ViewObject.Visibility = False

                except Exception as error:

                    FreeCAD.Console.PrintWarning(
                        f"No se pudo ocultar "
                        f"{obj.Label}: {error}\n"
                    )

            # =================================================
            # ADD PART
            # =================================================

            parts.append(
                part
            )

            # =================================================
            # DEBUG IMPORTED PART
            # =================================================

            FreeCAD.Console.PrintMessage(
                "\n===== IMPORTED BOSQO PART =====\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Label: {part.Label}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Length: {part.Length}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Width: {part.Width}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Thickness: {part.Thickness}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"LengthAxis: {part.LengthAxis}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"WidthAxis: {part.WidthAxis}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"ThicknessAxis: {part.ThicknessAxis}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Source: {part.Source}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Placement: {part.Placement}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Base: {part.Placement.Base}\n"
            )

            FreeCAD.Console.PrintMessage(
                f"Rotation: {part.Placement.Rotation}\n"
            )

        # =====================================================
        # RECOMPUTE
        # =====================================================

        try:

            document.recompute()

        except Exception as error:

            FreeCAD.Console.PrintWarning(
                f"Error durante recompute: "
                f"{error}\n"
            )

        # =====================================================
        # FINAL DEBUG
        # =====================================================

        FreeCAD.Console.PrintMessage(
            "\n===== IMPORT FINISHED =====\n"
        )

        for part in parts:

            try:

                FreeCAD.Console.PrintMessage(
                    f"\n{part.Label}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"Length = {part.Length}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"Width = {part.Width}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"Thickness = {part.Thickness}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"Placement = {part.Placement}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"Base = {part.Placement.Base}\n"
                )

                FreeCAD.Console.PrintMessage(
                    f"Rotation = {part.Placement.Rotation}\n"
                )

            except Exception as error:

                FreeCAD.Console.PrintWarning(
                    "No se pudo mostrar información "
                    f"de {part.Label}: {error}\n"
                )

        FreeCAD.Console.PrintMessage(
            f"\n{len(parts)} Bosqo Parts created.\n"
        )

        return parts