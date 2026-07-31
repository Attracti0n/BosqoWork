import FreeCAD


class MeshInspector:

    @staticmethod
    def inspect(obj):
        """
        Inspects a Mesh::Feature object and returns a report dictionary.
        """

        if obj is None:
            raise ValueError("Object is None.")

        if not hasattr(obj, "Mesh"):
            raise TypeError("Selected object is not a Mesh::Feature.")

        mesh = obj.Mesh

        report = {}

        #
        # General
        #

        report["name"] = obj.Name
        report["label"] = obj.Label
        report["type"] = obj.TypeId

        #
        # Geometry
        #

        report["vertices"] = mesh.CountPoints
        report["facets"] = mesh.CountFacets

        #
        # BoundBox
        #

        bb = mesh.BoundBox

        report["bound_box"] = {
            "xmin": bb.XMin,
            "xmax": bb.XMax,
            "ymin": bb.YMin,
            "ymax": bb.YMax,
            "zmin": bb.ZMin,
            "zmax": bb.ZMax,
        }

        #
        # Dimensions
        #

        report["dimensions"] = {
            "x": bb.XLength,
            "y": bb.YLength,
            "z": bb.ZLength,
        }

        #
        # Center
        #

        report["center"] = bb.Center

        return report

    @staticmethod
    def print(report):

        print("")
        print("===== MESH INSPECTOR =====")
        print("")

        print("General")
        print("----------------------------------")
        print(f"Name      : {report['name']}")
        print(f"Label     : {report['label']}")
        print(f"Type      : {report['type']}")

        print("")
        print("Geometry")
        print("----------------------------------")
        print(f"Vertices  : {report['vertices']}")
        print(f"Facets    : {report['facets']}")

        print("")
        print("BoundBox")
        print("----------------------------------")

        bb = report["bound_box"]

        print(f"XMin      : {bb['xmin']:.3f}")
        print(f"XMax      : {bb['xmax']:.3f}")

        print(f"YMin      : {bb['ymin']:.3f}")
        print(f"YMax      : {bb['ymax']:.3f}")

        print(f"ZMin      : {bb['zmin']:.3f}")
        print(f"ZMax      : {bb['zmax']:.3f}")

        print("")
        print("Dimensions")
        print("----------------------------------")

        d = report["dimensions"]

        print(f"X         : {d['x']:.3f}")
        print(f"Y         : {d['y']:.3f}")
        print(f"Z         : {d['z']:.3f}")

        print("")
        print("Center")
        print("----------------------------------")

        c = report["center"]

        print(f"X         : {c.x:.3f}")
        print(f"Y         : {c.y:.3f}")
        print(f"Z         : {c.z:.3f}")

        print("")