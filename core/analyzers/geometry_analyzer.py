from core.analyzers.shape_analyzer import ShapeAnalyzer
from core.analyzers.mesh_analyzer import MeshAnalyzer


class GeometryAnalyzer:

    @staticmethod
    def analyze(obj):

        if hasattr(obj, "Shape"):

            shape = obj.Shape

            if (
                shape is not None
                and not shape.isNull()
            ):

                return ShapeAnalyzer.analyze(
                    obj
                )

        if hasattr(obj, "Mesh"):

            mesh = obj.Mesh

            if mesh is not None:

                return MeshAnalyzer.analyze(
                    obj
                )

        raise Exception(
            "Object has no supported geometry."
        )