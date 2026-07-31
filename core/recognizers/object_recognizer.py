from core.data.object_data import ObjectData

from core.recognizers.panel_recognizer import PanelRecognizer
from core.recognizers.machining_recognizer import MachiningRecognizer


class ObjectRecognizer:

    @staticmethod
    def recognize(obj):

        result = ObjectData()

        result.Object = obj

        #
        # Panel
        #

        panel = PanelRecognizer.recognize(obj)

        if panel.IsPanel:

            result.Type = "Panel"
            result.IsValid = True
            result.Data = panel
            result.Message = panel.Message

            return result

        #
        # Machining
        #

        machining = MachiningRecognizer.recognize(obj)

        if machining.IsMachining:

            result.Type = "Machining"
            result.IsValid = True
            result.Data = machining
            result.Message = machining.Message

            return result

        #
        # Unknown
        #

        result.Type = "Unknown"
        result.IsValid = False
        result.Message = "Unsupported object."

        return result