import Part

from core.data.plane_data import PlaneData


class PlaneAnalyzer:

    @staticmethod
    def analyze(obj):

        if (
            not hasattr(obj, "Shape")
            or obj.Shape.isNull()
        ):

            raise Exception(
                "Object has no Shape."
            )

        planes = []

        for face in obj.Shape.Faces:

            surface = face.Surface

            if not isinstance(
                surface,
                Part.Plane
            ):

                continue

            plane = PlaneData()

            plane.Face = face

            plane.Area = face.Area

            plane.Center = face.CenterOfMass

            plane.Normal = face.normalAt(
                0,
                0
            )

            plane.SurfaceType = "Plane"

            plane.IsPlane = True

            planes.append(
                plane
            )

        return planes