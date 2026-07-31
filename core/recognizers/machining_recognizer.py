from core.data.machining_data import MachiningData


class MachiningRecognizer:

    @staticmethod
    def recognize(obj):

        machining = MachiningData()

        machining.Object = obj

        machining.IsMachining = False

        machining.Message = "Not implemented."

        return machining