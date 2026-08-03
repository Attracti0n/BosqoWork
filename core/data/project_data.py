import FreeCAD

from core.data.module_data import ModuleData
from core.data.part_data import PartData


class ProjectData:


    def __init__(self):

        self.Name = ""

        self.FileName = ""

        self.Modules = []

        self.Parts = []


    def fromDocument(
        self,
        document=None
    ):


        if document is None:

            document = FreeCAD.ActiveDocument


        if document is None:

            return self


        self.Name = document.Label

        self.FileName = document.FileName


        self.Modules = []

        self.Parts = []


        #
        # Read modules
        #

        moduleObjects = []


        for obj in document.Objects:


            if not hasattr(
                obj,
                "Proxy"
            ):

                continue


            if type(obj.Proxy).__name__ != "BosqoModule":

                continue


            moduleObjects.append(
                obj
            )


            module = ModuleData()

            module.fromObject(
                obj
            )

            self.Modules.append(
                module
            )


        #
        # Read loose parts
        #

        for obj in document.Objects:


            if not hasattr(
                obj,
                "Proxy"
            ):

                continue


            if type(obj.Proxy).__name__ != "BosqoPart":

                continue


            insideModule = False


            for module in moduleObjects:

                if obj in module.Group:

                    insideModule = True

                    break


            if insideModule:

                continue


            part = PartData()

            part.fromObject(
                obj
            )

            self.Parts.append(
                part
            )


        return self


    def toDict(
        self
    ):


        return {

            "Name":
                self.Name,

            "FileName":
                self.FileName,

            "Modules": [

                module.toDict()

                for module in self.Modules

            ],

            "Parts": [

                part.toDict()

                for part in self.Parts

            ]

        }