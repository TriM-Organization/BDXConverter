from io import BytesIO
from struct import pack, unpack
from ..General.GeneralClass import GeneralClass
from ..utils.getString import getByte, getString


class PlaceCommandBlockWithCommandBlockData(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'PlaceCommandBlockWithCommandBlockData'
        self.operationNumber: int = 36
        self.data: int = 0
        self.mode: int = 0
        self.command: str = ''
        self.customName: str = ''
        self.lastOutput: str = ''
        self.tickdelay: int = 0
        self.executeOnFirstTick: bool = True
        self.trackOutput: bool = True
        self.conditional: bool = False
        self.needsRedstone: bool = False

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(pack('>H', self.data) + pack('>I', self.mode) + self.command.encode(encoding='utf-8') + b'\x00' + self.customName.encode(encoding='utf-8') + b'\x00' + self.lastOutput.encode(encoding='utf-8') + b'\x00' + pack('>I', self.tickdelay) + self.executeOnFirstTick.to_bytes(
            length=1, byteorder='big', signed=False) + self.trackOutput.to_bytes(length=1, byteorder='big', signed=False) + self.conditional.to_bytes(length=1, byteorder='big', signed=False) + self.needsRedstone.to_bytes(length=1, byteorder='big', signed=False))

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.data = unpack('>H', getByte(buffer, 2))[0]
        self.mode = unpack('>I', getByte(buffer, 4))[0]
        self.command = getString(buffer)
        self.customName = getString(buffer)
        self.lastOutput = getString(buffer)
        self.tickdelay = unpack('>I', getByte(buffer, 4))[0]
        self.executeOnFirstTick = bool(getByte(buffer, 1)[0])
        self.trackOutput = bool(getByte(buffer, 1)[0])
        self.conditional = bool(getByte(buffer, 1)[0])
        self.needsRedstone = bool(getByte(buffer, 1)[0])
