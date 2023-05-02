from io import BytesIO
from General.GeneralClass import GeneralClass
from utils.getByte import getByte
from struct import pack, unpack


class PlaceBlockWithRuntimeId(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'placeBlockWithRuntimeId'
        self.operationNumber: int = 33
        self.runtimeId: int = 0

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(pack('>I', self.runtimeId))

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.runtimeId = unpack('>I', getByte(buffer, 4))[0]

    def Loads(self, jsonDict: dict) -> None:
        self.runtimeId = jsonDict['runtimeId'] if 'runtimeId' in jsonDict else 0
