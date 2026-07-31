import FreeCAD

from objects.bosqo_part import create_part
from core.recognizers.panel_recognizer import PanelRecognizer


class ImportBuilder:


    @staticmethod
    def build(document, objects):

        parts = []


        for obj in objects:


            try:

                panel = PanelRecognizer.recognize(obj)


            except Exception as error:


                FreeCAD.Console.PrintWarning(
                    f"{obj.Label}: {error}\n"
                )

                continue



            if not panel.IsPanel:


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


            part.Length = abs(panel.Length)

            part.Width = abs(panel.Width)

            part.Thickness = abs(panel.Thickness)



            #
            # Axis mapping
            #

            part.LengthAxis = panel.LengthAxis

            part.WidthAxis = panel.WidthAxis

            part.ThicknessAxis = panel.ThicknessAxis



            #
            # Source
            #

            part.Source = "Imported"



            #
            # Keep original object
            #

            if hasattr(part, "OriginalObject"):

                part.OriginalObject = obj



            #
            # Recover real position
            #
            # Imported meshes usually have Placement = 0.
            # The position is stored in the geometry coordinates.
            #

            bound = None


            if hasattr(obj, "Mesh"):

                bound = obj.Mesh.BoundBox


            elif hasattr(obj, "Shape"):

                bound = obj.Shape.BoundBox



            if bound:


                part.Placement.Base = FreeCAD.Vector(

                    bound.XMin,
                    bound.YMin,
                    bound.ZMin

                )


                FreeCAD.Console.PrintMessage(
                    "\n===== RECOVERED POSITION =====\n"
                )


                FreeCAD.Console.PrintMessage(
                    f"Position: {part.Placement.Base}\n"
                )



            #
            # Recover rotation
            #

            if hasattr(obj, "Placement"):


                part.Placement.Rotation = obj.Placement.Rotation



                FreeCAD.Console.PrintMessage(
                    "\n===== ORIGINAL ROTATION =====\n"
                )


                FreeCAD.Console.PrintMessage(
                    f"{obj.Placement.Rotation}\n"
                )



            #
            # Reset parametric coordinates
            #

            part.baseX = 0

            part.baseY = 0

            part.baseZ = 0



            #
            # Hide original object
            #

            if hasattr(obj, "ViewObject"):

                obj.ViewObject.Visibility = False



            parts.append(part)



        document.recompute()



        FreeCAD.Console.PrintMessage(
            "\n===== IMPORT FINISHED =====\n"
        )



        for part in parts:


            FreeCAD.Console.PrintMessage(
                f"{part.Label}\n"
            )


            FreeCAD.Console.PrintMessage(
                f"Placement = {part.Placement}\n"
            )


            FreeCAD.Console.PrintMessage(
                f"Position = {part.Placement.Base}\n\n"
            )



        FreeCAD.Console.PrintMessage(
            f"{len(parts)} Bosqo Parts created.\n"
        )



        return parts