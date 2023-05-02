from io import BytesIO
from struct import pack, unpack
from .structOfChest import ChestData
from ..General.GeneralClass import GeneralClass
from ..utils.getByte import getByte


class PlaceRuntimeBlockWithChestData(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'PlaceRuntimeBlockWithChestData'
        self.operationNumber: int = 37
        self.runtimeId: int = 0
        self.slotCount: int = 0
        self.data: ChestData = ChestData()

    def Marshal(self, writer: BytesIO) -> None:
        self.data.slotCount = self.slotCount
        writer.write(pack('>H', self.runtimeId) +
                     self.slotCount.to_bytes(length=1, byteorder='big', signed=False))
        self.data.Marshal(writer)

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.runtimeId = unpack('>H', getByte(buffer, 2))[0]
        self.slotCount = getByte(buffer, 1)[0]
        self.data.slotCount = self.slotCount
        self.data.UnMarshal(buffer)

    def Loads(self, jsonDict: dict) -> None:
        self.runtimeId = jsonDict['runtimeId'] if 'runtimeId' in jsonDict else 0
        self.slotCount = jsonDict['slotCount'] if 'slotCount' in jsonDict else 0
        newChestData = ChestData()
        if 'data' in jsonDict:
            newChestData.Loads(jsonDict['data'])
        self.data = newChestData

    def Dumps(self) -> dict:
        result: dict = {
            'operationName': self.operationName,
            'operationNumber': self.operationNumber,
            'runtimeId': self.runtimeId,
            'slotCount': self.slotCount,
            'data': self.data.Dumps()
        }
        return result
