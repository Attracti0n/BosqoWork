import FreeCAD

from objects.bosqo_part import create_part
from core.recognizers.panel_recognizer import PanelRecognizer


class ImportBuilder:

    @staticmethod
    def build(document, objects):

        parts = []

        # =====================================================
        # IMPORT OBJECTS
        # =====================================================

        for obj in objects:

            # =================================================
            # RECOGNIZE PANEL
            # =================================================

            try:
                panel = PanelRecognizer.recognize(obj)

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

                part = create_part(document)

            except Exception as error:

                FreeCAD.Console.PrintError(
                    f"No se pudo crear BosqoPart "
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

                part.Length = abs(panel.Length)
                part.Width = abs(panel.Width)
                part.Thickness = abs(panel.Thickness)

                part.LengthAxis = panel.LengthAxis
                part.WidthAxis = panel.WidthAxis
                part.ThicknessAxis = panel.ThicknessAxis

            except Exception as error:

                FreeCAD.Console.PrintError(
                    f"Error asignando datos geométricos "
                    f"a {obj.Label}: {error}\n"
                )

                try:
                    document.removeObject(part.Name)
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

            if hasattr(part, "OriginalObject"):

                try:

                    part.OriginalObject = obj

                except Exception as error:

                    FreeCAD.Console.PrintWarning(
                        f"No se pudo guardar OriginalObject "
                        f"de {obj.Label}: {error}\n"
                    )

            # =================================================
            # RECOVER ORIGINAL POSITION
            # =================================================
            #
            # IMPORTANTE:
            #
            # NO hacemos:
            #
            #     part.Placement = obj.Placement
            #
            # La BosqoPart tiene su propia geometría local.
            #
            # Recuperamos la posición mediante BoundBox,
            # igual que en la versión antigua que funcionaba.
            #

            bound = None

            if hasattr(obj, "Mesh"):

                try:
                    bound = obj.Mesh.BoundBox
                except Exception:
                    bound = None

            elif hasattr(obj, "Shape"):

                try:
                    bound = obj.Shape.BoundBox
                except Exception:
                    bound = None

            # =================================================
            # APPLY POSITION
            # =================================================

            if bound:

                try:

                    part.Placement.Base = FreeCAD.Vector(
                        bound.XMin,
                        bound.YMin,
                        bound.ZMin
                    )

                except Exception as error:

                    FreeCAD.Console.PrintWarning(
                        "No se pudo recuperar la posición "
                        f"de {obj.Label}: {error}\n"
                    )

            # =================================================
            # RECOVER ORIGINAL ROTATION
            # =================================================

            if hasattr(obj, "Placement"):

                try:

                    part.Placement.Rotation = (
                        obj.Placement.Rotation
                    )

                except Exception as error:

                    FreeCAD.Console.PrintWarning(
                        "No se pudo recuperar la rotación "
                        f"de {obj.Label}: {error}\n"
                    )

            # =================================================
            # HIDE ORIGINAL
            # =================================================

            if hasattr(obj, "ViewObject"):

                try:

                    obj.ViewObject.Visibility = False

                except Exception as error:

                    FreeCAD.Console.PrintWarning(
                        f"No se pudo ocultar {obj.Label}: "
                        f"{error}\n"
                    )

            # =================================================
            # ADD PART
            # =================================================

            parts.append(part)

            # =================================================
            # DEBUG
            # =================================================

            FreeCAD.Console.PrintMessage(
                "\n===== IMPORTED PART =====\n"
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
                f"Error durante recompute: {error}\n"
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
                    f"No se pudo mostrar Placement "
                    f"de {part.Label}: {error}\n"
                )

        FreeCAD.Console.PrintMessage(
            f"\n{len(parts)} Bosqo Parts created.\n"
        )

        return parts