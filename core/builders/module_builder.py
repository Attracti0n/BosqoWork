import FreeCAD

from objects.bosqo_part import create_part

from library.parts_library import PARTS_LIBRARY

from core.calculators.module_calculator import ModuleCalculator


class ModuleBuilder:

    @staticmethod
    def build(module):

        definitions = PARTS_LIBRARY["KitchenBase"]

        for definition in definitions:

            code = definition["Code"]

            part = ModuleBuilder.find(
                module,
                code
            )

            if part is None:

                part = ModuleBuilder.create(
                    module
                )

            data = ModuleCalculator.calculate(
                module,
                definition
            )

            part.Proxy.setData(
                part,
                data
            )

            part.touch()

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

        module.addObject(part)

        return part