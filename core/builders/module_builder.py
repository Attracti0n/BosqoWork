import FreeCAD

from objects.bosqo_part import create_part
from core.generators.generator_factory import GeneratorFactory


class ModuleBuilder:

    @staticmethod
    def build(module):

        #
        # Get generator
        #

        generator = GeneratorFactory.get(
            module.Type
        )

        #
        # Generate parts
        #

        parts_data = generator.generate(
            module
        )

        #
        # Create or update parts
        #

        for data in parts_data:

            code = data["Code"]

            part = ModuleBuilder.find(
                module,
                code
            )

            if part is None:

                part = ModuleBuilder.create(
                    module
                )

            part.Proxy.setData(
                part,
                data
            )

            part.touch()

        #
        # Remove obsolete parts
        #

        valid_codes = {
            data["Code"]
            for data in parts_data
        }

        for part in list(module.Group):

            if (
                hasattr(part, "Code")
                and part.Code not in valid_codes
            ):

                module.removeObject(part)
                module.Document.removeObject(part.Name)

    @staticmethod
    def find(module, code):

        for part in module.Group:

            if (
                hasattr(part, "Code")
                and part.Code == code
            ):

                return part

        return None

    @staticmethod
    def create(module):

        part = create_part(
            module.Document
        )

        #
        # Add part to module.
        # Do NOT create a reverse PropertyLink,
        # otherwise FreeCAD creates a cyclic graph (DAG error).
        #

        module.addObject(part)

        return part