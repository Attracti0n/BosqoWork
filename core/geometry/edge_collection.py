from core.geometry.edge_data import EdgeData


class EdgeCollection:

    def __init__(self):

        #
        # Logical edges
        #

        self.Top = EdgeData()

        self.Bottom = EdgeData()

        self.Left = EdgeData()

        self.Right = EdgeData()

        self.Top.Name = "Top"
        self.Bottom.Name = "Bottom"
        self.Left.Name = "Left"
        self.Right.Name = "Right"

    @property
    def All(self):

        return [
            self.Top,
            self.Bottom,
            self.Left,
            self.Right
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

        return None

    def __iter__(self):

        return iter(self.All)

    def __len__(self):

        return len(self.All)

    def __repr__(self):

        return (
            "EdgeCollection("
            f"{len(self.All)} edges)"
        )