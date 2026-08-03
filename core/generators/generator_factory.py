from core.generators.base_generator import BaseGenerator


class GeneratorFactory:

    @staticmethod
    def get(module_type):

        generators = {

            "Módulo bajo": BaseGenerator,

            # Próximamente
            # "Módulo alto": WallGenerator,
            # "Columna": TallGenerator,
            # "Armario": WardrobeGenerator,
            # "Cómoda": DresserGenerator,
            # "Mueble TV": TVUnitGenerator,

        }

        return generators.get(
            module_type,
            BaseGenerator
        )