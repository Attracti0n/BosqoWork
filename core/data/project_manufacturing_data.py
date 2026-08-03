from core.data.module_manufacturing_data import ModuleManufacturingData
from core.data.manufacturing_data import ManufacturingData



class ProjectManufacturingData:


    def __init__(self):


        #
        # Project
        #

        self.Name = ""

        self.FileName = ""


        #
        # Manufacturing groups
        #

        self.Modules = []

        self.Parts = []


        #
        # Status
        #

        self.Status = "Ready"



    #
    # Convert from ProjectData
    #

    def fromProjectData(
        self,
        projectData
    ):


        #
        # Basic data
        #

        self.Name = projectData.Name

        self.FileName = projectData.FileName


        #
        # Reset
        #

        self.Modules = []

        self.Parts = []



        #
        # Modules
        #

        for moduleData in projectData.Modules:


            manufacturing = ModuleManufacturingData()


            manufacturing.fromModuleData(
                moduleData
            )


            self.Modules.append(
                manufacturing
            )



        #
        # Loose parts
        #

        for partData in projectData.Parts:


            manufacturing = ManufacturingData()


            manufacturing.fromPartData(
                partData
            )


            self.Parts.append(
                manufacturing
            )



        return self



    #
    # Add module
    #

    def addModule(
        self,
        module
    ):

        self.Modules.append(
            module
        )



    #
    # Add loose part
    #

    def addPart(
        self,
        part
    ):

        self.Parts.append(
            part
        )



    #
    # Export
    #

    def toDict(
        self
    ):


        return {


            "Name":

                self.Name,


            "FileName":

                self.FileName,


            "Modules":

                [

                    module.toDict()

                    for module in self.Modules

                ],


            "Parts":

                [

                    part.toDict()

                    for part in self.Parts

                ],


            "Status":

                self.Status

        }