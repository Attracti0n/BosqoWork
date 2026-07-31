import FreeCAD

from objects.bosqo_part import create_part

from core.recognizers.panel_recognizer import PanelRecognizer


class ImportBuilder:

    @staticmethod
    def build(document, objects):

        parts = []

        imported = 0
        skipped = 0
        errors = 0

        for obj in objects:

            try:

                panel = PanelRecognizer.recognize(obj)

            except Exception as error:

                errors += 1

                FreeCAD.Console.PrintWarning(
                    f"{obj.Label}: {error}\n"
                )

                continue

            #
            # Not a panel
            #

            if not panel.IsPanel:

                #
                # Expected geometries
                #

                if panel.Reason in [

                    "ZERO_THICKNESS",
                    "INVALID_WIDTH",
                    "INVALID_LENGTH"

                ]:

                    skipped += 1
                    continue

                #
                # Unexpected problem
                #

                errors += 1

                FreeCAD.Console.PrintWarning(
                    f"{obj.Label}: {panel.Message}\n"
                )

                continue

            #
            # Create BOSQO Part
            #

            part = create_part(document)

            #
            # Basic properties
            #

            part.Label = obj.Label

            part.Length = panel.Length
            part.Width = panel.Width
            part.Thickness = panel.Thickness

            #
            # Orientation
            #

            part.LengthAxis = panel.LengthAxis
            part.WidthAxis = panel.WidthAxis
            part.ThicknessAxis = panel.ThicknessAxis

            #
            # Source
            #

            part.Source = "Imported"

            #
            # Geometry origin
            #

            if panel.BoundBox:

                part.OriginX = panel.BoundBox.XMin
                part.OriginY = panel.BoundBox.YMin
                part.OriginZ = panel.BoundBox.ZMin

            #
            # Keep reference to original object
            #

            if hasattr(part, "OriginalObject"):

                part.OriginalObject = panel.Object

            #
            # Hide original object
            #

            if hasattr(obj, "ViewObject"):

                obj.ViewObject.Visibility = False

            parts.append(part)

            imported += 1

        document.recompute()

        FreeCAD.Console.PrintMessage("\n")
        FreeCAD.Console.PrintMessage("===== IMPORT SUMMARY =====\n")
        FreeCAD.Console.PrintMessage(f"Panels imported : {imported}\n")
        FreeCAD.Console.PrintMessage(f"Skipped objects : {skipped}\n")
        FreeCAD.Console.PrintMessage(f"Errors          : {errors}\n")
        FreeCAD.Console.PrintMessage("==========================\n")

        return parts