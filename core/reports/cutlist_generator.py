class CutListGenerator:


    def __init__(self):

        pass



    #
    # Generate cut list from manufacturing module
    #

    def generate(
        self,
        module_manufacturing
    ):


        cutlist = []


        for part in module_manufacturing.Parts:


            item = {


                "Code": part.Code,


                "PartNumber": part.PartNumber,


                "Description": part.Description,


                "Role": part.Role,


                "Length": part.Length,


                "Width": part.Width,


                "Thickness": part.Thickness,


                "Quantity": part.Quantity,


                "Material": part.Material,


            }


            cutlist.append(
                item
            )



        return cutlist



    #
    # Text report
    #

    def toText(
        self,
        module_manufacturing
    ):


        lines = []


        lines.append(
            "LISTA DE CORTE"
        )


        lines.append(
            "============================"
        )


        lines.append(
            ""
        )


        lines.append(
            f"Modulo: {module_manufacturing.Name}"
        )


        lines.append(
            f"Tipo: {module_manufacturing.Type}"
        )


        lines.append(
            ""
        )


        lines.append(
            "Codigo | Pieza | Largo | Ancho | Espesor | Cantidad"
        )


        lines.append(
            "---------------------------------------------------"
        )


        for part in module_manufacturing.Parts:


            lines.append(

                f"{part.Code} | "
                f"{part.Description} | "
                f"{part.Length} | "
                f"{part.Width} | "
                f"{part.Thickness} | "
                f"{part.Quantity}"

            )


        return "\n".join(lines)