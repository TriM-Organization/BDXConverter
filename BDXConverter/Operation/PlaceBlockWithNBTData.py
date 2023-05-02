import nbtlib
from io import BytesIO
from struct import pack, unpack
from ..General.GeneralClass import GeneralClass
from ..utils.getByte import getByte
from ..utils.marshalNBT import MarshalPythonNBTObjectToWriter
from ..utils.unmarshalNBT import UnMarshalBufferToPythonNBTObject


class PlaceBlockWithNBTData(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'PlaceBlockWithNBTData'
        self.operationNumber: int = 41
        self.blockConstantStringID: int = 0
        self.blockStatesConstantStringID: int = 0
        self.blockNBT: nbtlib.tag.Compound = nbtlib.tag.Compound({})

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(pack('>H', self.blockConstantStringID) + pack('>H',
                     self.blockStatesConstantStringID) + pack('>H', self.blockStatesConstantStringID))
        MarshalPythonNBTObjectToWriter(writer, self.blockNBT, '')

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.blockConstantStringID = unpack('>H', getByte(buffer, 2))[0]
        self.blockStatesConstantStringID = unpack('>H', getByte(buffer, 2))[0]
        getByte(buffer, 2)  # do not delete this line because it is correct
        self.blockNBT, _ = UnMarshalBufferToPythonNBTObject(  # type: ignore
            buffer)

    def Loads(self, jsonDict: dict) -> None:
        self.blockConstantStringID = jsonDict['blockConstantStringID'] if 'blockConstantStringID' in jsonDict else 0
        self.blockStatesConstantStringID = jsonDict[
            'blockStatesConstantStringID'] if 'blockStatesConstantStringID' in jsonDict else 0
        self.blockNBT = nbtlib.parse_nbt(
            jsonDict['blockNBT']) if 'blockNBT' in jsonDict else nbtlib.tag.Compound({})

    def Dumps(self) -> dict:
        result: dict = {
            'operationName': self.operationName,
            'operationNumber': self.operationNumber,
            'blockConstantStringID': self.blockConstantStringID,
            'blockStatesConstantStringID': self.blockStatesConstantStringID,
            'blockNBT': nbtlib.serialize_tag(self.blockNBT)
        }
        return result
