from io import BytesIO
from struct import pack, unpack
from ..General.GeneralClass import GeneralClass
from ..utils.getByte import getByte


class AddInt16ZValue0(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'AddInt16ZValue0'
        self.operationNumber: int = 6
        self.value: int = 0

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(pack('>H', self.value))

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.value = unpack('>H', getByte(buffer, 2))[0]

    def Loads(self, jsonDict: dict) -> None:
        self.value = jsonDict['value'] if 'value' in jsonDict else 0
