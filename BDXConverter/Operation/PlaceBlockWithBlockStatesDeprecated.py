from io import BytesIO
from struct import pack, unpack
from ..General.GeneralClass import GeneralClass
from ..utils.getString import getByte, getString


class PlaceBlockWithBlockStatesDeprecated(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'PlaceBlockWithBlockStatesDeprecated'
        self.operationNumber: int = 13
        self.blockConstantStringID: int = 0
        self.blockStatesString: str = ''

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(pack('>H', self.blockConstantStringID) +
                     self.blockStatesString.encode(encoding='utf-8') + b'\x00')

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.blockConstantStringID = unpack('>H', getByte(buffer, 2))[0]
        self.blockStatesString = getString(buffer)

    def Loads(self, jsonDict: dict) -> None:
        self.blockConstantStringID = jsonDict['blockConstantStringID'] if 'blockConstantStringID' in jsonDict else 0
        self.blockStatesString = jsonDict['blockStatesString'] if 'blockStatesString' in jsonDict else ''
