from io import BytesIO
from General.GeneralClass import GeneralClass
from utils.getByte import getByte
from struct import pack, unpack


class AddInt16XValue(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'AddInt16XValue'
        self.operationNumber: int = 20
        self.value: int = 0

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(pack('>h', self.value))

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.value = unpack('>h', getByte(buffer, 2))[0]

    def Loads(self, jsonDict: dict) -> None:
        self.value = jsonDict['value'] if 'value' in jsonDict else 0
