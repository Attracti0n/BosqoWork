from core.data.cut_list import CutList
from core.data.cut_list_item import CutListItem



class CutListGenerator:


    def generate(
        self,
        manufacturing
    ):


        cutlist = CutList()



        #
        # Project information
        #

        if hasattr(
            manufacturing,
            "Name"
        ):

            cutlist.Project = manufacturing.Name

            cutlist.Module = manufacturing.Name



        if hasattr(
            manufacturing,
            "Type"
        ):

            cutlist.Type = manufacturing.Type



        #
        # Project with modules
        #

        if hasattr(
            manufacturing,
            "Modules"
        ):


            for module in manufacturing.Modules:


                for part in module.Parts:


                    self.addPart(
                        cutlist,
                        part
                    )



        #
        # Loose parts
        #

        if hasattr(
            manufacturing,
            "Parts"
        ):


            for part in manufacturing.Parts:


                self.addPart(
                    cutlist,
                    part
                )



        #
        # Summary
        #

        self.buildSummary(
            cutlist
        )


        return cutlist



    #
    # Add manufacturing part
    #

    def addPart(
        self,
        cutlist,
        part
    ):


        item = CutListItem()


        item.fromManufacturingData(
            part
        )


        cutlist.addItem(
            item
        )



    #
    # Summary
    #

    def buildSummary(
        self,
        cutlist
    ):


        summary = cutlist.Summary



        summary.TotalUniqueParts = len(
            cutlist.Items
        )


        summary.TotalParts = sum(

            item.Quantity

            for item in cutlist.Items

        )



        materials = {}

        totalArea = 0.0

        totalVolume = 0.0

        totalOperations = 0

        totalEdgeLength = 0.0



        for item in cutlist.Items:



            #
            # Materials
            #

            material = item.Material


            if not material:

                material = "Undefined"



            materials[material] = (

                materials.get(
                    material,
                    0
                )

                + item.Quantity

            )



            #
            # Area
            #

            area = (

                float(item.Length)

                *
                float(item.Width)

            )


            totalArea += (

                area

                *
                item.Quantity

            )



            #
            # Volume
            #

            volume = (

                area

                *
                float(item.Thickness)

            )


            totalVolume += (

                volume

                *
                item.Quantity

            )



            #
            # Operations
            #

            totalOperations += len(

                item.Operations

            )



            #
            # Edges
            #

            for edge in (

                item.EdgeTop,
                item.EdgeBottom,
                item.EdgeLeft,
                item.EdgeRight

            ):


                if edge:


                    if edge in (
                        "1",
                        "True",
                        True
                    ):


                        totalEdgeLength += (

                            float(item.Length)

                        )



        summary.Materials = materials

        summary.TotalMaterials = len(
            materials
        )

        summary.TotalArea = totalArea

        summary.TotalVolume = totalVolume

        summary.TotalOperations = totalOperations

        summary.TotalEdgeLength = totalEdgeLength