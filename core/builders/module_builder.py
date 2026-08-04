import FreeCAD

from objects.bosqo_part import create_part

from core.generators.generator_factory import GeneratorFactory
from core.calculators.module_calculator import ModuleCalculator


class ModuleBuilder:


    @staticmethod
    def build(
        module
    ):

        #
        # Get generator
        #

        generator = GeneratorFactory.get(
            module.Type
        )


        #
        # Get part definitions
        #

        definitions = generator.generate(
            module
        )


        #
        # Calculate complete part data
        #

        parts_data = []

        for definition in definitions:

            data = ModuleCalculator.calculate(
                module,
                definition
            )

            parts_data.append(
                data
            )


        #
        # Create or update parts
        #

        for data in parts_data:

            code = data["Code"]


            #
            # Find existing part
            #

            part = ModuleBuilder.find(
                module,
                code
            )


            #
            # Create if necessary
            #

            if part is None:

                part = ModuleBuilder.create(
                    module
                )


            #
            # Apply data
            #

            part.Proxy.setData(
                part,
                data
            )


            #
            # Recompute geometry
            #

            part.touch()


        #
        # Remove obsolete parts
        #

        valid_codes = {

            data["Code"]

            for data in parts_data

        }


        for part in list(
            module.Group
        ):

            #
            # Ignore objects that are not
            # BosqoPart objects
            #

            if not hasattr(
                part,
                "Code"
            ):

                continue


            #
            # Remove obsolete part
            #

            if part.Code not in valid_codes:

                module.removeObject(
                    part
                )

                module.Document.removeObject(
                    part.Name
                )


        #
        # Recompute document
        #

        module.Document.recompute()


    #
    # Find part
    #

    @staticmethod
    def find(
        module,
        code
    ):

        for part in module.Group:

            if not hasattr(
                part,
                "Code"
            ):

                continue


            if part.Code == code:

                return part


        return None


    #
    # Create part
    #

    @staticmethod
    def create(
        module
    ):

        part = create_part(
            module.Document
        )


        #
        # Add part to module
        #

        module.addObject(
            part
        )


        return part