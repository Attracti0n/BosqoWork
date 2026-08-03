from core.geometry.face_data import FaceData


class FaceCollection:

    def __init__(self):

        #
        # Logical faces
        #

        self.Top = FaceData()

        self.Bottom = FaceData()

        self.Left = FaceData()

        self.Right = FaceData()

        self.Front = FaceData()

        self.Back = FaceData()

        self.Top.Name = "Top"
        self.Bottom.Name = "Bottom"
        self.Left.Name = "Left"
        self.Right.Name = "Right"
        self.Front.Name = "Front"
        self.Back.Name = "Back"

    @property
    def All(self):

        return [

            self.Top,
            self.Bottom,

            self.Left,
            self.Right,

            self.Front,
            self.Back

        ]

    def get(self, name):

        if name == "Top":
            return self.Top

        if name == "Bottom":
            return self.Bottom

        if name == "Left":
            return self.Left

        if name == "Right":
            return self.Right

        if name == "Front":
            return self.Front

        if name == "Back":
            return self.Back

        return None

    def __iter__(self):

        return iter(self.All)

    def __len__(self):

        return len(self.All)

    def __repr__(self):

        return (
            f"FaceCollection({len(self.All)} faces)"
        )