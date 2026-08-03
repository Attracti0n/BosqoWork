from datetime import datetime

from core.data.cut_list_item import CutListItem
from core.data.cut_list_summary import CutListSummary


class CutList:


    def __init__(self):


        #
        # Project
        #

        self.Project = ""

        self.Module = ""

        self.Type = ""


        #
        # Metadata
        #

        self.Generated = datetime.now()

        self.Version = "1.0"


        #
        # Data
        #

        self.Items = []

        self.Summary = CutListSummary()



    #
    # Add item
    #

    def addItem(
        self,
        item
    ):

        if isinstance(
            item,
            CutListItem
        ):

            self.Items.append(
                item
            )



    #
    # Clear
    #

    def clear(self):

        self.Items.clear()

        self.Summary = CutListSummary()



    #
    # Count
    #

    @property
    def Count(self):

        return len(
            self.Items
        )



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


        self.Version = data.get(
            "Version",
            "1.0"
        )


        self.Items = []


        for itemData in data.get(
            "Items",
            []
        ):

            item = CutListItem()

            item.fromDict(
                itemData
            )

            self.Items.append(
                item
            )


        self.Summary = CutListSummary()

        self.Summary.fromDict(
            data.get(
                "Summary",
                {}
            )
        )


        return self



    #
    # Export
    #

    def toDict(self):


        return {

            "Project": self.Project,

            "Module": self.Module,

            "Type": self.Type,

            "Generated": str(
                self.Generated
            ),

            "Version": self.Version,

            "Items": [

                item.toDict()

                for item in self.Items

            ],

            "Summary": self.Summary.toDict()

        }



    def __iter__(self):

        return iter(
            self.Items
        )



    def __len__(self):

        return len(
            self.Items
        )



    def __repr__(self):

        return (

            f"CutList("
            f"Items={len(self.Items)})"

        )