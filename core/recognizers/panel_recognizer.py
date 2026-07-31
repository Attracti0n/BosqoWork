from core.data.panel_data import PanelData

from core.analyzers.shape_analyzer import ShapeAnalyzer
from core.analyzers.mesh_analyzer import MeshAnalyzer
from core.analyzers.plane_analyzer import PlaneAnalyzer


class PanelRecognizer:

    @staticmethod
    def recognize(obj):

        panel = PanelData()

        #
        # Null object
        #

        if obj is None:

            panel.Reason = "NULL_OBJECT"
            panel.Message = "Object is None."

            return panel

        #
        # Save source object
        #

        panel.Object = obj

        #
        # Analyze geometry
        #

        try:

            if hasattr(obj, "Shape"):

                geometry = ShapeAnalyzer.analyze(obj)

            elif hasattr(obj, "Mesh"):

                geometry = MeshAnalyzer.analyze(obj)

            else:

                panel.Reason = "UNSUPPORTED"

                panel.Message = "Unsupported object."

                return panel

        except Exception as e:

            panel.Reason = "ANALYSIS_ERROR"

            panel.Message = str(e)

            return panel

        #
        # Basic validation
        #

        if geometry.Thickness <= 0:

            panel.Reason = "ZERO_THICKNESS"

            panel.Message = "Not a panel."

            return panel

        if geometry.Width <= geometry.Thickness:

            panel.Reason = "INVALID_WIDTH"

            panel.Message = "Invalid width."

            return panel

        if geometry.Length <= geometry.Thickness:

            panel.Reason = "INVALID_LENGTH"

            panel.Message = "Invalid length."

            return panel

        #
        # Copy geometry
        #

        panel.IsPanel = True

        panel.Reason = "PANEL"

        panel.Length = geometry.Length
        panel.Width = geometry.Width
        panel.Thickness = geometry.Thickness

        panel.Center = geometry.Center
        panel.BoundBox = geometry.BoundingBox

        panel.LengthAxis = geometry.LengthAxis
        panel.WidthAxis = geometry.WidthAxis
        panel.ThicknessAxis = geometry.ThicknessAxis

        #
        # Shape only
        #

        if hasattr(obj, "Shape"):

            planes = PlaneAnalyzer.analyze(obj)

            if len(planes) >= 2:

                planes.sort(
                    key=lambda plane: plane.Area,
                    reverse=True
                )

                panel.FrontPlane = planes[0]
                panel.BackPlane = planes[1]

        panel.Message = "Panel recognized."

        return panel