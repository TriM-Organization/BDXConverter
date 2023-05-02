from io import BytesIO
from General.GeneralClass import GeneralClass
from utils.getByte import getByte
from struct import pack, unpack


class AddInt32YValue(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'AddInt32YValue'
        self.operationNumber: int = 23
        self.value: int = 0

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(pack('>i', self.value))

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.value = unpack('>i', getByte(buffer, 4))[0]

    def Loads(self, jsonDict: dict) -> None:
        self.value = jsonDict['value'] if 'value' in jsonDict else 0
