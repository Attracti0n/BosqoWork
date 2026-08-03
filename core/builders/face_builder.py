import FreeCAD

from core.geometry.face_collection import FaceCollection


class FaceBuilder:

    TOLERANCE = 0.001

    @staticmethod
    def build(obj):

        faces = FaceCollection()

        if not hasattr(obj, "Shape"):
            return faces

        shape = obj.Shape

        if shape is None:
            return faces

        #
        # Determine axis mapping
        #

        lengthAxis = obj.LengthAxis
        widthAxis = obj.WidthAxis
        thicknessAxis = obj.ThicknessAxis

        #
        # Candidate faces
        #

        lengthFaces = []
        widthFaces = []
        thicknessFaces = []

        for face in shape.Faces:

            normal = face.normalAt(0, 0)

            axis = FaceBuilder.getAxis(normal)

            center = face.CenterOfMass

            item = {

                "Face": face,
                "Axis": axis,
                "Center": center,
                "Normal": normal

            }

            if axis == lengthAxis:

                lengthFaces.append(item)

            elif axis == widthAxis:

                widthFaces.append(item)

            elif axis == thicknessAxis:

                thicknessFaces.append(item)

        #
        # Front / Back
        #

        FaceBuilder.assignPair(
            thicknessFaces,
            thicknessAxis,
            faces.Front,
            faces.Back
        )

        #
        # Left / Right
        #

        FaceBuilder.assignPair(
            lengthFaces,
            lengthAxis,
            faces.Left,
            faces.Right
        )

        #
        # Bottom / Top
        #

        FaceBuilder.assignPair(
            widthFaces,
            widthAxis,
            faces.Bottom,
            faces.Top
        )

        return faces

    @staticmethod
    def assignPair(source, axis, first, second):

        if len(source) != 2:
            return

        coordinate = axis.lower()

        source.sort(
            key=lambda item: getattr(
                item["Center"],
                coordinate
            )
        )

        FaceBuilder.fill(
            first,
            source[0]
        )

        FaceBuilder.fill(
            second,
            source[1]
        )

    @staticmethod
    def fill(faceData, item):

        face = item["Face"]

        faceData.Face = face

        faceData.Area = face.Area

        faceData.Center = face.CenterOfMass

        faceData.Normal = item["Normal"]

        faceData.Edges = face.Edges

        faceData.Vertexes = face.Vertexes

    @staticmethod
    def getAxis(vector):

        x = abs(vector.x)
        y = abs(vector.y)
        z = abs(vector.z)

        if x >= y and x >= z:
            return "X"

        if y >= x and y >= z:
            return "Y"

        return "Z"