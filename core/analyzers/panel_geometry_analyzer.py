import FreeCAD

from core.geometry.panel_geometry import PanelGeometry

from core.builders.geometry_builder import GeometryBuilder
from core.builders.placement_builder import PlacementBuilder
from core.builders.face_builder import FaceBuilder
from core.builders.edge_builder import EdgeBuilder


class PanelGeometryAnalyzer:


    @staticmethod
    def analyze(obj):

        geometry = PanelGeometry()


        #
        # Basic validation
        #

        if obj is None:

            geometry.Message = "No object"

            return geometry



        if not hasattr(obj, "Shape"):

            geometry.Message = "Object has no Shape"

            return geometry



        if obj.Shape is None:

            geometry.Message = "Empty Shape"

            return geometry



        #
        # Store original shape
        #

        geometry.setShape(
            obj.Shape
        )



        #
        # Dimensions
        #

        if hasattr(obj, "Length"):

            geometry.Length = abs(
                float(obj.Length)
            )

        if hasattr(obj, "Width"):

            geometry.Width = abs(
                float(obj.Width)
            )

        if hasattr(obj, "Thickness"):

            geometry.Thickness = abs(
                float(obj.Thickness)
            )



        #
        # Axis information
        #

        if hasattr(obj, "LengthAxis"):

            geometry.LengthAxis = obj.LengthAxis


        if hasattr(obj, "WidthAxis"):

            geometry.WidthAxis = obj.WidthAxis


        if hasattr(obj, "ThicknessAxis"):

            geometry.ThicknessAxis = obj.ThicknessAxis



        #
        # Placement
        #

        geometry.Placement = (
            obj.Placement
            if hasattr(obj, "Placement")
            else None
        )



        #
        # Center and bounding box
        #

        geometry.Center = (
            obj.Shape.CenterOfMass
        )


        geometry.BoundBox = (
            obj.Shape.BoundBox
        )



        #
        # Faces
        #

        geometry.Faces = FaceBuilder.build(
            obj
        )



        #
        # Edges
        #

        geometry.Edges = EdgeBuilder.build(
            obj
        )



        #
        # Geometry validation
        #

        if len(obj.Shape.Faces) >= 6:

            geometry.IsPanel = True

            geometry.Message = (
                "Panel geometry analyzed"
            )

        else:

            geometry.Message = (
                "Not enough faces"
            )



        return geometry