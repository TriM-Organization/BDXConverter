from io import BytesIO
from struct import pack, unpack
from .structOfChest import ChestData
from ..General.GeneralClass import GeneralClass
from ..utils.getByte import getByte


class PlaceRuntimeBlockWithChestData(GeneralClass):
    def __init__(self) -> None:
        super().__init__()
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
        if 'operationData' in jsonDict:
            jsonDict = jsonDict['operationData']
            self.runtimeId = jsonDict['runtimeId'] if 'runtimeId' in jsonDict else 0
            newChestData = ChestData()
            if 'data' in jsonDict:
                newChestData.Loads(jsonDict['data'])
            self.data = newChestData
            self.slotCount = self.data.slotCount

    def Dumps(self) -> dict:
        return {
            'operationName': self.operationName,
            'operationNumber': self.operationNumber,
            'operationData': {
                'runtimeId': self.runtimeId,
                'slotCount': len(self.data.chestData),
                'data': self.data.Dumps()
            }
        }
