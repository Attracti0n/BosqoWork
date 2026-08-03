import FreeCAD

from core.geometry.edge_collection import EdgeCollection


class EdgeBuilder:

    TOLERANCE = 0.001

    @staticmethod
    def build(obj):

        edges = EdgeCollection()

        if not hasattr(obj, "Shape"):
            return edges

        shape = obj.Shape

        if shape is None:
            return edges

        #
        # Determine panel plane
        #

        if obj.ThicknessAxis == "X":

            plane1 = "Y"
            plane2 = "Z"

        elif obj.ThicknessAxis == "Y":

            plane1 = "X"
            plane2 = "Z"

        else:

            plane1 = "X"
            plane2 = "Y"

        candidates = []

        #
        # Analyse every edge
        #

        for edge in shape.Edges:

            if len(edge.Vertexes) != 2:
                continue

            p1 = edge.Vertexes[0].Point
            p2 = edge.Vertexes[1].Point

            dx = abs(p2.x - p1.x)
            dy = abs(p2.y - p1.y)
            dz = abs(p2.z - p1.z)

            axis = ""

            if dx > dy and dx > dz:
                axis = "X"

            elif dy > dx and dy > dz:
                axis = "Y"

            else:
                axis = "Z"

            #
            # Ignore thickness direction
            #

            if axis == obj.ThicknessAxis:
                continue

            #
            # Ignore tiny edges
            #

            if edge.Length < 1:
                continue

            candidates.append({

                "Edge": edge,
                "Axis": axis,
                "Center": edge.CenterOfMass,
                "Length": edge.Length

            })

        #
        # Nothing found
        #

        if not candidates:
            return edges

        #
        # Separate both directions
        #

        first = [
            e for e in candidates
            if e["Axis"] == plane1
        ]

        second = [
            e for e in candidates
            if e["Axis"] == plane2
        ]

        #
        # Keep only the longest edges
        #

        first.sort(
            key=lambda e: e["Length"],
            reverse=True
        )

        second.sort(
            key=lambda e: e["Length"],
            reverse=True
        )

        first = first[:2]
        second = second[:2]

        #
        # Left / Right
        #

        if len(first) == 2:

            coord = plane2.lower()

            first.sort(
                key=lambda e: getattr(
                    e["Center"],
                    coord
                )
            )

            EdgeBuilder.fill(
                edges.Left,
                first[0]
            )

            EdgeBuilder.fill(
                edges.Right,
                first[1]
            )

        #
        # Bottom / Top
        #

        if len(second) == 2:

            coord = plane1.lower()

            second.sort(
                key=lambda e: getattr(
                    e["Center"],
                    coord
                )
            )

            EdgeBuilder.fill(
                edges.Bottom,
                second[0]
            )

            EdgeBuilder.fill(
                edges.Top,
                second[1]
            )

        return edges

    @staticmethod
    def fill(edgeData, data):

        edge = data["Edge"]

        edgeData.Edge = edge

        edgeData.Axis = data["Axis"]

        edgeData.Length = edge.Length

        edgeData.Start = edge.Vertexes[0].Point

        edgeData.End = edge.Vertexes[1].Point

        edgeData.Center = edge.CenterOfMass