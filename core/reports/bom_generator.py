from core.data.bom import BOM
from core.data.bom_item import BOMItem


class BOMGenerator:


    def generate(
        self,
        manufacturing
    ):

        bom = BOM()

        #
        # Project information
        #

        if hasattr(
            manufacturing,
            "Name"
        ):

            bom.Project = manufacturing.Name

            bom.Module = manufacturing.Name


        if hasattr(
            manufacturing,
            "Type"
        ):

            bom.Type = manufacturing.Type


        #
        # Parts
        #

        for part in manufacturing.Parts:

            key = (

                part.Code,

                part.Material,

                part.MaterialCode,

                part.Finish,

                part.GrainDirection,

                float(part.Length),

                float(part.Width),

                float(part.Thickness)

            )


            existing = bom.findItem(
                key
            )


            #
            # Already exists
            #

            if existing:

                existing.addQuantity(
                    part.Quantity
                )

                continue


            #
            # New item
            #

            item = BOMItem()

            item.fromManufacturingData(
                part
            )

            bom.addItem(
                item
            )


        #
        # Summary
        #

        self.buildSummary(
            bom
        )

        return bom


    #
    # Summary
    #

    def buildSummary(
        self,
        bom
    ):

        summary = bom.Summary

        summary.TotalUniqueParts = len(
            bom.Items
        )

        summary.TotalParts = sum(

            item.Quantity

            for item in bom.Items

        )

        materials = {}

        totalArea = 0.0

        totalVolume = 0.0

        totalOperations = 0

        totalEdgeLength = 0.0


        for item in bom.Items:

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

                * float(item.Width)

            )

            totalArea += (

                area

                * item.Quantity

            )

            #
            # Volume
            #

            volume = (

                area

                * float(item.Thickness)

            )

            totalVolume += (

                volume

                * item.Quantity

            )

            #
            # Operations
            #

            totalOperations += len(
                item.Operations
            )

            #
            # Edge length
            #

            for edge in (

                item.EdgeTop,
                item.EdgeBottom,
                item.EdgeLeft,
                item.EdgeRight

            ):

                if edge:

                    totalEdgeLength += float(
                        item.Length
                    )


        summary.Materials = materials

        summary.TotalMaterials = len(
            materials
        )

        summary.TotalArea = totalArea

        summary.TotalVolume = totalVolume

        summary.TotalOperations = totalOperations

        summary.TotalEdgeLength = totalEdgeLength