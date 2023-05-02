from io import BytesIO
from struct import pack, unpack
from ..General.GeneralClass import GeneralClass
from ..utils.getByte import getByte


class AssignDebugData(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'AssignDebugData'
        self.operationNumber: int = 39
        self.length: int = 0
        self.buffer: bytes = b''

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(pack('>I', self.length) + self.buffer)

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.length = unpack('>I', getByte(buffer, 4))[0]
        self.buffer = getByte(buffer, self.length)

    def Loads(self, jsonDict: dict) -> None:
        self.length = jsonDict['length'] if 'length' in jsonDict else 0
        self.buffer = b''.join(
            [
                i.to_bytes(length=1, byteorder='big', signed=False)
                for i in jsonDict['buffer']
            ]
        ) if 'buffer' in jsonDict else b''

    def Dumps(self) -> dict:
        result: dict = {
            'operationName': self.operationName,
            'operationNumber': self.operationNumber,
            'length': self.length,
            'buffer': [i for i in self.buffer]
        }
        return result
