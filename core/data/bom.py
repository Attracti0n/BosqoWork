from core.data.bom_item import BOMItem
from core.data.bom_summary import BOMSummary


class BOM:


    def __init__(self):


        #
        # Information
        #

        self.Project = ""

        self.Module = ""

        self.Type = ""


        #
        # Items
        #

        self.Items = []


        #
        # Summary
        #

        self.Summary = BOMSummary()


    #
    # Add item
    #

    def addItem(
        self,
        item
    ):

        self.Items.append(
            item
        )


    #
    # Find existing item
    #

    def findItem(
        self,
        key
    ):

        for item in self.Items:

            if (

                item.Code,
                item.Material,
                item.MaterialCode,
                item.Finish,
                item.GrainDirection,
                float(item.Length),
                float(item.Width),
                float(item.Thickness)

            ) == key:

                return item

        return None


    #
    # Export
    #

    def toDict(self):

        return {

            "Project":
                self.Project,

            "Module":
                self.Module,

            "Type":
                self.Type,

            "Items": [

                item.toDict()

                for item in self.Items

            ],

            "Summary":
                self.Summary.toDict()

        }


    #
    # Import
    #

    def fromDict(
        self,
        data
    ):

        self.Project = data.get(
            "Project",
            ""
        )

        self.Module = data.get(
            "Module",
            ""
        )

        self.Type = data.get(
            "Type",
            ""
        )

        self.Items = []


        for itemData in data.get(
            "Items",
            []
        ):

            item = BOMItem()

            item.fromDict(
                itemData
            )

            self.Items.append(
                item
            )


        self.Summary.fromDict(
            data.get(
                "Summary",
                {}
            )
        )

        return self