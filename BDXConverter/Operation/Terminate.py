from io import BytesIO
from ..General.GeneralClass import GeneralClass


class Terminate(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'Terminate'
        self.operationNumber: int = 88

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(b'E')

    def UnMarshal(self, buffer: BytesIO) -> None:
        match buffer.read(1):
            case b'E':
                pass
            case _:
                buffer.seek(-1, 1)
