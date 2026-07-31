from core.data.module_data import ModuleData


class ModuleRecognizer:

    @staticmethod
    def recognize(parts):

        module = ModuleData()

        if not parts:

            module.Message = "No parts."

            return module

        module.IsModule = True

        module.Parts = list(parts)

        #
        # Overall dimensions
        #

        width = 0.0
        height = 0.0
        depth = 0.0

        for part in parts:

            width = max(width, float(part.Width))
            height = max(height, float(part.Length))
            depth = max(depth, float(part.Thickness))

        module.Width = width
        module.Height = height
        module.Depth = depth

        module.Message = "Module recognized."

        return module