from io import BytesIO
from ..General.GeneralClass import GeneralClass


class Terminate(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'Terminate'
        self.operationNumber: int = 88

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(b'E')

    def UnMarshal(self, buffer: BytesIO) -> None:
        readResult = buffer.read(1)
        if readResult == b'E':
            pass
        else:
            buffer.seek(-1, 1)
