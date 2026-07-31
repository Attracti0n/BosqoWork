import FreeCAD

from objects.bosqo_part import create_part
from library.parts_library import PARTS_LIBRARY
from core.calculators.module_calculator import ModuleCalculator


class ModuleBuilder:


    @staticmethod
    def build(module):


        definitions = PARTS_LIBRARY["KitchenBase"]


        #
        # Existing parts
        #

        existing = {}


        for part in module.Group:


            if hasattr(part, "Code"):

                existing[part.Code] = part



        #
        # Build required parts
        #

        used = []


        for definition in definitions:


            code = definition["Code"]



            if code in existing:


                part = existing[code]


            else:


                part = ModuleBuilder.create(
                    module
                )

                part.Code = code



            data = ModuleCalculator.calculate(
                module,
                definition
            )



            part.Proxy.setData(
                part,
                data
            )


            part.touch()


            used.append(part)



        #
        # Remove obsolete parts
        #

        for part in list(module.Group):


            if part not in used:


                module.removeObject(
                    part
                )


                try:

                    module.Document.removeObject(
                        part.Name
                    )

                except:

                    pass



        module.Document.recompute()



    @staticmethod
    def create(module):


        part = create_part(
            module.Document
        )


        module.addObject(
            part
        )


        return part