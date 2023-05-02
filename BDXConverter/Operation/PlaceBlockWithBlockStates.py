from io import BytesIO
from struct import pack, unpack
from ..General.GeneralClass import GeneralClass
from ..utils.getByte import getByte


class PlaceBlockWithBlockStates(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'PlaceBlockWithBlockStates'
        self.operationNumber: int = 5
        self.blockConstantStringID: int = 0
        self.blockStatesConstantStringID: int = 0

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(pack('>H', self.blockConstantStringID) +
                     pack('>H', self.blockStatesConstantStringID))

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.blockConstantStringID = unpack('>H', getByte(buffer, 2))[0]
        self.blockStatesConstantStringID = unpack('>H', getByte(buffer, 2))[0]

    def Loads(self, jsonDict: dict) -> None:
        self.blockConstantStringID = jsonDict['blockConstantStringID'] if 'blockConstantStringID' in jsonDict else 0
        self.blockStatesConstantStringID = jsonDict[
            'blockStatesConstantStringID'] if 'blockStatesConstantStringID' in jsonDict else 0
